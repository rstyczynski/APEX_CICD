import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
const {PresentationFile,FileBlob}=await import(pathToFileURL(path.join(process.env.RUNTIME_NODE_MODULES,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const root=process.cwd(),skill=process.env.PRESENTATION_SKILL_DIR,python=process.env.PRESENTATION_RUNTIME_PYTHON;
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const build=path.join(root,'.local-apex/e3/presentation-build/file-effects-'+Date.now());await fs.mkdir(build,{recursive:true});
const before=path.join(build,'before.pptx');await fs.writeFile(before,execFileSync('git',['show','3bf6cd7:progress/E.3/sprint_E.3_increment_demo.pptx']));
const deck=await PresentationFile.importPptx(await FileBlob.load(before)),old=[...deck.slides.items];
if(old.length!==26)throw new Error('Expected the corrected 26-slide source deck');
for(const n of [13,16,18]){const b=await deck.export({slide:old[n-1],format:'png',scale:1});await fs.writeFile(path.join(build,`before-${n}.png`),new Uint8Array(await b.arrayBuffer()));}
const ink='#14313E',teal='#126B70',muted='#52636D';
function text(s,v,x,y,w,h,size=27,color=ink,bold=false,font='Arial'){let sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=v;sh.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;}
function slide(title,notes){const s=deck.slides.add();s.background.fill='#FFFFFF';text(s,title,64,40,1152,90,40,ink,true);s.speakerNotes.text='E.3 file-effect walkthrough. Sources: refs/apex-lifecycle-management-v3.pdf, June 2025 Version 3.2, printed pp.18–20 and 26–30. Verified actual files in examples/git-pipeline/baseline.bundle. Retained heading commit 568a06d, native release ed732c2. progress/E.3/tests/file-flow/provenance.json records inspection; this documentation work does not claim new export/stage/release/deployment. '+notes;return s;}
function code(s,v,x=64,y=220,w=1152,h=300,size=24){return text(s,v,x,y,w,h,size,ink,false,'Courier');}
function checkpoint(s,v){text(s,v,64,600,1152,62,25,teal,true);}
const add=new Map();function after(n,s){add.set(n,[...(add.get(n)||[]),s]);}
let s;
s=slide('project export: the running app becomes source files','The retained Home-heading diff is tests/file-flow/heading-source.diff. Paths and before/after values are historical observed source. SQL and readable YAML are source representations of the same APEX app.');
code(s,'project export',64,150,1152,42,28);
text(s,'Author APEX database: saved heading change',64,210,1152,38,29,teal,true);
text(s,'Before export: Git files still contain the earlier definition',64,261,1152,35,25);
code(s,'src/database/e1_dev_c/apex_apps/f810003/\n├── f810003.sql                         modified\n└── readable/application/\n    ├── f810003.yaml                    modified\n    └── pages/p00001.yaml               modified',64,320,1152,185,24);
code(s,'- name: Hello World - Working Copy\n+ name: Hello World - Git pipeline',64,515,1152,65,24);
checkpoint(s,'Show the source diff, then review/commit. Export has not installed anything in Integration.');after(13,s);
s=slide('project stage: APEX distribution files','The actual heading-only stage changed dist/releases/apex/f810003/f810003.sql and f810003.xml and added an empty e3-heading/stage.changelog.xml. pipeline.json in historical commit 568a06d is project-authored expectation metadata, not PROJECT-generated output.');
code(s,'project stage -branch-name e3-base',64,150,1152,45,28);
text(s,'Input: committed source plus the chosen Git baseline',64,215,1152,38,28,teal,true);
code(s,'dist/releases/\n├── apex/f810003/\n│   ├── f810003.sql                  modified app export\n│   └── f810003.xml                  modified import wrapper\n└── next/changes/e3-heading/\n    └── stage.changelog.xml          new empty stage marker',64,285,1152,245,24);
text(s,'A heading-only change generates no table migration.\nThe XML wrapper supplies the native APEX import and target mapping.',64,525,1152,70,26);
checkpoint(s,'Show git status and open new files. Stage writes to the current checkout; review/commit dist.');after(13,s);
s=slide('project stage: database scripts and include order','Selected initial-assembly paths are real historical files, shown under next as they existed before release ed732c2. Empty heading-only marker is not a database migration. Generated changesets have stable logicalFilePath. User-authored e3_initial_data.sql is registered once, not a dump of runtime business rows.');
text(s,'Retained database example (selected paths)',64,155,1152,40,29,teal,true);
code(s,'dist/releases/next/\n├── release.changelog.xml\n└── changes/e3-initial/\n    ├── stage.changelog.xml\n    ├── e1_dev_c/tables/hello_entries.sql\n    └── _custom/e3_initial_data.sql',64,220,1152,220,25);
text(s,'release.changelog.xml includes the stage changelog.\nThe stage changelog includes each SQL file in execution order.\nhello_entries.sql creates the table; custom seed SQL adds fixed demo data.',64,455,1152,115,26);
checkpoint(s,'Open one include and its SQL file. A changelog is the ordered installation plan; stage has not run it.');after(13,s);
s=slide('project verify: a file relationship check','Native current-release missing-file exercise follows .lastReleaseVersion, with next only as historical fallback. Its exact documented block ran successfully on 2026-11-06, recorded at tests/file-flow/manual-rehearsal.log. Native diagnostics can coexist with zero process exit status, so inspect Errors and exact missing path.');
code(s,'project verify -cbn e3-base -verbose',64,150,1152,45,28);
text(s,'Intact files',64,235,500,40,30,teal,true);text(s,'Referenced SQL file moved aside',670,235,545,40,29,teal,true);
code(s,'XML include exists\nSQL file exists\n\nErrors: 0',64,305,510,200,27);
code(s,'XML include still exists\nSQL file is missing\n\nErrors: 1',670,305,545,200,27);
text(s,'Restoring that file restores a passing result.\nNo numbered release, ZIP, Git commit or target installation is created.',64,510,1152,75,27);
checkpoint(s,'Show the specific missing-file rule, not just the process exit status.');after(13,s);
s=slide('project release: the numbered directory','Actual native freeze is ed732c2. Numbered distribution changes move from next to 1.0.5. Existing apex/ remains separate. Native release also emitted an empty changes/main/stage.changelog.xml bookkeeping file; selected tree omits that empty file. Full actual rename list is tests/file-flow/release-renames.txt.');
code(s,'project release -version 1.0.5',64,150,1152,45,28);
text(s,'Before',64,225,530,40,30,teal,true);text(s,'After',670,225,545,40,30,teal,true);
code(s,'dist/releases/\n├── apex/\n└── next/\n    ├── release.changelog.xml\n    └── changes/\n        └── e3-initial/',64,285,540,240,23);
code(s,'dist/releases/\n├── apex/                   retained\n├── 1.0.5/\n│   ├── release.changelog.xml\n│   └── changes/e3-initial/\n└── next/\n    └── release.changelog.xml',670,285,545,260,23);
text(s,'Selected paths shown; other files are omitted.',64,550,1152,30,21,muted);
checkpoint(s,'The SQL files move unchanged. next is ready for the next milestone. Review and commit before tagging.');after(16,s);
s=slide('project release: changed version and changelog','Selected exact native metadata before/after: tests/file-flow/project-version-before.json and project-version-after.json. Full main changelog before/after is retained in tests/file-flow. SQLcl JSON formatting can also change; do not equate every diff line with changed semantics.');
text(s,'.dbtools/project.config.json',64,155,1152,40,29,teal,true);
code(s,'Before: "lastReleaseVersion": ""\nAfter:  "lastReleaseVersion": "1.0.5"',64,215,1152,85,27);
text(s,'dist/releases/main.changelog.xml includes',64,340,1152,40,29,teal,true);
code(s,'Before: next/release.changelog.xml\n        apex/apex.changelog.xml\n\nAfter:  1.0.5/release.changelog.xml\n        apex/apex.changelog.xml\n        next/release.changelog.xml   now empty',64,397,1152,180,25);
checkpoint(s,'Show git diff and rename summary. Commit the native metadata and distribution, then publish the Git tag.');after(16,s);
s=slide('project gen-artifact: committed dist becomes a ZIP','The actual archive e3-1.0.5.zip contains 37 files, all byte-for-byte identical to committed dist at ed732c2. ZIP paths omit the dist prefix. artifact/ is Git-ignored, so git status alone is not an existence check. Member list and checksums are retained under tests/file-flow.');
code(s,'project gen-artifact -name e3 -version 1.0.5 -format zip',64,150,1152,45,26);
text(s,'Selected committed files',64,225,540,40,30,teal,true);text(s,'ZIP members (selected)',670,225,545,40,29,teal,true);
code(s,'dist/\n├── install.sql\n└── releases/\n    ├── main.changelog.xml\n    ├── 1.0.5/\n    └── apex/',64,285,540,250,24);
code(s,'install.sql\nreleases/\n├── main.changelog.xml\n├── 1.0.5/\n└── apex/',670,285,545,225,24);
text(s,'37 files match committed dist. No src, Git history, credentials or target properties in the ZIP.',64,540,1152,45,25);
checkpoint(s,'Show unzip -l and the archive hash. Packaging has not changed Integration.');after(18,s);
s=slide('project deploy: installer, includes and target mapping','Exact native installer and XML wrappers are inspected in baseline.bundle. install.sql invokes lb update with releases/main.changelog.xml and -defaults-file &DEFAULTS_FILE. Main includes numbered DB release, separate APEX distribution and empty next. APEX XML invokes APEX_APPLICATION_INSTALL to map source810003 to target810203; it imports f810003.sql. No text replacement of export.');
code(s,'project deploy -file artifact/e3-1.0.5.zip',64,150,1152,45,27);
text(s,'Native execution chain',64,225,545,40,29,teal,true);
code(s,'install.sql\n  releases/main.changelog.xml\n    1.0.5/release.changelog.xml\n      stage.changelog.xml\n        included SQL scripts\n    apex/apex.changelog.xml\n      f810003.xml\n        f810003.sql',64,285,550,275,23);
text(s,'Private target properties',670,225,545,40,29,teal,true);
code(s,'Source app: 810003\nTarget workspace: E3_TARGET\nTarget schema: E3_TARGET\nTarget app: 810203\nTarget alias: E3-LAB',670,285,545,240,23);
checkpoint(s,'Follow the XML include to its SQL file. Target mappings are deployment inputs outside the ZIP.');after(18,s);
s=slide('project deploy: visible target results','Actual 2026-11-05 supported-target qualification logs: tests/release-correction/supported-upgrade.log and supported-repeat.log. Counts are observed for that archive/target, not universal later-release expectations. Private before/after retained fields compared equal; readiness and native APEX session checks passed. No new target deployment in documentation work.');
text(s,'Observed upgrade',64,170,540,40,30,teal,true);text(s,'Observed repeat',670,170,545,40,30,teal,true);
code(s,'Run:              1\nPreviously run:  22\nTotal:           23',64,235,540,150,28);
code(s,'Run:              0\nPreviously run:  23\nTotal:           23',670,235,545,150,28);
text(s,'Liquibase records target execution history. Repeating this archive required no new changesets.\nNative APEX sessions passed; retained history/configuration compared equal.\nGit source and the ZIP remain unchanged by installation.',64,425,1152,150,27);
checkpoint(s,'Show the target heading/history and receipt. Counts alone do not prove business correctness.');after(18,s);
const ordered=[],mapping={};old.forEach((sl,i)=>{ordered.push(sl);mapping[i+1]=ordered.length;ordered.push(...(add.get(i+1)||[]));});ordered.forEach((sl,i)=>sl.moveTo(i));
// Renumber footers and old evidence slide references.
for(const [i,sl]of ordered.entries()){
 const foot=sl.shapes.items.find(sh=>Math.abs(sh.position.left-1170)<1&&Math.abs(sh.position.top-675)<1);if(foot)foot.text=String(i+1).padStart(2,'0');else text(sl,String(i+1).padStart(2,'0'),1170,675,45,22,16,muted);
 for(const sh of sl.shapes.items){const v=sh.text?.toString()||'';if(v.includes('Authoring evidence:'))sh.text='Oracle paper v3.2 · Authoring evidence: E.3 slides '+mapping[11]+'–'+mapping[15];if(v.includes('Pipeline evidence:'))sh.text='Oracle paper v3.2 · Pipeline evidence: E.3 slides '+mapping[16]+'–'+mapping[19];}
}
old[1].speakerNotes.text+=' Native authoring section now includes concrete export/stage/verify file-effect slides; release preparation shows numbered directory/metadata before-after; deployment section shows archive contents and actual target outcomes. See updated walkthrough slide map.';
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
const output=path.join(build,'output','file-effects.pptx');await fs.mkdir(path.dirname(output),{recursive:true});
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:output,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,fontPolicy:{basis:'design',families:['Arial','Courier']},receiptPath:path.join(build,'validation.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(output));let map=[];
for(const [i,sl]of final.slides.items.entries()){const png=await final.export({slide:sl,format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));map.push({slide:i+1,title:sl.shapes.items.find(sh=>Math.abs(sh.position.top-40)<1)?.text?.toString()||sl.shapes.items[0]?.text?.toString()});}
await fs.writeFile(path.join(build,'map.json'),JSON.stringify({mapping,slides:map},null,2));await fs.copyFile(output,path.join(root,'progress/E.3/sprint_E.3_increment_demo.pptx'));await fs.writeFile(path.join(root,'.local-apex/e3/presentation-build/file-effects-latest.json'),JSON.stringify({build,output,mapping,slides:map}));console.log(JSON.stringify({build,slides:map.length}));
