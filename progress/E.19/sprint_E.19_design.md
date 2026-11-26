# E.19 design

## Scope and responsibilities

Implement reusable Node actions for tool compatibility, native output and provenance, then qualify all remaining workflow Python support by inventory. Do not claim the initial three-action slice exhausts PBI-087. Use explicit exceptions, required input validation, regular-file checks and SHA-256. Actions return a validated output only on success and fail before any deployment action can run. Each action performs one check; workflows retain sequencing. No OCI interaction is selected in this slice.

## Child outcomes

PBI-087.1 (parent PBI-087): inventory and catalogue every current workflow Python dependency, with reasoned dispositions; acceptance is complete inventory and callable catalogue. PBI-087.2 depends on .1: migrate checks with input/refusal contracts and hosted action execution. PBI-087.3 depends on .2: equivalent runtime comparison, full regression, demonstration and audited handover. All remain unfinished until their evidence exists.

### Testing Strategy

Smoke loads each action and checks metadata. Unit tests exercise valid and missing/malformed inputs, exact tool/metadata version and qualified build, ANSI-stripped native error signatures, source/artifact/build mismatches and explicit failure independent of optimization. Integration invokes catalogued actions in real GitHub jobs with deployment downstream of valid gates; rejected checks must skip target mutation. Synthetic fixtures establish check contracts, not Oracle delivery. Compare Python baseline and JavaScript on identical bytes, runner image and repetitions; report setup, check and workflow separately. Full unfiltered smoke/unit/integration regression remains required.

## Test Specification

SM-19: metadata and Node source load. UT-19: positive and negative contracts for each migrated check. IT-19: actual hosted uses of each catalogue action, downstream mutation sentinel refusal, real tool identity qualification. PERF-19: cold/warm comparable samples and explicit limitations. UI-19: captures during actual inspection, local gallery navigation/link validation and rendered slides. ARCHIVE-19: timestamped native session exports with exact accessible coverage. No unrun case is a pass.

## Decision

YOLO design self-approval applies to this initial slice. Broader inventory can refine migration before implementation of additional actions. Neither fixture tests nor three pure checks alone establish parent acceptance.
