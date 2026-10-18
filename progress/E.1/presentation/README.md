# E.1 presentation authoring

[The handover](../sprint_E.1_handover.md) and [presentation walkthrough](../sprint_E.1_increment_demo.md) are the user-facing entry points. [build.mjs](build.mjs) creates the canonical PPTX with editable shapes/connectors and a native version table. [model-source.json](model-source.json) freezes labels/geometry and the SHA-256 of the working [draw.io model](../model.drawio) used for this handover. It excludes the historical backup page from the presentation.

## Rebuild

1. Resolve the bundled Node.js/Python/node_modules paths with `load_workspace_dependencies` and locate the installed presentations skill. Set `PRESENTATION_SKILL_DIR`, `PRESENTATION_RUNTIME_PYTHON` and `RUNTIME_NODE_MODULES` to those discovered paths; do not substitute host-specific paths into maintained instructions.
2. Run from the Git root. Copy the builder into the private `.local-apex/handover-build/` directory and link that directory's `node_modules` to the discovered runtime modules. Execute that copy with the discovered Node executable. The builder discovers the Git root itself.
3. For another revision, set `PRESENTATION_FINAL_PATH` to a new private output filename in an existing directory, and `PRESENTATION_RECEIPT_PATH` to a new receipt filename under the private build directory. Finalization refuses to overwrite an existing final file. Inspect every rendered slide and the validation receipt before replacing the canonical [PPTX](../sprint_E.1_increment_demo.pptx).
4. Keep the slide-linked walkthrough, handover and evidence synchronized. Recheck source-model changes before refreshing the frozen figure data. Do not overwrite someone else's working diagram edits.

Build outputs and full runtime receipts remain under `.local-apex/handover-build/`; the portable [delivered validation receipt](../tests/handover_presentation_validation_20261018.json) records the final deck hash. The original draw.io working model is not modified by the builder.
