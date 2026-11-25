# E.7 — Upgrade and release identity walkthrough

Status: completed bounded Elaboration experiment, accepted through delegated YOLO review in [handover](sprint_E.7_handover.md). [Setup](sprint_E.7_setup.md), [design](sprint_E.7_design.md), [implementation](sprint_E.7_implementation.md) and [tests](sprint_E.7_tests.md) own scope, intended behavior, actual mechanisms and evidence. [The manual](user_manual.md) owns prerequisites and recovery. [The 17-slide presentation](sprint_E.7_increment_demo.pptx) accompanies this sequence. Slides 1–4 cover goal/design, 5–10 the upgrade journey, 11–13 failure experiments, and 14–17 evidence/conclusions/Q&A.

## Goal and starting state

Inspect preserved synthetic data through an additive schema upgrade, detect five wrong states despite recorded migration history, inspect a release bundle and read the installed APEX release. Use the prepared apex-cicd Podman host with apex-db/apex-ords running and FREEPDB1 available. Each run creates dedicated E7R_<suffix> and E7C_<suffix> owners and an unused application ID. The retained final target is E7R_55D00B, app 817817. The earlier E7_APP/810703 fixture remains historical evidence. The existing SQLcl 25.4.1.0 / build 25.4.1.022.0618 and Java installation are prerequisite caches, never credential authority. New-host reproduction is unqualified. Python 3, Podman and Git are required; code must be on PATH for viewing.

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

The runner qualifies the cached SQLcl release/build, requires release input files to match HEAD exactly, and generates a fresh isolated schema/workspace and application identity. It binds those deployment mappings, migration/application bytes, exact committed source, contracts and report bytes into a pinned manifest. Baseline verification precedes owner/workspace creation and database migration. The baseline installs 1.0.0 and seeds greeting 7; the verified upgrade installs 1.1.0, checks retained data, metadata and real HTTP output, then repeats the identical upgrade archive. Finally, each selected wrong state must produce its specific assertion error and be restored. Unexpected failures propagate.

The displayed SQL uses logical E7_APP/E7_CONSUMER names. Before packaging, the runner replaces only these fixed fixture names and the fixed app ID with its generated target mappings; the exact executable SQL is retained in each verified ZIP. The trusted operator connection executes SQLPlus inside FREEPDB1; no business credential is stored. This is explicit SQL-bundle qualification, not the production SQLcl PROJECT controller.

The following commands were exercised. The retained passing offline report is already present; the first command refreshes it if desired. It is hashed as evidence bytes, not used as publisher authentication. Each replay creates a new isolated target rather than downgrading an upgraded schema. Retain the previous target and archives until intentionally retired; repeated runs consume laboratory accounts/workspaces.

```bash
python3 tests/test_release_integrity.py > progress/E.7/tests/unit-integrity.log 2>&1
python3 tests/release_lab.py
code progress/E.7/tests/deployment-receipts.json
code progress/E.7/tests/final-state.log
```

Expected result: PASS upgrade, preservation, contracts, five wrong states, repeat and APEX metadata. The final-state log includes E7_STATE_PASS. Receipts list release 1.0.0, 1.1.0 and repeated 1.1.0 with preserved=true and the exact artifact hashes. This satisfies the selected PBI-065/057/077 experiment outcomes; production delivery remains governed by the architecture.

## 4. Inspect the installed page and limitation

Open http://127.0.0.1:8080/ords/f?p=817817:1 in Chrome. The public laboratory page shows Installed release, Application release 1.1.0 | Source b2e8b9b15916783278727188f51601cdc3adb743 | Greeting contract 1.1.0, and footer 1.1.0. This information-only page has no submit operation. Compare the release with deployment-receipts.json and observed-2.log. The application version and component version are independent identities even when their values happen to match.

For the failure evidence, inspect detected-COLUMN.log and final-state.log in VS Code. Migration 1.1.0 remains recorded during injected failures; the state assertion, rather than history alone, rejects the wrong state. Review source_base_commit and bundled source files: for the final receipts this compatibility-named field is the exact selected committed local release revision b2e8b9b15916783278727188f51601cdc3adb743. The clean-input guard checks all release source inputs against it. Earlier receipts/archives without the committed-source guard remain historical. No remote publication or production release tag is claimed. No Product Owner satisfaction or production readiness is inferred from this demonstration.
