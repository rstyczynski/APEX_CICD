# E.6 — Secure contracts and transaction behavior

## Goal and starting state — slides 1–4

Use one greeting component through a native APEX page and backend consumers, distinguish context setup from password authentication, compare compatible/breaking behavior, and observe partial failure and competing transactions. [The 20-slide deck](sprint_E.6_increment_demo.pptx) accompanies this complete sequence. [The manual](user_manual.md) owns prerequisites/recovery; [contracts](../../docs/component-contracts.md) owns version promises; [design](sprint_E.6_design.md), [tests](sprint_E.6_tests.md) and [handover](sprint_E.6_handover.md) own mechanisms, executed evidence and live observations respectively. [SRS](../../docs/srs.md) remains the requirements authority.

This is the prepared apex-cicd Podman host with running apex-db/apex-ords, FREEPDB1, APEX 24.2, E6_APP workspace/app 810603 and isolated E6_TEST. The pinned existing utPLSQL framework is 3.2.3. Native processing must use SQLcl release 25.4.1.0 / build 25.4.1.022.0618 with its qualified Java runtime. The initial synthetic permissions are ALICE/PL and BOB/DE. The recorded page request BROWSER-ALLOW-1 already exists; it must be preserved. Tests create and clean only their generated request keys. Production/new-host qualification is outside this experiment.

Begin in a Terminal within the checkout and keep this shell for the commands below. Git discovery positions it at the root. The code command must be on PATH for viewing files.

```bash
cd "$(git rev-parse --show-toplevel)"
podman --connection apex-cicd ps --format '{{.Names}} {{.Status}}'
code progress/E.6/user_manual.md
```

Expected: both named containers are running. Do not reset retained volumes or schemas. The supported variations are allowed/denied identity-country pairs, argument/session country mismatch, missing context, failed initialization, caller rollback, second-write failure, and commit/rollback outcomes for the first competing writer. The synthetic initializer branch is explicit laboratory behavior, not a production authentication mechanism.

## 1. Authenticate the actual page user — slides 5–6

### What the access helper does

