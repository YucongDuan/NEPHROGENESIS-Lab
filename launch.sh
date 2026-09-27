#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 run.py serve --port 8765
