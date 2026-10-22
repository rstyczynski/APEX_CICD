# SQLcl PROJECT — assumptions, weaknesses and requirements fit

The register below preserves the accepted analysis-stage hypotheses. Current
execution results and fit dispositions are maintained in the
[gap analysis](oracle-gap-analysis.md); the statements about unexecuted work
below describe the analysis baseline, not the present laboratory state.

## Decision and evidence level

Source review date: 2026-10-19.

The decision is whether SQLcl PROJECT is an appropriate lifecycle tool for
this laboratory's requirements and developer/operator journeys. Command
coverage, Oracle recommendation and a successful demonstration are not by
themselves acceptance criteria. Compare the native workflow with the E.1
lower-level SQLcl/export plus reviewed-migration approach, including the effort
and controls required to make each satisfy the same relevant outcomes.

Current verdict: **conditional fit for the source/distribution/release core;
not yet validated for adoption, and not established as a complete solution to
all delivery requirements.** This is a documentation/code assessment. No native
PROJECT exercise, baseline synchronization or deployment has been executed in
E.2. Do not change requirements merely to make the tool fit.

The [SRS](../../docs/srs.md#functional-requirements) owns requirements. The
[analysis](sprint_E.2_analysis.md) owns AN-02 and EQ-2, and the
[review summary](sprint_E.2_inception.md#project-fit-decision) presents this
assessment. This register expands those findings; it does not introduce new
PBIs or independently approve experiments. The relevant baseline is APEX 24.2
and SQLcl 25.3.0.274.1210. E.1-stage authoring/reservation policies are subject
to reevaluation; preservation, attributable source and observable correctness
remain acceptance obligations.

“Possible design assumption” below means an inference from the documented
abstraction and operating model. It is not a claim about Oracle designers'
intent. Distinguish a documented limitation, an assumption to test and an
obligation outside the tool's documented scope. A missing guarantee in a
command reference is not proof that no supported solution exists.
An ordinary tool responsibility boundary is not itself a defect; its effect
on required integration, risk and operating effort determines suitability.

## Optional use and repository compatibility

PROJECT may be an optional alternative even if it does not become the default
delivery tool. The [analysis hypotheses](sprint_E.2_analysis.md#optional-tool-compatibility-hypotheses)
separate adoption from keeping a viable supported entry path. H-1 evaluates
native repository conventions versus a bounded adaptation, including verified
baseline adoption, source identity, one migration authority, component metadata
and switching cost. Existing-Git initialization is documented; compatibility
with this repository is not yet demonstrated. A layout resemblance alone does
not pass. PF-01–12 still apply to any claimed supported route.

H-2 independently evaluates optional Working Copy authoring feeding accepted
Git source. It does not imply that Working Copies prescribe a Git layout or
that PROJECT is required to capture their accepted changes. The combined
workflow must pass both assessments. No source tree is moved and no alternative
migration history is initialized during analysis.

## Reading the supplied Pretius article

Rafał Grzegorczyk's [article](https://pretius.com/pl/blog/project-oracle-sqlcl)
is dated 12 December 2024 and uses SQLcl 24.3.2. It demonstrates both initial
adoption and later changes, including explicit DML through custom staging.
For an existing target it marks the baseline through changelog synchronization.
Its conclusion recommends experimenting to determine suitability. Treat this
as a useful worked example and source of hypotheses, not evidence that the
lab's full requirements or the pinned 25.3 behavior have passed.

Version-specific Oracle sources below control technical conclusions. In
particular, the article's initial same-object-count statement is not sufficient
evidence that two installed definitions or their data are equivalent. Existing
E.1 migration identities must also be reconciled before adopting a different
generated changelog. No synchronization command is authorized by this analysis.

## Enumerated fit assessment

### PF-01 — Object state does not establish business-change intent

**Possible assumption:** developers can express the desired structural state
in DEV and use generated differences for routine evolution. Oracle describes
[snapshot/branch-diff generation](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/introduction.html),
section 6.1.4, and [custom staging](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
section 11.16.8.

**Weakness to assess:** structural differences alone do not establish the intent
of seed/configuration changes, data corrections or a data-preserving semantic
migration. Custom SQL is an intended extension, not automatically a tool defect.
For FR-1–5 and NFR-2, validate one intentional data change alongside generated
DDL, with its order and repeat behavior reviewed and old user configuration
unchanged. Verdict: conditional fit with explicit data-change responsibility;
automatic migration of arbitrary business intent is not established.

### PF-02 — A scoped DEV export must represent coherent accepted work

**Possible assumption:** the selected source application/schema is a suitable
capture boundary. [25.3 export filters](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/refining-exports-filters.html),
section 6.4, define selection, including particular application IDs.

**Weakness to assess:** a syntactically valid filter can still admit an unwanted
Working Copy, temporary object or unrelated team change, or omit a dependency.
Filter validity does not establish a coherent multi-object authoring checkpoint.
For FR-5/8/12 and NFR-1, inspect a complete expected/actual inventory and show
how pending work and source changes during capture are handled. Verdict:
configuration and coordination required; capture consistency remains unproved.
Do not presume an atomic cross-object snapshot or presume that none is possible.

### PF-03 — The Git comparison base and generated distribution must agree

**Possible assumption:** the current source branch and declared base describe
the intended change set. [About PROJECT](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html),
section 6.2, explains staging from that comparison.

**Weakness to assess:** a clean text merge does not prove the staged scripts
still implement the accepted source after parallel work, a changed base or
conflict resolution. This is not evidence of an existing staging bug. For
FR-5/8/11 and NFR-2, bind source, base, generated distribution and validation;
make a controlled base/source change and establish which regeneration and
revalidation are required. Verdict: plausible fit, pending branch/stage
consistency evidence rather than acceptance of a single linear example.

### PF-04 — Generated DDL still needs populated-target qualification

**Documented boundary:** Oracle requires build checks and testing against
systems with data in addition to `project verify`; its example includes a
constraint change conflicting with existing rows. See [25.3 release guidance](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html),
section 6.2.

**Weakness to assess:** a valid generated change can be inappropriate for an
actual target state. For FR-4/5/6 and NFR-2, qualify fresh and the declared
upgrade baseline, compare all retained history/settings fields, and repeat the
same artifact. Include a controlled invalid populated start that fails visibly.
Verdict: fit only with data-aware qualification; verify alone is insufficient.
Complex Foundation transformations stay in E.5 after stabilization.

### PF-05 — Automatic generation has a version-specific coverage boundary

**Documented limitation:** [25.3 supported objects and staging caveats](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/introduction.html),
sections 6.1.1–3, distinguish supported generation, custom additions and
limitations such as annotation-only table changes. They also require review
of some generated deletion statements.

**Weakness to assess:** export success does not establish complete executable
distribution. For FR-5/12/13, inventory the actual lab objects/dependencies,
review every staged change, and identify manual additions or unsupported cases.
Verdict: conditional fit for a declared object/change profile. A documented
limitation becomes a blocker only if a required case has no acceptable supported
path. Unused object types are not current blockers; fixed release-note bugs
must not be reported as observed defects.

### PF-06 — Brownfield adoption assumes a verified starting baseline

**Possible assumption:** an existing target already contains the definitions
being admitted into migration history. Oracle documents
[changelog-sync](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/liquibase.html),
section 11.12.2, as marking changes executed; that is not verification of their
effects. The article uses this operation for its existing target.

**Weakness to assess:** marking an unverified baseline can conceal missing or
different objects. Matching counts and version labels are insufficient. For
FR-10/12 and NFR-2, compare definitions/dependencies, reconstruct a fresh target,
reconcile existing E.1 migration history and deliberately reject a mismatched
adoption start. Verdict: conditional adoption path; synchronization cannot
substitute for baseline evidence. Do not deploy an initial creation script
blindly over a populated retained target either.

### PF-07 — Environment substitution does not by itself prove stable identity

**Possible assumption:** declared workspace/schema/application mappings define
the deployment target and the intended replacement behavior. The paper pages
29–30 and [APEX 24.2 import examples](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/Import-Script-Examples.html),
section 8.4, describe mapping capabilities.

**Weakness to assess:** ordinary installation success is narrower than stable
component IDs, retained saved reports and clean source comparison across
developer areas. For FR-6/11/12 and NFR-2, verify actual target identity and
repeat/upgrade identity behavior, using the
[E.1 identity evidence](../E.1/tests/apex_identity_20261018.txt) as the comparison.
Separately assess the paper's page-34 branch-instance identity requirement.
Verdict: mapped deployment is documented; our complete identity contract is
pending execution, with no assumed equivalence or incompatibility.

### PF-08 — Semantic versioning and component dependencies require validation

**Possible assumption:** one staged project release is a useful deployment
unit. Oracle's [release command](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
section 11.16.6, labels a body of work; it does not establish the lab's business
compatibility declarations.

**Weakness to assess:** do not equate the project version with Foundation,
Hello and World interface compatibility or their runtime state. For FR-7/9,
demonstrate the component manifest/installed records and accepted/rejected
combination around a native artifact. Verdict: not established as a native-only
solution to these requirements; supported project-specific checks may compose
with native delivery. Any policy simplification needs an explicit decision.
No Foundation version coexistence or independent availability is proved here.

Explicit validation must determine whether PROJECT provides semantic-version
and dependency behavior natively, through documented bundled facilities, or
only through project-specific additions. A `-version` argument establishes
neither support nor absence of semantic-version interpretation.

Apply the [Elaboration criticality decision](sprint_E.2_analysis.md#elaboration-criticality-decision--component-contracts):
the required outcome is preservation/enforcement of explicit approved component
combinations, not automatic inference of compatibility from changes. E.1's
bounded manifest/checks are the comparison baseline. Version parsing, ordering
and range support below are capability discovery; inspect documentation/help
before allocating runtime exercises. They do not require building a general
resolver or interface analyser. Select only missing observations that can
change the architecture/fit verdict.

1. **Version interpretation:** are versions opaque labels or parsed semantic
   versions? Check supported syntax, numeric ordering such as 1.10.0 versus
   1.2.0, and invalid-version handling. Record prerelease/build metadata support
   as capability discovery, not an additional mandatory lab feature. Syntax
   handling does not prove that a code change is actually compatible.
2. **Component declarations:** can Foundation, Hello and World have separate
   versions and declared dependencies within one project? Identify the supported
   declaration format and whether exact versions, ranges or only release
   ordering are understood. The lab requires explicit approved combinations;
   a general range resolver is not added to scope by this check.
3. **Compatibility enforcement:** show an allowed combination accepted and a
   proposed incompatible Foundation major version rejected while Hello/World
   still require the earlier contract. Assess missing, unknown and inconsistent
   metadata too. Require rejection before migration/import writes, with target
   definitions and retained data unchanged. Migration ordering alone is not
   semantic compatibility enforcement.
4. **Source-to-target consistency:** establish that declarations survive source
   review, staging and artifact generation, and that admission checks use both
   observed installed versions and proposed versions. Reconcile final installed
   metadata with the same artifact's declarations; a filename is insufficient.
5. **Fit verdict:** identify native, bundled, configured and custom guarantees
   separately. If a separate compatibility check is needed, evaluate that
   integration rather than attribute it to PROJECT. Determine whether the
   resulting solution satisfies FR-7 and relevant FR-5/9/10 obligations.

These are inputs to the managed exercise design, not executed tests. The
incompatible-major example tests metadata admission without implementing a
Foundation 2.0 transition. Complex schema/API upgrades remain in E.5.

### PF-09 — Migration tracking is not the complete live-target safety contract

**Possible assumption:** an appropriately controlled target is available to the
installer. [PROJECT deploy](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
section 11.16.5, executes the artifact installer. That description alone does
not establish target-wide fencing, live-content admission or application
request draining. [DDL commit semantics](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/COMMIT.html)
also prevent assuming all-or-nothing release behavior.

**Weakness to assess:** recorded migration history cannot alone establish actual
live content or safe recovery after every partially committed operation. For
FR-6/9/10, establish guards for wrong/stale/drifted targets, competing or
interrupted deployment and inspected forward repair, proportionate to approved
exercises. Verdict: native-only fulfillment is not established; additional
coordination/control may be required. Reevaluate E.1 implementations without
silently deleting the required safety outcomes.

### PF-10 — Project verification is not application acceptance

**Documented boundary:** [25.3 release guidance](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command.html),
section 6.2, calls for separate system testing. Paper pages 22–26 and 40–44
place logic/UI tests and pipeline progression around the lifecycle commands.

**Weakness to assess:** structural verification can be useful without detecting
an incorrect greeting, lost history, authorization regression or unusable page.
For FR-1–5/13 and NFR-3, use separate business/browser tests, retain reports and
prove that failed or stale results prevent downstream deployment. Verdict:
PROJECT can be a delivery engine within the pipeline; full acceptance is an
integration responsibility, not implied by a passing verify result.

### PF-11 — Artifact generation is not the complete promotion-trust contract

**Documented capability:** [gen-artifact](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html),
section 11.16.4, packages project state and offers naming/version options and
an explicit overwrite flag.

**Weakness to assess:** a filename/version does not bind an artifact to an
accepted commit, independent validation or the exact bytes already qualified.
For FR-5 and NFR-1/2, bind source/config/tool versions and checksums; promote
identical qualified bytes and reject changed bytes or stale/missing evidence.
For shared service use, reconcile the PBI-031 trust boundary. Verdict:
conditional fit with artifact/evidence controls; neither reproducible byte
identity across independent builds nor trusted attestation is established by
the packaging command alone. The requirement to promote the same bytes does
not require two independent ZIP builds to be byte-identical.

### PF-12 — A useful CLI core still needs a viable operating model

**Possible assumption:** a team supplies working development areas, database
access, repository conventions, credentials and competent review. Oracle's
[25.3 examples](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project-command-usage-examples.html)
state connection/schema prerequisites. The native CLI is only part of the
complete developer/operator journey.

**Weakness to assess:** an approach can be technically possible yet require too
many fragile manual decisions or excessive custom repair code. For FR-11/13
and NFR-1/2/3, record actual setup/refresh/review/deploy steps, privileges,
error handling and recovery effort. Check the pinned version and supported
interfaces; keep human authoring/review distinct from automated operations.
Verdict: usability and operating fit are unmeasured. Reject claims of lower
maintenance or full automation until the demonstrated workflow supports them.

## Requirements coverage and adoption criteria

FR-1–4 remain application requirements: PROJECT is evaluated on whether delivery
preserves and validates their behavior/data, not on whether the CLI implements
the greeting UI. PF-01/04/10 address that indirect obligation. FR-5 maps to
PF-01–05/10/11; FR-6 to PF-04/07/09; FR-7 to PF-08; FR-8 to PF-02/03 and the
Working Copy assessment; FR-9/10 to PF-06/08/09; FR-11 to PF-03/07/12; FR-12 to
PF-02/05/06/07; FR-13 to PF-05/10/12 and supported integration paths. NFR-1–3
are evaluated through capture scope, privileges, provenance, reproducibility,
preservation, actual test results and error handling. This is a coverage map,
not a list of passed requirements.

Adopt PROJECT as the lifecycle core only if the selected supported profile can
meet these obligations with reviewed configuration and justified supplements,
and the observed operating burden is acceptable. Accept an explicit bounded
limitation where the corresponding requirement is not applicable or the
Product Owner approves a changed scope. A required case with no safe supported
path is a blocker for that profile, not automatically for every PROJECT version.
If native adoption requires recreating most of E.1 around it, compare that cost
with retaining lower-level Oracle tools and explicit migrations before deciding.

Validation must distinguish three outcomes: established by current official
documentation/source; conditionally covered by configuration/integration; and
pending a focused runtime exercise. The twelve entries are the requirements
validation plan and provisional assessment. They do not mark runtime fit passed.
Derive the smallest exercises that discriminate between native adoption,
qualified adoption with supplements and retention of the lower-level approach.
Keep complex Foundation upgrades in E.5 after toolchain stabilization.

## Backlog and process boundary

PF-01–07 reconcile with PBI-020/021/027/035/036/037/038 and collaboration
PBI-019/039. PF-08/09 reconcile with PBI-021–024/045. PF-10 maps to
PBI-034/040/041/043. PF-11 maps to PBI-021/030/031/043. PF-12 maps to
PBI-017/025/027/028/029/046/047. These are existing outcomes, not newly assigned
work. E.2 may establish the discriminating evidence without completing the
later full workflows. Analysis remains at managed review; exercise design and
implementation have not been accepted by adding this register.
