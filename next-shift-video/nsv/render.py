"""Frame rendering (SVG -> PNG via cairosvg) in parallel chunks, encoded by FFmpeg."""
from __future__ import annotations

import bisect
import os
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor

from . import brand as B
from .compose import scene_svg


WATERMARK = ('<g opacity="0.75"><rect x="760" y="1000" width="400" height="44" rx="6" fill="#FF5A4E"/>'
             '<text x="960" y="1030" font-family="Inter SemiBold" font-size="22" fill="#0B0C0F" '
             'text-anchor="middle" letter-spacing="3">DRAFT \u2014 NOT APPROVED</text></g></svg>')


def _frame_svg(tl, starts, T, watermark=False):
    i = max(0, bisect.bisect_right(starts, T) - 1)
    sc = tl[i]
    svg = scene_svg(sc, T - sc["start"], sc["dur"], T)
    return svg[:-6] + WATERMARK if watermark else svg


def _render_chunk(args):
    import cairosvg
    tl, f0, f1, fps, w, h, out, crf, preset, wm, theme = args
    B.apply_theme(theme)
    starts = [s["start"] for s in tl]
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(fps),
                           "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
                           "-pix_fmt", "yuv420p", "-r", str(fps), out], stdin=subprocess.PIPE)
    last_svg, last_png = None, None
    for f in range(f0, f1):
        svg = _frame_svg(tl, starts, f / fps, wm)
        if svg != last_svg:
            last_png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h)
            last_svg = svg
        ff.stdin.write(last_png)
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg failed on chunk {out}")
    return out


def still(tl, T, path, scale=1.0):
    import cairosvg
    starts = [s["start"] for s in tl]
    cairosvg.svg2png(bytestring=_frame_svg(tl, starts, T).encode(), write_to=str(path),
                     output_width=int(B.W * scale), output_height=int(B.H * scale))


def render_video(project, tl, total, audio_path, draft=False, workers=None, burn_subs=None, log=print,
                 full_res=False):
    """draft=True: unapproved render, always watermarked. Half-res/15fps unless full_res."""
    fps = B.FPS if (full_res or not draft) else 15
    scale = 1.0 if (full_res or not draft) else 0.5
    w, h = int(B.W * scale), int(B.H * scale)
    nframes = int(total * fps)
    workers = workers or max(1, (os.cpu_count() or 2))
    n_chunks = workers * 3                      # smaller chunks balance load better
    seg_dir = project.build / ("segments_draft" if draft else "segments")
    seg_dir.mkdir(exist_ok=True)
    for f in seg_dir.glob("*.mp4"):
        f.unlink()
    bounds = [round(i * nframes / n_chunks) for i in range(n_chunks + 1)]
    jobs = [(tl, bounds[i], bounds[i + 1], fps, w, h, str(seg_dir / f"seg_{i:03d}.mp4"),
             23 if draft else 16, "veryfast" if draft else "medium", draft, B.THEME)
            for i in range(n_chunks) if bounds[i + 1] > bounds[i]]
    t0 = time.time()
    log(f"rendering {nframes} frames at {w}x{h}@{fps} on {workers} workers...")
    with ProcessPoolExecutor(workers) as ex:
        segs = []
        for k, s in enumerate(ex.map(_render_chunk, jobs)):
            segs.append(s)
            log(f"  chunk {k + 1}/{len(jobs)} done ({time.time() - t0:.0f}s)")
    lst = seg_dir / "list.txt"
    lst.write_text("".join(f"file '{os.path.basename(s)}'\n" for s in segs))
    silent = project.build / ("video_draft_silent.mp4" if draft else "video_silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(silent)], check=True)
    out = project.out / ("draft.mp4" if draft else "video.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(audio_path)]
    if burn_subs:
        style = ("FontName=Inter SemiBold,FontSize=15,PrimaryColour=&H00F7F5F4,OutlineColour=&H00000000,"
                 "BorderStyle=1,Outline=1.2,Shadow=0,MarginV=36")
        cmd += ["-vf", f"subtitles={burn_subs}:force_style='{style}'", "-c:v", "libx264", "-crf", "18",
                "-preset", "medium", "-pix_fmt", "yuv420p"]
    else:
        cmd += ["-c:v", "copy"]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.3f}",
            "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    log(f"render done in {time.time() - t0:.0f}s -> {out}")
    return out
