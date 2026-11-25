# E.7 — Upgrade and release identity walkthrough

Status: implemented laboratory rehearsal; full acceptance remains pending as described in [handover](sprint_E.7_handover.md). [Setup](sprint_E.7_setup.md), [design](sprint_E.7_design.md), [implementation](sprint_E.7_implementation.md) and [tests](sprint_E.7_tests.md) own scope, intended behavior, actual mechanisms and evidence. [The manual](user_manual.md) owns prerequisites and recovery. No presentation deck is delivered yet.

## Goal and starting state

Inspect preserved synthetic data through an additive schema upgrade, detect five wrong states despite recorded migration history, inspect a release bundle and read the installed APEX release. Use the prepared apex-cicd Podman host with apex-db/apex-ords running and FREEPDB1 available. E7_APP and E7_CONSUMER are dedicated test owners; app 810703 uses workspace E7_APP. The existing SQLcl 25.4.1.0 / build 25.4.1.022.0618 and Java installation are prerequisite caches, never credential authority. New-host reproduction is unqualified. Python 3, Podman and Git are required; code must be on PATH for viewing.

## 1. Position the shell and inspect inputs

Git discovery positions a Terminal opened inside this checkout at its repository root. VS Code displays the exact migration/assertion sources below.

```bash
cd "$(git rev-parse --show-toplevel)"
code examples/release-validation/sql
```

The baseline creates greetings, reference and migration tables, installs greeting_api and grants its execution to the synthetic consumer. It commits the initial schema data. The upgrade adds LANGUAGE_CODE only if absent, adds its named constraint only if absent, replaces the compatible package body and merges the migration version. The assertion checks dictionary state, reference data, recorded migration and selected rendering behavior, raising STATE:<category> on failure. These statements operate only on E7 objects; the runner uses a trusted SYSDBA connection in FREEPDB1. Their complete source follows.

### baseline.sql

```sql
create table e7_app.greetings(id number primary key, message varchar2(100) not null);
create table e7_app.release_reference(code varchar2(20) primary key, value varchar2(40));
insert into e7_app.release_reference values('LANGUAGE','en');
create table e7_app.migrations(version varchar2(20) primary key);
insert into e7_app.migrations values('1.0.0');
create or replace package e7_app.greeting_api as function render(p_text varchar2) return varchar2; end;
/
create or replace package body e7_app.greeting_api as function render(p_text varchar2) return varchar2 is begin return 'Hello '||trim(p_text); end; end;
/
grant execute on e7_app.greeting_api to e7_consumer;
commit;
```

### upgrade.sql

```sql
declare n number; begin
 select count(*) into n from dba_tab_columns where owner='E7_APP' and table_name='GREETINGS' and column_name='LANGUAGE_CODE';
 if n=0 then execute immediate 'alter table e7_app.greetings add language_code varchar2(2) default ''en'' not null'; end if;
 select count(*) into n from dba_constraints where owner='E7_APP' and constraint_name='E7_LANGUAGE_CK';
 if n=0 then execute immediate 'alter table e7_app.greetings add constraint e7_language_ck check(language_code in (''en'',''pl''))'; end if;
end;
/
create or replace package body e7_app.greeting_api as function render(p_text varchar2) return varchar2 is begin return 'Hello '||trim(p_text); end; end;
/
merge into e7_app.migrations d using(select '1.1.0' version from dual) s on(d.version=s.version) when not matched then insert(version) values(s.version);
commit;
```

### assert_state.sql

```sql
declare n number;
 procedure require_state(ok boolean,label varchar2) is begin if not ok then raise_application_error(-20701,'STATE:'||label); end if; end;
begin
 select count(*) into n from dba_tab_columns where owner='E7_APP' and table_name='GREETINGS' and column_name='LANGUAGE_CODE' and data_type='VARCHAR2' and char_length=2 and nullable='N';
 require_state(n=1,'COLUMN');
 select count(*) into n from dba_constraints where owner='E7_APP' and constraint_name='E7_LANGUAGE_CK' and status='ENABLED' and validated='VALIDATED';
 require_state(n=1,'CONSTRAINT');
 select count(*) into n from dba_tab_privs where owner='E7_APP' and table_name='GREETING_API' and grantee='E7_CONSUMER' and privilege='EXECUTE';
 require_state(n=1,'GRANT');
 select count(*) into n from dba_objects where owner='E7_APP' and status<>'VALID';
 require_state(n=0,'INVALID_OBJECT');
 select count(*) into n from e7_app.release_reference where code='LANGUAGE' and value='en';
 require_state(n=1,'REFERENCE');
 select count(*) into n from e7_app.migrations where version='1.1.0';
 require_state(n=1,'HISTORY');
 require_state(e7_app.greeting_api.render(' World ')='Hello World','CONSUMER');
 dbms_output.put_line('E7_STATE_PASS');
end;
/
```

## 2. Exercise integrity rejection

### Script explanation

The offline unittest suite builds a ZIP with a hashed manifest and separately pinned digest, then changes migration, report and manifest bytes and removes or empties evidence. Each negative case must raise rather than count as valid. These are controlled integrity checks, not Oracle deployments or publisher authentication.

```bash
python3 tests/test_release_integrity.py
```

Expected result: six tests, OK. This exercises PBI-077's integrity boundary, with the gaps recorded in implementation.

## 3. Rehearse the laboratory upgrade and five failures

### Script explanation

The runner qualifies the cached SQLcl version/build, creates the isolated owners/workspace on first use and seeds greeting 7. On repeat it requires the known retained marker and uses a merge to resume. It generates source-bound bundles for baseline/upgrade, verifies them, imports the corresponding APEX source, compares retained data and metadata, checks real HTTP content, repeats the upgrade, then injects COLUMN, CONSTRAINT, GRANT, INVALID_OBJECT and REFERENCE faults. Each must produce the matching STATE error. Each restoration runs in finally; any unexpected error stops the experiment. The first database baseline setup is still outside verification and therefore is explicitly not a completed release deployment guard.

The report input used for packaging must exist. Capture the offline suite output first; the following sequence was exercised on this host. Evidence is regenerated only under E.7. Rehearsal does not reset a populated upgraded database back to the prior database schema; the original initial setup evidence is distinct from later repeat rehearsals.

```bash
python3 tests/test_release_integrity.py > progress/E.7/tests/unit-integrity.log 2>&1
python3 tests/release_lab.py
code progress/E.7/tests/deployment-receipts.json
code progress/E.7/tests/final-state.log
```

Expected result: PASS upgrade, preservation, contracts, five wrong states, repeat and APEX metadata. The final-state log includes E7_STATE_PASS. Receipts list release 1.0.0, 1.1.0 and repeated 1.1.0 with preserved=true and the exact artifact hashes. This covers selected PBI-065/057 outcomes; it does not close the remaining provenance and deployment gaps.

## 4. Inspect the installed page and limitation

Open http://127.0.0.1:8080/ords/f?p=810703:1 in Chrome. The public laboratory page shows Installed release, Application release 1.1.0 | Greeting contract 1.1.0, and footer 1.1.0. This information-only page has no submit operation. Compare the release with deployment-receipts.json and observed-2.log. The application version and component version are independent identities even when their values happen to match.

For the failure evidence, inspect detected-COLUMN.log and final-state.log in VS Code. Migration 1.1.0 remains recorded during injected failures; the state assertion, rather than history alone, rejects the wrong state. Review source_base_commit and bundled source files: this is currently a Git base plus exact working bytes, not an accepted release tag. No Product Owner satisfaction or production readiness is inferred from this demonstration.
