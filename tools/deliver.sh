#!/usr/bin/env bash
# Delivery after the gates pass and master is pushed: gh-pages copy, iteration zip and git bundle in /mnt/project-files/thv/.
# The Artifact republish and the laptop copy (device_commit_files, unzip into source\, move the old zip to !DELETE ME, README state line)
# are tool calls and stay manual. Usage: tools/deliver.sh NN
set -eu
N=${1:?iteration number}
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GHP=${GHP:-/tmp/ghp}                      # worktree of branch gh-pages-pub; create it with: git worktree add /tmp/ghp gh-pages-pub
OUT=/mnt/project-files/thv; mkdir -p "$OUT"
cp "$ROOT/index.html" "$GHP/index.html"
(cd "$GHP" && git add -A && git commit -qm "Iteration $N" && git push -q -f origin gh-pages-pub:gh-pages)
(cd "$ROOT" && git archive --format=zip -o "$OUT/the-human-variable_iteration$N.zip" HEAD && git bundle create "$OUT/the-human-variable.bundle" --all >/dev/null 2>&1)
ls -la "$OUT" | tail -3
