import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile, FileBlob} from '@oai/artifact-tool';

const root=process.cwd();
const skill=process.env.PRESENTATION_SKILL_DIR;
const python=process.env.PRESENTATION_RUNTIME_PYTHON;
if(!skill || !python) throw new Error('Supply presentation skill and bundled Python runtime paths.');
const {makeNativeBulletParagraphs,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const build=path.join(root,'.local-apex/e2/po-handover-build');
const out=path.join(root,'.local-apex/e2/po-handover-output');
const rev=process.argv[2]||'v1';
await fs.mkdir(build,{recursive:true}); await fs.mkdir(out,{recursive:true});
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const C={navy:'#14313E',teal:'#126B70',muted:'#52636D',paper:'#FFFFFF',pale:'#F0F5F4',amber:'#966315',red:'#9E3D2A',soft:'#D5E4E6'};
const map=[];
function text(s,str,x,y,w,h,size=28,color=C.navy,bold=false,font='Arial'){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=str; sh.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;
}
function slide(title,sources=[],dark=false){
 const s=deck.slides.add();s.background.fill=dark?C.navy:C.paper;
 text(s,title,64,46,1152,100,44,dark?'#FFFFFF':C.navy,true);
 text(s,String(deck.slides.items.length).padStart(2,'0'),1170,676,45,22,16,dark?C.soft:C.muted);
 s.speakerNotes.text='E.2 Product Owner handover, 22 October 2026. Decisions pending.\nSources:\n'+sources.join('\n');
 map.push({slide:deck.slides.items.length,title,sources});return s;
}
function note(s,value){s.speakerNotes.text+='\n'+value;}
function bullets(s,items,x,y,w,h,size=29,color=C.navy){
 const sh=text(s,'',x,y,w,h,size,color);
 sh.text=makeNativeBulletParagraphs(items,{marginLeftPoints:20,hangingPoints:10,spaceAfterPoints:18});
 return sh;
}
function table(s,values,widths,y=175,height=390,size=27){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:64,top:y,width:1152,height,columnWidths:widths,values});
 t.styleOptions={headerRow:true,bandedRows:false};
 t.borders.assign({fill:'#FFFFFF',width:2,style:'solid'});
 for(let r=0;r<values.length;r++){
  for(let c=0;c<values[0].length;c++){
   const cell=t.getCell(r,c);cell.fill=r===0?C.navy:(r%2?C.pale:'#FFFFFF');
   cell.text.style={typeface:'Arial',fontSize:r===0?24:size,color:r===0?'#FFFFFF':C.navy,bold:r===0||c===0,insets:16,autoFit:'none',verticalAlignment:'middle'};
  }
 }
 return t;
}
const E='progress/E.2/';
let s=slide('E.2\nProduct Owner handover',[E+'sprint_E.2_handover.md',E+'oracle-gap-analysis.md'],true);
text(s,'SQLcl PROJECT and Working Copies\nfit the delivery approach',64,228,1110,120,46,'#FFFFFF',true);
text(s,'Continue qualification before production adoption',64,392,1100,65,32,C.soft);
text(s,'Give developers flexibility through stable,\nindustry-standard tools and techniques.',64,512,1050,85,29,C.soft);
text(s,'22 October 2026',64,650,700,30,20,C.soft);
note(s,'Recommendation only. No Product Owner decision, sprint closure or production certification is implied. E.1 historical evidence remains unchanged.');

s=slide('Demonstrated delivery outcomes',[E+'tests/project-integration-mapped-validation.json',E+'tests/project-uat-promotion-validation.json',E+'tests/project-f2-upgrade-validation.json',E+'sprint_E.2_handover.md']);
table(s,[
 ['Capability','E.2 result'],
 ['PROJECT lifecycle','Capture, stage, package and mapped deployment worked'],
 ['Initial delivery','Integration and UAT used the same initial archive'],
 ['Hello 1.0.1 patch','Fresh installation, populated upgrade and repeat passed'],
 ['Runtime access','Restricted verifier access and native publication worked']
],[310,842],165,375,27);
text(s,'Reference patch runs: 26 fresh, 4 applied on upgrade, 0 on repeat',64,574,1115,48,28,C.teal,true);
text(s,'Integration receipts record preparation. The Product Owner reported F, including UAT, completed.',64,632,1115,44,21,C.muted);
note(s,'Counts concern the reference assessment patch, not a new acceptance claim for every artifact. Retained F verification still fails. Operator-reported F completion is separate from preparation receipts.');

