# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

{{FAMILY_BLURB}}  <!-- kit declarations are manifests-as-data over `lib-*`
     packages — what this kit assembles (prelude modules, server kit, …) -->

## Layout

```text
{{TREE}}  <!-- kit data/fragments, src/, crates/ if any transitional rust -->
```

## Gate

```bash
HNL=../host-cli/target/debug/hnl scripts/hnl-gate.sh
```

<!-- If the repo gates via ci.sh/bupha instead of hnl-gate.sh, use `./ci.sh`. -->

## License

MIT.
