#!/usr/bin/env bash
# Run every gate in one go, never two at once (a browser fight makes tests time out):
# build check, design lint (about 12 min), pytest (about 20 min). Run it as ONE background command and do not edit files meanwhile.
# Usage: tools/gates.sh NN   -> /tmp/claude-0/lintNN.txt, /tmp/claude-0/pytestNN.txt, each ending in an exit= line.
set -u
N=${1:?iteration number}
cd "$(dirname "$0")/.."
python3 src/build.py --check > "/tmp/claude-0/build$N.txt" 2>&1; echo "exit=$?" >> "/tmp/claude-0/build$N.txt"
python3 tools/design_lint.py > "/tmp/claude-0/lint$N.txt" 2>&1; echo "exit=$?" >> "/tmp/claude-0/lint$N.txt"
python3 -m pytest -q tests > "/tmp/claude-0/pytest$N.txt" 2>&1; echo "exit=$?" >> "/tmp/claude-0/pytest$N.txt"
