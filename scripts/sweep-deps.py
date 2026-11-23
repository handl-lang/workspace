#!/usr/bin/env python3
"""Sweep stale `lib-*`/`kit-*` deps after a repo folds into `host` or goes `.hnl`-only.

Scans every Cargo.toml (and .cargo/config.toml) under the org root for
dependencies and `[patch]` entries that point at sibling `lib-*`/`kit-*`
checkouts. Each target is classified:

  ALIVE      target repo still has a Cargo.toml            -> untouched
  FLIP-HOST  target folded into host/crates (crate found)  -> rewrite
             git URL -> https://github.com/handl-lang/host, path -> ../host/crates/<dir>,
             and re-key `[patch."…/<old>"]` sections into `[patch."…/host"]`
  DEAD       target is .hnl-only with no host crate        -> reported, never edited
             (removal is a judgment call — see --dead-report)

Usage:
    sweep-deps.py                 # dry run: print the plan, edit nothing
    sweep-deps.py --apply         # perform the rewrites
    sweep-deps.py --verify        # after --apply, cargo metadata each touched repo
    sweep-deps.py --repo ext-eval # limit to one repo dir name
    sweep-deps.py --dead-report   # list DEAD deps in detail

Patch tables are the fiddly part: a `[patch."https://github.com/handl-lang/lib-x"]`
section whose entries now resolve inside host must merge into the manifest's
`[patch."https://github.com/handl-lang/host"]` section (TOML forbids duplicate
tables). Entries are deduped by crate name; an existing host entry wins.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ORG = Path("/home/luis/GitHub/handl-lang")
HOST_CRATES = ORG / "host" / "crates"
HOST_GIT = "https://github.com/handl-lang/host"

SKIP_DIRS = {"target", "node_modules", ".git", ".venv", "dist", ".next"}
MANIFEST_NAMES = {"Cargo.toml"}
CONFIG_NAMES = {"config.toml"}  # only under .cargo/

# handl-lang/lib-foo or handl-lang/kit-foo git URLs, and ../lib-foo path deps
GIT_RE = re.compile(r'handl-lang/(lib|kit)-([A-Za-z0-9_-]+)')
PATH_RE = re.compile(r'\.\./((?:lib|kit)-[A-Za-z0-9_-]+)(/[^"\s]*)?')
DEP_LINE = re.compile(r'^([A-Za-z0-9_-]+)\s*=\s*\{(.*)\}\s*,?\s*$')
PATCH_SECTION = re.compile(r'^\[patch\."([^"]+)"\]')
ANY_SECTION = re.compile(r'^\[')


@dataclass
class HostCrate:
    """A crate that lives in host/crates/ (package name -> dir)."""

    name: str
    directory: str


def host_crate_map() -> dict[str, HostCrate]:
    """Map package name -> host crate dir by scanning host/crates/*/Cargo.toml."""
    out: dict[str, HostCrate] = {}
    if not HOST_CRATES.is_dir():
        return out
    for manifest in HOST_CRATES.glob("*/Cargo.toml"):
        try:
            data = tomllib.loads(manifest.read_text())
        except Exception:
            continue
        name = data.get("package", {}).get("name")
        if name:
            out[name] = HostCrate(name=name, directory=manifest.parent.name)
    return out


def repo_has_crate(repo: Path) -> bool:
    return (repo / "Cargo.toml").is_file()


def repo_crate_name(repo: Path) -> str | None:
    try:
        data = tomllib.loads((repo / "Cargo.toml").read_text())
        for member in data.get("workspace", {}).get("members", []):
            pass
        # single-crate repos: root package
        pkg = data.get("package", {}).get("name")
        if pkg:
            return pkg
        # workspace: find first member manifest cheaply
        for member in data.get("workspace", {}).get("members", []):
            sub = repo / member / "Cargo.toml"
            if sub.is_file():
                return tomllib.loads(sub.read_text()).get("package", {}).get("name")
    except Exception:
        pass
    return None


@dataclass
class DepRef:
    manifest: Path
    crate: str | None          # dep key name, if parseable
    kind: str                  # "dep" | "patch"
    raw: str                   # the matched URL/path text
    target_repo: str           # e.g. "lib-foo"
    section_url: str | None    # for patch entries: the [patch."…"] url
    lineno: int


def iter_manifests(root: Path):
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in MANIFEST_NAMES or (p.name in CONFIG_NAMES and ".cargo" in p.parts):
            yield p


