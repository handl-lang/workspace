#!/usr/bin/env bash
# clone-gate.sh — prove engine repos build/test with NO sibling checkouts.
#
# A viewer's clone has none: no `.cargo/config.toml` and no `../<repo>` paths.
# This extracts the committed tree of each repo into a temp dir (`git archive`,
# so untracked/ignored dev files cannot leak in) and runs the CI gate there.
#
#   scripts/clone-gate.sh                 # all engine-* repos
#   scripts/clone-gate.sh tool-lex ...  # a subset
#   CI_STAGE=build scripts/clone-gate.sh  # override the cargo subcommand
#
# Exit 1 if any repo fails. This is the check that keeps the `[patch]` tables
# out of published manifests (see project/plans/engine-public-readiness.md D7).
set -uo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
stage="${CI_STAGE:-test}"
repos=("$@")
if [ ${#repos[@]} -eq 0 ]; then
    mapfile -t repos < <(cd "$root" && ls -d engine-* 2>/dev/null)
fi

fail=0
for r in "${repos[@]}"; do
    src="$root/$r"
    if [ ! -d "$src/.git" ]; then
        printf '%-26s SKIP (no repo at %s)\n' "$r" "$src"
        continue
    fi
    work="$(mktemp -d)"
    dst="$work/$r"
    mkdir -p "$dst"
    if ! git -C "$src" archive HEAD | tar -x -C "$dst"; then
        printf '%-26s FAIL (git archive)\n' "$r"
        fail=1
        rm -rf "$work"
        continue
    fi
    # A committed lock or patch table would make the clone non-buildable.
    if grep -q '^\[patch' "$dst/Cargo.toml" 2>/dev/null; then
        printf '%-26s FAIL ([patch] in manifest)\n' "$r"
        fail=1
        rm -rf "$work"
        continue
    fi
    if [ -f "$dst/Cargo.lock" ]; then
        printf '%-26s FAIL (committed Cargo.lock)\n' "$r"
        fail=1
        rm -rf "$work"
        continue
    fi
    log="$work/gate.log"
    if ( cd "$dst" && cargo "$stage" --quiet ) >"$log" 2>&1; then
        printf '%-26s ok (cargo %s)\n' "$r" "$stage"
    else
        printf '%-26s FAIL (cargo %s)\n' "$r" "$stage"
        tail -12 "$log" | sed 's/^/    /'
        fail=1
    fi
    rm -rf "$work"
done

if [ "$fail" -ne 0 ]; then
    echo -e '\nclone-gate: FAILED' >&2
    exit 1
fi
echo -e '\nclone-gate: ok'
