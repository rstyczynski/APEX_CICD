import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const root=process.cwd(),skill=process.env.PRESENTATION_SKILL_DIR,python=process.env.PRESENTATION_RUNTIME_PYTHON;
const {makeNativeBulletParagraphs,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const build=path.join(root,'.local-apex/e3/presentation-build'),out=path.join(root,'.local-apex/e3/presentation-output');
const revision=process.argv[2]||'v1';await fs.mkdir(build,{recursive:true});await fs.mkdir(out,{recursive:true});
const deck=Presentation.create({slideSize:{width:1280,height:720}}),map=[];
const C={ink:'#14313E',teal:'#126B70',muted:'#52636D',soft:'#D5E4E6',red:'#9E3D2A'};
function text(s,value,x,y,w,h,size=28,color=C.ink,bold=false,font='Arial'){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;
}
function slide(title,source,dark=false){const s=deck.slides.add();s.background.fill=dark?C.ink:'#FFFFFF';text(s,title,64,40,1152,105,42,dark?'#FFFFFF':C.ink,true);text(s,String(deck.slides.items.length).padStart(2,'0'),1170,675,45,22,16,dark?C.soft:C.muted);s.speakerNotes.text='E.3 handover. Sources: '+source;map.push({slide:deck.slides.items.length,title,source});return s;}
function bullets(s,items,y=180,size=30){const sh=text(s,'',64,y,1130,430,size);sh.text=makeNativeBulletParagraphs(items,{marginLeftPoints:20,hangingPoints:10,spaceAfterPoints:18});return sh;}
function code(s,items,y=230,size=25){return text(s,items.join('\n'),64,y,1152,325,size,C.ink,false,'Courier');}
async function shot(s,file,y=160,h=430,crop){const bytes=await fs.readFile(path.join(root,file));s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:path.basename(file),fit:'contain',crop,position:{left:64,top:y,width:1152,height:h}});}
const E='progress/E.3/';let s;
s=slide('E.3 Git development pipeline\nArchitecture prototype',E+'sprint_E.3_handover.md',true);
text(s,'Working Copy → reviewed Git source\nAutomated version and changelog\nManual deployment by version tag',64,235,1120,220,42,'#FFFFFF',true);
text(s,'3 November 2026 · one lab target · real GitHub and Oracle execution',64,610,1100,50,24,C.soft);
s=slide('Walkthrough agenda',E+'sprint_E.3_increment_demo.md');
text(s,'1. Author and capture one heading change\n\n2. Review the PR and prepare version 1.0.1\n\n3. Deploy the selected tag and inspect history\n\n4. Review failure evidence and remaining risks',64,185,1120,420,32);
s=slide('Architecture and responsibilities',E+'sprint_E.3_design.md');
const rows=[['Developer / APEX Working Copy','Edit metadata; compare and merge into DEV Main'],['Git + SQLcl PROJECT','Review source and stage native Liquibase distribution'],['GitHub-hosted checks + Release Please','Validate label/title; generate release PR, version and changelogs'],['Deployer / local runner','Select tag; verify, package and deploy to E3_TARGET']];
rows.forEach(([a,b],i)=>{text(s,a,64,165+i*108,1130,40,30,C.teal,true);text(s,b,92,211+i*108,1100,46,25);});
text(s,'PR merge, tag creation and GitHub Release publication do not deploy.',64,630,1130,34,26,C.red,true);
s=slide('Working Copy: change one Home heading',E+'tests/working-copy-inspection.png');
await shot(s,E+'tests/working-copy-inspection.png',152,440,{left:0.42,top:0,right:0,bottom:0.5});
text(s,'Later inspection of retained Working Copy 100 · Main 810003 · shared schema',64,620,1135,42,25,C.teal,true);
s=slide('Native comparison and Main checkpoint',E+'tests/working-copy-diff.png');
text(s,'Observed native comparison: 1 changed · 0 added · 0 missing',64,180,1130,70,34,C.teal,true);
bullets(s,['Selected component: Page 1, Home','Original heading: Hello World - Working Copy','Accepted heading: Hello World - Git pipeline','Target backup enabled; Working Copy retained','Main merge completed successfully'],280,29);
s.speakerNotes.text+=' Raw original comparison capture is retained; no later screenshot is represented as the historical merge.';
s=slide('Native source capture and staging',E+'sprint_E.3_implementation.md');
code(s,['bash scripts/capture.sh','git diff -- src pipeline.json','python3 scripts/lab.py stage','python3 scripts/lab.py verify','git diff -- dist'],190,29);
text(s,'Source adapter replaces the inherited E1 controller hook before stage.\nNative verification must report zero errors.',64,540,1130,100,28,C.teal,true);
s=slide('PR labels and Conventional Commits','https://github.com/rstyczynski/APEX_CICD_E3/pull/1');
bullets(s,['patch → fix: update Home heading','minor → feat: add a compatible capability','major → feat!: change the contract','Hosted checks reject missing/conflicting labels or title mismatch','Squash merge retains the classification in Git history'],175,30);
text(s,'Performed: PR 1 heading fix and PR 3 runtime correction; both patch.',64,635,1120,35,24,C.teal,true);
s=slide('Release Please: version and both changelogs','https://github.com/rstyczynski/APEX_CICD_E3/pull/2');
bullets(s,['Two accepted fixes accumulated into release PR 2','Generated version.txt: 1.0.0 → 1.0.1','Generated CHANGELOG.md and matching GitHub Release notes','Hosted checks were manually dispatched on the bot PR head','Release-PR merge created tag v1.0.1; target stayed unchanged'],175,30);
s=slide('Manual deployment of the selected tag',E+'tests/release-receipt.json');
code(s,['gh workflow run release.yml \\','  --repo rstyczynski/APEX_CICD_E3 \\','  --ref main -f version_tag=v1.0.1','','gh run view 41664798289 \\','  --repo rstyczynski/APEX_CICD_E3'],195,27);
text(s,'Succeeded: native verify → one archive → target deployment → preservation',64,545,1135,75,28,C.teal,true);
text(s,'Exact tag source uses a named local build branch; no live DEV export.',64,630,1135,40,24,C.muted);
s=slide('Deployed application and retained history',E+'tests/deployed-home.png; '+E+'tests/deployed-history.png');
await shot(s,E+'tests/deployed-home.png',155,380);
text(s,'Observed in browser: Hello World - Git pipeline\nRetained Hello World history row and all prior fields verified.',64,555,1130,85,28,C.teal,true);
text(s,'Repository release: v1.0.1. APEX display metadata remains 1.0.0.',64,650,1100,25,20,C.muted);
s=slide('Observed failures and corrections',E+'sprint_E.3_tests.md');
bullets(s,['Slash-containing branch: native source/dist verification failed; use explicit slashless demo branches','Mapping file lookup: resolve committed properties from the selected checkout','Inherited E1 runtime hook: correct reviewed source before native staging','Detached HEAD: first remote run stopped; corrected workflow uses a named build branch','Missing changeset: real native verification rejected it; target unchanged'],160,28);
s=slide('Results and handover boundary',E+'sprint_E.3_handover.md; '+E+'sprint_E.3_tests.md');
text(s,`1. PBI-053.1: Working Copy, Git capture and native verification

2. PBI-053.2: classified PRs, release PR, version and changelogs

3. PBI-053.3: selected-tag deployment, preservation and failure gate`,64,165,1130,290,29);
text(s,`New smoke and integration gates passed; existing smoke regression passed.

Parallelism, full identity coverage, drift/fencing and general recovery remain later work.`,64,465,1130,150,27);
text(s,'Technical handover delivered. Product Owner acceptance and sprint closure remain separate.',64,635,1135,46,23,C.teal,true);
const candidate=path.join(build,`candidate-${revision}.pptx`);await(await PresentationFile.exportPptx(deck)).save(candidate);
const finalPath=path.join(out,`sprint_E.3_increment_demo-${revision}.pptx`);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Arial','Courier']},verifyArtifactToolImport:true,receiptPath:path.join(build,`validation-${revision}.json`)});
const imported=await PresentationFile.importPptx(await FileBlob.load(finalPath));const renderDir=path.join(build,`render-${revision}`);await fs.mkdir(renderDir,{recursive:true});for(const [i,sl]of imported.slides.items.entries()){const png=await imported.export({slide:sl,format:'png',scale:1});await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));}
await fs.writeFile(path.join(build,`slide-map-${revision}.json`),JSON.stringify(map,null,2));console.log(JSON.stringify({finalPath,renderDir,slides:map.length}));