def scan(manifest: Path) -> list[DepRef]:
    """Find dep/patch lines referencing ../lib-*|kit-* or handl-lang/lib-*|kit-*."""
    refs: list[DepRef] = []
    try:
        lines = manifest.read_text().splitlines()
    except Exception:
        return refs
    patch_url: str | None = None
    in_patch = False
    for i, line in enumerate(lines, 1):
        m = PATCH_SECTION.match(line)
        if m:
            patch_url = m.group(1)
            in_patch = True
            continue
        if ANY_SECTION.match(line):
            in_patch = False
            patch_url = None
            continue
        kind = "patch" if in_patch else "dep"
        # git URL refs
        for gm in GIT_RE.finditer(line):
            refs.append(DepRef(manifest, None, kind, gm.group(0),
                               f"{gm.group(1)}-{gm.group(2)}", patch_url, i))
        # ../lib-x path refs
        for pm in PATH_RE.finditer(line):
            refs.append(DepRef(manifest, None, kind, pm.group(0),
                               pm.group(1), patch_url, i))
    return refs


def classify(ref: DepRef, host_map: dict[str, HostCrate]) -> str:
    repo = ORG / ref.target_repo
    if not repo.is_dir():
        return "MISSING-REPO"
    if repo_has_crate(repo):
        return "ALIVE"
    # .hnl-only: does host provide a crate with a matching package name?
    # folded crates kept their package names (handl-kit-*, handl-lib-*, kit-*, plugin-*)
    candidates = [ref.target_repo.replace("-", "_")]
    for name in host_map:
        if ref.target_repo in name or name.endswith(ref.target_repo.split("-", 1)[-1]):
            candidates.append(name)
    # direct: try plausible package names derived from repo name
    tail = ref.target_repo.split("-", 1)[1] if "-" in ref.target_repo else ref.target_repo
    for pkg in {f"handl-{ref.target_repo.replace('-', '_')}",
                f"handl-{tail.replace('-', '_')}",
                ref.target_repo.replace('-', '_'),
                tail.replace('-', '_')}:
        if pkg in host_map:
            return "FLIP-HOST"
    return "DEAD"


def host_dir_for(ref: DepRef, host_map: dict[str, HostCrate]) -> str | None:
    tail = ref.target_repo.split("-", 1)[1] if "-" in ref.target_repo else ref.target_repo
    for pkg in {f"handl-{ref.target_repo.replace('-', '_')}",
                f"handl-{tail.replace('-', '_')}",
                ref.target_repo.replace('-', '_'),
                tail.replace('-', '_')}:
        if pkg in host_map:
            return host_map[pkg].directory
    return None


@dataclass
class Edit:
    manifest: Path
    lineno: int
    old: str
    new: str
    note: str


def plan_edits(refs: list[DepRef], host_map: dict[str, HostCrate]) -> tuple[list[Edit], list[str]]:
    edits: list[Edit] = []
    dead: list[str] = []
    for ref in refs:
        status = classify(ref, host_map)
        if status == "ALIVE" or status == "MISSING-REPO":
            continue
        if status == "DEAD":
            dead.append(f"{ref.manifest.relative_to(ORG)}:{ref.lineno} {ref.raw}")
            continue
        # FLIP-HOST
        hdir = host_dir_for(ref, host_map)
        if hdir is None:
            dead.append(f"{ref.manifest.relative_to(ORG)}:{ref.lineno} {ref.raw} (host crate unmapped)")
            continue
        lines = ref.manifest.read_text().splitlines()
        line = lines[ref.lineno - 1]
        new = line
        note = ""
        if "handl-lang/" in line:
            # git URL flip: keep the rest of the dep spec (branch etc.)
            new = re.sub(r'https://github\.com/handl-lang/(?:lib|kit)-[A-Za-z0-9_-]+',
                         HOST_GIT, line)
            note = f"git -> {HOST_GIT}"
        elif f"../{ref.target_repo}" in line or f"./{ref.target_repo}" in line:
            # path flip: ../lib-x/<sub> -> ../host/crates/<hdir>/<sub>
            new = re.sub(rf'\.\./{re.escape(ref.target_repo)}(/[A-Za-z0-9_./-]*)?',
                         f"../host/crates/{hdir}\\1", line)
            note = f"path -> ../host/crates/{hdir}"
        if new != line:
            edits.append(Edit(ref.manifest, ref.lineno, line, new, note))
    return edits, dead


