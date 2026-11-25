# E.12 verification defects and repairs

These defects are folded into the active sprint's mandatory quality work under [PLAN](../../PLAN.md), not promoted into new product scope. [Implementation](sprint_E.12_implementation.md) owns the repairs, [test results](sprint_E.12_tests.md) own verification, and the [requirement checklist](sprint_E.12_remaining_work.md) owns remaining acceptance. Historical failed logs remain evidence of failure.

## Runner dropped the final manifest record

Observed full integration ran twenty entries while its manifest contained twenty-one; the final Foundation entry lacked a trailing newline. The Bash loop now processes a nonempty record returned at EOF. The real runner unit case executes the same record with and without a trailing newline and requires one execution in each case. Full unscoped integration must still prove that the Foundation entry is included.

## Historical controller used an incompatible retained fixture

The old E.1 checks expected four/five changelog entries and controlled initial/patch receipts. Retained native UAT had a different lineage, while isolation recreated integration_test without reconstructing its application. Replaying those checks against retained state was invalid. A separate labelled database now supplies the exact FREEPDB1/schema/application identities with fresh private profiles and input files. The initial E12REG alternative failed native identity checks and was retired rather than changing those checks. The retained native UAT is not reset or adopted.

## Full release test was an unconditional failure

The IT-1 stub could never pass. It is replaced by real source validation, archive creation, clean reconstruction, fresh/baseline patch qualification and promotion. The accepted corrected source is linked to actual merged PR #1 using read-only metadata and local ancestry. Negative cases cover stale source proof, changed bytes, missing qualification and unsupported starting metadata. Native authenticated HTTP submissions must create an actual additional greeting; API fixture preparation alone does not satisfy that assertion. Repeated admission must take the no-op branch and preserve complete business fields and release generation/receipt.

## Native setup and observation faults

The seed PDB lacked USERS (ORA-00959); ORDS required its documented installer privileges (ORA-01031); an unbounded installer JVM was killed under the VM's memory pressure (exit 137). These were diagnosed and corrected with native setup and bounded temporary heaps. The separate-instance database/ORDS are local regression resources, not production sizing recommendations.

The unavailable Foundation page needs a cookie-preserving HTTP client. Its expected banner exists in create_application.sql; the retained later DEV state was not that snapshot. SQLcl's generated DATABASECHANGELOG_DETAILS view also remained invalid after the initial Liquibase creation of DATABASECHANGELOG. Native dependency recompilation cleared the sole observed compile error, and the original integrity gate remains enabled.

## Original-history evidence gap

The first experiment exercised intentional update/delete challenges but had no untouched original history sentinel. ID 0 was added to the 1.0.0 baseline and must retain its complete original message and null language in both representations after upgrade/recovery. The real strengthened A3 run records RETAINED_HISTORY_PASS; a subsequent live query inspected that row, 1.1.0 and language=en. This repairs evidence for PBI-048's existing criterion rather than adding a new one.

Final verification of the combined repairs depends on the stable-source unscoped integration gate and the completed documentation audit. This file does not declare those pending outcomes passed.

## Retired scratch-profile default found during final audit

Although integration already used private profiles, the legacy unit SQL boundary still selected a saved connection under checkout scratch and loaded retired root credentials.env by default. That violated AGENTS.md's current configuration rule. The default author path now uses only the explicitly retained read-only author-schema password lookup, a direct in-memory connection and a temporary native home; a real composition/history check passed with that path. Default administrative/provisioning calls and checkout profile paths are refused. Mutable platform state/credential writers also refuse checkout-local state before reading or writing it. Additional mocked boundary cases verify those refusals and temporary-home cleanup. The retained e1-secrets.json record is not moved, copied, rewritten or deleted, and its production NFR-4 deferral remains explicit.

## Child consumed the runner manifest

The 21:17 full run passed 20 cases but omitted Foundation and failed source stability while credential guards changed. A separate isolated two-case runner reproduction proves a child reading stdin silently consumes the following record. Each test subprocess now receives /dev/null; the actual-runner unit check requires both cases. tests/runner-stdin-defect.log preserves the observed pre-fix failure. A frozen checkout avoids source mutations; before/after hashes retain any difference. The shared real database fixture uses a kernel-owned lock, directly tested to reject a second worker before preparing targets. The current full 21-case rerun remains the acceptance evidence, not the 20-case diagnostic.

## Runner allowed a child to consume its manifest

The two-case reproduction in [runner-stdin-defect.log](tests/runner-stdin-defect.log) executed only the input-draining first case. Each case now receives /dev/null on stdin. The actual runner unit requires both cases and a final count of two, alongside the EOF variants. The stable-source full regression must independently show all 21 registered integration cases.

## Shared fixture concurrency

The 21:34 run's integration-area provisioning returned nonzero while another continuation was also preparing the same fixture. Both active processes were observed; the exact inner SQL error was not emitted. That run failed and is retained, rather than being accepted on a concurrency hypothesis. The new wrapper takes a nonblocking native file lock for its full lifetime. The frozen checkout copies the executable source set and records hashes, so documentation work cannot invalidate or silently change the tested code. Its result is reusable only if its source hashes still match the canonical checkout. This is verification isolation, not a waiver of a failed test.

## Final disposition

All described repairs are verified by the six passing gates in tests/stable-final-gates.json, including the complete 21/21 integration run with outer exit zero. Both runner selection defects are covered by actual-runner unit cases and full selection. Native setup/release/HTTP/preservation/drift checks execute successfully; the strengthened Foundation case runs at the end. All 247 frozen source hashes match before/after and the canonical checkout. Earlier pending statements describe the findings before this final disposition, not remaining failed criteria. No mandatory gate is waived.
