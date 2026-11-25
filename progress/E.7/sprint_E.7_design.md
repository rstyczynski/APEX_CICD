# E.7 — Design

Status: self-approved in explicitly authorized YOLO mode.

## Interfaces and feasibility

Python builds immutable ZIP bundles and a manifest bound to the current Git source, component declarations, SQL migration bytes, application metadata, configuration and test evidence. Verification takes a separately pinned manifest digest, rejects absent/empty evidence and mismatched bytes before Oracle work. SHA-256 integrity relies on the trusted pinned digest; it is not publisher authentication. Native Oracle dictionary views and APEX import APIs are already available on the prepared host. No new GitHub API capability is required.

#### PBI-065

Install baseline 1.0.0, seed an attributable retained row, upgrade to 1.1.0 with an additive column and package change, compare retained data and run consumer calls. Assert actual column type/nullability, named check constraint status, consumer EXECUTE grant, valid package and reference row. Inject each wrong state while migration ledger remains complete; require the selected assertion and restore in finally. Repeat upgrade without changing business rows.

#### PBI-077

Bind exact source revision and migration, contract, configuration, test-report and APEX bytes to an externally pinned manifest digest. Reject modified archive, report and missing evidence before deployment. Receipt records verified digest and observed state; historical versions alone are insufficient.

#### PBI-057

Import app 810703 into E7_APP with release metadata and a visible release region. Install baseline, upgrade and repeat; verify dictionary metadata and actual rendered APEX page independently of database assertions.

### Testing Strategy

SM-1 verifies required sources and syntax. UT-1 challenges digest, archive/report substitution and missing evidence without database access. IT-1 executes the real isolated Oracle upgrade, five state mutations/restoration, preservation, consumers, repeat and APEX metadata. Browser observation verifies the visible identity. A1/A2/A3 precede full B1 smoke and B2 unit regression. No integration failure is accepted as sprint completion.

## Test Specification

SM-1 maps to all assigned items. UT-1 maps to PBI-077 and explicitly tests archive/report substitution and absent evidence. IT-1 maps to PBI-065/057/077; passing requires the retained row, all five negative assertions, restored state, safe repeat and actual metadata for all three installs. Browser release visibility is separately recorded; automated metadata alone is insufficient.

## Finalization correction

The finalization run uses a fresh generated E7R schema, E7C consumer and unused application ID per execution. It verifies the baseline bundle before creating owners/workspace or applying any migration. Every release source input must exactly match HEAD; deployment receipts and the visible APEX region expose that exact local Git release revision. Local acceptance is delegated in YOLO mode; remote publication remains unauthorized. These explicit SQL bundles qualify only the accepted bounded Elaboration upgrade, not the production native PROJECT controller. Fresh targets prevent a repeat rehearsal from masquerading as a previous-state upgrade. The prior 810703 experiment is retained untouched.
