// Run from checkout root after four measured cells have passed the evidence reader.
import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const skill=process.env.PRESENTATION_SKILL;
const {makeNativeBulletParagraphs,finalizePresentation,applyPresentationChartFont}=await import(`${skill}/container_tools/artifact_tool_utils.mjs`);
const data=JSON.parse(await fs.readFile('progress/E.18/tests/measurements/capacity-results.json','utf8'));
const report=await fs.readFile('progress/E.18/capacity_report.md','utf8');
const board=await fs.readFile('PROGRESS_BOARD.md','utf8');const pbiStatus=board.split('\n').find(l=>l.startsWith('| Sprint E.18 |')).split('|')[4].trim();
const coldCommand=[
  "gh workflow run native.yml \\",
  "  -R rstyczynski/APEX_CICD_E.18 --ref capacity-v1 \\",
  "  -f cache=cold -f parallel=1"
].join("\n");
const warmCommands=[
  "gh workflow run native.yml -R rstyczynski/APEX_CICD_E.18 \\",
  "  --ref capacity-v1 -f cache=warm -f parallel=1",
  "",
  "gh workflow run native.yml -R rstyczynski/APEX_CICD_E.18 \\",
  "  --ref capacity-v1 -f cache=warm -f parallel=2"
].join("\n");
const p=Presentation.create({slideSize:{width:1280,height:720}});
const dir='.local-apex/e18-deck';await fs.mkdir(dir+'/output',{recursive:true});const validated=`output/validated-${process.env.DECK_REVISION||'1'}.pptx`;
const specs=[
 ['Complete pipeline feedback','Sprint E.18 · PBI-086\nCold/warm downloads and one/two runner slots'],
 ['Agenda','1. Scope and architecture\n2. Complete workload journey\n3. Feedback and resource measurements\n4. Failures and recovery\n5. Capacity recommendation and limits'],
 ['Scope and architecture','Delivery operators need predictable pipeline feedback.\nEight complete samples compare downloads and runner slots.\nEvery mandatory check and fresh candidate state is retained.'],
 ['Native responsibilities','GitHub Actions: dispatch/source → isolated phases and evidence\nGit: pinned workflow/native project → verifiable release history\nJDK 21 + SQLcl PROJECT 25.4.1: source → verified native artifacts\nOracle + utPLSQL 3.1.14: backend cases → test/preservation results\nAPEX 24.2 + ORDS 25.3: native target row → authenticated page\nArchive cache (optional): verified ZIP files → reused downloads'],
 ['Complete workload journey','Known source → fresh job → useful application result'],
 ['Dispatch cold serial execution','gh workflow run native.yml \\\n  -R rstyczynski/APEX_CICD_E.18 \\\n  -f cache=cold -f parallel=1\n\nTwo replicas: one starts; the second waits for its slot.\nThe unique download-cache key establishes a cold acquisition.'],
 ['Observe matrix admission','Exploratory start at f2be037: first replica active; second queued.\nCapture 01 precedes the installer repair; final measurements use capacity-v1.'],
 ['Native SQLcl PROJECT commands','-- job-private workspace: author source, then target deployment\nproject export -schemas AUTHOR16\nproject stage -branch-name baseline\nproject verify -compared-branch-name baseline -verbose\nproject release -version 1.0.0\nproject gen-artifact -name native16 -version 1.0.0\nproject deploy -file $GITHUB_WORKSPACE/result/native16-1.0.0.zip'],
 ['Inspect safety and application results','Reject wrong artifact, source, tool and substituted archive bytes.\nCompare target state before and after refusals.\nAuthenticate through real ORDS/APEX and read the retained row.\nRemove private connections, generated inputs and owned containers.\nOnly successful complete jobs enter the timing report.'],
 ['Warm and concurrent variations','Populate download caches first; exclude population measurements.\nRun warm trials with verified hits and parallel one, then two.\nFresh databases and every native check remain in both variants.\nConcurrent replicas use separate hosted machines and private state.'],
 ['Feedback and resource measurements','Declared sample counts and limits\nRaw API timestamps and host observations remain in evidence'],
 ['Measured feedback','Native editable chart; source: capacity-results.json'],
 ['Observed resource demand',Object.entries(data.groups).map(([k,v])=>`${k}: peak used memory ${(v.peak_host_used_bytes.p95/2**30).toFixed(1)} GiB; host CPU ${v.host_cpu_busy_percent.median.toFixed(1)}%; minimum free disk ${(Math.min(...data.samples.filter(s=>`${s.cache}-parallel-${s.parallel}`===k).map(s=>s.minimum_disk_free_bytes))/2**30).toFixed(1)} GiB`).join('\n')],
 ['Failures and recovery','Failed observations are excluded from successful distributions'],
 ['Installer directory ownership','Native utPLSQL setup could not create params.sql.tmp.\nIts downstream test and APEX stages were skipped.\nGive the copied vendor source to the native oracle account.\nKeep the actual installer and its failure gate; rerun the workload.\nEvidence: BUG-18.1 and gallery capture 02.'],
 ['Invoker rights during utPLSQL execution','Exploratory SYS execution failed ORA-06598.\nInstalling objects did not prove the tests could execute.\nRun application tests through their own authenticated schema.\nNo grant of SYS inheritance was added.\nActual five-case success is required for every admitted sample.'],
 ['Capacity recommendation and limits','Decision based on the retained measurements'],
 ['Measurement limits','Two successful replicas per cell; nearest-rank p95 is the maximum.\nNo production tail latency or service-level guarantee is established.\nFive-second host sampling can miss short resource peaks.\nIndependent hosted jobs do not measure shared-host contention.\nOnly archive downloads are warm; database provisioning stays fresh.\nOther cohorts overlap in time; account-wide quiet conditions are uncontrolled.'],
 ['Assigned work and next decisions',`PBI-086: ${pbiStatus}; eight qualified samples and a bounded recommendation.\nPBI-087 remains Planned in E.19; this sprint does not activate it.\nRetain all mandatory checks and job isolation when applying caches.\nRe-measure controlled, larger samples before production service-level commitments.\nThe handover records final gates, demonstration and lifecycle decisions.`],
 ['Q&A','Inspect the live Actions phases, report and local gallery.\nSource authority: BACKLOG, PLAN and the E.18 evidence checklist.']
];
specs.splice(specs.findIndex(s=>s[0]==='Inspect safety and application results'),0,['Blank login before private input','Actual live browser starting state before private inputs. The job enters its fresh account, activates Sign In and waits for the retained row. Capture 07; no manual Product Owner login is claimed.']);
specs.splice(7,0,['Actual backend validation','Five real backend cases pass through the application schema. Capture 04 records zero failed, errored, disabled and warning cases before native platform/release processing continues.']);
specs.splice(specs.findIndex(s=>s[0]==='Failures and recovery'),0,['Queue and p95 feedback',Object.entries(data.groups).map(([k,v])=>`${k}: feedback p95 ${(v.feedback_seconds.p95/60).toFixed(1)} min; median total wait ${(v.queue_seconds.median/60).toFixed(1)} min`).join('\n')]);
specs.splice(specs.findIndex(s=>s[0]==='Measurement limits'),0,['Runner and cache decision',`Retain the measured four-logical-CPU hosted shape: 15.3–15.6 GiB reported RAM per job.\nTwo isolated slots: cold batch 22.6 → 13.1 minutes; warm batch 23.7 → 11.1 minutes.\nCache remains optional: acquisition plus cache overhead improves only 2.0–3.5 seconds in this cohort.\nDifferent hardware/JDK builds and n=2 prevent causal cache or production-tail claims.\nShared-host packing and cost were not qualified.`]);
specs.splice(specs.findIndex(s=>s[0]==='Capacity recommendation and limits'),0,['Hostname and execution identity','A supplemental check initially required eight unique hostnames.\nOne hostname repeats in nonoverlapping jobs; that condition was too strict.\nAll eight API runner execution IDs are distinct.\nThe corrected audit checks bound source/run receipts, sixteen namespaces and cleanup.\nPhysical-host identity and provider-layer warmth remain uncontrolled.']);
await fs.writeFile(`${dir}/slide-map.json`,JSON.stringify(specs.map((s,i)=>({slide:i+1,title:s[0]})),null,2));
for(let i=0;i<specs.length;i++){
 const s=p.slides.add();s.background.fill='#102638';
 function text(value,y,h,size,font='Arial',bullets=false){const sh=s.shapes.add({geometry:'textbox',position:{left:60,top:y,width:1160,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});sh.text=bullets?makeNativeBulletParagraphs(value.split('\n'),{marginLeftPoints:18,hangingPoints:9,spaceAfterPoints:12}):value;sh.text.style={fontSize:size,typeface:font,color:'#FFFFFF',autoFit:'none',insets:0};}
 text(specs[i][0],42,95,42);
 const title=specs[i][0];
 const image=({'Observe matrix admission':'01-cold-serial-slide-framed.png','Inspect safety and application results':'08-live-result-framed.png','Blank login before private input':'07-live-login-controls.png','Installer directory ownership':'02-utplsql-failure-framed.png','Actual backend validation':'04-backend-framed.png'})[title];
 if(image){
  const bytes=await fs.readFile(`progress/E.18/screenshots/${image}`);
  s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:specs[i][0],fit:'contain',position:{left:60,top:165,width:1160,height:345}});
  text(title==='Inspect safety and application results'?'Actual live run 45848145737: authenticated APEX reads the retained row after native upgrade/repeat. Timings excluded from measurements. See gallery capture 08 and native receipts.':title==='Installer directory ownership'?'Trial installer failed; downstream stages skipped and no release was produced. Disposable databases were cleaned. Give the copied source to oracle:oinstall and rerun; BUG-18.1/capture 02 preserve the evidence.':specs[i][1],530,125,22);
 }else if(title==='Dispatch cold serial execution'){
  text(coldCommand,180,150,24,'Courier New');
  text('Two replicas: one starts; the second waits for its slot.\nA unique per-run download-cache key establishes a miss.\nOriginal cold runs used main at the same commit now frozen as capacity-v1.',375,220,26);
 }else if(title==='Warm and concurrent variations'){
  text(warmCommands,180,220,24,'Courier New');
  text('Populate caches first when absent; require actual restore hits.\nEvery sample retains fresh databases, native validation and private cleanup.',460,130,26);
 }else if(title==='Measured feedback'){
  const keys=Object.keys(data.groups);
  const chart=s.charts.add('bar',{position:{left:70,top:160,width:1130,height:430},categories:keys.map(k=>k.replace('-parallel-',' / slots ')),series:[{name:'Median execution minutes',values:keys.map(k=>Number((data.groups[k].execution_seconds.median/60).toFixed(2))),fill:'#4CADD8'},{name:'Median feedback minutes',values:keys.map(k=>Number((data.groups[k].feedback_seconds.median/60).toFixed(2))),fill:'#E7B45A'}],hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:'16pt',typeface:'Arial',fill:'#FFFFFF'}},xAxis:{textStyle:{fontSize:'16pt',typeface:'Arial',fill:'#FFFFFF'}},yAxis:{min:0,numberFormatCode:'0',textStyle:{fontSize:'16pt',typeface:'Arial',fill:'#FFFFFF'}},dataLabels:{showValue:false}});
  applyPresentationChartFont(chart,{fontFamily:'Arial'});
  text('n=2 per cell · minutes rounded to 0.01 · feedback includes admission/queue',610,50,22);
 }else{text(specs[i][1],180,title==='Observed resource demand'?330:460,['Dispatch cold serial execution','Native SQLcl PROJECT commands'].includes(title)?24:28,['Dispatch cold serial execution','Native SQLcl PROJECT commands'].includes(title)?'Courier New':'Arial',!['Complete pipeline feedback','Agenda','Scope and architecture','Complete workload journey','Dispatch cold serial execution','Native SQLcl PROJECT commands','Feedback and resource measurements','Failures and recovery','Capacity recommendation and limits','Q&A'].includes(title));}
 text(String(i+1),675,30,18);
 if(title==='Observed resource demand')text('CPU values are medians of two per-job mean busy percentages.\nMemory/disk are observed extremes at five-second sampling.',550,90,22);
 s.speakerNotes.text='Sources: progress/E.18/sprint_E.18_checklist.md; capacity_report.md; sprint_E.18_tests.md; screenshots/index.html. All plotted values derive from tests/measurements/capacity-results.json. '+(specs[i][0]==='Runner and cache decision'?report:'');
 const png=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`${dir}/slide-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
}
await(await PresentationFile.exportPptx(p)).save(`${dir}/candidate.pptx`);
await finalizePresentation({workspaceDir:process.cwd(),candidatePath:`${process.cwd()}/${dir}/candidate.pptx`,finalPath:`${process.cwd()}/${dir}/${validated}`,pythonExecutable:process.env.RUNTIME_PYTHON||'/usr/bin/python3',integrityValidatorPath:`${skill}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${skill}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Arial','Courier New']},materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:`${process.cwd()}/${dir}/validation-${process.env.DECK_REVISION||'1'}.json`});
await fs.copyFile(`${dir}/${validated}`,'progress/E.18/sprint_E.18_increment_demo.pptx');
