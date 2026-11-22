"""Project folders, state and the human approval gates."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # repository root
VIDEOS = Path(os.environ.get("NSV_VIDEOS", ROOT / "videos"))

GATES = ("research", "script")   # what a human must approve before a final render
GATE_FILES = {"research": ["research.json"], "script": ["research.json", "storyboard.json"]}


class Project:
    def __init__(self, slug: str):
        self.slug = slug
        self.dir = VIDEOS / slug
        if not self.dir.exists():
            raise SystemExit(f"No project at {self.dir}. Create it with: nsv new {slug} --title ...")
        self.build = self.dir / "build"
        self.out = self.dir / "output"
        self.build.mkdir(exist_ok=True)
        self.out.mkdir(exist_ok=True)

    # files ------------------------------------------------------------------
    def path(self, name):
        return self.dir / name

    def load(self, name):
        p = self.path(name)
        if not p.exists():
            raise SystemExit(f"Missing {p}")
        try:
            return json.loads(p.read_text())
        except json.JSONDecodeError as e:
            raise SystemExit(f"{p} is not valid JSON: {e}")

    @property
    def research(self):
        return self.load("research.json")

    @property
    def storyboard(self):
        return self.load("storyboard.json")

    # state & approvals --------------------------------------------------------
    def _state_path(self):
        return self.dir / "state.json"

    def state(self):
        p = self._state_path()
        return json.loads(p.read_text()) if p.exists() else {"approvals": {}}

    def save_state(self, s):
        self._state_path().write_text(json.dumps(s, indent=2))

    def fingerprint(self, gate):
        h = hashlib.sha256()
        for f in GATE_FILES[gate]:
            h.update(self.path(f).read_bytes())
        return h.hexdigest()[:16]

    def approve(self, gate, by):
        s = self.state()
        s["approvals"][gate] = {"by": by, "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                "fingerprint": self.fingerprint(gate)}
        self.save_state(s)

    def gate_status(self, gate):
        """'approved', 'stale' (file changed after approval) or 'missing'."""
        a = self.state()["approvals"].get(gate)
        if not a:
            return "missing"
        return "approved" if a["fingerprint"] == self.fingerprint(gate) else "stale"

    def require_gates(self):
        bad = {g: self.gate_status(g) for g in GATES if self.gate_status(g) != "approved"}
        if bad:
            msg = "\n".join(f"  - {g}: {st}" for g, st in bad.items())
            raise SystemExit("Final render blocked. Human approval required:\n" + msg +
                             f"\nReview, then run: nsv approve {self.slug} <research|script> --by <name>"
                             "\n(Use --draft for an unapproved preview render.)")


def new_project(slug: str, title: str):
    d = VIDEOS / slug
    if d.exists():
        raise SystemExit(f"{d} already exists - refusing to overwrite.")
    d.mkdir(parents=True)
    tpl = Path(__file__).resolve().parents[1] / "templates"
    for f in ("research.json", "storyboard.json"):
        txt = (tpl / f).read_text().replace("{{TITLE}}", title).replace("{{SLUG}}", slug)
        (d / f).write_text(txt)
    return d
