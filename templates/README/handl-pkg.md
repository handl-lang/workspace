# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

{{PROVENANCE_NOTE}}  <!-- e.g. "Part of the stdlib → `lib-*` split (ADR-0128). History is a `git subtree split` of `stdlib/handl-packages/<name>/`." -->

## Layout

```text
{{TREE}}  <!-- src/*.hnl, pkg.hnl, ci.sh / scripts/hnl-gate.sh -->
```

## Gate

```bash
HNL=../host-cli/target/debug/hnl scripts/hnl-gate.sh
```

<!-- If the repo gates via ci.sh/bupha instead of hnl-gate.sh, use:
     `./ci.sh`  is the gate. -->

## License

{{LICENSE}}  <!-- MIT unless LICENSE says otherwise -->