s=slide('Working Copy integration and the team checkpoint',[E+'tests/e2_desktop_repeat_merge_full.jpg',E+'tests/desktop_repeat_main_preservation.json',E+'tests/project-f1-working-copy-validation.json','https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html']);
const bytes=await fs.readFile(path.join(root,E+'tests/e2_desktop_repeat_merge_full.jpg'));
s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/jpeg',alt:'Retained desktop repeat showing a selected page merge into Main with target backup enabled',fit:'contain',crop:{left:0.022,top:0.12,right:0.255,bottom:0.455},position:{left:64,top:164,width:1152,height:440}});
text(s,'Reviewed Main state reaches Git through PROJECT export',64,623,1152,40,28,C.teal,true);
text(s,'Retained desktop repeat on the earlier fixture',64,666,1050,24,18,C.muted);
note(s,'Image is a later desktop repeat on the earlier reduced fixture, not a screenshot of the Product Owner F execution. Native comparison, selective refresh and merge are observed. Working Copies share the parsing schema. Direct private-copy export is possible through selection filters but is not the demonstrated release path. A team checkpoint remains part of the Working Copy/Main journey.');

s=slide('Native tools replace specific custom responsibilities',[E+'oracle-gap-analysis.md','deploy/control.sql','deploy/release_control.sql','deploy/recovery/control.sql']);
text(s,'Native capabilities',64,175,530,50,32,C.teal,true);
bullets(s,['APEX restricted access and publication','PROJECT source, distribution and artifacts','Liquibase migration execution history'],64,252,530,310,29);
text(s,'Controls still requiring qualification',680,175,530,82,32,C.red,true);
bullets(s,['Component compatibility and artifact admission','Deployment ownership and provenance','Live-drift rejection and reviewed recovery'],680,282,530,310,29);
text(s,'E1_CTRL covers more than runtime access. Installed component versions are separate.',64,622,1152,48,24,C.muted);
note(s,'Avoid a wholesale replacement claim. Native availability covers the exercised access gate, not request draining, stale-attempt fencing or promotion trust. Prefer native functions where qualified. Do not duplicate capture or packaging in a new controller.');

s=slide('G, H and I: native support gaps',[E+'tests/project-verify-fix-validation.json',E+'h-live-drift-evidence.md',E+'cicd-walkthrough.md','https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.2/sqcug/update.html']);
text(s,'Specified automatic protections in the evaluated APEX / SQLcl PROJECT workflow',64,148,1152,45,23,C.muted);
table(s,[
 ['Scenario','Native support','Required response'],
 ['G  Dependencies','Not supported','Explicit component contracts and admission'],
 ['H  Live drift','Not supported in evaluated path','Compare target definitions and reject before writes'],
 ['I  Automatic repair','Not supported','Inspect partial state and design a reviewed repair']
],[238,355,559],218,346,27);
text(s,'Reviewed forward repair is supported by SQLcl/Liquibase. E.2 has not exercised it.',64,608,1152,65,25,C.red,true);
note(s,'G: 25.4.1 clean native verification accepted both allowed and conflicting project declarations. H: limited export comparison detected the edit; zero-change replay proves neither rejection nor overwrite behavior for a pending import. Do not infer absence of every Oracle drift capability. I: automatic repair and reviewed forward repair are different capabilities. E.1-equivalent repair remains missing E.2 validation. Business-data equality is not application/schema drift detection.');

