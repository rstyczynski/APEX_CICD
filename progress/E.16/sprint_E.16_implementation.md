# E.16 implementation

[Design](sprint_E.16_design.md) owns the YOLO-approved experiment; [checklist](sprint_E.16_checklist.md) retains mandatory criteria. The dedicated private repository is rstyczynski/APEX_CICD_E.16. The mirrored source is [sprint-work/E.16](../../sprint-work/E.16).

The workflow initializes E.15's pinned real Oracle image with isolated disposable schemas and installs checksum-pinned SQLcl 25.4.1.022.0618. Python drives actual native PROJECT init/export/stage/verify/release/gen-artifact/deploy commands and retains each native output. The guard independently checks source, approved build and archive hash before invoking deployment. Unit tests exercise actual guard logic; they do not establish Oracle results or a separate trust authority. The initial lifecycle run is pending; no installation/upgrade/repeat claim is accepted yet.

The default Podman connection failed, but the existing named apex-cicd connection works. No VM recreation or retained credential change was needed. Full regression can therefore use its existing owned E12 database. Generated historical-directory outputs will be retained under E.16 and historical tracked snapshots restored after the suite, preserving earlier sprint records.

## Verified native outcome

The initial pending statement above is historical. Current hosted run 45802390235 passes the native lifecycle and all four refusal cases at companion bd4b2b5. [Source review](sprint_E.16_source_review.md#verified-current-revision) records the generated commits, actual build, archive digest and target observations. Integration now downloads the real artifact and validates both archive digests, workflow identity, wrong-tool measurement and unchanged target observations. [The walkthrough](sprint_E.16_increment_demo.md) supplies the complete significant SQL, usage, prerequisites, expected output and recovery; [manual](user_manual.md) owns supported tasks. Production source metadata remains unchanged.

The companion's later 9394dbc commit changes presentation tooling only; it does not replace the immutable tested native workflow revision. Presentation source uses Artifact Tool, with installed artifact dependencies and PRESENTATION_UTILS pointing to that tooling's helper module. Final PPTX and validation are retained in this progress repository.
