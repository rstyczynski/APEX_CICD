# E.19 screenshot evidence index

## Initial hosted guard inspection

[01-hosted-contract-success.png](01-hosted-contract-success.png): actual Chrome application-window capture of run 45873741697 summary at source 6b6a412 after completion. Observed success and retained run/source identity. PBI-087 real workflow action execution; synthetic fixture boundary. [Execution metadata](../tests/initial-hosted-run.json).

[02-hosted-action-steps.png](02-hosted-action-steps.png): opened actual job detail after summary inspection. Observed valid tool/output/provenance actions, skipped mutation sentinel and successful refusal assertion. Detailed expected rejection was not expanded; [log](../tests/initial-hosted-run.log) owns that text.

[03-action-refusal-framed.png](03-action-refusal-framed.png): framed derivative of capture 02 for legibility in the handover slide. No new execution or interaction is implied. Preserves the three valid actions, expected rejection step, skipped mutation and final assertion. The original full application window is retained.

## Coverage and limits

The initial dispatch itself was not captured. Browser host connector was unavailable. Native Chrome later lost window binding; native Safari rendered the gallery and next/previous anchors worked. Unrelated tabs/content are not screenshot evidence. Native APEX interaction captures below were captured during the actual successful hosted browser stage. [Requirement checklist](../sprint_E.19_checklist.md) and [gallery](index.html) own the navigation/coverage context.

## Actual native application interaction

[04-native-blank-login.png](04-native-blank-login.png): actual 1440×1000 Chromium viewport captured by browser.mjs in successful native run 45874462191 at workflow source 4d9b208, before entering fresh job-private authentication inputs. PBI-087 native workflow regression context. No password or token is present. The browser had already completed actual native install/upgrade/repeat/refusal checks.

[05-native-retained-row.png](05-native-retained-row.png): same actual job, after filling the fresh account, activating Sign In and waiting for the exact retained-row text. Observed authenticated APEX/ORDS page showing Row 1: retained across upgrade. This supports the [functional native receipts](../tests/qualified/native-45874462191/success.json) and [actual browser receipt](../tests/qualified/native-45874462191/authenticated-access.json). It does not replace the native archive/source/tool checks. The application viewport is captured directly, not an entire monitor. Private values are never captured between fill and click.

[06-native-row-framed.png](06-native-row-framed.png): derivative of capture 05, cropping the application header and retained-row result for readable handover display. No new execution is implied. Full original capture 05 preserves the authenticated-user context and viewport.

[07-final-matrix-summary.png](07-final-matrix-summary.png): actual Chrome summary opened during the live handover inspection of final matrix 45876173032 at source 860eb1f. Observed success in 23 seconds. The capture was cropped to the real application-content bounds to remove empty scaling padding; the raw capture is retained in tests/final-matrix-summary-raw.png. This is a later repeat, not a screenshot of the earlier dispatch. [Final matrix metadata](../tests/qualified/45876173032.json) records each action/refusal outcome.
