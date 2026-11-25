# E.11 implementation

[Design](sprint_E.11_design.md) owns the bounded choices. [Driver](../../scripts/reproducible_delivery.py) implements fresh Git clone, dynamic loading of the clean E.10 controller, Alpine checksum/version validation, per-run private input, measured download/cache reuse, uniquely labelled image import and scoped cleanup. [Walkthrough](sprint_E.11_increment_demo.md) supplies user documentation, prerequisites, exact commands, options and error recovery. Retain this as an Elaboration experiment, not production tool setup.

The first diagnostic probe checked clean-source identity without invoking it; its receipt/log remain in tests/initial_probe.* and are excluded from final acceptance. The next run used the clean controller but only archived its file; tests/controller_run.* preserve that intermediate result. Final implementation makes a full local Git clone, verifies cleanliness and executes the clean controller. Unique imported image labels prevent removal of another run's image with identical rootfs bytes. The prepared host and VM remain declared dependencies; this is not evidence of fresh private service access by a second operator.

No SQLcl PROJECT operation was run, no version pin changed and no production native toolchain qualification is claimed. No remote repository/ref/status was written. Preserve all unrelated broker session modifications.