s=slide('Release qualification remains open',[E+'tests/project-verify-fix-validation.json',E+'tests/project-f2-upgrade-validation.json',E+'oracle-gap-analysis-detail.md']);
text(s,'Retained F artifacts',64,168,530,55,32,C.navy,true);
text(s,'SQLcl 25.3',64,245,530,65,46,C.red,true);
bullets(s,['One native verification error remains','Post-stage APEX edits create source/distribution inconsistency'],64,345,530,210,28);
text(s,'Separate clean comparison',680,168,530,55,32,C.navy,true);
text(s,'SQLcl 25.4.1',680,245,530,65,46,C.teal,true);
bullets(s,['Verification passed on consistent source','Does not recertify retained F artifacts'],680,345,530,210,28);
text(s,'Next: pin the client, qualify a consistent release and verify mapped identity preservation.',64,615,1152,58,26,C.navy,true);
note(s,'25.4.1 comparison: Errors 0 / Warnings 0 / Info 15. Negative controls failed on a missing stage include and post-stage APEX alteration. Earlier mapped import changed observed region IDs, so required identity/saved-report preservation remains to qualify. This is a release-qualification blocker rather than general PROJECT/Working Copy incompatibility.');

s=slide('Follow-up order in the existing backlog',['BACKLOG.md',E+'oracle-gap-analysis.md']);
const steps=[
 ['1. Toolchain and release identity','Pinned client, consistent source/distribution and target mappings','PBI-028/029/037/038'],
 ['2. Collaboration and component contracts','Working Copy checkpoints, one migration owner and SemVer rules','PBI-020/039/042/052'],
 ['3. Delivery protections and reviewed repair','Compatibility, drift rejection, ownership fencing and partial-state repair','PBI-021/022/023/024/045'],
 ['4. Quality checks and pipeline operation','utPLSQL, audits and browser checks against the same candidate','PBI-040/041/043/046']
];
steps.forEach(([title,body,ids],i)=>{
 const y=166+i*106;text(s,title,64,y,1120,40,29,C.navy,true);text(s,body,95,y+44,785,54,24,C.muted);text(s,ids,920,y+44,296,56,20,C.teal);
});
text(s,'Complex Foundation upgrades stay in E.5 after stabilization (PBI-048/049/050).',64,626,1152,44,25,C.red,true);
note(s,'Dependency order, not new sprint scheduling. Contract definition can begin during stabilization. Existing backlog owns priority and assignment. No duplicate root items. Combine checks without claiming any single audit, coverage measure or import proves overall correctness.');

s=slide('Product Owner decisions',[E+'sprint_E.2_handover.md',E+'oracle-gap-analysis.md'],true);
const decisions=[
 ['1. Accept the assessment with its limits','Recommended: accept findings, retain protection gaps and missing repair validation'],
 ['2. Keep PROJECT and Working Copies as options','Recommended: compatible repository conventions and one migration authority'],
 ['3. Prioritize stabilization and protection','Recommended: qualify those outcomes before pipeline adoption'],
 ['4. Reevaluate E.1 authoring restrictions','Recommended: allow native collaboration where required controls remain satisfied'],
 ['5. Retain the E.5 boundary','Recommended: complex Foundation upgrades follow toolchain stabilization']
];
decisions.forEach(([title,body],i)=>{const y=156+i*92;text(s,title,64,y,1145,39,29,'#FFFFFF',true);text(s,body,96,y+40,1120,49,23,C.soft);});
text(s,'All decisions pending. Acceptance does not certify production readiness.',64,650,1110,30,21,C.soft);

