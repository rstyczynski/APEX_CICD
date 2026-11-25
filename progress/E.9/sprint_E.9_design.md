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
GitHub protections require hosted evidence and are a separate verification gate.
