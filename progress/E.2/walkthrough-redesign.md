# E.2 — PROJECT-focused walkthrough design correction

This correction defines the preloaded, native-command operating journey.
A/B/C capture and D's mapped integration assessment are implemented and observed.
The native APEX availability correction was approved on 2026-10-20; its scope and
remaining verification finding are recorded in the
[design](sprint_E.2_design.md#approved-mapped-integration-completion--2026-10-20)
and [implementation](sprint_E.2_implementation.md#completed-mapped-initial-integration-exercise).
The [operating guide](cicd-walkthrough.md) contains D's exact commands and results.
Same-byte UAT promotion and baseline capture are now exercised through the
small wrapper prototype. F1 native Working Copy refresh/merge and PROJECT
capture are rehearsed on a separate Main copy, with exact operator steps for
verification on 810003. F.2 now supplies the native Hello patch and rehearsed
fresh/populated integration qualification. UAT promotion is ready for operator
execution. The Product Owner subsequently reported F completed. G now has an
operator procedure with clean SQLcl 25.4.1 native comparison; it preserves the
F artifacts and UAT. H–I remain separate work. Historical
exercise evidence and the presentation Markdown remain unchanged.

## Product Owner direction

Start from zero after removing the project Podman machine. Demonstrate how
SQLcl PROJECT is used with a preloaded, functional application. Make Foundation,
Hello, World, initial delivery and upgrade outcomes understandable as in E.1.
The operator must not create applications, pages or LOVs to prepare the exercise.
A small Working Copy edit is an appropriate operator action. Stop repairing the
old runs as the route to the revised walkthrough.

## What failed in the previous design and implementation

The approved design selected a reduced fixture created in Builder. The delivered
fixture exposes Home and History but no greeting controls. Hello/World assertions
run in the database, while the walkthrough sends the operator through extensive
Builder setup. High-level B orchestration hides the native PROJECT operations
the Product Owner wants to inspect. Title/Name confusion and incomplete recovery
then require repair work before the intended demonstration becomes visible.
This is a mismatch in the demonstration design, not merely unclear wording.

## Proposed journey

1. **Prepare the lab and preload reviewed inputs.** Follow pinned infrastructure
   installation from an absent `apex-cicd` machine. A bounded setup operation
   loads a versioned native application export and its schema/data inputs into
   owned authoring resources. Print usable login details and URLs. Show a working
   Hello/World application before asking the operator to begin PROJECT work.
   Browser-visible greeting, component versions and saved history are required;
   no manual application/page/LOV construction belongs to this journey.
2. **Initialize PROJECT in a new Git repository.** Show and execute native
   `project init`, inspect `.dbtools/` and explain the schema/application capture
   boundary. Keep tool setup and application repository responsibilities clear.
3. **Capture and review.** Show `project export -list` and `project export`.
   Inspect actual SQL/YAML and schema files, Git status and diff. Explain how
   Foundation objects and Hello/World components map to captured source and
   declarations. Retain reviewed source before staging.
4. **Stage a deliverable.** Show `project stage -branch-name ...`, inspect
   generated changelogs and use `project stage add-custom` only for intentional
   release data. Explain dependency order and the one migration authority.
   Show the target defaults-file hook and component declaration separately as
   adaptations, not silently attributed native PROJECT capabilities.
5. **Verify, package and deliver.** Show `project verify`, `project gen-artifact`
   and `project deploy` with exact pinned-client arguments. Open the reconstructed
   working application. Show identical-artifact qualification/promotion, archive
   identity and saved-history preservation. A failed native verification blocks
   formal release; a prerelease assessment must be labeled as such.
6. **Make a small Working Copy change.** Supply Main already working. The operator
   creates a copy, makes a visible bounded change, compares/refreshes/merges it,
   and captures the agreed Main checkpoint with PROJECT into the same repository.
   Do not use a document-title-only change as the sole visible application result.
   Keep the checkpoint, Git and Working Copy reasoning together.
7. **Capture and deliver the upgrade.** Inspect the actual component change,
   stage it from the declared baseline, package and qualify a fresh reconstruction
   plus the populated upgrade. Open the result and show the intended change and
   retained history/settings. Repeat delivery with an explained outcome.
8. **Show bounded rejection and assess findings.** Demonstrate declared dependency
   rejection and stale artifact binding using retained E.1 controls where needed.
   Distinguish those controls from native PROJECT behavior. Reconcile follow-up
   with the existing gap analysis/backlog; complex Foundation upgrades stay E.5.

## Preloaded application decision to settle in design

Prefer reviewed E.1 business application/schema inputs over inventing another
empty fixture. Its exported application has an `E1_CTRL.e1_release.assert_runtime`
dependency and native availability restrictions. The preload design must enumerate
and provision the required control objects, grants, accounts and initial runtime
state, or explicitly specify and justify a scoped native-source adaptation.
It must not silently remove a runtime gate to make the browser open, nor claim
that importing the application alone reproduces E.1's protection guarantees.

Define the displayed Foundation/Hello/World checkpoints and exact reviewed inputs
before implementation. If component-by-component assembly is shown, prepare its
input snapshots and native PROJECT comparison bases; do not fake three independent
component releases by changing version labels. If the primary journey starts
from the complete preloaded assembly, label assembly as preparation and show
the initial-to-patch delivery as the executed PROJECT journey.

## Operating interfaces and readiness

Setup helpers may provision owned resources, obtain credentials and preload
reviewed inputs. The operator-facing delivery chapters must show the exact native
PROJECT command, its connection and working directory, its inputs, output and
next decision. Keep commands executable directly in the documented SQLcl session;
a wrapper invocation alone is not the teaching interface. Section scripts remain
separate and expose equivalent commands and progress when used for replay.

Each chapter needs starting state, numbered actions, expected browser/terminal
result, stop conditions and a usable resume command for its human checkpoints.
Validate the complete written journey from an absent VM, then repeat its small
edit/recovery path before giving it back as ready. Retain failed attempts and
distinguish rehearsal from Product Owner acceptance.

No new implementation or resource provisioning is claimed by this design note.
The managed review must settle the preload dependency closure and the exact
component-stage journey before implementing the replacement exercise.

## Authorized reset performed — 2026-10-19

The Product Owner explicitly requested destruction of the project Podman machine.
Executed `podman machine rm --force apex-cicd`; it exited successfully. A subsequent
machine inventory contains only `apex-cicd-rehearsal` and `podman-machine-default`,
both stopped. The project VM and its database/APEX state are gone. Host-side
Git repositories, source, local credentials/tools and historical evidence were
not deleted. Existing run inventories describe the destroyed runtime and cannot
authorize reuse against a newly provisioned database.
