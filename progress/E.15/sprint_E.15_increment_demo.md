# E.15 demonstration walkthrough — draft

The goal is a real PR through Oracle Testing, Review and ordinary enforced merge, including failed freshness/authority/isolation/cleanup attacks. [Checklist](sprint_E.15_checklist.md) tracks each mandatory outcome. Current starting state is a private sanitized sprint repository with trusted workflow source and one open PR. This draft is not a completed live demonstration or accepted handover. The presentation and slide map remain pending verified outcomes.

## Inspect the proposed change

The GitHub CLI reads the actual PR and its diff; it does not merge or publish validation. The expected visible change is concatenation of Hello and World with identical result.

```bash
gh pr view 1 --repo rstyczynski/APEX_CICD_E.15
gh pr diff 1 --repo rstyczynski/APEX_CICD_E.15
```

## Inspect trusted execution

The list command shows workflow event, branch, run ID and conclusion. Open the actual run log with the returned ID. An Oracle job must show container health, pinned driver installation and the real greeting/schema assertion. The latest initializer revision additionally proves the target private table exists before application-user denial. Earlier runs do not establish that stronger test.

```bash
gh run list --repo rstyczynski/APEX_CICD_E.15 --limit 10
```

## Inspect the merge-control limitation

The API request reads branch protection only. Current observed response is HTTP 403 requiring GitHub Pro or public visibility. Fixing the YAML dispatch issue did not fix this independent account boundary. A user-visible public conversion requires Product Owner authorization; the question is pending. Ordinary merge, stale publication, concurrent PR interruption and cleanup acceptance exercises are still pending.

```bash
gh api repos/rstyczynski/APEX_CICD_E.15/branches/main/protection
```

## Draft presentation map

The [editable deck](sprint_E.15_increment_demo.pptx) contains 12 slides: scope 1–3, architecture 4, Oracle journey 5–7, failures/interruption 8–10, remaining acceptance 11 and Q&A 12. All slides were rendered and inspected in a contact sheet; package, layout, approved fonts and first-party import checks passed. The deck describes a partial increment and cannot serve as completed integrated handover.

## Trusted Review

The Codex reviewer role inspected candidate B's actual one-line SQL diff. It preserves the greeting without new privileges or data access. Trusted main revision 664ed35 records the report outside candidate control, binds it to SHA-256 of the reviewed SQL and rejects changes outside candidate.sql. This is an implementation choice to make this bounded fixture review reproducible. It does not establish GitHub enforcement or general application review quality. A fresh candidate B run is exercising that step; earlier passing runs do not prove it.
