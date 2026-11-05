import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const root=process.cwd(),skill=process.env.PRESENTATION_SKILL_DIR;
const build=await fs.mkdtemp(path.join(root,'.local-apex/e3/presentation-build/closing-'));
const input=path.join(root,'progress/E.3/sprint_E.3_increment_demo.pptx');
await fs.copyFile(input,path.join(build,'original.pptx'));
const deck=await PresentationFile.importPptx(await FileBlob.load(input));
const old=[...deck.slides.items];
if(old.length!==21) throw new Error('Expected 21 slides before closing slide insertion');
const ink='#14313E',teal='#126B70',soft='#D5E4E6';
function text(s,value,x,y,w,h,size=28,color=ink,bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;
}
const closing=deck.slides.add();closing.background.fill=ink;
text(closing,'Thank you',64,245,1152,110,64,'#FFFFFF',true);
text(closing,'Q&A',64,405,1152,70,36,soft);
text(closing,'22',1170,675,45,22,16,soft);
closing.speakerNotes.text='Closing slide. Invite questions about the E.3 architecture prototype and its mapping to Oracle lifecycle guidance.';
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(build,'output','closing.pptx');await fs.mkdir(path.dirname(finalPath),{recursive:true});
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:process.env.PRESENTATION_RUNTIME_PYTHON,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:22,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(const [i,s] of final.slides.items.entries()){
 const png=await final.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
await fs.writeFile(path.join(root,'.local-apex/e3/presentation-build/closing-latest.json'),JSON.stringify({build,finalPath}));
console.log(JSON.stringify({build,finalPath}));
