#!/usr/bin/env bash
# Gate every engine-* repo through the repo's own `ci.sh`.
#
# Each engine is its own repository with an identical `ci.sh` (fmt -> clippy ->
# test -> doc). This umbrella runs them in turn so a drift in one crate cannot
# hide; the per-repo gate stays the single source of truth.
#
# Usage: scripts/check-engines.sh [--quick] [repo ...]
#   --quick   fmt + clippy only (skip test/doc)
set -uo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"

quick=0
repos=()
for arg in "$@"; do
    case "$arg" in
        --quick) quick=1 ;;
        *) repos+=("$arg") ;;
    esac
done
if [ ${#repos[@]} -eq 0 ]; then
    mapfile -t repos < <(cd "$root" && ls -d engine-* 2>/dev/null)
fi

failed=0
for c in "${repos[@]}"; do
    printf '\n== %s\n' "$c"
    if [ ! -f "$root/$c/ci.sh" ]; then
        echo "   no ci.sh (not migrated yet)" >&2
        failed=1
        continue
    fi
    if [ "$quick" -eq 1 ]; then
        ( cd "$root/$c" && bash ci.sh fmt && bash ci.sh clippy ) || { echo '   fmt/clippy: FAIL' >&2; failed=1; }
    else
        ( cd "$root/$c" && bash ci.sh ) || { echo '   ci: FAIL' >&2; failed=1; }
    fi
done

if [ "$failed" -ne 0 ]; then
    echo -e '\nengines: FAILED' >&2
    exit 1
fi
echo -e '\nengines: ok'