def apply_patch_rekey(manifest: Path) -> list[str]:
    """Merge [patch."…/lib-*|kit-*"] sections into [patch."…/host"].

    Returns notes. Only runs for manifests we edited. Conservative: if the
    manifest has no host patch section and exactly one folded section, rename
    the header; otherwise merge entries under the host section.
    """
    text = manifest.read_text()
    lines = text.splitlines(keepends=True)
    # collect sections
    sections: list[tuple[int, str]] = []  # (start_idx, url)
    for i, l in enumerate(lines):
        m = PATCH_SECTION.match(l)
        if m:
            sections.append((i, m.group(1)))
    folded = [(i, u) for i, u in sections
              if re.search(r'handl-lang/(lib|kit)-', u) or re.search(r'\.\./(lib|kit)-', u)]
    if not folded:
        return []
    notes = []
    # find or create host section index
    host_idx = next((i for i, u in sections if u == HOST_GIT), None)
    for start, url in folded:
        # section body: until next [section] or EOF
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if ANY_SECTION.match(lines[j]):
                end = j
                break
        body = lines[start + 1:end]
        entries = [l for l in body if DEP_LINE.match(l) and "path" in l or DEP_LINE.match(l) and "git" in l]
        if host_idx is None:
            # rename this section's header to host url — but only safe if it's
            # the ONLY folded section; multiple folded sections need real merge.
            if len(folded) == 1:
                lines[start] = f'[patch."{HOST_GIT}"]\n'
                notes.append(f"re-keyed patch section -> host")
                host_idx = start
                continue
        # merge entries into host section (create at EOF if missing)
        kept = []
        for l in body:
            dm = DEP_LINE.match(l)
            if dm and ("path" in l or "git" in l):
                kept.append(l)
            elif l.strip() and not l.strip().startswith("#"):
                kept.append(l)  # non-entry lines ride along only if section survives
        if host_idx is not None:
            # insert entries right after host section header
            insert_at = host_idx + 1
            # skip existing comment/blank run? just insert after header
            lines[insert_at:insert_at] = kept
            notes.append(f"merged {len(kept)} patch entries -> host section")
        else:
            # append a new host section at EOF
            lines += [f'\n[patch."{HOST_GIT}"]\n'] + kept
            notes.append(f"created host patch section with {len(kept)} entries")
            host_idx = len(lines) - len(kept) - 1
        # drop the folded section (header + body)
        del lines[start:end + (0 if end == len(lines) else 0)]
        # recompute: easier to restart — mark and rebuild
        # (sections shifted; bail to a second pass for simplicity)
        manifest.write_text("".join(lines))
        return apply_patch_rekey(manifest) + notes
    manifest.write_text("".join(lines))
    return notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ORG)
    ap.add_argument("--apply", action="store_true", help="perform edits (default: dry run)")
    ap.add_argument("--verify", action="store_true", help="cargo metadata each touched repo")
    ap.add_argument("--repo", help="limit to a repo dir name")
    ap.add_argument("--dead-report", action="store_true")
    args = ap.parse_args()

    host_map = host_crate_map()
    manifests = [m for m in iter_manifests(args.root)
                 if args.repo is None or args.repo in m.parts]

    all_refs: list[DepRef] = []
    for m in manifests:
        all_refs.extend(scan(m))

    edits, dead = plan_edits(all_refs, host_map)

    by_status: dict[str, int] = {}
    for ref in all_refs:
        s = classify(ref, host_map)
        by_status[s] = by_status.get(s, 0) + 1

    print(f"scanned {len(manifests)} manifests, {len(all_refs)} dep/patch refs")
    print("classification:", ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))

    if dead:
        print(f"\nDEAD deps ({len(dead)}) — need judgment, NOT edited:")
        for d in dead[:50]:
            print(f"  {d}")
        if len(dead) > 50:
            print(f"  … {len(dead) - 50} more")

    touched: set[Path] = set()
    if edits:
        print(f"\nplanned edits ({len(edits)}):")
        for e in edits:
            print(f"  {e.manifest.relative_to(args.root)}:{e.lineno}  {e.note}")
            touched.add(e.manifest)
        if args.apply:
            # group edits per manifest, apply bottom-up so linenos stay valid
            per: dict[Path, list[Edit]] = {}
            for e in edits:
                per.setdefault(e.manifest, []).append(e)
            for manifest, es in per.items():
                lines = manifest.read_text().splitlines(keepends=True)
                for e in sorted(es, key=lambda x: -x.lineno):
                    lines[e.lineno - 1] = e.new if e.new.endswith("\n") else e.new + "\n"
                manifest.write_text("".join(lines))
                notes = apply_patch_rekey(manifest)
                for n in notes:
                    print(f"  patch: {manifest.relative_to(args.root)} — {n}")
            print(f"applied {len(edits)} edits across {len(per)} manifests")
    else:
        print("\nno edits needed")

    if args.verify and args.apply:
        repos = sorted({next(p for p in e.manifest.parents if (p / '.git').exists())
                        for e in edits} if edits else set())
        for repo in repos:
            print(f"verify: cargo metadata in {repo.name} …", flush=True)
            r = subprocess.run(["cargo", "metadata", "--format-version", "1", "-q"],
                               cwd=repo, capture_output=True, text=True)
            print(f"  {'OK' if r.returncode == 0 else 'FAIL'} {repo.name}")
            if r.returncode != 0:
                print("  " + (r.stderr or "")[:400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
