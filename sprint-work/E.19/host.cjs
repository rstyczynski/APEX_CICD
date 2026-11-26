'use strict';
// One declared platform operation per invocation. Actions owns their sequence.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {spawnSync}=require('node:child_process');
const {check}=require('./actions/checks.cjs');
const env=process.env,tmp=env.RUNNER_TEMP,priv=path.join(tmp,'e19-private');
fs.mkdirSync('result',{recursive:true});
let secrets=[env.NATIVE_PASSWORD,env.APEX_ADMIN_PASSWORD].filter(Boolean);
function run(args,body,label){
 const p=spawnSync(args[0],args.slice(1),{input:body,encoding:'utf8',timeout:1800000,maxBuffer:32*1024*1024});
 let output=(p.stdout||'')+(p.stderr||'');
 for(const secret of secrets)output=output.split(secret).join('[REDACTED]');
 if(label)fs.writeFileSync(`result/${label}.log`,output);
 if(p.error||p.status!==0)throw Error(`${label||args[0]} failed: ${output.slice(-2000)}`);
 return output;
}
function sql(container,body,label){
 const text=run(['docker','exec','-i',container,'sqlplus','-s','/ as sysdba'],`whenever sqlerror exit failure\nset echo off verify off define off\nalter session set container=FREEPDB1;\n${body}\nexit\n`,label);
 check('output',{log:`result/${label}.log`});return text;
}
async function main(){
 const mode=process.argv[2],a=env.ORACLE_CONTAINER,t=env.TARGET_CONTAINER,pw=env.NATIVE_PASSWORD,admin=env.APEX_ADMIN_PASSWORD;
 if(mode==='inputs'){
  fs.mkdirSync(priv,{mode:0o700});
  const pw='Aa1_'+crypto.randomBytes(20).toString('hex'),admin='Aa1_'+crypto.randomBytes(20).toString('hex');
  secrets.push(pw,admin);for(const v of [pw,admin])console.log('::add-mask::'+v);
  fs.appendFileSync(env.GITHUB_ENV,`NATIVE_PASSWORD=${pw}\nAPEX_ADMIN_PASSWORD=${admin}\n`);
  for(const [c,label] of [[a,'author'],[t,'target']])sql(c,`create user AUTHOR16 identified by "${pw}" quota unlimited on users;\ngrant connect,resource,create view to AUTHOR16;`,label+'-schema');
  fs.writeFileSync('result/host.json',JSON.stringify({run:env.GITHUB_RUN_ID,source:env.GITHUB_SHA,host:run(['hostname']).trim(),fresh_inputs:true,database_containers:[a,t]}));
 }else if(mode==='apex-download'){
  const archive=path.join(tmp,'apex.zip');
  if(!fs.existsSync(archive))run(['curl','--fail','--location','--retry','3','https://download.oracle.com/otn_software/apex/apex_24.2.zip','-o',archive],null,'download-apex');
  if(crypto.createHash('sha256').update(fs.readFileSync(archive)).digest('hex')!=='a7ad0ba94f70b2d581f7dde97fe27cd07afc98c32ecc146d89fd70cce9b76456')throw Error('APEX checksum mismatch');
  run(['unzip','-q',archive,'-d',path.join(tmp,'apex-install')]);
  run(['docker','cp',path.join(tmp,'apex-install/apex'),t+':/tmp/apex'],null,'copy-apex');
  run(['docker','exec','--user','root',t,'chown','-R','oracle:oinstall','/tmp/apex']);
 }else if(mode==='apex-install'){
  run(['docker','exec','-i','--workdir','/tmp/apex',t,'sqlplus','-s','/ as sysdba'],'whenever sqlerror exit failure\nalter session set container=FREEPDB1;\n@apexins.sql SYSAUX SYSAUX TEMP /i/\nexit\n','apex-install');
  check('output',{log:'result/apex-install.log'});
 }else if(mode==='apex-configure'){
  sql(t,`alter user APEX_PUBLIC_USER account unlock;\nbegin apex_instance_admin.add_workspace(p_workspace=>'E17',p_primary_schema=>'AUTHOR16'); apex_util.set_security_group_id(apex_util.find_security_group_id('E17')); apex_util.create_user(p_user_name=>'LAB_USER',p_email_address=>'e19@example.invalid',p_web_password=>'${admin}',p_change_password_on_first_use=>'N'); commit; end;\n/`,'apex-configure');
 }else if(mode==='application-import'){
  sql(t,"begin apex_application_install.set_workspace('E17'); apex_application_install.set_schema('AUTHOR16'); apex_application_install.set_application_id(810503); apex_application_install.generate_offset; end;\n/\n"+fs.readFileSync('application.sql','utf8'),'application-import');
 }else if(mode==='ords-install'){
  run(['docker','pull',env.ORDS_IMAGE],null,'ords-pull');run(['docker','exec',t,'resetPassword',admin],null,'ords-admin-input');
  run(['docker','run','--user',`${process.getuid()}:${process.getgid()}`,'--env','HOME=/tmp','--rm','--network','host','-i','-v',priv+':/etc/ords/config',env.ORDS_IMAGE,'install','--admin-user','SYS','--proxy-user','--db-hostname','127.0.0.1','--db-port','1522','--db-servicename','FREEPDB1','--gateway-mode','proxied','--gateway-user','APEX_PUBLIC_USER','--password-stdin'],admin+'\n'+pw+'\n','ords-install');
 }else if(mode==='ords-start'){
  run(['docker','run','--user',`${process.getuid()}:${process.getgid()}`,'--env','HOME=/tmp','-d','--name','e17-ords','--network','host','-v',priv+':/etc/ords/config','-v',path.join(tmp,'apex-install/apex/images')+':/opt/oracle/apex/images:ro',env.ORDS_IMAGE,'serve','--port','8080','--apex-images','/opt/oracle/apex/images'],null,'ords-start');
 }else if(mode==='verify'){
  const url='http://127.0.0.1:8080/ords/f?p=810503:LOGIN';
  for(let i=0;i<90;i++){
   try{const r=await fetch(url,{signal:AbortSignal.timeout(10000)}),body=await r.text();if(r.status===200&&/password/i.test(body)&&body.includes('APEX Delivery Laboratory')){fs.writeFileSync('result/application-access.json',JSON.stringify({url,status:r.status,login:true}));console.log('PASS actual APEX login');return;}}catch{}
   await new Promise(r=>setTimeout(r,4000));
  }throw Error('application unavailable');
 }else throw Error('unknown platform operation');
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
