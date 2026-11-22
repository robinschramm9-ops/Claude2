#!/usr/bin/env bash
# Convenience wrapper: ./next-shift-video/nsv.sh <command> ...
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHONPATH="$DIR${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m nsv "$@"
