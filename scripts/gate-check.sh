#!/usr/bin/env bash
# gate-check.sh — fleet gate hygiene for the handl-lang workspace.
#
# The contract (see workflows/gates/ + each repo's AGENTS.md):
#   * every repo carries workflows/gate.yaml — the ONLY fleet gate
#     entry point (`peregrin campaign run workflows/gate.yaml`)
#   * fleet-facing paths never invoke `scripts/ci.sh` as the gate —
#     bare `ci.sh` / `ci.sh ci` runs the whole pipeline and bypasses
#     the campaign's verdict/results contract. Per-stage calls
#     (`ci.sh test`, `ci.sh dogfood`, …) are the implementation seam
#     and allowed.
#
# Checks, per repo checkout under the workspace root (siblings of
# this repo; `*.git` mirror clones skipped):
#   FAIL  no workflows/gate.yaml
#   FAIL  bare `scripts/ci.sh` / `scripts/ci.sh ci` in
#         workflows/gate.yaml, scripts/ci-watch.sh, or bupha*.toml
#   WARN  handl-gates include pin older than the newest installed
#         bundle version (tamias store)
#
# Usage: scripts/gate-check.sh [workspace-root]   (default: the
# directory containing this repo — i.e. handl-lang/)
set -uo pipefail

SELF="$(cd "$(dirname "$0")" && pwd)"
ROOT="${1:-$(dirname "$(dirname "$SELF")")}"   # handl-lang/
[ -d "$ROOT" ] || { echo "gate-check: no such root: $ROOT" >&2; exit 2; }

fails=0 warns=0 checked=0

# Newest installed handl-gates version (for the pin-freshness warn).
newest_gates="$(tamias list 2>/dev/null | sed -n 's/^handl-gates@\([0-9.]*\).*/\1/p' | sort -V | tail -1)"

bare_ci() { # file — prints whole-gate ci.sh invocations (bare or `ci` stage)
  # Invocations look like `bash scripts/ci.sh` / `./scripts/ci.sh`;
  # path references (`"$REPO/scripts/ci.sh"`, `../scripts/ci.sh`)
  # and comment lines are not invocations.
  grep -nE 'scripts/ci\.sh' "$1" 2>/dev/null \
    | grep -vE '^[0-9]+:[[:space:]]*#' \
    | grep -vE '["'"'"'/]scripts/ci\.sh' \
    | grep -vE 'scripts/ci\.sh[[:space:]]+(doctor|test|test-shard|doctests|coverage-report|coverage-gate|dogfood|smoke|verify-all|help)([^a-zA-Z0-9_-]|$)' || true
}

for dir in "$ROOT"/*/; do
  repo="$(basename "$dir")"
  case "$repo" in
    *.git|assets*|crates*|scripts*|kit-py-smoke*|.gate-env*) continue ;;
  esac
  [ -e "$dir/.git" ] || continue          # not a checkout — skip
  checked=$((checked + 1))

  gate="$dir/workflows/gate.yaml"
  if [ ! -f "$gate" ]; then
    echo "FAIL  $repo: no workflows/gate.yaml"
    fails=$((fails + 1)); continue
  fi

  # Bare whole-gate ci.sh invocation inside the campaign itself.
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    echo "FAIL  $repo: bare ci.sh in workflows/gate.yaml — $hit"
    fails=$((fails + 1))
  done < <(bare_ci "$gate")

  # Fleet-facing scripts must route through the campaign too.
  for f in "$dir/scripts/ci-watch.sh" "$dir"/bupha*.toml "$dir"/ci-watch*.toml; do
    [ -f "$f" ] || continue
    while IFS= read -r hit; do
      [ -n "$hit" ] || continue
      echo "FAIL  $repo: bare ci.sh in $(basename "$f") — $hit"
      fails=$((fails + 1))
    done < <(bare_ci "$f")
  done

  # Include-pin freshness (warn only — pins are deliberate).
  pin="$(sed -n 's/.*tamias:handl-gates@\([0-9.]*\).*/\1/p' "$gate" | sort -uV | tail -1)"
  if [ -n "$pin" ] && [ -n "$newest_gates" ] && [ "$pin" != "$newest_gates" ]; then
    echo "WARN  $repo: handl-gates pin @$pin < newest installed @$newest_gates"
    warns=$((warns + 1))
  fi
done

echo "gate-check: $checked repos, $fails failure(s), $warns warning(s)"
[ "$fails" -eq 0 ]
