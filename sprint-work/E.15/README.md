# E.15 sanitized Oracle candidate experiment

The trusted pull_request_target workflow selects base-owned validation code and
retrieves only candidate.sql from the immutable event head. Oracle executes the
SQL as a disposable application user. No retained laboratory credentials or
production application source are included.

PR 4 completed real Oracle Testing, byte-bound Review, separate code-owner
approval and ordinary protected merge at 8ee003ad9f45ae62d5fe0d1a0bb389e311c1b27a.
Native protection is enabled, including administrator enforcement, strict
Integrated checking, code-owner approval and stale-review dismissal.

The integrated isolation criterion remains unresolved. A candidate-owned
workflow requesting write permissions cancelled another run in this repository.
Code-owner approval protects merge authority but does not prevent that API
interference. The positive merge is not full E.15 acceptance. A proposed
separate candidate authority boundary still requires authorization and real
validation. Do not merge the negative fixtures or declare the sprint complete.

The APEX_CICD progress repository owns the requirement checklist, exact logs,
regression results, operating walkthrough and lifecycle state. This README is
an orientation, not a replacement for that evidence.
