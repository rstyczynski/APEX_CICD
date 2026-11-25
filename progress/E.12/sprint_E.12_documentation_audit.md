# E.12 documentation audit

## Scope and inspection

Reviewed BACKLOG PBI-048/PBI-081 and PLAN E.12 against setup, design, implementation and test record. PLAN activation and YOLO mode are explicitly Product Owner authorized. Board remains unfinished. Reviewed shared SRS, architecture, test profile and README: added reciprocal navigation to the isolated experiment and preserved production maintenance/toolchain boundaries. No other sprint lifecycle was changed. SQL sources in walkthrough are generated from the actual driver and must be synchronized after edits. The walkthrough, manual and presentation consistently identify the cutover lock, finite traffic and unsupported browser/production claims.

All 12 deck slides were rendered and visually inspected in the montage: no visible clipping, overlap or unreadable command listings. Package, geometry, font and Artifact Tool re-import checks pass; this is not native PowerPoint verification. Presentation finalizer first failed for missing RUNTIME_NODE_MODULES; rerun with the bundled runtime path passed. No editable charts or tables exist to preserve. Agenda, section dividers, slide map and Q&A ending are present.

## Open audit findings

The full integration regression is unresolved. There is no PBI completion commit, accepted handover or recorded closure. The current evidence checklist is an experiment result, not complete acceptance. A final command/link audit and a demonstrator-led handover remain required after regression repair. This audit is incomplete and blocks completion under patch P8. Checkpoint preservation must not be described as a completion commit.

## Preservation checks

python3 -m py_compile tests/foundation_lab.py passed. Manifest-filtered smoke and unit reran successfully (1/1 each). git diff --check passed after generated historical outputs were preserved under E.12 and their original tracked files restored. Local file link targets in E.12 Markdown pass; section-anchor validation and full factual audit remain pending. Backlog navigation symlinks were created for the two assigned items and point to existing E.12 records. This is resumable work, not a passed completion audit.

Direct live result inspection was performed after rehearsal; handover records its exact scope. The final working-tree preservation commit is explicitly WIP and cannot satisfy P8's completed-increment marker while four integration failures remain.

Whitespace-only log normalization was needed for git diff --check. Exact original bytes for affected logs/JSON are retained in tests/original-whitespace-evidence.zip; readable copies remove trailing whitespace only. No error text or result was altered.

## Fresh resume verification

Inspected the implementation directly and reran the real Oracle experiment, rather than accepting prior pass claims. Recovery evidence now includes the subprocess failure marker, explicit rollback observation and target-side insert/update/delete assertions. Source SHA-256 and per-schema immutable run copies bind evidence to the executing driver. New smoke/unit passed, full smoke passed 10/10 and full unit passed 9/9. Full integration was rerun with output in tests/resume-full-integration.log; its final result must be inspected before any acceptance claim.

The authenticated assembly probe used native APEX login with the existing LAB_USER credential without printing it. An initial checksum error was corrected by sending the page-items protected field rather than the page-submission token. Login succeeded; the authenticated home page still lacked the expected assembly message. Thus adding login alone is insufficient. Read-only control inspection found both target records at epoch 0/new, while UAT retains its application and business tables. Integration has no application after the isolation reset. Neither condition justifies deleting UAT data or fabricating successful release receipts. Supported repair/adoption work remains unresolved, not an established external blocker.

Deck slides 5–7 now separate commands from explanation. Slide 11 uses native bullets for assigned PBI outcomes and explicitly names the planned E.13/E.14 follow-up. Changed slide 6 and 11 renders were inspected at 1280x720: readable, intact text and no clipping. Finalizer path-validation failures were diagnosed as temporary-directory placement errors and retried with canonical paths and an existing output directory; no tooling blocker is claimed.

Presentation finalization succeeded after correcting all candidate/output/receipt paths to their canonical workspace paths and creating the required directories. tests/resume-presentation-validation.json records package, geometry, fonts and import verification; the validated deck replaced the draft. This resolves the presentation tool failure, not the sprint gate failures.

Full regression finished at 16/20 with the same four failures. Inspection then found the final Foundation line was silently omitted because component_delivery.manifest lacks a terminating newline. The shared runner now handles the last nonempty record at EOF; a real Oracle integration invocation from an intentionally unterminated manifest checks that behavior. Full regression under the corrected runner remains required for acceptance. Generated changes to 45 tracked historical evidence files were preserved byte-for-byte in tests/resume-historical-generated.zip and their tracked paths restored to HEAD, leaving historical sprint records intact. Unrelated pre-existing broker and coordination changes remain outside this work's scope.

The deliberately unterminated-manifest integration check passed 1/1 and printed the real Oracle PASS result. Raw changed/new textual evidence is preserved before whitespace normalization in tests/resume-exact-text.zip; readable log/SQL copies remove trailing whitespace only. Recovery, source hashing and target assertions are verified, while the audit remains incomplete for the unresolved full regression and handover requirements. Any preservation commit remains WIP, not a PBI completion marker.
