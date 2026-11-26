# JavaScript support action catalogue — initial slice

These actions use the GitHub runner's Node 24 action runtime. They need no npm dependencies, setup-node, Python installation or Python execution. A runner supporting node24 is required. The metadata runtime is documented by [GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax#runs-for-javascript-actions).

## Tool compatibility

`actions/tool` requires `log` (SQLcl version output) and `config` (native `.dbtools/project.config.json`). It validates release 25.4.1.0, qualified build 25.4.1.022.0618 and matching native metadata. Missing metadata is rejected, deliberately tightening the old helper's optional-file behavior to enforce AGENTS.md/NFR-5. It does not launch SQLcl or establish that the supplied log came from the current executable; the workflow must capture it immediately before native processing.

## Native output

`actions/output` requires `log`, the actual native tool output. It rejects empty output, common native error signatures and nonzero Errors counts after stripping ANSI color sequences. This complements the native process exit status; a clean text file alone does not prove command execution or semantic correctness.

## Provenance

`actions/provenance` requires `archive`, `receipt` (JSON containing source, build, sha256), `source` (expected 40-character lowercase Git SHA) and `build` (actual qualified build). It binds exact archive bytes to independently supplied source/build expectations. Every mismatch throws an explicit error; runtime optimization cannot disable it. Receipt authenticity and expected-source authority are workflow responsibilities.

## Shared behavior and usage

All three emit `validated=true` only after success and return nonzero on a missing file, final-component symlink, malformed input or failed check. They never mutate a target. Use ordinary GitHub Actions success dependencies to prevent deployment after rejection. Do not set continue-on-error on a production guard. The qualification workflow deliberately uses it to inspect an expected rejection.

Check out this repository at a reviewed immutable commit and invoke a local action:

```yaml
- uses: ./actions/tool
  with:
    log: result/tool.txt
    config: .dbtools/project.config.json
- uses: ./actions/output
  with:
    log: result/native-command.log
- uses: ./actions/provenance
  with:
    archive: result/release.zip
    receipt: result/receipt.json
    source: ${{ steps.reviewed-source.outputs.sha }}
    build: ${{ steps.actual-tool.outputs.build }}
```

This is a wiring example requiring real producer steps and reviewed files, not a runnable native delivery demonstration. Full qualification and inventory remain pending; see the progress repository's E.19 checklist.