s=slide('PROJECT repository: retained application source',[E+'cicd-walkthrough.md',E+'repository-layout.md','.local-apex/e2/project-walkthrough/component-repo-f2']);
text(s,'Abbreviated from component-repo-f2; omitted descendants are not shown',64,145,1152,40,23,C.muted);
text(s,[
 'repo/',
 '|-- .dbtools/',
 '|   |-- project.config.json',
 '|   `-- filters/project.filters',
 '|-- src/database/e1_dev_c/',
 '|   |-- apex_apps/f810003/',
 '|   |   |-- f810003.sql',
 '|   |   `-- readable/application/',
 '|   |-- tables/',
 '|   `-- package_bodies/'
].join('\n'),64,216,578,410,25,C.navy,false,'Courier');
text(s,[
 'repo/',
 '|-- dist/',
 '|   |-- install.sql',
 '|   |-- component-contract.json',
 '|   |-- releases/',
 '|   |   |-- 1.0.0/',
 '|   |   |-- next/',
 '|   |   `-- apex/',
 '|   `-- utils/properties/',
 '`-- artifact/'
].join('\n'),680,216,536,410,25,C.navy,false,'Courier');
text(s,'The application Git repository is retained evidence. Only laboratory runtime resources are disposable.',64,641,1152,35,22,C.muted);
note(s,'Actual local app repo .local-apex/e2/project-walkthrough/component-repo-f2 inspected during authoring. Tree abbreviated. artifact holds generated archives; tracked source/distribution and private archives are different retention responsibilities. .dbtools filters select Main 810003 for demonstrated release capture. Do not confuse this application repository with the parent APEX_CICD delivery repository.');

s=slide('Native commands and evidence boundaries',[E+'cicd-walkthrough.md','https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html']);
text(s,'SQLcl PROJECT performs capture, staging and artifact deployment',64,162,1152,60,30,C.teal,true);
text(s,'project export -list\nproject export\nproject stage -branch-name e2-world -verbose\nproject gen-artifact -name e2 -version 1.0.1 -format zip\nproject deploy -file artifact/e2-1.0.1.zip',64,275,1152,245,27,C.navy,false,'Courier');
text(s,'Illustrative command sequence. Prepared mappings, baseline branches and release inputs are required.',64,569,1152,65,25,C.muted);
note(s,'This appendix is an explanation, not a new runnable walkthrough or a request to generate/overwrite archives. Actual artifact names and mappings are in cicd-walkthrough.md. PROJECT export does not commit to Git. Git reviews/commits are separate operations. Native commands do not infer component compatibility or implement a target drift admission policy.');

s=slide('Evidence and next review',[E+'sprint_E.2_handover.md',E+'oracle-gap-analysis.md',E+'tests/project-integration-mapped-validation.json',E+'tests/project-f2-upgrade-validation.json',E+'tests/project-verify-fix-validation.json','refs/apex-lifecycle-management-v3.pdf']);
text(s,'Decision brief and gap analysis',64,170,1100,45,32,C.teal,true);
text(s,'sprint_E.2_handover.md\noracle-gap-analysis.md',64,237,1110,100,29,C.navy,false,'Courier');
bullets(s,['Receipts identify actual clients, targets and reference runs','The Product Owner reported F completed on 20 October','G/H/I retain the stated native limits and unfinished validation'],64,376,1130,203,28);
text(s,'Next review: decide the direction and follow-up priority. E.1 evidence remains intact.',64,620,1152,56,27,C.teal,true);
note(s,'All source file paths relative to repository root. Primary Oracle sources: refs/apex-lifecycle-management-v3.pdf; https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.3/sqcug/project.html; https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.4/sqcug/project.html; https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/about-working-copies.html; https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/using-shared-component-subscriptions.html; https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.2/sqcug/update.html. The historical increment deck remains separate. Product Owner decisions and sprint status have not been changed.');

const candidate=path.join(build,`candidate-${rev}.pptx`);
await (await PresentationFile.exportPptx(deck)).save(candidate);
const finalPath=path.join(out,`sprint_E.2_product_owner_handover-${rev}.pptx`);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','2','--require-native-table-slide','5'],
 requiredNativeTableOwnerSlides:[2,5],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'design',families:['Arial','Courier']},verifyArtifactToolImport:true,
 receiptPath:path.join(build,`validation-${rev}.json`)});
const finalDeck=await PresentationFile.importPptx(await FileBlob.load(finalPath));
const renderDir=path.join(build,`render-${rev}`);await fs.mkdir(renderDir,{recursive:true});
for(const [i,sl] of finalDeck.slides.items.entries()){
 const png=await finalDeck.export({slide:sl,format:'png',scale:1});
 await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
await fs.writeFile(path.join(build,`slide-map-${rev}.json`),JSON.stringify(map,null,2));
console.log(JSON.stringify({slides:map.length,finalPath,renderDir}));
