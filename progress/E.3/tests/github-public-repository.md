# E.3 public source and repository creation check

2026-11-03: at the Product Owner's request,
[rstyczynski/APEX_CICD_E3](https://github.com/rstyczynski/APEX_CICD_E3)
was changed from private to public. GitHub CLI reported PUBLIC; an unauthenticated
GET to the GitHub repository API returned `private: false`, `visibility: public`.
External contributor workflow approval was set to `all_external_contributors`
and read back successfully. Existing environments, secrets and runner
registration were retained; no deployment was dispatched for this change.

Before/around publication, Gitleaks 8.30.1 (official macOS ARM64 archive checked
against the release checksum) scanned 27 commits in the local application
repository's refs with no findings. All seven available workflow artifacts,
including nested archives, were scanned with no findings. Of 45 workflow runs,
39 logs were available and scanned with no findings; six returned log-not-found
and could not be inspected. Scanner documentation's example secrets triggered
two findings in an initial scratch-directory scan; those files were not from
the application repository or workflow outputs. The final output scan excluded
scanner distribution files. These automated checks are not a guarantee that
every form of sensitive data has been detected.

A new local clone of `examples/git-pipeline/baseline.bundle` had a clean working
tree, tags v1.0.0 through v1.0.4 and a resolvable native baseline commit
`082052a6519ef706067db1d6c5fc18e71402a878`. No history was rewritten. The
[creation procedure](../sprint_E.3_increment_demo.md#create-your-own-application-repository-once)
uses full history and tags rather than a template-generated unrelated history.
It documents importing seed GitHub Release notes, labels, Actions permissions,
environment configuration and repository-specific runner registration.

The runner's fresh-install precondition now checks repository administration
permission rather than requiring private visibility. Bash syntax and ShellCheck
passed. A new GitHub repository and a new Oracle/APEX/ORDS installation were not
created as part of this verification; the recipe retains the existing native
lab prerequisite. Full independent clean-lab provisioning is not claimed.
