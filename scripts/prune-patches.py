#!/usr/bin/env python3
"""Drop `[patch."…"]` entries that point at a package which no longer exists.

Deleting a `lib-*` crate (ADR-0160 P3) leaves two kinds of stale patch tables
behind, and cargo *hard-fails* on either:

- the shared dev config at `<workspace>/.cargo/config.toml`, and
- each repo's own `[patch]` table (`host/Cargo.toml` is the big one).

Paths in a patch table are relative to the manifest that holds them (the
workspace root for the shared config, the repo root for a repo manifest), so the
script resolves each entry against its own base.

    scripts/prune-patches.py            # rewrite in place, report what it dropped
    scripts/prune-patches.py --check    # report only, exit 1 if anything is stale
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ENTRY = re.compile(r'^([A-Za-z0-9_-]+)\s*=\s*\{\s*path\s*=\s*"([^"]+)"')
SECTION = re.compile(r'^\[patch\."')


def prune(manifest: Path, base: Path, check: bool) -> list[str]:
    """Return the dropped crate names; rewrites `manifest` unless `check`."""
    lines = manifest.read_text().splitlines(True)
    out: list[str] = []
    dropped: list[str] = []
    pending: str | None = None
    for line in lines:
        if SECTION.match(line):
            pending = line
            continue
        if pending is not None:
            m = ENTRY.match(line)
            if m:
                target = base / m.group(2) / "Cargo.toml"
                if target.is_file():
                    out += [pending, line]
                else:
                    dropped.append(m.group(1))
                pending = None
                continue
            out.append(pending)
            pending = None
        out.append(line)
    if pending is not None:
        out.append(pending)
    if dropped and not check:
        manifest.write_text("".join(out))
    return dropped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent.parent
    targets = [(root / ".cargo" / "config.toml", root)]
    targets += [(p, p.parent) for p in sorted(root.glob("*/Cargo.toml"))]
    targets += [(p, p.parent) for p in sorted(root.glob("*/*/Cargo.toml"))]

    total = 0
    for manifest, base in targets:
        if not manifest.is_file():
            continue
        dropped = prune(manifest, base, args.check)
        if dropped:
            total += len(dropped)
            shown = manifest.relative_to(root)
            print(f"{shown}: drop {len(dropped)} ({', '.join(sorted(dropped)[:4])}…)")

    if total == 0:
        print("prune-patches: clean")
        return 0
    if args.check:
        print(f"prune-patches: {total} stale entries", file=sys.stderr)
        return 1
    print(f"prune-patches: dropped {total} stale entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
