#!/usr/bin/env bash
# manifest-gate.sh — keep published manifests installable from a git URL.
#
# Fails when an engine repo's committed Cargo.toml carries a `[patch."..."]`
# table (dev-only; it points at `../<sibling>` paths that do not exist for a
# viewer) or when a `Cargo.lock` is committed (dev state that breaks `--locked`
# in a clean clone). Dev overrides belong in a gitignored `.cargo/config.toml`.
#
#   scripts/manifest-gate.sh                 # all engine-* repos
#   scripts/manifest-gate.sh tool-lex ...
set -uo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
repos=("$@")
if [ ${#repos[@]} -eq 0 ]; then
    mapfile -t repos < <(cd "$root" && ls -d engine-* 2>/dev/null)
fi

fail=0
for r in "${repos[@]}"; do
    manifest="$root/$r/Cargo.toml"
    [ -f "$manifest" ] || continue
    problems=()
    if grep -q '^\[patch\.' "$manifest"; then
        problems+=("[patch] table in manifest")
    fi
    if git -C "$root/$r" ls-files --error-unmatch Cargo.lock >/dev/null 2>&1; then
        problems+=("Cargo.lock is tracked")
    fi
    if [ ${#problems[@]} -eq 0 ]; then
        printf '%-26s ok\n' "$r"
    else
        printf '%-26s FAIL: %s\n' "$r" "$(IFS='; '; echo "${problems[*]}")"
        fail=1
    fi
done

if [ "$fail" -ne 0 ]; then
    echo -e '\nmanifest-gate: FAILED' >&2
    exit 1
fi
echo -e '\nmanifest-gate: ok'
