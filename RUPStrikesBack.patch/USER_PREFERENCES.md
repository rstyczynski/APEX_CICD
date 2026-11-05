# Product Owner preferences

This is the project-local, user-editable preferences file for RUP Strikes
Back. The Product Owner can ask Codex to add or change a preference here.
Each preference states its scope in ordinary language. These preferences
guide presentation of new or revised project artifacts; they do not change
Product Backlog priorities, sprint status, or required process state.

## Markdown presentation — 2026-10-01

For narrative Markdown documents, design reviews, and user-facing reports,
write in paragraphs with clear headings. Do not use Markdown tables for
comparisons, mappings, or acceptance evidence in those documents. A numbered
list is welcome when I ask for enumerated arguments or when order matters.

Keep `PROGRESS_BOARD.md` as the RUP method's required four-column Markdown
table. Do not reformat completed historical sprint evidence solely to apply
this preference.

## Metric terminology — 2026-10-04

Use the full name “Word Error Rate” in explanations, presentations and
project-authored narrative documents. Do not shorten this metric to initials.
Retain machine-readable field names and historical raw test evidence.

## Working style and sprint boundaries — 2026-10-16

Avoid unnecessary bureaucracy. Keep sprint records focused on useful decisions,
deliverables and evidence; do not turn conversation wording into a running
incident account. Communicate directly and keep routine process detail brief.

Work only on the current sprint. Do not edit other sprints' artifacts. Shared
product documents and the current sprint's plan/board entries may be updated
as required for its authorized work.


## Portable operating instructions — 2026-10-17

Use Git repository discovery to position commands at the repository root. Never
hard-code a developer's home directory or host-specific checkout path in
maintained instructions or scripts. Preserve historical raw evidence as recorded;
new executable examples must be portable. Keep cleanup/preparation and walkthrough
chapters/scripts synchronized, with explicit scope and preservation behavior.

## File and directory viewing — 2026-10-20

Use the VS Code `code` command in maintained operating instructions to view
files and directories on macOS and Windows. Prefer `code path/to/file` and
`code path/to/directory` over platform-specific viewer commands such as macOS
`open` or `open -t`. State that the `code` command must be available on PATH.
This viewing preference does not imply that all other shell commands or
runtime prerequisites are portable between operating systems.

## Explain encapsulated scripts before invocation — 2026-11-04

Before each script invocation in operating instructions or a demonstration,
provide an introduction/explanation subsection describing the code it hides.
For SQL files, explain the significant SQL, PL/SQL and native tool commands,
their inputs, connection context, effects, checks and failure behavior. For
other scripts or workflow automation, explain non-obvious techniques and how
they relate to the visible manual operations. Address an experienced engineer;
omit basic Bash, SQL and command-line tutorials. Repeated invocations may refer
to an earlier explanation, but must identify their particular purpose before
execution. Encapsulation must not obscure the operation being demonstrated.
Include the complete SQL source in a fenced SQL block in the document before
its invocation, alongside the explanation; prose, selected command names and
links to a source file alone do not satisfy this requirement. Keep displayed
source synchronized with the executable file. Repeat the small SQL source
when a separate exercise needs it to be understandable in place.

## Presentation agenda and section headers — 2026-11-05

Always include an agenda near the start of a multi-slide presentation, immediately
after the cover when present, and a dedicated section header slide before each
major section. Apply this when creating and editing PPTX decks. Keep agenda
labels, section titles, slide numbers and walkthrough references synchronized.
Reuse existing agenda/divider slides rather than adding duplicates. Follow an
explicit later request for a different structure or fixed slide count.

## Presentation closing slide — 2026-11-05

Always end a multi-slide presentation with a dedicated closing slide such as
“Thank you” or “Q&A”. Apply this to new decks and edits, preserving an existing
closing slide when present. Match the deck style and keep the slide map current.
A later explicit request for a different ending takes precedence.
