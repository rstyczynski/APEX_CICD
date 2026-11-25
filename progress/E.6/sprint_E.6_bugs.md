# E.6 — Resolved experiment issues

The first native application import failed CREATE_FLOW with PLS-00306 because the proposed initialization parameter was unsupported. Read-only vendor package inspection identified p_vpd; the corrected import and actual initialization-failure case both passed. This failure occurred before accepting a complete E.6 application; no retained application or data was reset.

A copied helper initially targeted the prior sprint's evidence directory. Before staging, its E.6 logs/archive were relocated and all prior tracked evidence was restored byte-for-byte from Git. Output paths now target E.6, and final audit requires no changes under progress/E.5. The shared backend unit helper supports an explicit evidence directory so current regression cannot rewrite historical sprint evidence. Neither issue creates a new product backlog item or changes acceptance criteria.
