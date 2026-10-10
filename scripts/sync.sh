#!/usr/bin/env bash
# Bring main up to date with every session branch (origin/claude/*), then push main.
# Usage: scripts/sync.sh <repo-dir>   (run once for the harness, once for recomp)
# Stops with exit 1 on a merge conflict, leaving the repo clean. Never resolves conflicts itself.
set -euo pipefail
repo="${1:?usage: sync.sh <repo-dir>}"
cd "$repo"
# merge commits need an identity; fall back only if the session has none configured
git config user.email >/dev/null || export GIT_AUTHOR_NAME=alttp-sync GIT_AUTHOR_EMAIL=sync@localhost \
  GIT_COMMITTER_NAME=alttp-sync GIT_COMMITTER_EMAIL=sync@localhost
git fetch -q origin
git checkout -q main 2>/dev/null || git checkout -q -b main origin/main
git merge -q --ff-only origin/main 2>/dev/null || git merge -q --no-edit origin/main
merged=0
for b in $(git branch -r --list 'origin/claude/*'); do
  if git merge-base --is-ancestor "$b" HEAD; then continue; fi
  if git merge -q --no-edit "$b"; then
    echo "merged $b"; merged=$((merged + 1))
  else
    git merge --abort
    echo "CONFLICT merging $b into main. Stop and report it; do not resolve it yourself."
    exit 1
  fi
done
if [ -f scripts/ledger.py ]; then python3 scripts/ledger.py validate; fi
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
  git push -q origin HEAD:main && echo "pushed main ($merged branch(es) merged)"
else
  echo "main already up to date"
fi