The helper securely prompts for a password of at least 16 characters, selects only workspace E6_APP and updates its existing ALICE account through the native APEX API. It does not grant a developer role or write a password file. Diagnostics redact the supplied password. [Oracle's EDIT_USER API](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/EDIT_USER-Procedure.html) requires identical web/new password arguments. The complete significant SQL template follows; the helper supplies the secure prompt value.

```sql
begin
 apex_util.set_security_group_id(apex_util.find_security_group_id('E6_APP'));
 apex_util.edit_user(
  p_user_id=>apex_util.get_user_id('ALICE'),p_user_name=>'ALICE',
  p_web_password=>'<password from secure prompt>',
  p_new_password=>'<same password from secure prompt>',
  p_change_password_on_first_use=>'N');
 commit;
end;
/
```

```bash
python3 tests/contracts_login.py
```

Open http://127.0.0.1:8080/ords/f?p=810603:1. Sign in as ALICE once with an incorrect password: expect “Invalid Login Credentials.” Respect the native short retry delay. Then sign in with the supplied correct password: expect Secure greetings, signed in as alice. Do not save the password in checkout scratch. This manual password check is distinct from the privileged CREATE_SESSION fixture API.

## 2. Submit an allowed and a denied country — slides 7–8

With Country PL, use a fresh synthetic request key such as E6-REVIEW-001 and Greeting text World, then Submit greeting. Expect “Greeting request saved.” The original recorded run used BROWSER-ALLOW-1. Reusing a committed country/key must report the duplicate error rather than overwrite it; choose a different fresh key for another successful demonstration.

Set Country DE and a different key such as E6-REVIEW-DENIED-001 and submit. ALICE lacks DE permission: expect “ORA-20402: Country access denied.” Changing a submitted country does not confer permission. The recorded run used BROWSER-DENIED-1 and database assertions confirm zero rows for that denied key. The [browser record](tests/browser-observations.json) and [live database check](tests/page-business-check.log) preserve the actual outcomes. This is PBI-063's manual authentication/page proof, not a simulated session result.

## 3. Inspect contracts and execute existing consumers — slides 9–12

### What the pure component and unit runner do

The pure renderer preserves named arguments, trimmed greeting text and -20410 invalid-input behavior. The optional suffix and separate JSON renderer are additive. The legacy hello call remains deprecated but callable. The schema and complete current component source follow; they define storage/constraints and ordinary behavior. These sources do not depend on a native APEX session.

<details>
<summary>Complete SQL source: examples/secure-backend/sql/schema.sql</summary>

```sql
create table country_permissions (
 user_name varchar2(255) not null,
 country_code varchar2(2) not null check (country_code in ('PL','DE')),
 enabled char(1) default 'Y' not null check (enabled in ('Y','N')),
 primary key (user_name,country_code)
);
create table greeting_requests (
 country_code varchar2(2) not null,
 request_key varchar2(80) not null,
 greeting_text varchar2(200) not null,
 actor varchar2(255) not null,
 primary key (country_code,request_key)
);
create table greeting_audit (
 country_code varchar2(2) not null,
 request_key varchar2(80) not null,
 actor varchar2(255) not null,
 primary key (country_code,request_key),
 foreign key (country_code,request_key) references greeting_requests(country_code,request_key)
);
```

</details>

<details>
<summary>Complete SQL source: examples/secure-backend/sql/greeting_contract.sql</summary>

```sql
create or replace package greeting_contract authid definer as
 function render(p_text varchar2, p_suffix varchar2 default null) return varchar2;
 -- Deprecated in 1.1; callable for all 1.x consumers, removal requires 2.0.
 function hello(p_name varchar2) return varchar2;
 function render_v2(p_text varchar2) return varchar2;
end;
/
create or replace package body greeting_contract as
 function render(p_text varchar2, p_suffix varchar2 default null) return varchar2 is
 begin
  if trim(p_text) is null or length(trim(p_text))>100 then
   raise_application_error(-20410,'Greeting text must contain 1 to 100 characters.');
  end if;
  return 'Hello '||trim(p_text)||p_suffix;
 end;
 function hello(p_name varchar2) return varchar2 is
 begin
  return render(p_text=>p_name);
 end;
 function render_v2(p_text varchar2) return varchar2 is
 begin
  return json_object('message' value render(p_text) returning varchar2);
 end;
end;
/
```

</details>

The unit entry point uses the shared manifest runner and real utPLSQL under E6_TEST. Its three existing consumers are shown completely below. A temporary random database password exists only for the gate's execution and is removed in finally; native OS authentication is used only by the prepared operator boundary to establish/clean that access. Missing, errored, failed or disabled suites do not satisfy this gate.

<details>
<summary>Complete SQL source: tests/sql/contracts/test_contract.sql</summary>

```sql
create or replace package test_contract as
 --%suite(Stable greeting consumers)
 --%suitepath(contracts)

 --%test(Existing named call preserves its result)
 procedure existing_consumer;
 --%test(Deprecated consumer remains callable)
 procedure legacy_consumer;
 --%test(Invalid input preserves its documented error)
 procedure invalid_input;
end;
/
create or replace package body test_contract as
 procedure existing_consumer is
 begin
  ut.expect(e6_app.greeting_contract.render(p_text=>'World')).to_equal('Hello World');
 end;
 procedure legacy_consumer is
 begin
  ut.expect(e6_app.greeting_contract.hello(p_name=>'World')).to_equal('Hello World');
 end;
 procedure invalid_input is
  l_text varchar2(200);l_code number:=0;
 begin
  begin l_text:=e6_app.greeting_contract.render('   ');
  exception when others then l_code:=sqlcode;
  end;
  ut.expect(l_code).to_equal(-20410);
 end;
end;
/
```

</details>

```bash
bash tests/run.sh --unit --new-only progress/E.6/new_tests.manifest
code progress/E.6/tests/unit.log
code docs/component-contracts.md
```

Expected: one registered unit gate passes; three real tests pass with zero failures/errors/disabled tests. Review patch/minor/major examples for APEX item/request contracts, shared LOV codes/defaults, database calls/errors/transactions and retained-data interpretation. The declarations use distinct application, migration and component identities. The build guard checks explicit supported dependency bounds; it does not infer compatibility from code changes.

## 4. Compare compatible versions and detect a break — slides 10–12

### What the compatibility experiment changes

The integration runner temporarily installs three real package variants into isolated E6_APP. It derives the pre-extension 1.0 specification by removing the optional suffix/JSON operation; its known whitespace defect is then fixed in 1.0.1. Existing valid World consumers pass in both; padded text is checked separately for the patch. Version 1.1 restores the complete current source above and adds suffix/JSON behavior while preserving existing named and deprecated calls. A controlled mutant changes the legacy return to BREAKING RESULT, so the real consumers fail. Finally restores the current complete source and reruns the consumers. No mutant is packaged.

The significant return variants are respectively `return 'Hello '||p_text;`, `return 'Hello '||trim(p_text);`, the full 1.1 return above, and `return 'BREAKING RESULT';`. They are derived in the helper, not external SQL files. The helper's entire current specification/body above defines the final contract; no variant changes the stated -20410 invalid-input promise. Inspect the actual package transformations and test output rather than assuming compilation means compatibility.

## 5. Exercise native context and transaction boundaries — slides 13–16

### What the request operation does

The complete package below requires app 810603, a nonanonymous native context, matching P1_COUNTRY and an enabled permission. It treats the country argument as untrusted. The operation savepoint name is reserved by this fixture. A request/audit pair shares the caller transaction; duplicate keys are rejected and exceptions roll back only to the operation savepoint. The caller owns commit/rollback. No public identity-impersonation helper is installed.

<details>
<summary>Complete SQL source: examples/secure-backend/sql/secure_greetings.sql</summary>

```sql
create or replace package secure_greetings authid definer as
 procedure submit_request(p_key varchar2,p_country varchar2,p_text varchar2);
end;
/
create or replace package body secure_greetings as
 procedure submit_request(p_key varchar2,p_country varchar2,p_text varchar2) is
  l_actor varchar2(255):=upper(apex_application.g_user);
  l_country varchar2(2);
  l_message varchar2(200);
  l_count number;
 begin
  savepoint greeting_operation;
  if apex_application.g_flow_id<>810603 or apex_application.g_flow_id is null
     or apex_application.g_instance is null or apex_application.g_instance=0
     or l_actor is null or l_actor in ('NOBODY','ANONYMOUS','APEX_PUBLIC_USER') then
   raise_application_error(-20400,'An authenticated application context is required.');
  end if;
  l_country:=apex_util.get_session_state('P1_COUNTRY');
  if l_country is null or p_country is null or p_country<>l_country then
   raise_application_error(-20401,'Country context mismatch.');
  end if;
  select count(*) into l_count from country_permissions
   where user_name=l_actor and country_code=p_country and enabled='Y';
  if l_count<>1 then raise_application_error(-20402,'Country access denied.'); end if;
  if trim(p_key) is null or length(p_key)>80 then
   raise_application_error(-20404,'A request key of 1 to 80 characters is required.');
  end if;
  l_message:=greeting_contract.render(p_text);
  insert into greeting_requests values(p_country,p_key,l_message,l_actor);
  insert into greeting_audit values(p_country,p_key,l_actor);
 exception
  when dup_val_on_index then
   rollback to greeting_operation;
   raise_application_error(-20403,'Duplicate request rejected.');
  when others then
   rollback to greeting_operation;
   raise;
 end;
end;
/
```

</details>

### What the native-session fixture does

[CREATE_SESSION](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/CREATE_SESSION-Procedure.html) supplies a test identity, establishes environment and runs application initialization; [DELETE_SESSION](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/DELETE_SESSION-Procedure.html) removes it and resets the attached environment. That is privileged test setup, not password authentication. The following complete test source exercises no context, ALICE/PL, BOB/DE, country mismatch, denied country, initialization failure and explicit session cleanup.

<details>
<summary>Complete SQL source: tests/sql/contracts/session_transactions.sql</summary>

```sql
declare
 l_sid number; l_code number; l_count number;
 procedure expect_rejection(p_country varchar2,p_code number) is
 begin
  l_code:=0;
  begin e6_app.secure_greetings.submit_request('SESSION-DENY',p_country,'World');
  exception when others then l_code:=sqlcode; end;
  if l_code<>p_code then raise_application_error(-20480,'Wrong country rejection: '||l_code); end if;
 end;
begin
 expect_rejection('PL',-20400);
 apex_session.create_session(810603,1,'ALICE');l_sid:=apex_application.g_instance;
 apex_util.set_session_state('P1_COUNTRY','PL');
 e6_app.secure_greetings.submit_request('ALLOWED-ROLLBACK','PL','World');
 expect_rejection('DE',-20401);
 apex_util.set_session_state('P1_COUNTRY','DE');
 expect_rejection('DE',-20402);
 rollback;
 apex_session.delete_session(l_sid);l_sid:=null;
 apex_session.create_session(810603,1,'BOB');l_sid:=apex_application.g_instance;
 apex_util.set_session_state('P1_COUNTRY','DE');
 e6_app.secure_greetings.submit_request('BOB-ALLOWED','DE','World');
 rollback;
 apex_session.delete_session(l_sid);l_sid:=null;
 -- This app's actual initialization code throws for this synthetic test identity.
 l_code:=0;
 begin apex_session.create_session(810603,1,'INIT_FAIL');
 exception when others then l_code:=sqlcode; dbms_output.put_line('INIT_FAILURE:'||sqlerrm); end;
 if l_code=0 then raise_application_error(-20481,'Initialization failure swallowed'); end if;
 if apex_application.g_instance is not null and apex_application.g_instance<>0 then
  apex_session.delete_session(apex_application.g_instance);
 end if;
 dbms_output.put_line('E6_SESSION_PASS: allowed ALICE/PL and BOB/DE; mismatch and denied writes rejected; initialization failure propagated; sessions deleted');
exception when others then
 rollback;
 if l_sid is not null then apex_session.delete_session(l_sid); end if;
 raise;
end;
/
```

</details>

### What the partial-failure fixture does

The first SQL file temporarily adds an audit trigger only for the selected FAIL-AUDIT key. The second places an unrelated caller marker, invokes the API, requires the propagated -20499 failure, checks that the marker survives and explicitly rolls back. The Python runner always drops the temporary trigger in finally, compares unrelated business snapshots and compares native session counts. The marker table belongs to E6_TEST and was created during one-time fixture setup; it is not release source.

<details>
<summary>Complete SQL source: tests/sql/contracts/fault_setup.sql</summary>

```sql
create or replace trigger e6_app.e6_test_audit_failure
before insert on e6_app.greeting_audit for each row
begin
 if :new.request_key='FAIL-AUDIT' then
  raise_application_error(-20499,'Selected second-write failure');
 end if;
end;
/
```

</details>

<details>
<summary>Complete SQL source: tests/sql/contracts/partial_failure.sql</summary>

```sql
declare l_sid number;l_code number:=0;l_count number;
begin
 apex_session.create_session(810603,1,'ALICE');l_sid:=apex_application.g_instance;
 apex_util.set_session_state('P1_COUNTRY','PL');
 insert into caller_markers values(1);
 begin e6_app.secure_greetings.submit_request('FAIL-AUDIT','PL','World');
 exception when others then l_code:=sqlcode; end;
 if l_code<>-20499 then raise_application_error(-20482,'Wrong injected error: '||l_code); end if;
 select count(*) into l_count from caller_markers where id=1;
 if l_count<>1 then raise_application_error(-20483,'Caller work was rolled back'); end if;
 rollback;
 apex_session.delete_session(l_sid);
 dbms_output.put_line('E6_PARTIAL_PASS: second-write error propagated, caller marker preserved until explicit rollback');
exception when others then
 rollback;
 if l_sid is not null then apex_session.delete_session(l_sid); end if;
 raise;
end;
/
```

</details>

### What the competing-session fixture controls

Two independent Oracle subprocesses create native sessions. Writer A inserts one generated country/key and signals that it holds the transaction. Writer B submits the same key. Before releasing A, the operator query requires B to be WAITING on `enq: TX - row lock contention` in v$session. With A commit, B must receive -20403; with A rollback, B must succeed and commit. Each case requires exactly one request and one matching audit, then deletes only that run's generated keys. Client deadlines terminate unexpected waits. This does not prove general fairness, all isolation levels, distributed transactions or exactly-once delivery.

The following entry point executes all three integration groups: compatibility, sessions/partial failure/competing requests, and archive/page assertions. It does not redo your password entry; it checks the separately recorded browser observations against live database state.

```bash
bash tests/run.sh --integration --new-only progress/E.6/new_tests.manifest
code progress/E.6/tests/compatible-patch-fix.log
code progress/E.6/tests/incompatible-detected.log
code progress/E.6/tests/compat-restored-consumers.log
code progress/E.6/tests/sessions.log
code progress/E.6/tests/partial-failure.log
code progress/E.6/tests/transaction-results.json
```

Expected: all three integration groups pass. The deliberate incompatible run contains failed assertions; the restored run contains three passing consumers. Session output includes the propagated setup error. Transaction receipts show an observed wait and one request/audit in both selected interleavings. Test-owned requests and native sessions are cleaned up; your prior committed browser request remains.

## 6. Inspect the whole-application native archive — slides 17–18

The retained native release uses only E6_APP, includes the application and both component packages, and excludes E6_TEST/suites and the temporary fault trigger. The builder validates explicit dependency declarations before native processing. [The receipt](tests/native-release.json) binds the selected Git source commit, qualified SQLcl build, declaration hash/version map and archive hash. The complete application source is in examples/secure-backend/apex/f810603.sql. Packaging remains whole-application; no selective component deployment or populated upgrade is claimed.

The standard-library ZIP command below lists the actual archive without extracting or deploying it. The code commands open the declarations and exact native output.

```bash
python3 -m zipfile -l progress/E.6/tests/e6-backend-1.0.0.zip
code examples/secure-backend/contracts.json
code progress/E.6/tests/native-release.json
code progress/E.6/tests/native-stage-verify.log
```

Expected: 20 native entries including the application and secure_greetings, with no test schema/suite or fault-trigger objects. An initial unsupported initialization parameter failed native import; read-only vendor signature inspection identified p_vpd and the corrected import passed. The laboratory INIT_FAIL branch remains explicit prototype behavior, not a production initialization recommendation.

## 7. Run the selected regression and review the boundary — slides 19–20

### What the scoped regression runs

The secure_backend regression manifest retains all current pipeline/platform smoke checks plus the backend/contract smoke checks. Its unit slice runs the prior five-test backend suite and the three-test contract suite. A fresh output directory redirects prior backend regression receipts into E.6, preserving completed E.5 artifacts. The inactive E.1 controller/fixture tests are explicitly outside the activation's approved experiment scope. The helper supports only serial gate execution; it is not a general concurrent test orchestrator.

```bash
APEX_TEST_EVIDENCE_DIR="$PWD/progress/E.6/tests/regression-backend" bash tests/run.sh --smoke --component secure_backend
APEX_TEST_EVIDENCE_DIR="$PWD/progress/E.6/tests/regression-backend" bash tests/run.sh --unit --component secure_backend
code progress/E.6/sprint_E.6_handover.md
```

Expected: five smoke checks and two unit groups pass (five prior backend tests plus three contract tests). Review the four PBI outcomes and prototype limitations in handover. No later sprint is activated. Schema owners/admins remain trusted; country permissions, initializer fault identity and test data are synthetic. Production hardening, fresh-host reproduction and broader concurrency/data-evolution evidence remain later programme work.
