# E.9 design

Self-approved under delegated YOLO authority. [Setup](sprint_E.9_setup.md)
owns scope; [implementation](sprint_E.9_implementation.md) records behavior.

Controller policy requires security, correctness and testing assessments,
known severities, no unresolved blocker, and reason plus evidence for dismissal.
The authenticated submitter is an argument from trusted caller context, never a
report field. Candidate tuple is base, head, policy digest, immutable report
hash. Store canonical report bytes outside source, rehash on read, and compare
the live report revision. Head/base/policy changes, edits, withdrawal, deletion
and publication races revoke authorization. Merge requires Testing and Review
success from selected publishers for the current tuple, no open conversation,
and independent approval when selected. Bypass is separately recorded.

### Testing Strategy

SM-1 compiles the controller. UT-1 accepts a complete report and challenges
missing assessments, unauthorized submitters, unknown severity, blockers and
acknowledgement-only dismissal (PBI-069). UT-2 mutates each tuple field, edits,
withdraws, deletes and races publication (PBI-070). UT-3 denies missing, stale,
failed, wrong-publisher evidence, conversations, unauthorized writers and absent
independent approval; records bypass (PBI-071). IT-1 creates real Git base/head,
retains annotations through initial/refreshed summaries and corrects unsupported
success; accepts a real Codex report and merges through the controller (068–071).
No database changes. Full smoke/unit regression uses tests/run.sh.

## Test Specification

Register wrappers in component_review.manifest and the delivery manifest.
Tests first fail importing the absent controller. Synthetic negative records
prove policy logic only. A local Git merge proves controller integration only;
GitHub-specific protection qualification would require hosted evidence; it is not required by the backlog. The authenticated service below is the selected repository-control experiment.

## Resumption design — local authenticated service

The earlier hosted-only gate was an implementation choice, not a backlog
requirement. Replace that choice with an actual loopback HTTP service owning a
disposable Git repository. Separate random bearer capabilities authenticate the
developer, Testing publisher, reviewer, integrator, independent approver and
administrator. Caller-supplied role strings confer no authority. Capability
secrets exist only in test-process memory and transient private test directories.
The trusted service and host administrator are outside the proposed-source trust
boundary; hostile same-OS-user isolation remains E.10, not an E.9 claim.

Every mutation and merge shares one server lock. Review publication validates a
snapshot, releases the lock for preparation, then compares the entire generation
before publishing under lock. Merge revalidates current base/head/policy/report,
checks authenticated publisher records, conversations and independent approval,
constructs a real Git merge commit and updates main with Git compare-and-swap.
Direct receive-pack writes are refused by a real pre-receive hook. Only the
trusted service's merge endpoint changes the protected ref. This is a local
capability/protected-ref experiment, not GitHub rule qualification. Merge queue
is not selected; independent approval and auditable administrator bypass are.

Add IT-2 before implementation: start the service, reject invalid credentials
and role spoofing, execute every report/freshness/merge refusal through HTTP,
race publication and merge against candidate events, retrieve immutable accepted
report bytes, reject a native Git receive attempt and perform the allowed merge.
Accepted report history survives editing, withdrawal and logical deletion. Keep
server receipts and Git bundle. Unit tests continue covering pure policy logic.
