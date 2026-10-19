# Prompts to relay

Fill every bracketed field from actual repository evidence before handing a prompt to the user. These are reusable templates, not artifacts to create unchanged. Keep the expert's allowed actions within the user's authorization and accessible inputs; explicit read-only source review is the normal starting point. If execution is authorized, name the allowed checks and targets rather than granting general mutation access.

## Initial or subsequent expert review

```text
You are the independent external reviewer for [repository/product], sprint [ID], review round [N].
Lifecycle phase and objective: [phase, accepted use cases and the decision this review supports].
Git repository URL: [actual configured project remote URL, or explicitly no remote].
Branch/ref: [named review branch/ref and whether its remote availability was verified].
Review revision: [full SHA]. [Matches maintained baseline / differs as explained].
Source access: [provided checkout/files or repository/ref actually containing this SHA].
Publication evidence: [verified remote/ref and full source SHA, or explicitly attached complete fallback package; never only a local path].
Working changes included: [none, or exact supplied patch/files and their relation to the SHA].
Review subject: the active sprint [ID]. Use the whole project context as needed, including vision, requirements, architecture, backlog and earlier evidence. Explain each finding's impact on this sprint; identify wider concerns as proposed follow-up without changing other sprints.
Reviewed document/stage and filename base: [exact subject and its document stem or stage base; append all review suffixes to this base].
Start with: [relevant source/design/evidence list; additional project context may be inspected within the allowed actions].
Prior rounds and finding IDs: [linked/supplied artifacts, or none].
Allowed actions: [source/evidence inspection only; no execution, target mutation or push unless explicitly listed].

First recheck earlier findings not verified or rejected, retaining their IDs and assessing their closing/deferral conditions. Report verified, still-open or regressed with evidence; do not claim to execute checks you only read about. Then add new findings as R[N]-H/M/L[k], giving severity, source location, impact, proposed correction and acceptance check. Reopen a rejected finding only with new evidence. Identify the exact revision and what you did not inspect or run.

Judge against the accepted phase/objective. During Elaboration, prioritize failures of the demonstration, evidence, reproducibility or safe experiment boundary. Identify production hardening as conditional work rather than treating all production features as current blockers. Be candid; do not merely agree with the engineering position.

Save your response as [exact relative <base>_review-<N>.md path]. Begin with subject/round/type, full revision, reviewer, scope/exclusions, inputs and a per-finding status table, followed by detailed findings. If you cannot write that path, return the complete Markdown for the user to save there. Do not alter project source or earlier review files. Do not request credentials or runtime business data; state unavailable evidence as a limitation.
```

Before handing off, apply the skill's publication/access gate. Attach/supply the actual round-contract header/status guidance if the expert cannot access the skill files. Give the user a concise list of necessary source/evidence inputs. Do not include local secrets, entire ignored working directories or unsupported claims that a remote branch contains an unpublished SHA.

## Expert reaction to the engineering response

```text
Act as the external reviewer for sprint [ID], round [N], reacting to the engineering response.
Original reviewed revision: [full SHA]. Engineering answer/current revision: [full SHA and explained differences].
Git repository URL and branch/ref: [actual project URL and relevant refs; identify separately supplied changes].
Inputs: [original review, engineering response, relevant evidence and earlier decisions].
Allowed actions: [read-only inspection or explicitly authorized checks].

For each existing finding ID, accept the response, accept with a stated correction, or dispute it with evidence. Distinguish an accepted proposal from a verified implemented fix. State the remaining closing condition and whether the proposed deferral fits the lifecycle objective. Identify factual errors or missing evidence and state what you did not read/run. Keep IDs stable. New findings belong to the next review round; label them as candidates rather than rewriting this round's scope.

Save the complete Markdown to [exact <base>_review-<N>-feedback.md path], retaining the original subject base, with subject/round/revision/reviewer/scope/inputs and finding statuses first. Preserve the original review and engineering response. If file writing is unavailable, return Markdown for the user to save at that path.
```

## Focused clarification

```text
External review clarification for sprint [ID], round [N], message [K].
Finding IDs: [existing IDs]. Revision: [full SHA and any relevant change].
Git repository URL and branch/ref: [actual project URL and relevant ref].
Inputs: [prior expert message, engineering answer and bounded evidence].
Unresolved question: [one concrete uncertainty preventing a decision].
Engineering position: [evidence-backed answer and acknowledged limits].
Please resolve that question or state what evidence is missing. Distinguish proposal agreement from execution proof. Do not widen the review or alter prior files. Allowed actions: [read-only scope or explicitly permitted checks].
Save your reply as [exact <base>_review-<N>-clarification-<K>.md path], retaining the original subject base, or return its Markdown for the user to save.
```
