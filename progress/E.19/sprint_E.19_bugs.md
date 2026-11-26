# E.19 observed failures and repairs

## BUG-19.1 — candidate metadata permission

Actual candidate dispatch 45875288879 failed in Bind companion candidate as data with `Resource not accessible by integration (HTTP 403)`. The workflow had contents:read but lacked pull-requests:read. No candidate action or Oracle candidate SQL ran after that failure. Add only pull-requests:read at workflow scope; status publication remains denied in the validation job. Retry 45875727042 is pending. [Exact redacted error](tests/candidate-first-failure.log) preserves the failure.

## Measurement correction — unequal image rollout

Run 45875048579 passed checks but Python replicas spanned two image revisions while JavaScript used one. It is excluded from the accepted comparison. Run 45875517420 executes both runtimes on each host, with reversed order on the second host. See [comparison](comparison_report.md). No unsupported speedup or Python installation cost is claimed.

## Browser recovery and archive privacy

The browser host is unavailable. Native Chrome window binding later failed; native Safari rendered the gallery and next/previous anchors worked. Some native UI commands reported user-changed surface state; no action result is inferred from those messages. Unrelated initial browser content and personal tab metadata are explicitly redacted in subsequent versioned chat exports. No unrelated screenshot is used as sprint evidence.
