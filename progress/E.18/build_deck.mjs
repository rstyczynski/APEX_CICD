// Run from checkout root after four measured cells have passed the evidence reader.
import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const skill=process.env.PRESENTATION_SKILL;
const {makeNativeBulletParagraphs,finalizePresentation,applyPresentationChartFont}=await import(`${skill}/container_tools/artifact_tool_utils.mjs`);
const data=JSON.parse(await fs.readFile('progress/E.18/tests/measurements/capacity-results.json','utf8'));
const report=await fs.readFile('progress/E.18/capacity_report.md','utf8');
const p=Presentation.create({slideSize:{width:1280,height:720}});
const dir='.local-apex/e18-deck';await fs.mkdir(dir,{recursive:true});
const specs=[
 ['Complete pipeline feedback','Sprint E.18 · PBI-086\nCold/warm downloads and one/two runner slots'],
 ['Agenda','1. Scope and architecture\n2. Complete workload journey\n3. Feedback and resource measurements\n4. Failures, limits and runner recommendation'],
 ['Scope and architecture','A reproducible measurement experiment\nNo mandatory validation removed'],
 ['Native responsibilities','GitHub Actions: matrix admission, setup, cache and visible phases\nOracle Database: fresh author and independent delivery target\nutPLSQL: five existing backend behavior cases\nSQLcl PROJECT: export, stage, verify, release, package and deploy\nAPEX and ORDS: authenticated access to preserved native rows'],
 ['Complete workload journey','Known source → fresh job → useful application result'],
 ['Dispatch cold serial execution','gh workflow run native.yml \\\n  -R rstyczynski/APEX_CICD_E.18 \\\n  -f cache=cold -f parallel=1\n\nTwo replicas: one starts; the second waits for its slot.\nThe unique download-cache key establishes a cold acquisition.'],
 ['Observe matrix admission','Actual starting state: first replica active; second queued.\nEvidence: gallery capture 01; workflow timestamps supply timings.'],
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
 ['Measurement limits','Two successful replicas per cell; nearest-rank p95 is the maximum.\nNo production tail latency or service-level guarantee is established.\nFive-second host sampling can miss short resource peaks.\nIndependent hosted jobs do not measure shared-host contention.\nOnly archive downloads are warm; database provisioning stays fresh.'],
 ['Assigned work and next decisions','PBI-086: assess against every linked acceptance observation.\nFull smoke, unit and integration regression must pass before closure.\nKeep mandatory checks and candidate isolation when applying caches.\nRe-measure with larger samples before production capacity commitments.\nSee handover for final lifecycle and demonstration decisions.'],
 ['Q&A','Inspect the live Actions phases, report and local gallery.\nSource authority: BACKLOG, PLAN and the E.18 evidence checklist.']
];
for(let i=0;i<specs.length;i++){
 const s=p.slides.add();s.background.fill='#102638';
 function text(value,y,h,size,font='Arial',bullets=false){const sh=s.shapes.add({geometry:'textbox',position:{left:60,top:y,width:1160,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});sh.text=bullets?makeNativeBulletParagraphs(value.split('\n'),{marginLeftPoints:18,hangingPoints:9,spaceAfterPoints:12}):value;sh.text.style={fontSize:size,typeface:font,color:'#FFFFFF',autoFit:'none',insets:0};}
 text(specs[i][0],42,95,42);
 const image=i===6?'01-cold-serial-start-framed.png':i===8?'05-population-authenticated-framed.png':i===14?'02-utplsql-failure-framed.png':null;
 if(image){
  const bytes=await fs.readFile(`progress/E.18/screenshots/${image}`);
  s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:specs[i][0],fit:'contain',position:{left:60,top:165,width:1160,height:345}});
  text(i===8?'Actual cache-population run 45846157988: authenticated APEX reads the retained row after native upgrade/repeat. Timings excluded from warm samples. See gallery capture 05 and native receipts.':i===14?'Installer failed before downstream execution. Fix directory ownership, then rerun. Capture 02 and BUG-18.1 preserve the error and repair.':specs[i][1],530,125,22);
 }else if(i===11){
  const keys=Object.keys(data.groups);
  const chart=s.charts.add('bar',{position:{left:70,top:160,width:1130,height:430},categories:keys.map(k=>k.replace('-parallel-',' / slots ')),series:[{name:'Median execution minutes',values:keys.map(k=>data.groups[k].execution_seconds.median/60),fill:'#4CADD8'},{name:'Median feedback minutes',values:keys.map(k=>data.groups[k].feedback_seconds.median/60),fill:'#E7B45A'}],hasLegend:true,xAxis:{textStyle:{fontSize:'16pt',fontFamily:'Arial'}},yAxis:{textStyle:{fontSize:'16pt',fontFamily:'Arial'}},dataLabels:{showValue:false}});
  applyPresentationChartFont(chart,{fontFamily:'Arial'});
  text('n=2 per cell · feedback includes admission/queue · full phase timings in report',610,50,22);
 }else{text(specs[i][1],180,460,[5,7].includes(i)?24:28,[5,7].includes(i)?'Courier New':'Arial',![0,1,2,4,5,7,10,13,16,19].includes(i));}
 text(String(i+1),675,30,18);
 s.speakerNotes.text='Sources: progress/E.18/sprint_E.18_checklist.md; capacity_report.md; sprint_E.18_tests.md; screenshots/index.html. All plotted values derive from tests/measurements/capacity-results.json. '+(i===16?report:'');
 const png=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`${dir}/slide-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
}
await(await PresentationFile.exportPptx(p)).save(`${dir}/candidate.pptx`);
await finalizePresentation({workspaceDir:process.cwd(),candidatePath:`${process.cwd()}/${dir}/candidate.pptx`,finalPath:`${process.cwd()}/${dir}/validated.pptx`,pythonExecutable:process.env.RUNTIME_PYTHON||'/usr/bin/python3',integrityValidatorPath:`${skill}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${skill}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Arial','Courier New']},materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:`${process.cwd()}/${dir}/validation.json`});
await fs.copyFile(`${dir}/validated.pptx`,'progress/E.18/sprint_E.18_increment_demo.pptx');
