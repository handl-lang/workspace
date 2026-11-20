# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

## Layout

```text
{{TREE}}  <!-- src/*.hnl, pkg.hnl, ci.sh / scripts/hnl-gate.sh -->
```

## Gate

```bash
HNL=../host-cli/target/debug/hnl scripts/hnl-gate.sh
```

<!-- If the repo gates via ci.sh/bupha instead of hnl-gate.sh, use `./ci.sh`. -->

## License

MIT.
