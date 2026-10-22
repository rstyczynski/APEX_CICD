**Round:** E.2 design-document review, round 1  
**Subject:** proposed exercise design and test specification (`progress/E.2/sprint_E.2_design.md`)  
**Repository:** https://github.com/rstyczynski/APEX_CICD (clone: https://github.com/rstyczynski/APEX_CICD.git)  
**Reviewed SHA:** `74bff78f48cbac91beb867d38d1ce555c354a9a2` (detached HEAD at “docs(e2): prepare approved-analysis follow-up and design review”)  
**Reviewer/model:** Grok 4.7 (independent external)  
**Date of review:** 2026-10-19  

**Actual inputs inspected:**  
- Primary design: `progress/E.2/sprint_E.2_design.md`.  
- Approved analysis and supporting records: `sprint_E.2_analysis.md`, `sprint_E.2_inception.md`, `project-fit-assessment.md`, `sprint_E.2_analysis_review-1.md` (prior independent review with no findings), `sprint_E.2_analysis_review-1-response.md`, `sprint_E.2_assessment.md`, `sprint_E.2_setup.md`, `sprint_E.2_proposedchanges.md`, corrected design-review prompt.  
- Wider context: `docs/srs.md` (actors, UC mappings, FR-5/6/7/8/9/10/11/13), `docs/architecture.md`, `docs/test-profile.md`, `BACKLOG.md`, `PLAN.md`, `PROGRESS_BOARD.md`, `ROADMAP.md`.  
- E.1 implementation relevant to the design: `release/manifest.json`, `scripts/cicd-artifact.py`, `scripts/cicd-compatibility.py`, `deploy/operator/capture.sql` and related operator scripts, `config/areas.json`.  
- Oracle paper: `refs/apex-lifecycle-management-v3.pdf` (v3.2).  
- Official version-specific documentation re-checked for design-relevant claims: APEX 24.2 Working Copies (section 5.9.1), SQLcl 25.3 PROJECT command (section 6.2 and examples), related export/filter, staging, Advisor and subscription references.  

**Checks performed:**  
Read-only inspection of the pinned commit; traceability of design children, exercises X1–X3 and conditional EQ-3/EQ-5 handling to approved analysis (H-1/H-2, EQ-1–5, AN-01–14, PF-01–12); evaluation of reduced fixture scope and stated limitations against intended conclusions; assessment of resource ownership, preservation, stop conditions and bridge binding; review of test oracles and the proposed regression-scope amendment; verification that later-sprint allocations (E.3/E.4 full workflows, E.5 Foundation upgrades, PBI-052) remain deferred.  

**Exclusions / unexecuted:**  
No repository scripts, SQL, tests, installations, provisioning or live Oracle calls were executed. No source changes, commits or external uploads. Historical E.1 evidence and documentation claims were treated as previously reviewed baseline, not re-executed.  

## Finding-status table

| ID     | Severity (relative to Elaboration) | Status | Summary |
|--------|------------------------------------|--------|---------|
| —      | —                                  | —      | No findings. Design is sufficient for Product Owner acceptance. |

No open, accepted or deferred design findings. New findings would use stable IDs `R1-H1`, `R1-M1`, `R1-L1`, etc., explicitly scoped to E.2 DESIGN round 1, with initial status `open`. None are required.

## Detailed findings

None. The proposed design meets the criteria for focused exercise design and subsequent gap-report / roadmap / handover preparation.

## Design blockers, non-blocking refinements and later work

- **Design blockers:** None. Traceability to the approved analysis is coherent; the four child outcomes (PBI-051.1–.4) are well-scoped and dependency-ordered. The reduced greeting/LOV fixture is explicitly limited to transport, migration, identity and metadata conclusions; omitted E.1 behaviors (full fencing, controller dependence, account security, availability) are identified as unproved and left to existing follow-ups. Working Copy authoring, team checkpoint, Git acceptance and reconstruction (X1) address EQ-1/H-2 with concrete oracles (both headings, LOV/greeting, stale/deletion/abandonment, shared-schema marker, usability effort). PROJECT’s complete capture/staging/release/deployment workflow (X2) addresses EQ-2/H-1 with generated vs. intentional changes, fresh/baseline/repeat, mapped identities and optional coexistence trial without competing source or migration authorities. The declaration bridge reuses the existing `cicd-compatibility.py` validator, binds archive/source/declaration/target/observed state, blocks deploy before writes on failure, and separates unit-injected control-flow proofs from required real-target observations. Resource ownership, retained-E.1 preservation, foreign-target refusal, read-only preflight and non-automatic cleanup are concrete. Test oracles are meaningful and observable. The planned gap report, roadmap and reproducible live handover distinguish evidence levels and preserve later-sprint allocations.  
- **Non-blocking refinements:** None required before implementation. The regression-scope proposal is proportionate and correctly flagged as requiring explicit Product Owner inclusion in design acceptance (see assessment below). Minor documentation cross-references could be tightened after approval but do not affect exercise selection or safety boundaries.  
- **Later product work (correctly deferred):** Full pipeline delivery and hosted workflows (E.3/E.4), complex Foundation upgrades (PBI-048–050 in E.5), automatic semantic inference, general dependency resolver, PBI-052 contract-definition delivery, and nonessential subscription-specific exercises. Private-instance cloning and additional committed-DDL fault injection remain conditional amendments only if a recommendation depends on them.

## Regression-scope proposal assessment

The proposed E.2-only domain regression (`oracle_lifecycle` covering helpers, fixtures and reused compatibility behavior) is justified and proportionate. Existing registered E.1 integration tests write retained E.1 state and include unfinished acceptance criteria; blindly replaying the full suite would conflict with the design’s preservation boundary and the known unfinished status of those tests. Production E.1 code remains unchanged under this proposal. The design correctly states that PLAN still requests the full registered suite, that the amendment has not been applied, and that design acceptance must explicitly include the scope change (or retain the full gate only with a separately safe disposable E.1 topology). No silent narrowing or manufactured passes are proposed. The proposal is acceptable as part of design acceptance; it does not itself constitute a design defect.

## Consequential Oracle claims verified and unresolved evidence limitations

**Verified (documentation / paper, carried forward from approved analysis):**  
PROJECT existing-repo initialization, export filters, generated/custom staging, release/artifact/deploy/verify, data-aware qualification guidance (SQLcl 25.3 section 6.2 and examples; paper pages 18–20, 26–30). Working Copies compare/refresh/replacement merge, unsupported types, manual deletion handling (APEX 24.2 section 5.9.1; paper pages 12–14, 32). Team checkpoint export of agreed Main state into Git. Branch-instance identity requirements (paper page 34). Advisor and related audit interfaces as distinct from unit/browser evidence.

**Unresolved limitations correctly left for exercises (not claimed passed):**  
Actual export fidelity, reconstruction completeness, identity stability under mapping, generated-vs-intentional change behavior on populated targets, native artifact metadata carrying capacity, practical usability and operating effort, shared-schema exposure, and real-target admission observations. No runtime verification has been performed under this design.

## Conclusion

**Ready for Product Owner design acceptance.**

The design is coherent with the approved analysis, appropriately bounded, safety-conscious and decision-relevant. It supports the four child outcomes, reduced-fixture X1–X3 exercises, conditional source-first handling of EQ-3/EQ-5, explicit custom-bridge trial, and the proposed E.2-only regression scope. Acceptance of this design (including the regression-scope amendment) is required before code, test skeletons, provisioning or runtime exercises. Expert agreement does not authorize implementation, amend PLAN or close the sprint.