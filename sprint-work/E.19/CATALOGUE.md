# JavaScript support action catalogue

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

This is a wiring example requiring real producer steps and reviewed files, not a runnable native delivery demonstration. The full inventory, real native qualification, paired measurements and gate outcomes are recorded in the progress repository's progress/E.19 checklist. Lifecycle authority remains there.

## Candidate identity

`actions/candidate` requires `event`, a trusted GitHub pull-request JSON response. It rejects closed candidates, a base other than main, and malformed head/base commit identities. Success emits `validated=true`. Missing/malformed JSON fails the action. API acquisition and freshness remain native workflow responsibilities. `testing.yml` shows its actual wiring followed by jq field extraction.

## Trusted Review binding

`actions/review` requires `changed` (JSON file-name array), `report` (trusted JSON decision/hash) and `sql` (candidate SQL bytes). It requires exactly candidate.sql, an accept decision and the exact SHA-256 of those bytes. All inputs are required regular files. Rejected/unreviewed/stale/missing/malformed inputs fail before application validation. It emits `validated=true` only on success. `testing.yml` obtains changed paths and candidate bytes through native GitHub API steps before invoking the action.

## Qualification and installation

`acceptance.yml` exercises all five actions, including valid, missing, malformed and relevant mismatch cases. Every expected rejection has a conditionally skipped mutation sentinel and an outcome assertion. The fixtures are synthetic contract evidence. `native.yml` separately checks actual qualified SQLcl output, generated native project metadata and SQLcl-generated archive receipts before native deployment, and observes unchanged real target data across refusals. Its host.cjs and sql.sh adapters expose one native operation per invocation; they do not sequence the lifecycle.

`baseline/` and `actions/benchmark` are comparison-only tools. Python is intentionally executed in the baseline benchmark and separate Oracle application test. Neither belongs to the Python-free delivery-check runtime. Historical source copies are preserved in the progress repository. No npm dependency, bundler or setup action is required for the five guards. Checkout must include the shared `actions/checks.cjs`; copying one subdirectory alone is unsupported. Pin use to an immutable reviewed repository commit.
