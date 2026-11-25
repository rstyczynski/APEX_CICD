# E.11 design

Status: Accepted autonomously in authorized YOLO mode.

## Selected journey and choices

Operator obtains a clean tracked-source checkout, supplies a new synthetic private token in memory, downloads pinned Alpine 3.23.0 ARM64 userspace, validates SHA-256, imports a disposable image, runs a candidate with read-only root/no network/no capabilities/private tmpfs, verifies success and cleanup. The supported slice is the E.10 container execution boundary, not database deployment. Git, Python 3 standard library, curl and a Linux ARM64 Podman service are declared prerequisites. No retained business data or credential files are consumed. Rootfs checksum is pinned from the Alpine release checksum endpoint, not accepted from the candidate.

Three paired cold/warm samples are an experimental choice. Cold means empty per-experiment download cache; it does not mean cold host filesystem or VM storage. Warm reuses identical verified bytes. Record bytes fetched, phase durations, sample counts, median and nearest-rank 95th percentile; n=3 is exploratory. Choose one worker unless fixture isolation and measured savings justify another. Do not infer parallel throughput from serial timings. Invalid version metadata and changed cache must fail before import/execution. Credentials remain outside the reusable tar cache.

### Testing Strategy

Keep PLAN smoke/unit/integration and full smoke/unit regression. Smoke compiles the new driver. Unit verifies checksum/version rejection and percentile calculation. Integration downloads/imports real tools, runs clean-source isolated candidate payloads with newly generated secrets and records measurements; scan retained reports/cache for markers. New tests first run red before implementation.

## Test Specification

SM-1 compiles scripts/reproducible_delivery.py. Prerequisite only.

UT-1 rejects wrong release and corrupt bytes; accepts pinned bytes; verifies nearest-rank statistics. These synthetic fixtures prove validation logic only.

IT-1 runs three real cold/warm pairs, checks exact BusyBox runtime identity, private input round trip, negative payload isolation, cleanup and no token in reusable cache or receipt. A clean Git archive of the declared source revision provides the payload. It establishes automated reproduction on this prepared service, not independent operator or clean-host setup.

## Mandatory requirement-to-evidence checklist

R75.1 BACKLOG PBI-075 Test: cold/warm samples and median/95th percentile phase times, pending IT-1.

R75.2 Same source: wrong-version/corrupt-cache rejection and clean-cache success, pending UT-1/IT-1.

R75.3 Same source: justified worker/cache choice and proposed budgets, pending measured analysis. Additional worker conditional on savings/isolation; not mandatory by itself.

R78.1 BACKLOG PBI-078 Test: clean-checkout journey with declared inputs, or reproduced blocker, bounded remedy and unsupported-path decision. Pending IT-1 and operator record.

RP.1 PLAN E.11: second operator and fresh private inputs with pinned tools; automated fresh inputs will not establish independent operation.

RQ.1 PLAN E.11: A1/A2/A3 and full B1/B2; pending logs.

RH.1 patch P8/P9 and canonical documentor: reconciled audit, local commits, runnable manual, live demonstration, presentation pair and truthful closure. Pending handover. These are mandatory method outcomes, not extra product requirements.


## Verification disposition

R75.1–R75.3: final benchmark receipt and test report establish all selected measurements, real cache reuse/rejection and the single-worker decision. No conditional second-worker experiment is claimed. R78.1: automated clean-source execution passes, but separate operator/access remains pending under RP.1; see the blocker audit. RQ.1: A1/A2/A3 and B1/B2 pass, with exact counts in tests. RH.1: presentation, walkthrough, reconciliation and local increment commit are prepared; live P9 review and closure remain pending. This disposition supersedes the planning-time “pending” labels above without rewriting their original specification.
