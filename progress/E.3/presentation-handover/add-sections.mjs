import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const root=process.cwd(),skill=process.env.PRESENTATION_SKILL_DIR;
const build=await fs.mkdtemp(path.join(root,'.local-apex/e3/presentation-build/sections-'));
const input=path.join(root,'progress/E.3/sprint_E.3_increment_demo.pptx');
await fs.copyFile(input,path.join(build,'original.pptx'));
const deck=await PresentationFile.importPptx(await FileBlob.load(input));
const old=[...deck.slides.items];
if(old.length!==15) throw new Error('Expected 15 slides before agenda/section insertion');
const ink='#14313E',teal='#126B70',soft='#D5E4E6';
function text(s,value,x,y,w,h,size=28,color=ink,bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;
}
const sections=[
 ['Architecture and setup','Application structure, responsibilities and GitHub configuration',[1,2,3]],
 ['Native authoring and capture','Working Copy, Main checkpoint and SQLcl PROJECT source',[4,5,6]],
 ['Review and release preparation','Pull requests, versioning and changelogs',[7,8]],
 ['Deployment and results','Selected-tag deployment, retained history and handover',[9,10,11]],
 ['Oracle lifecycle mapping','Official guidance, E.3 adaptations and remaining gaps',[12,13,14]],
];
const agenda=deck.slides.add();agenda.background.fill='#FFFFFF';
text(agenda,'Agenda',64,40,1152,105,42,ink,true);
sections.forEach(([title,desc],i)=>{text(agenda,`${i+1}. ${title}`,64,165+i*90,1152,38,29,teal,true);text(agenda,desc,105,203+i*90,1111,34,23);});
agenda.speakerNotes.text='Agenda for the E.3 prototype handover. Section order matches the following divider slides and operator walkthrough.';
const ordered=[old[0],agenda],mapping={1:1};
sections.forEach(([title,desc,indices],i)=>{
 const s=deck.slides.add();s.background.fill=ink;
 text(s,`SECTION ${i+1}`,64,155,1152,45,25,soft,true);
 text(s,title,64,245,1152,145,50,'#FFFFFF',true);
 text(s,desc,64,430,1152,110,30,soft);
 s.speakerNotes.text=`Section ${i+1}: ${title}. ${desc}. Content and evidence follow in the next slides.`;
 ordered.push(s);
 for(const n of indices){ordered.push(old[n]);mapping[n+1]=ordered.length;}
});
ordered.forEach((s,i)=>s.moveTo(i));
if(deck.slides.items.some((s,i)=>s.id!==ordered[i].id)) throw new Error('Slide order mismatch');
ordered.forEach((s,i)=>{
 const footer=s.shapes.items.find(sh=>Math.abs(sh.position.left-1170)<1&&Math.abs(sh.position.top-675)<1);
 if(footer)footer.text=String(i+1).padStart(2,'0');
 else text(s,String(i+1).padStart(2,'0'),1170,675,45,22,16,i===1?'#52636D':soft);
});
const foot13=old[12].shapes.items.find(sh=>Math.abs(sh.position.top-635)<1);foot13.text='Oracle paper v3.2 · Authoring evidence: E.3 slides 8–12';
const foot14=old[13].shapes.items.find(sh=>Math.abs(sh.position.top-635)<1);foot14.text='Oracle paper v3.2 · Pipeline evidence: E.3 slides 13–16';
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(build,'output','sections.pptx');await fs.mkdir(path.dirname(finalPath),{recursive:true});
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:process.env.PRESENTATION_RUNTIME_PYTHON,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:21,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(const [i,s] of final.slides.items.entries()){
 const png=await final.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
await fs.writeFile(path.join(build,'mapping.json'),JSON.stringify(mapping,null,2));
await fs.writeFile(path.join(root,'.local-apex/e3/presentation-build/sections-latest.json'),JSON.stringify({build,finalPath,mapping}));
console.log(JSON.stringify({build,finalPath,mapping}));
