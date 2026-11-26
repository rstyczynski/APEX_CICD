const {spawnSync}=require('node:child_process');const fs=require('node:fs');
const runtime=process.env.INPUT_RUNTIME;
fs.mkdirSync('.dbtools',{recursive:true});fs.copyFileSync('fixtures/config','.dbtools/project.config.json');
const commands=runtime==='javascript'?['tool','output','provenance','candidate','review'].map(kind=>[process.execPath,['actions/checks.cjs',kind]]):[
 ['python3',['baseline/check_tool.py','fixtures/tool']],['python3',['baseline/check_output.py','fixtures/output']],['python3',['baseline/provenance.py','fixtures/archive','fixtures/receipt','a'.repeat(40),'25.4.1.022.0618']]];
if(runtime==='python')commands.push(['python3',['baseline/candidate.py','fixtures/event']],['python3',['baseline/review.py','fixtures/changed','fixtures/report','fixtures/sql']]);
const env={...process.env,INPUT_CONFIG:'fixtures/config',INPUT_ARCHIVE:'fixtures/archive',INPUT_RECEIPT:'fixtures/receipt',INPUT_SOURCE:'a'.repeat(40),INPUT_BUILD:'25.4.1.022.0618',INPUT_EVENT:'fixtures/event',INPUT_CHANGED:'fixtures/changed',INPUT_REPORT:'fixtures/report',INPUT_SQL:'fixtures/sql'};
const version=spawnSync(runtime==='javascript'?process.execPath:'python3',['--version'],{encoding:'utf8'}).stdout.trim();
const samples=[];
for(let i=0;i<11;i++){
 const start=process.hrtime.bigint();
 for(let j=0;j<commands.length;j++){
  const [cmd,args]=commands[j];const e={...env,INPUT_LOG:j===1?'fixtures/output':'fixtures/tool'};
  delete e.GITHUB_OUTPUT;
  const p=spawnSync(cmd,args,{env:e,encoding:'utf8'});if(p.status!==0)throw Error(p.stderr||p.stdout);
 }
 samples.push({phase:i===0?'cold-first-process':'warm-repeat',milliseconds:Number(process.hrtime.bigint()-start)/1e6});
}
fs.mkdirSync('measurement/'+runtime,{recursive:true});fs.writeFileSync('measurement/'+runtime+'/result.json',JSON.stringify({runtime,version,runner_image:process.env.ImageOS,image_version:process.env.ImageVersion,source:process.env.GITHUB_SHA,run:process.env.GITHUB_RUN_ID,samples,setup:'runner preinstalled Python; action-provided Node24; no runtime installation',workload:'five independent helper processes over identical tool/output/archive bytes; valid shared domain only',limits:'cold is first invocation in a fresh job, not guaranteed cold physical host; warm is repeated process execution with filesystem caches'},null,2));
