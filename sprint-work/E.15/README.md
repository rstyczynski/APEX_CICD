# E.15 sanitized candidate experiment

This repository contains disposable SQL and a trusted Oracle candidate validator.
The pull_request_target workflow loads validator code from the event base and
only candidate.sql from the immutable head. Candidate SQL runs in a disposable
Oracle application schema; it never runs as shell or Python on the runner.
No retained credentials or production source are included.

This is work in progress. Passing this workflow alone does not enforce merge,
prove review freshness, or establish all E.15 acceptance requirements.
The private repository currently lacks protected branches on this account.
