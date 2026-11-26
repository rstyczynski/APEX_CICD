# E.18 operator reference

The [complete walkthrough](sprint_E.18_increment_demo.md) owns setup, dispatch, source explanations, expected observations and failure recovery. The [design](sprint_E.18_design.md) owns cache and concurrency definitions; the [checklist](sprint_E.18_checklist.md) owns current requirement coverage. [Screenshots](screenshots/index.html) support observations without replacing functional checks.

Supported tasks are cold/warm download-cache trials and one/two-slot independent hosted execution of the complete E.17 native workload plus pinned utPLSQL. Prerequisites are authenticated GitHub CLI and sufficient Actions capacity. Local performance is not measured. Host background demand and small samples limit recommendations.

Private inputs are newly generated per job. Never copy retained laboratory credentials to a hosted job. Interrupted runs should be inspected for the always-run cleanup outcome; ephemeral hosted machines provide the final isolation boundary. A failed or missing cleanup receipt is not a successful sample. Do not delete shared local scratch or retained credential records when reproducing this experiment.

The [measured report](capacity_report.md) owns numeric results and recommendations, and the [handover](sprint_E.18_handover.md) owns the live review/closure record. [README](../../README.md) returns to project orientation.
