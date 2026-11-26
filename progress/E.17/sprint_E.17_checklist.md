# E.17 requirement-to-evidence checklist

[PBI-085](../../BACKLOG.md#pbi-085-reproduce-complete-native-delivery-on-a-clean-host) owns acceptance; [PLAN](../../PLAN.md#sprint-e17---reproduce-complete-native-delivery-on-a-clean-host) adds combined E.15/E.16 journey. [Local P8/P9](../../RUPStrikesBack.patch/RUP_patch.md) own audit/demo/presentation. [Test profile](../../docs/test-profile.md) owns regression commands.

Mandatory, pending actual observations: another attributable operator; genuinely independent clean host; declared prerequisites and newly supplied private inputs; Database/APEX/ORDS provisioning; application access; native installation, upgrade and repeat; preserved test data; documented tool identities and cleanup. Combined hosted validation/review/ordinary merge behavior from E.15 must be reproduced, rather than inferred from its old results.

Mandatory process outcomes, pending: new smoke/unit/integration gates; all three full regression levels; reconciled documentation and link audit; live demonstration; rendered and inspected presentation pair; local commits; verified recorded closure and final origin publication.

Implementation choices, not extra acceptance requirements: hosted Ubuntu, disposable technical account, pinned E.16 image, selected example APEX application, temporary generated passwords. No human study, production deployment, capacity benchmark or new toolchain upgrade is required.

## Current verification ledger

R1 — Independent clean host and attributable operator, mandated by PBI-085 description and PLAN E.17: pending host/run/identity observations. Hosted Ubuntu and its technical account are the chosen reproduction boundary, not evidence yet.

R2 — Declared prerequisites and newly supplied private inputs, mandated by PBI-085: pending measured identities and actual fresh-input provisioning. Existing prepared-host credentials are not read or transferred.

R3 — Database/APEX/ORDS provisioning and application access, mandated by PBI-085 test and PLAN: pending real install logs and HTTP observation. The initial reader checks the actual application login page; authenticated user behavior is not yet verified and must be assessed before acceptance.

R4 — Native installation, upgrade, repeat and preserved data, mandated by PBI-085 test: pending E.17 named Actions outcomes, archive receipts and target SQL observations. E.16 results establish reusable source qualification only.

R5 — Combined E.15/E.16 journey, mandated by PLAN E.17: verified fresh hosted run 45819877026, candidate PR 1 ordinary merge 1763f1b, stale-review refusal run 45820491077 before SQL execution, and protected merge refusal for PR 2. Raw records are under tests/; tests/clean_host.py independently rechecks terminal outcomes and branch/candidate execution policy. This establishes the combined reviewed candidate journey, not native platform delivery.

R6 — Documented tool identities, inputs and cleanup, mandated by PBI-085 test and NFR-5: pending actual release/build, project metadata and private-state cleanup observations.

R7 — All selected acceptance and regression gates, mandated by PLAN Test/Regression and RUP manager Phase 4: initial smoke passes 1/1; unit and integration plus full regressions pending. Initial run is diagnostic, not final gate evidence.

R8 — Documentation, demonstration, presentation, audit, commits and closure, mandated by local P8/P9 and RUP manager Phase 5: design resumption committed as b713427; final records and all delivery outcomes pending.
