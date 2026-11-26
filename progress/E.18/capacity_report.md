# Complete pipeline feedback and runner capacity

## Scope and evidence

[PBI-086](../../BACKLOG.md#pbi-086-measure-complete-pipeline-feedback-and-runner-capacity) requires the complete JDK, SQLcl, utPLSQL and Oracle workload. The [design](sprint_E.18_design.md) defines this Elaboration experiment. Every admitted sample runs the existing five backend cases and complete E.17 native delivery, refusal, authenticated APEX/ORDS and cleanup checks. [Verification](sprint_E.18_tests.md) records gates; [cohort audit](tests/cohort-isolation.log) checks execution namespaces and cleanup; [raw measurements](tests/measurements/capacity-results.json) contain individual samples and phase times. Failed and exploratory trials are excluded, retained in the [bug record](sprint_E.18_bugs.md).

Two successful replicas per comparison cell yield eight observations. The initial warm population run is excluded. Median is the sample median; p95 uses nearest rank and equals the maximum at n=2. No production tail estimate is implied. All times below are seconds, with API timestamp resolution of one second. Cache warmth covers checksum-verified SQLcl/APEX archive downloads only; Oracle image pulls, fresh databases, native validation and backend execution remain in every job.

## cold-parallel-1

Actual [run 45846143379](https://github.com/rstyczynski/APEX_CICD_E.18/actions/runs/45846143379) at source `aea3a771cac687fa32ac09d24faf6d2d55bd2342`.

Execution: n=2, median 673.5, nearest-rank p95 705.0 seconds.

Workflow-to-completion feedback: n=2, median 999.5, nearest-rank p95 1353.0 seconds.

Total admission and queue: n=2, median 326.0, nearest-rank p95 648.0 seconds.

Observed host used-memory peak range 6.83–7.00 GiB. Minimum observed free root disk 87.85 GiB. Mean host CPU busy across each sample ranges 28.7–32.2%. These include background runner demand.

Observed job overlap: 0.0s (zero establishes serial execution; positive overlap establishes actual concurrent job lifetimes).

Raw scheduling intervals: replica 1: job creation to start 2.0s; workflow creation to job creation 2.0s; 126 resource observations; replica 2: job creation to start 646.0s; workflow creation to job creation 2.0s; 138 resource observations.

Recorded tool/hardware inputs: replica 1: JDK 21.0.13-2, SQLcl 25.4.1.022.0618, processor Intel(R) Xeon(R) 6975P-C, 4 logical CPUs and 15.33 GiB memory; replica 2: JDK 21.0.13-2, SQLcl 25.4.1.022.0618, processor Intel(R) Xeon(R) 6975P-C, 4 logical CPUs and 15.33 GiB memory. utPLSQL source is pinned to 072dfbc1d0ed37f8da9c0ff87823906483ea3887; Oracle and ORDS image digests are retained in the workflow and job logs.

### Phase timings

Each line reports median and observed range across the two replicas. Setup/checkout/post phases are retained where GitHub reports success.

- Set up job: median 2.5s; range 2.0–3.0s.
- Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 4.0s; range 4.0–4.0s.
- Start resource observations: median 0.5s; range 0.0–1.0s.
- Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 0.0s; range 0.0–0.0s.
- Prepare declared clean host disk capacity: median 101.0s; range 81.0–121.0s.
- Qualify native ORDS architecture and private configuration: median 44.5s; range 37.0–52.0s.
- Start isolated Oracle databases: median 69.5s; range 69.0–70.0s.
- Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.5s; range 0.0–1.0s.
- Install qualified SQLcl: median 4.0s; range 3.0–5.0s.
- Supply fresh private inputs and schemas: median 0.5s; range 0.0–1.0s.
- Install pinned utPLSQL: median 7.5s; range 7.0–8.0s.
- Execute actual utPLSQL regression: median 1.0s; range 1.0–1.0s.
- Acquire checksum pinned APEX: median 10.5s; range 10.0–11.0s.
- Install APEX natively: median 227.0s; range 225.0–229.0s.
- Configure APEX workspace: median 0.5s; range 0.0–1.0s.
- Install ORDS natively: median 16.0s; range 16.0–16.0s.
- Start ORDS listener: median 0.0s; range 0.0–0.0s.
- Initialize job-private workspace: median 0.0s; range 0.0–0.0s.
- Save job-private SQLcl connections: median 8.5s; range 8.0–9.0s.
- Create author fixture: median 4.0s; range 4.0–4.0s.
- Initialize native SQLcl project: median 4.0s; range 4.0–4.0s.
- Export source 1.0.0: median 10.5s; range 10.0–11.0s.
- Stage changes 1.0.0: median 9.0s; range 9.0–9.0s.
- Verify changes 1.0.0: median 6.0s; range 6.0–6.0s.
- Prepare release 1.0.0: median 4.0s; range 4.0–4.0s.
- Package release 1.0.0: median 5.0s; range 5.0–5.0s.
- Install verified release 1.0.0: median 7.0s; range 7.0–7.0s.
- Seed retained target data: median 4.0s; range 4.0–4.0s.
- Import application through native APEX API: median 1.5s; range 1.0–2.0s.
- Verify initial application access: median 1.5s; range 1.0–2.0s.
- Apply additive author change: median 4.0s; range 4.0–4.0s.
- Export source 1.1.0: median 8.0s; range 8.0–8.0s.
- Stage changes 1.1.0: median 6.5s; range 6.0–7.0s.
- Verify changes 1.1.0: median 5.5s; range 5.0–6.0s.
- Prepare release 1.1.0: median 4.5s; range 4.0–5.0s.
- Package release 1.1.0: median 4.5s; range 4.0–5.0s.
- Upgrade with verified release 1.1.0: median 7.0s; range 7.0–7.0s.
- Assert retained data after upgrade: median 4.0s; range 4.0–4.0s.
- Repeat identical verified release 1.1.0: median 6.0s; range 6.0–6.0s.
- Assert retained data after repeat: median 4.0s; range 4.0–4.0s.
- Observe target before refusal checks: median 5.0s; range 5.0–5.0s.
- Reject mismatched artifact evidence: median 0.0s; range 0.0–0.0s.
- Reject mismatched source evidence: median 0.0s; range 0.0–0.0s.
- Reject actual incompatible SQLcl build: median 1.0s; range 1.0–1.0s.
- Reject substituted archive bytes: median 0.0s; range 0.0–0.0s.
- Assert refusal cases preserved target: median 4.5s; range 4.0–5.0s.
- Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 3.0s; range 2.0–4.0s.
- Install declared browser test dependencies: median 34.5s; range 28.0–41.0s.
- Verify application after native delivery: median 4.0s; range 4.0–4.0s.
- Clean job-private connection material: median 3.0s; range 3.0–3.0s.
- Finish resource observations: median 0.0s; range 0.0–0.0s.
- Preserve experiment evidence: median 2.0s; range 2.0–2.0s.
- Post Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 0.0s; range 0.0–0.0s.
- Post Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.0s; range 0.0–0.0s.
- Post Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 4.0s; range 4.0–4.0s.
- Post Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 0.0s; range 0.0–0.0s.
- Complete job: median 0.0s; range 0.0–0.0s.

## cold-parallel-2

Actual [run 45846150456](https://github.com/rstyczynski/APEX_CICD_E.18/actions/runs/45846150456) at source `aea3a771cac687fa32ac09d24faf6d2d55bd2342`.

Execution: n=2, median 751.5, nearest-rank p95 782.0 seconds.

Workflow-to-completion feedback: n=2, median 755.5, nearest-rank p95 786.0 seconds.

Total admission and queue: n=2, median 4.0, nearest-rank p95 4.0 seconds.

Observed host used-memory peak range 6.75–6.81 GiB. Minimum observed free root disk 85.12 GiB. Mean host CPU busy across each sample ranges 28.9–39.5%. These include background runner demand.

Observed job overlap: 721.0s (zero establishes serial execution; positive overlap establishes actual concurrent job lifetimes).

Raw scheduling intervals: replica 1: job creation to start 2.0s; workflow creation to job creation 2.0s; 155 resource observations; replica 2: job creation to start 2.0s; workflow creation to job creation 2.0s; 142 resource observations.

Recorded tool/hardware inputs: replica 1: JDK 21.0.13-9, SQLcl 25.4.1.022.0618, processor AMD EPYC 7763 64-Core Processor, 4 logical CPUs and 15.61 GiB memory; replica 2: JDK 21.0.13-9, SQLcl 25.4.1.022.0618, processor Intel(R) Xeon(R) 6975P-C, 4 logical CPUs and 15.33 GiB memory. utPLSQL source is pinned to 072dfbc1d0ed37f8da9c0ff87823906483ea3887; Oracle and ORDS image digests are retained in the workflow and job logs.

### Phase timings

Each line reports median and observed range across the two replicas. Setup/checkout/post phases are retained where GitHub reports success.

- Set up job: median 2.5s; range 1.0–4.0s.
- Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 3.0s; range 1.0–5.0s.
- Start resource observations: median 0.0s; range 0.0–0.0s.
- Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 0.5s; range 0.0–1.0s.
- Prepare declared clean host disk capacity: median 94.0s; range 52.0–136.0s.
- Qualify native ORDS architecture and private configuration: median 33.5s; range 33.0–34.0s.
- Start isolated Oracle databases: median 75.5s; range 68.0–83.0s.
- Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.5s; range 0.0–1.0s.
- Install qualified SQLcl: median 2.0s; range 2.0–2.0s.
- Supply fresh private inputs and schemas: median 1.0s; range 1.0–1.0s.
- Install pinned utPLSQL: median 8.5s; range 7.0–10.0s.
- Execute actual utPLSQL regression: median 1.5s; range 1.0–2.0s.
- Acquire checksum pinned APEX: median 15.0s; range 10.0–20.0s.
- Install APEX natively: median 286.0s; range 233.0–339.0s.
- Configure APEX workspace: median 1.0s; range 1.0–1.0s.
- Install ORDS natively: median 18.5s; range 15.0–22.0s.
- Start ORDS listener: median 0.0s; range 0.0–0.0s.
- Initialize job-private workspace: median 0.5s; range 0.0–1.0s.
- Save job-private SQLcl connections: median 11.0s; range 10.0–12.0s.
- Create author fixture: median 5.0s; range 4.0–6.0s.
- Initialize native SQLcl project: median 4.5s; range 4.0–5.0s.
- Export source 1.0.0: median 13.0s; range 11.0–15.0s.
- Stage changes 1.0.0: median 10.5s; range 10.0–11.0s.
- Verify changes 1.0.0: median 6.5s; range 5.0–8.0s.
- Prepare release 1.0.0: median 5.5s; range 5.0–6.0s.
- Package release 1.0.0: median 5.0s; range 4.0–6.0s.
- Install verified release 1.0.0: median 9.0s; range 7.0–11.0s.
- Seed retained target data: median 4.5s; range 4.0–5.0s.
- Import application through native APEX API: median 2.0s; range 2.0–2.0s.
- Verify initial application access: median 1.5s; range 1.0–2.0s.
- Apply additive author change: median 5.0s; range 4.0–6.0s.
- Export source 1.1.0: median 10.5s; range 9.0–12.0s.
- Stage changes 1.1.0: median 7.5s; range 6.0–9.0s.
- Verify changes 1.1.0: median 6.5s; range 6.0–7.0s.
- Prepare release 1.1.0: median 5.5s; range 4.0–7.0s.
- Package release 1.1.0: median 5.5s; range 5.0–6.0s.
- Upgrade with verified release 1.1.0: median 8.5s; range 7.0–10.0s.
- Assert retained data after upgrade: median 5.5s; range 5.0–6.0s.
- Repeat identical verified release 1.1.0: median 7.5s; range 6.0–9.0s.
- Assert retained data after repeat: median 5.0s; range 4.0–6.0s.
- Observe target before refusal checks: median 5.5s; range 5.0–6.0s.
- Reject mismatched artifact evidence: median 0.0s; range 0.0–0.0s.
- Reject mismatched source evidence: median 0.0s; range 0.0–0.0s.
- Reject actual incompatible SQLcl build: median 1.5s; range 1.0–2.0s.
- Reject substituted archive bytes: median 0.0s; range 0.0–0.0s.
- Assert refusal cases preserved target: median 5.5s; range 5.0–6.0s.
- Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 2.5s; range 1.0–4.0s.
- Install declared browser test dependencies: median 32.5s; range 27.0–38.0s.
- Verify application after native delivery: median 6.5s; range 6.0–7.0s.
- Clean job-private connection material: median 3.0s; range 2.0–4.0s.
- Finish resource observations: median 0.5s; range 0.0–1.0s.
- Preserve experiment evidence: median 0.5s; range 0.0–1.0s.
- Post Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 0.5s; range 0.0–1.0s.
- Post Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.5s; range 0.0–1.0s.
- Post Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 2.0s; range 2.0–2.0s.
- Post Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 0.0s; range 0.0–0.0s.
- Complete job: median 0.0s; range 0.0–0.0s.

## warm-parallel-1

Actual [run 45848134832](https://github.com/rstyczynski/APEX_CICD_E.18/actions/runs/45848134832) at source `aea3a771cac687fa32ac09d24faf6d2d55bd2342`.

Execution: n=2, median 708.5, nearest-rank p95 773.0 seconds.

Workflow-to-completion feedback: n=2, median 1035.5, nearest-rank p95 1423.0 seconds.

Total admission and queue: n=2, median 327.0, nearest-rank p95 650.0 seconds.

Observed host used-memory peak range 6.62–6.79 GiB. Minimum observed free root disk 84.86 GiB. Mean host CPU busy across each sample ranges 30.7–38.8%. These include background runner demand.

Observed job overlap: 0.0s (zero establishes serial execution; positive overlap establishes actual concurrent job lifetimes).

Raw scheduling intervals: replica 1: job creation to start 3.0s; workflow creation to job creation 1.0s; 127 resource observations; replica 2: job creation to start 649.0s; workflow creation to job creation 1.0s; 153 resource observations.

Recorded tool/hardware inputs: replica 1: JDK 21.0.13-2, SQLcl 25.4.1.022.0618, processor Intel(R) Xeon(R) 6975P-C, 4 logical CPUs and 15.33 GiB memory; replica 2: JDK 21.0.13-9, SQLcl 25.4.1.022.0618, processor AMD EPYC 9V74 80-Core Processor, 4 logical CPUs and 15.61 GiB memory. utPLSQL source is pinned to 072dfbc1d0ed37f8da9c0ff87823906483ea3887; Oracle and ORDS image digests are retained in the workflow and job logs.

### Phase timings

Each line reports median and observed range across the two replicas. Setup/checkout/post phases are retained where GitHub reports success.

- Set up job: median 2.5s; range 2.0–3.0s.
- Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 1.5s; range 1.0–2.0s.
- Start resource observations: median 0.5s; range 0.0–1.0s.
- Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 5.0s; range 4.0–6.0s.
- Prepare declared clean host disk capacity: median 64.5s; range 38.0–91.0s.
- Qualify native ORDS architecture and private configuration: median 41.5s; range 34.0–49.0s.
- Start isolated Oracle databases: median 69.5s; range 69.0–70.0s.
- Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.0s; range 0.0–0.0s.
- Install qualified SQLcl: median 2.0s; range 2.0–2.0s.
- Supply fresh private inputs and schemas: median 0.5s; range 0.0–1.0s.
- Install pinned utPLSQL: median 9.5s; range 8.0–11.0s.
- Execute actual utPLSQL regression: median 1.5s; range 1.0–2.0s.
- Acquire checksum pinned APEX: median 9.5s; range 7.0–12.0s.
- Install APEX natively: median 284.0s; range 225.0–343.0s.
- Configure APEX workspace: median 1.0s; range 1.0–1.0s.
- Install ORDS natively: median 18.5s; range 15.0–22.0s.
- Start ORDS listener: median 0.0s; range 0.0–0.0s.
- Initialize job-private workspace: median 0.0s; range 0.0–0.0s.
- Save job-private SQLcl connections: median 11.0s; range 10.0–12.0s.
- Create author fixture: median 4.5s; range 4.0–5.0s.
- Initialize native SQLcl project: median 4.5s; range 4.0–5.0s.
- Export source 1.0.0: median 11.5s; range 9.0–14.0s.
- Stage changes 1.0.0: median 11.0s; range 10.0–12.0s.
- Verify changes 1.0.0: median 6.5s; range 6.0–7.0s.
- Prepare release 1.0.0: median 5.0s; range 4.0–6.0s.
- Package release 1.0.0: median 5.0s; range 4.0–6.0s.
- Install verified release 1.0.0: median 9.5s; range 8.0–11.0s.
- Seed retained target data: median 4.0s; range 3.0–5.0s.
- Import application through native APEX API: median 2.0s; range 2.0–2.0s.
- Verify initial application access: median 2.0s; range 2.0–2.0s.
- Apply additive author change: median 4.0s; range 3.0–5.0s.
- Export source 1.1.0: median 10.5s; range 9.0–12.0s.
- Stage changes 1.1.0: median 7.0s; range 6.0–8.0s.
- Verify changes 1.1.0: median 6.0s; range 5.0–7.0s.
- Prepare release 1.1.0: median 6.0s; range 5.0–7.0s.
- Package release 1.1.0: median 4.5s; range 4.0–5.0s.
- Upgrade with verified release 1.1.0: median 9.0s; range 7.0–11.0s.
- Assert retained data after upgrade: median 5.0s; range 4.0–6.0s.
- Repeat identical verified release 1.1.0: median 6.5s; range 6.0–7.0s.
- Assert retained data after repeat: median 5.0s; range 4.0–6.0s.
- Observe target before refusal checks: median 5.0s; range 4.0–6.0s.
- Reject mismatched artifact evidence: median 0.0s; range 0.0–0.0s.
- Reject mismatched source evidence: median 0.0s; range 0.0–0.0s.
- Reject actual incompatible SQLcl build: median 2.0s; range 2.0–2.0s.
- Reject substituted archive bytes: median 0.0s; range 0.0–0.0s.
- Assert refusal cases preserved target: median 5.0s; range 4.0–6.0s.
- Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 2.5s; range 1.0–4.0s.
- Install declared browser test dependencies: median 27.0s; range 22.0–32.0s.
- Verify application after native delivery: median 5.0s; range 4.0–6.0s.
- Clean job-private connection material: median 3.5s; range 3.0–4.0s.
- Finish resource observations: median 0.0s; range 0.0–0.0s.
- Preserve experiment evidence: median 1.0s; range 1.0–1.0s.
- Post Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 0.5s; range 0.0–1.0s.
- Post Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.5s; range 0.0–1.0s.
- Post Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 0.0s; range 0.0–0.0s.
- Post Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 0.0s; range 0.0–0.0s.
- Complete job: median 0.0s; range 0.0–0.0s.

## warm-parallel-2

Actual [run 45848140354](https://github.com/rstyczynski/APEX_CICD_E.18/actions/runs/45848140354) at source `aea3a771cac687fa32ac09d24faf6d2d55bd2342`.

Execution: n=2, median 654.5, nearest-rank p95 662.0 seconds.

Workflow-to-completion feedback: n=2, median 659.5, nearest-rank p95 667.0 seconds.

Total admission and queue: n=2, median 5.0, nearest-rank p95 5.0 seconds.

Observed host used-memory peak range 6.61–6.74 GiB. Minimum observed free root disk 84.64 GiB. Mean host CPU busy across each sample ranges 30.5–31.5%. These include background runner demand.

Observed job overlap: 647.0s (zero establishes serial execution; positive overlap establishes actual concurrent job lifetimes).

Raw scheduling intervals: replica 1: job creation to start 3.0s; workflow creation to job creation 2.0s; 127 resource observations; replica 2: job creation to start 3.0s; workflow creation to job creation 2.0s; 131 resource observations.

Recorded tool/hardware inputs: replica 1: JDK 21.0.13-2, SQLcl 25.4.1.022.0618, processor Intel(R) Xeon(R) 6975P-C, 4 logical CPUs and 15.33 GiB memory; replica 2: JDK 21.0.13-2, SQLcl 25.4.1.022.0618, processor AMD EPYC 9V45 96-Core Processor, 4 logical CPUs and 15.61 GiB memory. utPLSQL source is pinned to 072dfbc1d0ed37f8da9c0ff87823906483ea3887; Oracle and ORDS image digests are retained in the workflow and job logs.

### Phase timings

Each line reports median and observed range across the two replicas. Setup/checkout/post phases are retained where GitHub reports success.

- Set up job: median 2.0s; range 2.0–2.0s.
- Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 2.5s; range 1.0–4.0s.
- Start resource observations: median 0.5s; range 0.0–1.0s.
- Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 5.5s; range 4.0–7.0s.
- Prepare declared clean host disk capacity: median 76.0s; range 68.0–84.0s.
- Qualify native ORDS architecture and private configuration: median 41.0s; range 38.0–44.0s.
- Start isolated Oracle databases: median 81.5s; range 70.0–93.0s.
- Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.0s; range 0.0–0.0s.
- Install qualified SQLcl: median 2.0s; range 2.0–2.0s.
- Supply fresh private inputs and schemas: median 0.0s; range 0.0–0.0s.
- Install pinned utPLSQL: median 8.5s; range 8.0–9.0s.
- Execute actual utPLSQL regression: median 1.5s; range 1.0–2.0s.
- Acquire checksum pinned APEX: median 8.0s; range 7.0–9.0s.
- Install APEX natively: median 228.5s; range 226.0–231.0s.
- Configure APEX workspace: median 0.5s; range 0.0–1.0s.
- Install ORDS natively: median 16.0s; range 16.0–16.0s.
- Start ORDS listener: median 0.0s; range 0.0–0.0s.
- Initialize job-private workspace: median 0.0s; range 0.0–0.0s.
- Save job-private SQLcl connections: median 9.5s; range 8.0–11.0s.
- Create author fixture: median 3.5s; range 3.0–4.0s.
- Initialize native SQLcl project: median 4.5s; range 4.0–5.0s.
- Export source 1.0.0: median 9.5s; range 9.0–10.0s.
- Stage changes 1.0.0: median 9.0s; range 9.0–9.0s.
- Verify changes 1.0.0: median 6.0s; range 6.0–6.0s.
- Prepare release 1.0.0: median 4.5s; range 4.0–5.0s.
- Package release 1.0.0: median 4.5s; range 4.0–5.0s.
- Install verified release 1.0.0: median 7.5s; range 7.0–8.0s.
- Seed retained target data: median 4.0s; range 4.0–4.0s.
- Import application through native APEX API: median 2.0s; range 2.0–2.0s.
- Verify initial application access: median 1.0s; range 1.0–1.0s.
- Apply additive author change: median 4.0s; range 4.0–4.0s.
- Export source 1.1.0: median 8.5s; range 8.0–9.0s.
- Stage changes 1.1.0: median 6.5s; range 6.0–7.0s.
- Verify changes 1.1.0: median 5.5s; range 5.0–6.0s.
- Prepare release 1.1.0: median 4.5s; range 4.0–5.0s.
- Package release 1.1.0: median 4.0s; range 4.0–4.0s.
- Upgrade with verified release 1.1.0: median 7.5s; range 7.0–8.0s.
- Assert retained data after upgrade: median 4.5s; range 4.0–5.0s.
- Repeat identical verified release 1.1.0: median 6.0s; range 6.0–6.0s.
- Assert retained data after repeat: median 4.5s; range 4.0–5.0s.
- Observe target before refusal checks: median 4.5s; range 4.0–5.0s.
- Reject mismatched artifact evidence: median 0.0s; range 0.0–0.0s.
- Reject mismatched source evidence: median 0.0s; range 0.0–0.0s.
- Reject actual incompatible SQLcl build: median 1.5s; range 1.0–2.0s.
- Reject substituted archive bytes: median 0.0s; range 0.0–0.0s.
- Assert refusal cases preserved target: median 4.5s; range 4.0–5.0s.
- Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 4.5s; range 2.0–7.0s.
- Install declared browser test dependencies: median 28.5s; range 21.0–36.0s.
- Verify application after native delivery: median 3.5s; range 3.0–4.0s.
- Clean job-private connection material: median 5.5s; range 3.0–8.0s.
- Finish resource observations: median 0.0s; range 0.0–0.0s.
- Preserve experiment evidence: median 1.5s; range 1.0–2.0s.
- Post Run actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020: median 0.0s; range 0.0–0.0s.
- Post Run actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3: median 0.0s; range 0.0–0.0s.
- Post Run actions/cache@5a3ec84eff668545956fd18022155c47e93e2684: median 0.5s; range 0.0–1.0s.
- Post Run actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683: median 0.0s; range 0.0–0.0s.
- Complete job: median 0.0s; range 0.0–0.0s.

## Observed comparisons

Cold two-job batch completion: one slot 1353.0s, two slots 786.0s; observed ratio 1.72. This includes admission/queue and uses the slowest completion in each two-job batch.

Warm two-job batch completion: one slot 1423.0s, two slots 667.0s; observed ratio 2.13. This includes admission/queue and uses the slowest completion in each two-job batch.

At parallel 1, combined SQLcl/APEX acquisition phase median is cold 14.5s versus warm 11.5s (difference 3.0s). Cache restore/save overhead is listed separately in phase timings; hardware/network/time variation prevents a causal speedup claim.

Including observed cache restore/save phases, the corresponding medians are cold 18.5s and warm 16.5s (difference 2.0s). These phases include verification/extraction/copying as well as acquisition.

At parallel 2, combined SQLcl/APEX acquisition phase median is cold 17.0s versus warm 10.0s (difference 7.0s). Cache restore/save overhead is listed separately in phase timings; hardware/network/time variation prevents a causal speedup claim.

Including observed cache restore/save phases, the corresponding medians are cold 19.5s and warm 16.0s (difference 3.5s). These phases include verification/extraction/copying as well as acquisition.


## Qualified runner shape

Observed shapes: 4 logical CPUs / 15.33 GiB RAM, 4 logical CPUs / 15.61 GiB RAM. Retain at least the measured per-job allocation for this bounded workload; two slots allocate two independent hosts of that shape.

## Capacity and caching recommendation

Recommend two independent 4-logical-CPU, approximately 16-GB-class hosted runner slots for a two-candidate batch, retaining fresh author/target databases and all validation per job. The observed slowest-completion ratios are 1.72 for cold and 2.13 for warm execution. One slot remains the qualified serialized fallback when longer feedback is acceptable; no cost measurements were made. The observed serial/concurrent feedback and resource values above establish this bounded tradeoff, not a measured shared-host packing limit. Do not place two complete database workloads on one host based on these independent-host results.

Retain the measured hosted runner shape as the qualified starting capacity; inspect each sample's cpu.txt and memory-start.txt for exact processor and memory observations. Keep the explicit disposable-host disk preparation: the original E.17 worker exhausted disk without it. Preserve measured free-disk margin rather than treating remaining free bytes as a safe reduction. Retain the qualified immutable-archive cache as an optional Actions configuration, with checksum revalidation and every native check unchanged. Including cache overhead, observed acquisition-phase median differences are only 2.0 seconds at one slot and 3.5 seconds at two slots. These small, confounded differences do not establish a causal overall-feedback improvement; do not make caching a latency or capacity guarantee. Leave database-state caching outside the qualified configuration because it was not studied and fresh state preserves isolation. Native APEX installation and release work dominate this measured workload.

## Measurement limits

The workload is the bounded laboratory native-release path and five-case backend suite, not a production application load test. Human review/merge lead time and the separate E.17 review lane are not timed here; full regression still checks its existing controls. The actual samples include different Intel/AMD processor models and Temurin installation builds 21.0.13-2 and 21.0.13-9, as recorded above. Hosted hardware, network and image prepopulation vary between jobs. One hostname repeats across two nonoverlapping jobs with distinct API runner IDs; hostnames do not establish physical-host identity, and physical freshness/provider-layer warmth are not controlled. The separate cohort audit records eight distinct runner execution identities and sixteen author/target namespaces. Trials at different times do not isolate cache as the sole cause of elapsed-time differences. Host CPU counters and available memory are sampled every five seconds from after checkout through private cleanup; short peaks, process attribution and later upload/cache-post resource use are unmeasured. The recorded queue intervals use GitHub job/workflow creation and start times. Job creation may precede matrix admission; these fields do not isolate GitHub infrastructure queueing from intentional matrix waiting. JDK setup can use the hosted preinstallation, so cold does not mean every tool binary was absent. Serial admission is part of feedback, not application execution. Larger repeated samples and representative production datasets are needed before service-level or shared-host sizing commitments. Mandatory validation and isolation remain unchanged.

Serial/concurrent describes each workflow matrix admission limit. Distinct cohorts, cache population and live work can overlap in wall-clock time; an account-wide quiet baseline and controlled causal hardware/cache comparison are not established.
