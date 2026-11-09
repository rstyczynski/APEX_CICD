# E.4 handover — round 1 engineering response

Round: E.4 handover, 1, engineering response. Original review revision:
`e32ae318df3c999712d724f73e1bee0ad2977f98`. Corrected maintained source:
`75e904161b0450684a0fa2c5cf03d19a678e4066`, published on main at
https://github.com/rstyczynski/APEX_CICD.git and verified by ls-remote.
Reviewer: independent gpt-6-astra chat; respondent: implementation Codex operator.
Scope: R1-L1 measurement labeling and its evidence-reader assertion, no target change.
Inputs: [original report](sprint_E.4_handover_review-1.md),
[handover](sprint_E.4_handover.md), [calculation](tests/native-overlap-calculation.json),
[recheck request](sprint_E.4_handover_review-1-feedback-prompt.md).

## R1-L1 — fixed@75e9041; independent recheck requested

Agreed. The broader author-worker intersection is approximately 24.84 seconds and
includes version checks/Git work. Calling it a continuous native-process interval
was inaccurate. The exact three-way native capture intersection is 14.757295 seconds;
the independent stage/verify intersection is 4.155229 seconds. Distinct successful
native PIDs still establish the accepted concurrency requirement.

Implementation, test report, walkthrough and slide 13 now distinguish these measures.
The original worker/process receipts and expert text are unchanged. The original
report SHA-256 is `7ed808d3c8b3dbba5667c4031f5b50a9760416cd6a53cffea2b1e2441433ec12`.
The existing IT-1 reader now also checks distinct PIDs, successful return codes,
matching private-home aliases and positive overlap separately for capture and
stage/verify. This is a bounded strengthening of existing provenance checks, not a
new runtime scenario or evidence that three humans worked concurrently.

The corrected presentation SHA-256 is
`04269d957cbaed85e1d2da8598b43a7c20bb59f0be16a3fdd1b852638d52be2a`.
The package/layout/import checks passed, all slides rerendered, and changed slide 13
plus the closing slide were visually checked. No other slide content changed.

Acceptance: independently recompute min(finish) minus max(start) for both native
phases and verify the new prose/PPTX uses the corresponding duration. Inspect the
bounded test change, and confirm no unsupported native-duration claim remains.

## Checks performed

Recomputed both intervals directly from the six retained native process receipts.
Ran A1 → A3 → B1 after the change: 1/1, 3/3 and 2/2 passed, with retained logs
20261109_160118. Checked changed prose/script whitespace and presentation structure,
fonts, import and rendered readability. Full SQL bodies are unchanged. No Oracle,
APEX, ORDS, release artifact, branch-selection state or business data was modified.
The independent report's limitations on private evidence, PowerPoint rendering and
future fresh replay remain accepted boundaries. Live PO acceptance remains pending.
