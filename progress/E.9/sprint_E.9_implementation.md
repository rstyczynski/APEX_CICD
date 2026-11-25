# E.9 implementation

[Design](sprint_E.9_design.md) defines the experiment; [tests](sprint_E.9_tests.md)
own the results. `scripts/review_control.py` implements pure policy validation,
canonical report hashes, freshness, a second publication read and ordinary merge
eligibility. `tests/review_lab.py` constructs a real disposable Git history,
executes a greeting assertion and merges through the controller. Source history
is retained in `tests/candidate.bundle`; reports are retained outside that source.

Codex reviewed the retained initial and refreshed diffs in a serial reviewer
role. The report template records actual observations, including blank-name
limitations and one-assertion coverage. Reusing that template for identical
content does not mean a new agent invocation occurred on every test execution.
The two summary documents retain the developer annotation, distinguish unrun
and passing tests, and remove a deliberately unsupported security-success claim.

## Trust boundary and unresolved work

The controller trusts caller-supplied submitter, writer, approval, publisher and
candidate state. The local test deliberately injects these values. It rejects
unauthorized *values*, but cannot authenticate a caller or prevent direct Git
writes. The publication double read rejects the injected race between reads;
it does not close the race after that read. The report hash detects editing,
but the filesystem has no server-enforced immutable retention or withdrawal log.
These are material implementation gaps, not independent production concerns
that may be waived from the accepted experiment.

The completed local work must be retained as a prototype only. It is not wired
into production workflows. E.9 remains Progress; no PBI is asserted Done. A
hosted disposable-repository exercise needs a candidate pushed to a repository,
protected branch/rules administration and test identities with distinct
privileges. Current authorization explicitly forbids remote pushes. A pure local
library, synthetic event replay or read-only GitHub inspection cannot establish
server-enforced direct-write refusal and an atomic integration boundary.

The supported local alternative would be a real authenticated Git server with
trusted receive hooks and distinct principals. This checkout provides no such
configured service or principals; inventing identity strings cannot substitute.
No convenience-tool failure blocked local implementation or testing.
