# E.9 verification

[Design](sprint_E.9_design.md) owns expected behavior; [implementation](sprint_E.9_implementation.md) explains mechanisms; [handover](sprint_E.9_handover.md) owns acceptance.

## Gate results

The resumed final run at 20261125_191638 passed A1 smoke (one wrapper), A2 unit
(one wrapper, three isolated groups), A3 integration (both real local Git and
real HTTP/Git service drivers), B1 full smoke (seven entries) and B2 full unit
(six entries including real Oracle suites). No selected gate was skipped, no
failure threshold was relaxed and no flaky case was deferred. B3 integration
regression is not selected by PLAN. Initial red imports failed as expected
before each controller/service existed. No implementation-failure retry was
needed in the resumed final gate run.

## Acceptance and evidence

PBI-068: initial and refreshed diffs/summaries retain the developer annotation,
state tests honestly and correct the unsupported security-success claim. The
refreshed source adds the exact executed Hello World assertion. Both versions
are retained in the source bundles.

PBI-069: actual retained Codex serial review is accepted for the declared source.
Real authenticated HTTP requests reject unauthorized submission and malformed
policy evidence: missing assessment, unknown severity, unresolved blocker and
acknowledgement-only dismissal. Rejections leave the reviewed head unchanged.
Reports stay outside source and do not constitute independent approval or proof
of complete defect discovery.

PBI-070: real service events revoke evidence after head/base/policy changes,
report edits, withdrawal and logical deletion. Accepted report bytes remain
retrievable by content hash. Four concurrent HTTP publication cases reject
changed state. A report edit racing integration is serialized behind the real
merge and then rejected against its new base; events arriving first prevent
integration. The lock and expected-old-ref update protect the selected ordinary
service boundary.

PBI-071: missing, stale or nonpassing Testing/Review, unresolved conversation,
absent separate-role approval and wrong publisher all refuse ordinary merge.
Actual API role spoofing rejects with HTTP 403; persisted-record corruption is
separately labelled fault injection. Native local Git send-pack is refused by
the pre-receive hook with main unchanged. Successful ordinary merge retains both
parents and executes the merged assertion. An administrator exception requires
and records its reason. Separate approver capability behavior is exercised;
there is no claim of a human endorsement. Merge queue is not selected because
this service has no merge-queue integration.

## Demonstration and limits

The live repeated journey saved live-context.json and live-service.log. It
printed the real context correction, native receive refusal, controlled merge
and recorded bypass. Service results contain 174 HTTP/setup/inspection
observations, not 174 independent test cases. The accepted report receipt,
events, actual diffs and complete Git bundle are retained under tests/service.
Earlier pure-library-only logs remain historical and do not establish the
replacement authentication boundary. The earlier implementation's identity and
last-read gaps are explained in the implementation record and presentation.
GitHub portability, hostile-host isolation and production identity remain
outside this bounded experiment; they are not inferred from local checks.

## Artifacts

[test_run_A1_smoke_20261125_190609.log](test_run_A1_smoke_20261125_190609.log)

[test_run_A1_smoke_20261125_191638.log](test_run_A1_smoke_20261125_191638.log)

[test_run_A2_unit_20261125_190609.log](test_run_A2_unit_20261125_190609.log)

[test_run_A2_unit_20261125_191638.log](test_run_A2_unit_20261125_191638.log)

[test_run_A3_integration_20261125_190609.log](test_run_A3_integration_20261125_190609.log)

[test_run_A3_integration_20261125_191638.log](test_run_A3_integration_20261125_191638.log)

[test_run_B1_smoke_20261125_190609.log](test_run_B1_smoke_20261125_190609.log)

[test_run_B1_smoke_20261125_191638.log](test_run_B1_smoke_20261125_191638.log)

[test_run_B2_unit_20261125_190609.log](test_run_B2_unit_20261125_190609.log)

[test_run_B2_unit_20261125_191638.log](test_run_B2_unit_20261125_191638.log)

[Original red](tests/red.log), [service red](tests/service-red.log),
[service rehearsal](tests/service-rehearsal.log), [live context](tests/live-context.json),
[live service](tests/live-service.log), [service observations](tests/service/results.json),
[service events](tests/service/events.json), [accepted receipt](tests/service/receipt.json),
[native refusal](tests/service/direct-write.log), [source bundle](tests/service/candidate.bundle),
[presentation validation](tests/presentation-validation.json) and
[presentation montage](tests/presentation-montage.png).

## Final evidence-writer recheck

The service driver passed again after preserving native Git receive output in
tests/service/direct-write.raw.gz and normalizing trailing padding in its readable
log. Raw bytes remain recoverable; no refusal text or outcome changed. See
[final service recheck](tests/service-final-recheck.log). This is an evidence-format
repair after the full selected gate run, with the affected integration rerun.

## Closure reverification

A repeated request found E.9 already closed in local commit dce97ef. All five
selected gates were executed again successfully; no lifecycle restart was needed.
Fresh artifacts (all PASS):

[A1_smoke](test_run_A1_smoke_20261125_reverification.log)

[A2_unit](test_run_A2_unit_20261125_reverification.log)

[A3_integration](test_run_A3_integration_20261125_reverification.log)

[B1_smoke](test_run_B1_smoke_20261125_reverification.log)

[B2_unit](test_run_B2_unit_20261125_reverification.log)
