# E.2 — Git repository layout for the handover

This abbreviated tree shows actual tracked paths in the retained exercise
repository, initialized with SQLcl PROJECT 25.3. It retains application source
and Git history, separately from the delivery repository containing this document.
The laboratory runtime resources are disposable; this retained repository is
part of the exercise evidence and is not designated for deletion.
Its local location is `.local-apex/e2/e2-20261019-01/repo`.

```text
repo/
├── .dbtools/
│   ├── project.config.json
│   ├── project.sqlformat.xml
│   └── filters/project.filters
├── .gitignore
├── README.md
├── src/database/e2_0254c95f_a/
│   ├── apex_apps/f821788/
│   │   ├── f821788.sql
│   │   └── readable/application/
│   │       ├── f821788.yaml
│   │       ├── pages/p00001.yaml
│   │       ├── pages/p00002.yaml
│   │       └── shared_components/lovs.yaml
│   ├── package_specs/e2_greeting.sql
│   ├── package_bodies/e2_greeting.sql
│   └── tables/
│       ├── e2_components.sql
│       ├── e2_history.sql
│       └── e2_settings.sql
├── dist/
│   ├── component-contract.json
│   ├── install.sql
│   ├── releases/
│   │   ├── main.changelog.xml
│   │   ├── apex/
│   │   │   ├── apex.changelog.xml
│   │   │   └── f821788/
│   │   │       ├── f821788.sql
│   │   │       └── f821788.xml
│   │   └── next/
│   │       ├── release.changelog.xml
│   │       └── changes/
│   │           ├── codexe2-initial/
│   │           ├── e2-patch/
│   │           └── e2-working-copy/
│   └── utils/
│       ├── prechecks.sql
│       └── recompile.sql
└── artifact/                         # local archives; Git-ignored
```

Repeated files/subdirectories are omitted; `artifact/` exists locally but its
archives are excluded by the observed `.gitignore`.

## Responsibilities and coexistence

| Area | What to inspect during handover |
| --- | --- |
| `.dbtools/` | PROJECT configuration, export choices and bounded capture filters. |
| `src/database/` | Main application SQL, readable YAML and schema definitions. YAML supports review; it is not a second independently maintained source. |
| `dist/releases/` and `dist/install.sql` | Native staged migration/install hierarchy. Separate generated changes from intentional seed/patch SQL under `_custom/`. The separate APEX changelog is an exercise adaptation; not every file is untouched PROJECT output. |
| `dist/component-contract.json` | Exercise-added component/dependency declaration used by retained admission controls. This does not demonstrate a native PROJECT SemVer dependency solver. |
| `artifact/` | Generated candidate archives, separate from committed source/distribution. |
| Working Copies | Native authoring and selected integration into Main, followed by PROJECT capture into this same repository. No separate Working Copy source tree was required in the demonstrated path. |
| E.1 controls | Reused for dependency admission and preservation evidence where appropriate. Their scripts remain in the delivery repository; the whole E.1 layout need not be copied into the application repository. |

## Live inspection sequence

Run from the delivery repository root. These commands only read retained Git
data; they do not capture, stage, merge or deploy anything.

```bash
E2_REPO=.local-apex/e2/e2-20261019-01/repo
git -C "$E2_REPO" ls-files
git -C "$E2_REPO" log --all --oneline --decorate -12
git -C "$E2_REPO" diff --stat e2-before-working-copy d5c3334
git -C "$E2_REPO" diff e2-before-working-copy d49bc94 -- \
  src/database/e2_0254c95f_a/apex_apps/f821788/readable/application/pages/
git -C "$E2_REPO" show d5c3334:dist/component-contract.json
```

Inspect configuration and source first, then Working Copy/Main changes, then
distribution and the declaration. Trace what changed in source versus staged
migrations, and distinguish custom SQL from generated files.

Without the local lab, extract the retained
[evidence archive](tests/e2-20261019-01-evidence.zip) into a new directory and
clone its `scratch-repository.bundle` into another empty directory. Inspect the
same tracked paths and commits there. This restores Git history for inspection;
it does not provision Oracle.

This layout supports the demonstrated coexistence. The recorded native
verification blocker remains; compatibility with every PROJECT version or
alternative Working Copy export strategy has not been established.
