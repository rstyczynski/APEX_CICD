import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const skill=process.env.PRESENTATION_SKILL;
const {makeNativeBulletParagraphs,finalizePresentation}=await import(`${skill}/container_tools/artifact_tool_utils.mjs`);
const p=Presentation.create({slideSize:{width:1280,height:720}}),dir='.local-apex/e19-deck';
const specs=[
 ['JavaScript support actions','Sprint E.19 · PBI-087\nReusable guards with explicit refusal behavior'],
 ['Agenda','1. Scope and responsibilities\n2. Operator walkthrough\n3. Measurements and repairs\n4. Evidence and handover'],
 ['Scope and responsibilities','Five support checks and a discoverable catalogue'],
 ['Native responsibilities','Actions: reviewed revision and inputs produce named stages and receipts.\nSQLcl PROJECT 25.4.1: native source produces archives and target changes.\nNode24 guards: logs, metadata and receipts produce validation or failure.\nGit: reviewed files produce immutable version history.\nOracle/APEX/ORDS: target data produces the authenticated user result.\nNo model inference or OCI API interaction is selected.'],
 ['The five guards','Tool: qualified release/build and native metadata.\nOutput: native error signatures and empty evidence.\nProvenance: source, qualified tool and exact archive bytes.\nCandidate: open state, main base and source identities.\nReview: sole changed file, trusted decision and SQL bytes.'],
 ['Operator walkthrough','Known repository source and real hosted inputs'],
 ['Discover the catalogue','cd "$(git rev-parse --show-toplevel)"\ncode sprint-work/E.19/CATALOGUE.md\n\nInspect each purpose, required input, output and refusal.\nThe five guards need no npm packages or Python.'],
 ['Dispatch the action matrix','gh workflow run acceptance.yml \\\n  -R rstyczynski/APEX_CICD_E.19\n\nFive valid action paths and missing/malformed inputs.\nSource, artifact, build and trusted Review mismatch cases.\nEvery refusal must skip its mutation sentinel.'],
 ['Observed hosted action results','Initial real run 45873741697 at 6b6a412.\nThree valid actions succeeded.\nExpected provenance rejection skipped downstream mutation.\nFull five-action matrix is separate acceptance evidence.','03-action-refusal-framed.png'],
 ['Actual native delivery','gh workflow run native.yml \\\n  -R rstyczynski/APEX_CICD_E.19\n\nFresh databases and private inputs in RUNNER_TEMP.\nQualified SQLcl 25.4.1.022.0618 and metadata 25.4.1.0.\nVisible native export, stage, verify, release and deployment.'],
 ['Refusal and recovery','A failed action stops normal downstream steps.\nInspect the named action error and independently expected source.\nCorrect evidence or the producer, then run qualification again.\nNever set continue-on-error on a production guard.\nTest-only expected failures assert outcome and skipped mutation.'],
 ['Measurements and repairs','Equivalent workloads, explicit limits and observed failures'],
 ['Equivalent process measurements','Five helpers per batch, two paired hosts, reversed runtime order.\nNode v24.22.1: first median 167.27 ms, repeated median 168.45 ms.\nPython 3.12.3: first median 120.97 ms, repeated median 138.60 ms.\nFirst batches n=2; repeated batches n=20 per runtime.\nSmall-file helper timing does not establish whole-pipeline speed.'],
 ['Setup and maintenance','No runtime installation occurred on these hosts.\nGitHub supplies the action Node24 runtime; Python was preinstalled.\nFive guards have zero npm dependencies and one shared implementation.\nAction metadata and entrypoints add maintenance files.\nThe reason to migrate is reusable Python-free checks, not assumed speed.'],
 ['Image rollout correction','An exploratory timing run mixed hosted image revisions.\nIt passed functionality but could not support equal-condition comparison.\nThe corrected run pairs both runtimes on each host.\nIt reverses order on the second host and retains all sample records.\nProvider warmth and background load remain uncontrolled.'],
 ['Candidate permission repair','Actual PR-metadata lookup failed HTTP 403 in trial 45875288879.\nCandidate checks and SQL did not run after that failure.\nThe validation job needed pull-requests:read for the selected PR.\nThe repair grants read access; status publication remains denied.\nRetry 45875727042 passed candidate, Review and Oracle checks.'],
 ['Evidence and handover','Acceptance, regression and operating references'],
 ['Evidence boundaries','Matrix fixtures prove action contracts and workflow conditions.\nNative receipts prove actual SQLcl delivery and target preservation.\nA real PR exercises trusted candidate/Review binding with Oracle.\nFull regression retains earlier laboratory and hosted checks.\nScreenshots support observations and never replace functional checks.'],
 ['Assigned outcome and next decisions','PBI-087: Done. All accepted outcomes and six gates pass.\nPBI-087.1: Done; inventory and catalogue.\nPBI-087.2: Done; five guards and actual native qualification.\nPBI-087.3: Done; comparison, regression and handover.\nLifecycle Architecture and production rollout remain separate decisions.'],
 ['Q&A','Inspect the catalogue, real Actions steps and comparison report.\nThe walkthrough and screenshot gallery retain the complete journey.']
];
specs.splice(10,0,['Actual APEX result after delivery','Run 45874462191: fresh credentials, actual Sign In and retained-row rendering after native upgrade/repeat. Framed from capture 05; full viewport and derivative 06 are in the gallery.','06-native-row-framed.png']);
await fs.writeFile(`${dir}/slide-map.json`,JSON.stringify(specs.map((s,i)=>({slide:i+1,title:s[0]})),null,2));
for(let i=0;i<specs.length;i++){
 const s=p.slides.add();s.background.fill='#102638';
 function text(value,y,h,size,font='Arial',bullets=false){const sh=s.shapes.add({geometry:'textbox',position:{left:60,top:y,width:1160,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=bullets?makeNativeBulletParagraphs(value.split('\n'),{marginLeftPoints:18,hangingPoints:9,spaceAfterPoints:12}):value;sh.text.style={fontSize:size,typeface:font,color:'#FFFFFF',autoFit:'none',insets:0};}
 const [title,body,img]=specs[i];text(title,42,90,42);
 if(img){const bytes=await fs.readFile('progress/E.19/screenshots/'+img);s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:title,fit:'contain',position:{left:60,top:150,width:1160,height:360}});text(body,535,120,24);}
 else text(body,185,440,['Discover the catalogue','Dispatch the action matrix','Actual native delivery'].includes(title)?25:29,['Discover the catalogue','Dispatch the action matrix','Actual native delivery'].includes(title)?'Courier New':'Arial',!['JavaScript support actions','Agenda','Scope and responsibilities','Operator walkthrough','Discover the catalogue','Dispatch the action matrix','Actual native delivery','Measurements and repairs','Evidence and handover','Q&A'].includes(title));
 text(String(i+1),675,30,18);s.speakerNotes.text='Evidence: progress/E.19/sprint_E.19_checklist.md; comparison_report.md; sprint_E.19_tests.md; screenshots/index.html; sprint_E.19_inventory.md. Current lifecycle is authoritative in PLAN.md and handover, not this slide snapshot.';
 const png=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`${dir}/slide-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
}
await(await PresentationFile.exportPptx(p)).save(`${dir}/candidate.pptx`);
const revision=process.env.DECK_REVISION||'1';
await finalizePresentation({workspaceDir:process.cwd(),candidatePath:`${process.cwd()}/${dir}/candidate.pptx`,finalPath:`${process.cwd()}/${dir}/output/validated-${revision}.pptx`,pythonExecutable:'/usr/bin/python3',integrityValidatorPath:`${skill}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${skill}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Arial','Courier New']},verifyArtifactToolImport:true,receiptPath:`${process.cwd()}/${dir}/validation-${revision}.json`});
await fs.copyFile(`${dir}/output/validated-${revision}.pptx`,'progress/E.19/sprint_E.19_increment_demo.pptx');
