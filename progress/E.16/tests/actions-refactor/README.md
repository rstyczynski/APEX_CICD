# Retained Actions refactor evidence

The [correction record](../../sprint_E.16_actions_refactor.md) owns acceptance and outcomes. [verification.json](verification.json) records six passing gates and the pinned source; [workflow.json](workflow.json) records all 39 successful native job steps. [presentation-final.json](presentation-final.json) validates the canonical 15-slide deck. These summaries do not replace the raw evidence.

[raw-evidence.tar.gz](raw-evidence.tar.gz) preserves 305 original raw files byte-for-byte, including native SQLcl output, both release archives, the generated Git bundle, complete gate logs, failed attempts and historical regression replay. [raw-evidence-manifest.json](raw-evidence-manifest.json) records each original member name, byte length and SHA-256, plus the archive digest. Every archived member was read back and compared with its original digest before duplicate loose captures were removed. Native/generated whitespace remains intact in the archive; it was not normalized and no Git whitespace check was disabled.

## Read the retained evidence

From this progress-repository checkout, the following data-only commands extract the retained capture. They do not dispatch a workflow or change an Oracle target. The original member paths are restored underneath a fresh temporary directory.

```bash
repo_root="$(git rev-parse --show-toplevel)"
e16_evidence_dir="$(mktemp -d "${TMPDIR:-/tmp}/e16-evidence.XXXXXX")"
tar -xzf "$repo_root/progress/E.16/tests/actions-refactor/raw-evidence.tar.gz" -C "$e16_evidence_dir"
```

With the `code` launcher available on PATH, open the restored logs using `code "$e16_evidence_dir/B3-pinned.log"` and the native results using `code "$e16_evidence_dir/native"`. The extraction and restored bytes were verified; no Code or native PowerPoint UI execution is claimed.

Successful gate members are A1-pinned.log, A2-pinned.log, A3-pinned.log, B1-pinned.log, B2-pinned.log and B3-pinned.log. Earlier shared-checkout logs are A1.log through B3.log. Failed layout attempts retain their own logs under symlink-layout-attempt/ and tool-home-layout-attempt/.

The native/ directory contains receipt-1.0.0.json, receipt-1.1.0.json, native16-1.0.0.zip, native16-1.1.0.zip, native-history.bundle, reviewed-inputs.sha256, measured tools, exported/staged/verified/released/package/deployment output, preserved-row assertions and four refusal files. Read before/after observations and both receipts with the review record; a process exit or summary alone does not establish source-to-target provenance.

regression-pinned-replay/ retains the 222 generated replay files and their index. shared-checkout-replay/ retains the interrupted shared-checkout attempt and saved historical snapshots. Paths recorded inside raw output describe execution time. The archive keeps those originals, including their native formatting, rather than presenting reformatted derivatives as raw logs.
