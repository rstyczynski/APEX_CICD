#!/usr/bin/env bash
# Construct this checkpoint from reviewed source on fresh isolated areas.
source "$(dirname "${BASH_SOURCE[0]}")/cicd-walkthrough-common.sh"
prepare_stage '## C. Deliver World and complete the assembly' deploy/operator/import.sql scripts/cicd-artifact.py
test -f .local-apex/walkthrough/current/B_hello.done
pause 'Press any key to install C_world from reviewed source; q to quit.'
new_stage_source C_world
archive="$(cat .local-apex/releases/initial-selected.txt)"
python3 scripts/cicd-artifact.py unpack "$archive" "$stage_source/payload"
stage_source="$stage_source/payload"
check_result lab-dev-c "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_C E1_DEV_C
variable acquired_generation number
begin :acquired_generation:=E1_CTRL.e1_ownership.acquire('Foundation,Hello,World','walkthrough-C_world','0f7c500e064e4f262a42fb74f4984eb0e4349c88'); end;
/
column owned_generation new_value owned_generation noprint
select :acquired_generation owned_generation from dual;
begin dbms_output.put_line('WALKTHROUGH_GENERATION='||:acquired_generation); end;
/
cd \"$stage_source\"
lb validate -changelog-file db/changelog.xml
lb update -changelog-file db/changelog.xml
@\"$ROOT/deploy/operator/import.sql\" E1_DEV_C 810003 E1_DEV_C APEX-DELIVERY-LABORATORY-C \"$stage_source/apex/f810001\"
@\"$ROOT/deploy/operator/../checks/complete_assembly.sql\"
begin
 apex_util.set_workspace(user);
 apex_application_admin.set_application_status(810003,apex_application_admin.c_app_restricted_access,
  p_allowed_users_list=>apex_t_varchar2('VERIFIER'),p_message=>'Development verification in progress.');
 update lab_state set state='ready',reason='Fresh development: restricted verification' where state_key='Application';
 commit;
end;
/"
generation="$(sed -n 's/^WALKTHROUGH_GENERATION=//p' "$work/output" | tr -d '\r')"
[[ "$generation" =~ ^[0-9]+$ ]]
verify_runtime lab-dev-c E1_DEV_C 810003
check_result lab-dev-c "declare n number;
begin
 select count(*) into n from greeting_history where actor='VERIFIER' and greeting_text='Hello World';
 if n=0 then raise_application_error(-20803,'Runtime verification snapshot required'); end if;
 apex_util.set_workspace(user);
 apex_application_admin.set_application_status(810003,apex_application_admin.c_app_available);
 update lab_state set state='ready',reason='Fresh development: published after verification' where state_key='Application';
 commit;
end;
/"
check_result lab-dev-c "begin E1_CTRL.e1_ownership.release_task('walkthrough-C_world',$generation); end;
/"
touch .local-apex/walkthrough/current/C_world.done
echo 'DEPLOYED C_world: reviewed source installed in this fresh cycle.'
echo '1. In another terminal: python3 scripts/cicd-password.py LAB_USER'
echo '2. Sign out of VERIFIER. Open http://127.0.0.1:8080/ords/f?p=810003:1 and sign in as LAB_USER.'
echo '3. Create a greeting; refresh Greeting history; check Installed components shows all three at 1.0.0.'
echo '4. Return to this terminal to finish chapter C.'
pause 'View this chapter result at the runtime URL, then press any key to finish; q to quit.'
echo 'PASS result stage C_world.'
