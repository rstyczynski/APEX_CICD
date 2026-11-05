import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const root=process.cwd(),skill=process.env.PRESENTATION_SKILL_DIR;
const build=await fs.mkdtemp(path.join(root,'.local-apex/e3/presentation-build/mapping-accepted-'));
const input=path.join(root,'progress/E.3/sprint_E.3_increment_demo.pptx');
await fs.copyFile(input,path.join(build,'original.pptx'));
const deck=await PresentationFile.importPptx(await FileBlob.load(input));
const old=[...deck.slides.items];
if(old.length!==22) throw new Error('Expected 22 slides before mapping acceptance update');
const ink='#14313E',teal='#126B70',soft='#D5E4E6';
function text(s,value,x,y,w,h,size=28,color=ink,bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;
}
const mapping=old[20];
function replaceAt(slide,y,value){
 const sh=slide.shapes.items.find(sh=>Math.abs(sh.position.top-y)<1);
 if(!sh)throw new Error('Missing text at '+y);
 sh.text=value;
}
replaceAt(mapping,427,'utPLSQL: PBI-040. UI checks: PBI-034. Audits: PBI-041.\nPrivate branch environments: PBI-056. Mini-app reuse: PBI-044.');
replaceAt(mapping,496,'Accepted mapping and tracked gaps');
replaceAt(mapping,539,'Mapping accepted on 5 November 2026. Remaining capabilities stay in\nbacklog. Deployed APEX release identity is tracked by PBI-057.');
mapping.speakerNotes.text=mapping.speakerNotes.text.replace('This slide does not claim LC-1 completion or production qualification.','The Product Owner accepted LC-1 on 2026-11-05 and directed backlog follow-up. No separate acceptance/report gate remains. This does not claim production qualification.')+' Backlog dispositions: PBI-034 browser automation; PBI-040 PL/SQL coverage; PBI-041 audits; PBI-044 mini-app reuse; new PBI-056 repeatable private branch environments, distinct from PBI-019 parallel integration; new PBI-057 deployed APEX release identity. PBI-043 owns full test-gated pipelines. Source: sprint_E.3_pipeline_scope.md#lc-1--oracle-apex-lifecycle-alignment-validation and BACKLOG.md. New items remain Proposed and unscheduled.';
replaceAt(old[16],635,'Technical handover delivered. Oracle lifecycle mapping accepted; gaps tracked in backlog.');
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(build,'output','mapping-accepted.pptx');await fs.mkdir(path.dirname(finalPath),{recursive:true});
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:process.env.PRESENTATION_RUNTIME_PYTHON,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:22,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(const [i,s] of final.slides.items.entries()){
 const png=await final.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
await fs.writeFile(path.join(root,'.local-apex/e3/presentation-build/mapping-accepted-latest.json'),JSON.stringify({build,finalPath}));
console.log(JSON.stringify({build,finalPath}));
