#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${1:-https://github.com/dudsi101-svg/Human-os.git}"
BRANCH="${2:-main}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v git >/dev/null || { echo "Git is required"; exit 1; }
[ -d .git ] || git init -b "$BRANCH"
git remote get-url origin >/dev/null 2>&1 && git remote set-url origin "$REPO_URL" || git remote add origin "$REPO_URL"
git add .
git diff --cached --quiet || git commit -m "feat: publish Human OS Engine v0.6"
git push -u origin "$BRANCH"
