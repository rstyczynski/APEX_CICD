# Local RUP Strikes Back Patch

The full project patch is maintained at [RUPStrikesBack.patch/RUP_patch.md](RUPStrikesBack.patch/RUP_patch.md).

Read that file after this compatibility entry point. It contains the project-specific RUP Strikes Back policies and bootstrap refinements.

RUP Strikes Back adopts Rational Unified Process analysis discipline. The full policy's [P1.3](RUPStrikesBack.patch/RUP_patch.md#p13-adopt-rup-analysis-and-use-case-modeling-explicitly) requires an explicit Actors chapter and actor-led end-to-end use cases, with detail proportionate to the lifecycle phase.

The [rup-external-review skill](.agents/skills/rup-external-review/SKILL.md) coordinates external review through files: Codex prepares prompts for the Product Owner to relay, answers returned expert messages and tracks evidence-based decisions. The skill owns the complete procedure formerly maintained as P10.
