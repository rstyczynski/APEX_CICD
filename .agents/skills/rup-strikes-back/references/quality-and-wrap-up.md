# Codex Adapter: Quality and Wrap-up Roles

Canonical RUP Strikes Back procedures:

- `RUPStrikesBack/rules/generic/test_procedures.md`, Part 2 (test execution)
- `RUPStrikesBack/.claude/commands/agents/agent-documentor.md`

Read and execute them in the manager's Phase 4 then Phase 5 order. When the local wrapper is present and the iteration is non-code-bearing, apply its rules: run the approved review or experiment and record its evidence instead of asserting code-test gates.

When present, the local patch governs remote actions, project-level Transition meaning, and any project-specific traceability or documentation policy.

## Sprint presentation lists and evidence

In PPTX handover decks, format parallel items as editable native bullet paragraphs, rather than unmarked lines of text. Keep numbered lists for agendas, sequences and dependency-ordered roadmaps; do not add bullets alongside numbers. Treat a wrapped continuation as part of its item, with a hanging indent, and inspect the exported slides for marker spacing and wrapping. Leave prose, commands and titles unbulleted.

Use direct descriptive titles and identify tools unambiguously (for example, SQLcl PROJECT). Avoid evaluative filler. Use screenshots whose relevant controls and values are legible at presentation size. A narrow browser side panel is not evidence of desktop usability. When the Product Owner requests desktop screenshots, repeat the needed views at a desktop viewport and verify the captured content fits. Preserve raw historical captures and label later repeats accurately; a later screenshot does not record an earlier action. Keep requested screenshots rather than substituting text summaries without the Product Owner's agreement.

### Repository trees and code listings

Use Courier for directory trees, command listings and code blocks in this project's PPTX decks; keep the deck's existing typography for explanatory prose. Keep listings editable. Show directory hierarchy with aligned tree branches and one entry per line, rather than combining sibling paths with punctuation. An abbreviated tree must distinguish omitted content from literal paths and must reflect the repository actually inspected.

Size the listing frame for its longest line. Do not let paths, filenames or command arguments wrap unintentionally, especially at hyphens. Prefer shortening the displayed scope, moving detail into another slide or separating explanation from the listing before shrinking text below a readable presentation size. Preserve complete filenames and meaningful hierarchy.

Inspect the exported listing slides at presentation size in the intended viewer when available. Check alignment, intact filenames, command line breaks, margins and readability; package/layout checks alone do not establish this. Repair and inspect again after a font change, because monospaced text can be wider than the original font. When inserting slides, update page numbers and the maintained walkthrough's slide map.
