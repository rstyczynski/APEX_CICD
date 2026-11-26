# E.18 complete-workload demonstration

## Goal and real starting state

Measure the complete native delivery workload to choose runner slots and download caching. [PBI-086](../../BACKLOG.md#pbi-086-measure-complete-pipeline-feedback-and-runner-capacity) owns acceptance; the [design](sprint_E.18_design.md) defines measurement choices. The dedicated public repository contains Actions source, no private inputs. Each job starts fresh databases, generates private inputs and removes them on completion. The [gallery](screenshots/index.html) records actual UI states. This walkthrough is a draft while trials remain pending; it is not a completed demonstration.

Prerequisites: authenticated GitHub CLI with repository workflow dispatch/read access; Git and VS Code's `code` command; Python for local reporting. Oracle/JDK/SQLcl dependencies are declared in the workflow, not inherited from this checkout.

## 1. Inspect the real source

Position at the checkout root, then open the declared native workflow and measurement design. Expected: individually named Actions phases and the two-replica matrix. Inspect checksum pins, max-parallel and always-run cleanup. This establishes what each sample executes, not that it passed.

```bash
cd "$(git rev-parse --show-toplevel)"
code sprint-work/E.18/.github/workflows/native.yml
code progress/E.18/sprint_E.18_design.md
```

## 2. Dispatch the measurement cells

The workflow uses Actions matrix admission to select serial or two-slot execution. Each replica still performs native installation, upgrade, repeat deployment, preserved-data checks, evidence/tool refusal and real APEX/ORDS access. The lightweight observer only reads host counters every five seconds. JDK setup, archive acquisition and database provisioning remain visible Actions steps. Cache hits reuse checksum-verified downloads; they do not retain databases or skip validation. Commands below are exact dispatched forms; additional repeats should be retained as new observations rather than merged silently into earlier sample counts.

```bash
gh workflow run native.yml -R rstyczynski/APEX_CICD_E.18 -f cache=cold -f parallel=1
gh workflow run native.yml -R rstyczynski/APEX_CICD_E.18 -f cache=cold -f parallel=2
gh workflow run native.yml -R rstyczynski/APEX_CICD_E.18 -f cache=warm -f parallel=2
```

The first warm dispatch populates caches and is excluded. Wait for successful terminal outcomes before dispatching measured warm trials with parallel one and two. These warm measurement commands remain pending execution. Never relabel a miss as warm.

## 3. Inspect intermediate and final outcomes

In GitHub Actions open the run, select a replica and inspect named phases in order. Serial execution should show one active replica and one waiting. Concurrent execution should overlap two independent hosted jobs. Inspect the utPLSQL report, source/release phases, preserved row after upgrade/repeat, refused substitutions, authenticated application receipt and cleanup. A green summary alone is insufficient. Downloaded artifacts must match source/run identities.

```bash
gh run list -R rstyczynski/APEX_CICD_E.18 --limit 10
code progress/E.18/screenshots/index.html
```

## 4. Compare feedback and resources

The reporting reader obtains authoritative API timestamps and downloads actual artifacts. It rejects failed runs, absent mandatory phases, wrong source/run IDs, missing resource samples and unestablished cache conditions. It reports both execution and workflow-to-completion feedback; queue includes matrix admission and scheduler delay, separately exposed where available. Median and nearest-rank p95 use declared samples. With two replicas p95 equals the maximum and cannot support a production tail estimate. Host CPU/memory includes background runner services; five-second sampling may miss peaks. No shared-host contention or production capacity guarantee is implied. Report generation and final comparison remain pending four qualified cells.

## 5. Failure and recovery

A cache miss in a warm trial invalidates that cell. Populate the cache, inspect successful save and retry as a new run. A failed native step remains a failed attempt and does not enter successful timing distributions. Keep its logs, fix the actual cause and rerun; do not replace native operations with synthetic timing or waive checks. Each failure path still attempts job-private cleanup.

## Native SQL ledger

The following source is extracted from the visible workflow heredocs. It runs in the job-private author/target context shown in the workflow; SQLcl compatibility and provenance checks precede release/deployment. Native utPLSQL installation runs its pinned vendor install script as SYS in FREEPDB1. The platform adapter performs the same individually selected native provisioning operations as E.17; inspect its complete source alongside the workflow before dispatch. Private generated passwords remain in RUNNER_TEMP and masked environment inputs.

### Native SQL block 1

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
@install_headless.sql
exit
```

### Native SQL block 2

```sql
whenever sqlerror exit failure
alter session set container=FREEPDB1;
set serveroutput on
create or replace package ut3.test_capacity as
  --%suite(Capacity fixture)
  --%test(Oracle arithmetic)
  procedure arithmetic;
end;
/
create or replace package body ut3.test_capacity as
  procedure arithmetic is begin ut3.ut.expect(1+1).to_equal(2); end;
end;
/
exec ut3.ut.run('UT3.TEST_CAPACITY');
exit
```

### Native SQL block 3

```sql
connect -save native-author -savepwd AUTHOR16/${NATIVE_PASSWORD}@//127.0.0.1:1521/FREEPDB1
connect -save native-target -savepwd AUTHOR16/${NATIVE_PASSWORD}@//127.0.0.1:1522/FREEPDB1
```

### Native SQL block 4

```sql
create table preserved (id number primary key, message varchar2(80));
```

### Native SQL block 5

```sql
project init -name native16 -schemas AUTHOR16
```

### Native SQL block 6

```sql
project export -schemas AUTHOR16
```

### Native SQL block 7

```sql
project stage -branch-name baseline
```

### Native SQL block 8

```sql
project verify -compared-branch-name baseline -verbose
```

### Native SQL block 9

```sql
project release -version 1.0.0
```

### Native SQL block 10

```sql
project gen-artifact -name native16 -version 1.0.0
```

### Native SQL block 11

```sql
project deploy -file $GITHUB_WORKSPACE/result/native16-1.0.0.zip
```

### Native SQL block 12

```sql
insert into preserved values (1,'retained across upgrade');
commit;
```

### Native SQL block 13

```sql
alter table preserved add (extra varchar2(80));
```

### Native SQL block 14

```sql
project export -schemas AUTHOR16
```

### Native SQL block 15

```sql
project stage -branch-name baseline
```

### Native SQL block 16

```sql
project verify -compared-branch-name baseline -verbose
```

### Native SQL block 17

```sql
project release -version 1.1.0
```

### Native SQL block 18

```sql
project gen-artifact -name native16 -version 1.1.0
```

### Native SQL block 19

```sql
project deploy -file $GITHUB_WORKSPACE/result/native16-1.1.0.zip
```

### Native SQL block 20

```sql
select id,message,extra from preserved;
begin
 declare n number; begin select count(*) into n from preserved where id=1 and message='retained across upgrade'; if n<>1 then raise_application_error(-20016,'lost data');end if;end;
end;
/
```

### Native SQL block 21

```sql
project deploy -file $GITHUB_WORKSPACE/result/native16-1.1.0.zip
```

### Native SQL block 22

```sql
select id,message,extra from preserved;
begin
 declare n number; begin select count(*) into n from preserved where id=1 and message='retained across upgrade'; if n<>1 then raise_application_error(-20016,'lost data');end if;end;
end;
/
```

### Native SQL block 23

```sql
select id,message,extra from preserved;
```

### Native SQL block 24

```sql
select id,message,extra from preserved;
```
