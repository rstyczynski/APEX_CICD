import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';

const root=execFileSync('git',['rev-parse','--show-toplevel'],{encoding:'utf8'}).trim();
const build=path.join(root,'.local-apex/handover-build');
const skill=process.env.PRESENTATION_SKILL_DIR;
const python=process.env.PRESENTATION_RUNTIME_PYTHON;
if(!skill||!python) throw new Error('Set PRESENTATION_SKILL_DIR and PRESENTATION_RUNTIME_PYTHON from load_workspace_dependencies.');
const model=JSON.parse(await fs.readFile(path.join(root,'progress/E.1/presentation/model-source.json'),'utf8'));
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={ink:'#172F3B',muted:'#52636B',accent:'#BC4B35',teal:'#235F63',light:'#F2F5F5',white:'#FFFFFF',red:'#A43224',line:'#AAB9BE'};
const slideMap=[];
function text(s,str,x,y,w,h,size=28,color=C.ink,bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=str;sh.text.style={fontSize:size,typeface:'Arial',color,bold,autoFit:'none',verticalAlignment:'top',insets:0};return sh;
}
function slide(title,sources=[],dark=false){
 const s=P.slides.add();s.background.fill=dark?C.ink:C.white;
 text(s,title,60,45,1160,100,46,dark?C.white:C.ink,true);
 text(s,String(P.slides.items.length).padStart(2,'0'),1180,677,45,25,18,dark?'#C8D7DC':C.muted);
 s.speakerNotes.text=`Sources: ${sources.join('; ')}\nE.1 handover snapshot, 18 October 2026. PLAN: Progress; PROGRESS_BOARD: under_construction. No sprint closure or full quality-gate acceptance is implied.`;
 slideMap.push({number:P.slides.items.length,title,sources});return s;
}
function note(s,n){s.speakerNotes.text=s.speakerNotes.text+'\n'+n;}
function body(s,lines,x=65,y=180,w=1135,size=29,gap=84){lines.forEach((v,i)=>text(s,v,x,y+i*gap,w,gap-12,size));}
function command(s,str,y=550,size=25,x=65,w=1140){return text(s,str,x,y,w,80,size,C.teal,true);}
function label(s,str,x,y,w=1110,color=C.muted,size=23){return text(s,str,x,y,w,62,size,color);}
function box(s,str,x,y,w,h,size=26,fill=C.light){
 const sh=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:C.line,width:1.5}});
 sh.text=str;sh.text.style={fontSize:size,typeface:'Arial',color:C.ink,alignment:'center',verticalAlignment:'middle',insets:12,autoFit:'none'};return sh;
}
function link(s,a,b,from='right',to='left'){s.shapes.connect(a,b,{fromSide:from,toSide:to,kind:'elbow',line:{fill:C.teal,width:2.5},tail:{type:'triangle',width:'med',length:'med'}});}
function diagramNote(s,page,ids){
 const cells=model.pages[page].filter(c=>ids.includes(c.id));
 note(s,`Editable presentation adaptation of model.drawio page '${page}', cells ${ids.join(', ')}. Source SHA256 ${model.sha256}. Full cell labels: ${cells.map(c=>`${c.id}: ${c.value}`).join('\n')}`);
}

let s=slide('From Git to APEX', ['README.md','progress/E.1/cicd-walkthrough.md'],true);
text(s,'Traceable releases. Safe upgrades.\nProtected deployments.',65,210,1100,140,44,C.white,true);
text(s,'One application. A repeatable delivery path.\nEvidence at every gate.',65,400,1090,110,32,'#DCE7EB');
text(s,'Oracle APEX CI/CD Laboratory · 18 October 2026',65,590,1050,50,24,'#DCE7EB');

s=slide('Review agenda',['progress/E.1/cicd-walkthrough.md']);
body(s,['1. The application, source and delivery roles','2. A–F: assembly, release and compatible patch','3. G–I: incompatibility, drift and forward repair','4. Evidence, remaining risks and next decision'],65,175,1140,31,104);

s=slide('The selected prototype',['progress/E.1/sprint_E.1_design.md','config/areas.json']);
body(s,['One APEX application per area on one Oracle host','Foundation, Hello and World share one Git repository','Private A/B/C areas, disposable integration_test, retained UAT','Supported Oracle interfaces and small operator scripts'],65,175,1140,29,90);
label(s,'Bounded repair is proved; concurrency and complete fencing remain open',65,565,1130,C.red,26);

s=slide('The delivery path',['progress/E.1/model.drawio','progress/E.1/repo_layout.md']);
const lanes=[
 ['Development','Private A / B / C\nAuthor and capture\nSmoke-check C'],
 ['Shared Git','Reviewed source\nCandidate evidence\nOne release archive'],
 ['Integration test','Install that archive\nVerify the application\nRecord successful receipt'],
 ['User acceptance test','Promote same archive\nPreserve history/settings\nLAB_USER uses release']
];
const nodes=lanes.map(([t,b],i)=>{text(s,t,65+i*300,180,255,65,29,C.teal,true);return box(s,b,65+i*300,275,250,230,25);});
for(let i=0;i<3;i++) link(s,nodes[i],nodes[i+1]);
label(s,'The development team releases the package. The Deployer moves the same bytes through both targets.',65,565,1140,C.ink,26);
diagramNote(s,'lifecycle',['dev','git','q','t','packager','build','qarchive','same']);

s=slide('Foundation, Hello and World',['progress/E.1/model.drawio','docs/architecture.md']);
const f=box(s,'Foundation\nComposition, history and runtime state',390,175,500,115,27);
const h=box(s,'Hello\nEntries and configuration',170,390,400,110,27);
const w=box(s,'World\nEntries and configuration',710,390,400,110,27);
link(s,h,f,'top','bottom');link(s,w,f,'top','bottom');
label(s,'Both components depend on Foundation. The release installs the complete application.',100,560,1080,C.ink,27);
diagramNote(s,'lifecycle',['f','h','w','hf','wf']);

s=slide('Oracle toolchain and responsibilities',['docs/architecture.md','progress/E.1/cicd-walkthrough.md']);
body(s,[
 'APEX / ORDS: authoring, application metadata and HTTP runtime',
 'SQLcl + Java: saved connections, SQL checks and native capture/import',
 'SQLcl Liquibase: ordered migrations and applied-change checksums',
 'E1_CTRL SQL packages: reservations, deployment epochs and receipts',
 'Git + SHA-256: accepted source and immutable release identity',
 'Bash / Python: explicit operator steps and focused lab checks'
],65,165,1140,27,78);

s=slide('APEX interfaces: export, import and fingerprint',['deploy/operator/capture.sql','deploy/operator/import.sql','docs/architecture.md','scripts/cicd-drift-diff.py']);
body(s,[
 'Author: App Builder saves application definitions in a developer area',
 'Capture: SQLcl apex export writes split SQL files for Git review',
 'Deploy: APEX_APPLICATION_INSTALL maps the target; install.sql imports',
 'Guard: APEX_EXPORT.GET_APPLICATION computes the live fingerprint',
 'Database: separate Liquibase migrations change schema objects'
],65,165,1140,27,78);
label(s,'Git and immutable archives carry releases. APEX Working Copies and Team Development are not used for release integration or promotion.',65,575,1140,C.teal,25);
note(s,'Capture uses apex export -applicationid with -split -skipExportDate -expOriginalIds -expSupportingObjects N and a staging -dir. Import sets workspace, application ID, schema, alias and supported offset context before executing native exported install.sql. APEX_EXPORT.GET_APPLICATION with CHECKSUM-SH256 fingerprints live APEX metadata. ORDS serves runtime HTTP; it is not the release deployment API. APEX export is application metadata, not business data or a database schema migration. Working Copies remain a candidate break-glass option in the architecture; this prototype does not validate their compare/merge workflow. Team Development is not the CI/CD engine.');

s=slide('Git repository layout',['progress/E.1/repo_layout.md','release/manifest.json']);
text(s,'APEX_CICD/',65,160,1140,50,32,C.teal,true);
const directories=[
 ['apex/f810001/','Complete split APEX application export'],
 ['db/changes/','Ordered database migrations'],
 ['release/','Versions, dependencies and release proposals'],
 ['deploy/','Target guards, import and publication SQL'],
 ['config/areas.json','Workspace, schema and application mappings'],
 ['scripts/ + tests/','Operator steps and executable checks']
];
directories.forEach(([dir,description],i)=>{text(s,dir,65,225+i*57,310,45,27,C.ink,true);text(s,description,400,225+i*57,800,45,27);});
label(s,'Real Git history; one shared application source tree. Private A/B/C schema/workspace areas are separate from Git. Credentials and runtime history stay outside source control.',65,600,1140,C.teal,24);
note(s,'The repository is the current APEX_CICD checkout. The sprint guide progress/E.1/repo_layout.md is the detailed draft reference. A–C replay existing reviewed Git revisions; there are no separate component repositories or per-environment canonical export trees.');

s=slide('Developer cooperation: proposed branch workflow',['progress/E.1/repo_layout.md','docs/architecture.md']);
body(s,[
 '1. Reserve scope; start a task branch from the accepted Git base',
 '2. Author in a private APEX area; export owned changes to that branch',
 '3. Review pages, shared files, migrations and dependency metadata',
 '4. Validate the combined candidate in a disposable area',
 '5. Accept the source; package one immutable release archive'
],65,170,1140,28,77);
label(s,'Future validation: concurrent Hello/World branches and competing Hello tasks. Today A–C replay reviewed sequential snapshots; live PR/parallel integration is not demonstrated.',65,590,1140,C.red,24);

s=slide('APEX SQL exports can be merged as text',['progress/E.1/repo_layout.md','https://docs.oracle.com/en/database/oracle/apex/24.2/aeadm/exporting-one-or-more-applications.html']);
body(s,[
 'Split SQL exports belong in Git as text, not as binary application blobs',
 'Different page files usually reduce conflicts; shared definitions still overlap',
 'Review install.sql, IDs, shared components and cross-page dependencies',
 'Resolve conflicts with an APEX-aware reviewer; do not blindly pick a side',
 'Import the complete merged tree and test it before accepting the release'
],65,170,1140,27,77);
label(s,'A clean Git merge proves only that text combined. It does not prove a valid APEX application. Database migrations need their own order and compatibility review.',65,590,1140,C.teal,25);
note(s,'Oracle APEX 24.2 Administration Guide, section 3.12.11.1.6.4, recommends split exports for granular source-control review and notes install.sql/create_application.sql change when a page is added. Git merging is a text operation, not an APEX semantic merge. Stable capture options (-skipExportDate/-expOriginalIds) reduce noise but do not guarantee portable identity or semantic safety. Actual parallel capture/merge proof remains unfinished. Binary assets may be managed separately; this slide refers to the generated SQL source.');

s=slide('Future CI pipelines',['progress/E.1/repo_layout.md','progress/E.1/sprint_E.1_assessment.md']);
const steps=[
 ['Task / pull request','Capture + review\nScope and dependencies\nCandidate validation'],
 ['Accepted Git revision','Build once\nHash the archive\nRetain provenance'],
 ['Integration test','Fresh + upgrade checks\nRuntime verification\nSuccessful receipt'],
 ['UAT promotion','Same archive bytes\nPreflight guards\nPreserve user history']
];
const pipeline=steps.map(([t,b],i)=>{text(s,t,65+i*300,180,265,65,28,C.teal,true);return box(s,b,65+i*300,275,250,230,25);});
for(let i=0;i<3;i++)link(s,pipeline[i],pipeline[i+1]);
label(s,'Extension proposal: a CI runner, protected branches and release approvals call these gates. Remote CI/PR automation and concurrent integration remain future work.',65,575,1140,C.red,25);
note(s,'No CI provider, repository server or production target is selected. Existing local scripts establish the delivery path; this slide proposes automation around it rather than claiming hosted CI exists. Candidate checks run against the candidate/base; accepted-source packaging and integration testing precede same-artifact UAT promotion.');

s=slide('Walkthrough',['progress/E.1/cicd-walkthrough.md'],true);
text(s,'The Product Owner sees\nresults after each operation',65,240,1110,160,48,C.white,true);
text(s,'The following slides follow the implemented A–I journey',65,490,1130,75,29,'#DCE7EB');

s=slide('Infrastructure and project setup',['docs/deploy.md','progress/E.1/cicd-walkthrough.md']);
text(s,'Fresh replay only: destruction removes every lab database row',65,160,1120,62,27,C.red,true);
command(s,'python3 scripts/cicd-release-inputs.py',225);
command(s,'bash scripts/cicd-walkthrough-prerequisites.sh',280);
command(s,'bash scripts/cicd-walkthrough-host.sh',335);
command(s,'bash scripts/apex-destroy.sh',390);
command(s,'bash scripts/cicd-walkthrough-apex-init.sh',445);
body(s,['Then initialize E1_CTRL and provision each named area separately.','Expected result: vanilla DB/APEX/ORDS first, then empty isolated project areas.'],65,535,1140,25,63);
note(s,'Full commands, credentials, separate area provisioning and developer login setup are in companion Markdown stage 2. Infrastructure initialization cannot create project schemas. An independent clean-checkout A–I rehearsal passes at 54c0fd3 using a new empty engine, fresh credentials, reconstructed archives and explicit runtime API fixtures. Browser acceptance is separate.');

s=slide('A–C: assemble the application',['progress/E.1/cicd-walkthrough.md','progress/E.1/model.drawio']);
command(s,'bash scripts/cicd-walkthrough-A_foundation.sh',170);
command(s,'bash scripts/cicd-walkthrough-B_hello.sh',235);
command(s,'bash scripts/cicd-walkthrough-C_world.sh',300);
const aa=box(s,'A\nFoundation only\n810001',65,405,335,140,26);
const bb=box(s,'B\nFoundation + Hello\n810002',470,405,335,140,26);
const cc=box(s,'C\nComplete 1.0.0\n810003',875,405,335,140,26);
link(s,aa,bb);link(s,bb,cc);
label(s,'A and B remain unavailable. VERIFIER checks C, then LAB_USER can use it.',65,580,1140,C.ink,26);
diagramNote(s,'lifecycle',['devnote','a','b','c','f','h','w','devcheck']);
note(s,'This walkthrough replays reviewed sequential source checkpoints. Real concurrent Hello/World development is not proved by A–C. C uses independent Hello/World selectors; configure defaults when using the default greeting path.');

s=slide('D: install in integration_test',['progress/E.1/model.drawio','scripts/cicd-walkthrough-D_integration_test.sh']);
command(s,'bash scripts/cicd-walkthrough-D_integration_test.sh',155);
const dnodes=[
 box(s,'Inspect the archive\nHash, members and source',65,270,520,100,26),
 box(s,'Admit the target\nOwned attempt and epoch',685,270,520,100,26),
 box(s,'Apply migrations\nSQLcl Liquibase checks',65,435,520,100,26),
 box(s,'Import native APEX source\nApplication 810004 stays blocked',685,435,520,100,26)
];
link(s,dnodes[0],dnodes[1]);link(s,dnodes[1],dnodes[2],'bottom','top');link(s,dnodes[2],dnodes[3]);
label(s,'Source comes from the Git-built archive. No live export from C and no copied developer data.',65,590,1140,C.ink,25);
diagramNote(s,'D integration_test',['step2','step3','step4','step5','step6']);

s=slide('D: verify before publication',['progress/E.1/model.drawio','deploy/operator/publish_initial.sql']);
const verify=box(s,'Automated integrity\nand unit checks',65,190,335,105,27);
const browser=box(s,'VERIFIER browser check\nSave Hello World',470,190,335,105,27);
const publish=box(s,'Publish ready state\nFingerprint + receipt',875,190,335,105,27);
link(s,verify,browser);link(s,browser,publish);
command(s,'python3 scripts/cicd-password.py VERIFIER',370);
label(s,'Open http://127.0.0.1:8080/ords/f?p=810004:1',65,455,1140,C.teal,27);
body(s,['A missing required greeting repeats the verification prompt.','After publication, LAB_USER can use the complete application.'],65,535,1140,27,65);
diagramNote(s,'D integration_test',['step7','step8','step9','step10','step11','step12','step14']);

s=slide('E: promote the same initial archive',['scripts/cicd-walkthrough-E_promotion.sh','progress/E.1/tests/environment_rename_20261018.txt']);
command(s,'bash scripts/cicd-walkthrough-E_promotion.sh',165);
const q=box(s,'integration_test\nSuccessful 1.0.0 receipt',100,290,435,130,28);
const t=box(s,'user_acceptance_test\nSame archive hash',745,290,435,130,28);
link(s,q,t);
body(s,['UAT application 810005 becomes available to LAB_USER.','Capture the field-level history/configuration baseline for F.'],65,500,1140,28,80);
diagramNote(s,'lifecycle',['qarchive','same','retain']);
note(s,'Initial archive SHA256 d99fe83ec3d149739a12ec0cf2f01081ae027d1ec015e16d5a971ff3c602ab45. Source 08a5cf27e8a31ff7b77b6fd694f673847726eda1. E and F passed in the Product Owner walkthrough. The initial runtime is historical after F; do not downgrade UAT to replay it. A successful UAT deployment is not Product Owner acceptance of the full product.');

s=slide('F: Hello 1.0.1 with preserved history',['scripts/cicd-walkthrough-F_hello_patch.sh','release/manifest.json']);
command(s,'bash scripts/cicd-walkthrough-F_hello_patch.sh',155);
const table=s.tables.add({rows:4,columns:3,left:65,top:265,width:1140,height:255,values:[['Component','Before','After'],['Foundation','1.0.0','1.0.0'],['Hello','1.0.0','1.0.1'],['World','1.0.0','1.0.0']]});
for(let r=0;r<4;r++)for(let c=0;c<3;c++){let cell=table.getCell(r,c);cell.fill=r===0?C.ink:C.white;cell.text.style={fontSize:28,typeface:'Arial',color:r===0?C.white:C.ink,bold:r===0||r===2};}
table.borders.assign({fill:C.line,width:1,style:'solid'});
body(s,['Integration test checks fresh install and upgrade from 1.0.0.','The same patch archive upgrades UAT. All 21 baseline history rows and settings remain unchanged.'],65,550,1140,25,65);
note(s,'Current handover read-only comparison: PASS all fields of 21 prior history rows, old entries and complete configuration unchanged. New rows may append. Patch SHA256 4ba3abb8709f256c7a47e3e9294d3e7303f742145a95cb58d808ca6c6bcf7200, source ee8f1af8e35f81bb3b75051243df2ab9c6e4c0e5. Complete application archive contains the Hello-only version change and additive migration; Foundation and World versions remain unchanged.');

s=slide('G: reject a known incompatibility',['release/proposals/foundation-major.json','scripts/cicd-compatibility.py']);
command(s,'bash scripts/cicd-walkthrough-G_incompatible_upgrade.sh',155,24);
body(s,['Proposal: Foundation 2.0.0 with Hello 1.0.1 and World 1.0.0','Hello and World still declare Foundation 1.0.0 as required'],65,265,1140,29,85);
text(s,'REJECTED INCOMPATIBLE:\nHello requires Foundation 1.0.0; proposed Foundation 2.0.0',65,445,1140,105,29,C.red,true);
label(s,'Stops before maintenance, migration or import. Target and release records remain unchanged.',65,580,1140,C.ink,26);
note(s,'Dependency rules live in release/manifest.json and the breaking proposal. Controller executes the archived checker before its deployment connection. Explicit exact versions and supported triples are prototype policy, not SQL semantic inference. G passed in the Product Owner walkthrough.');

s=slide('H: one drift check, three situations',['scripts/cicd-protection-check.sh','progress/E.1/cicd-walkthrough.md']);
command(s,'bash scripts/cicd-protection-check.sh drift',160);
body(s,['1. Before an edit: NO DRIFT','2. After a real Page Designer save: DETECTED DRIFT','3. After the scripted fixture: DETECTED DRIFT'],65,280,1140,31,95);
label(s,'Restore the original definition between cases. The check never overwrites the edit.',65,590,1140,C.ink,27);
note(s,'The checker exits successfully after a recognized clean/protected outcome and unchanged snapshots. DETECTED DRIFT is a blocked deployment, not permission to deploy. Unexpected errors fail. Manual detection is observed in current E1_UAT. Synthetic fixture remains optional repeatable test setup.');

s=slide('H: inspect the changed source',['scripts/cicd-drift-diff.py','progress/E.1/tests/handover_live_drift_20261018.txt']);
command(s,'bash scripts/cicd-protection-check.sh drift --show',155);
text(s,'Published code',65,265,500,55,31,C.teal,true);
text(s,'Live edit',685,265,500,55,31,C.accent,true);
text(s,'Page title\nAPEX Delivery Laboratory\n\nRegion name\nAPEX Delivery Laboratory',65,350,500,230,28);
text(s,'Page title\nManual drift demonstration\n\nRegion name\nAPEX Delivery XX Laboratory',685,350,500,230,28);
label(s,'The command preserves both source trees and complete diffs. No restoration occurs.',65,610,1140,C.ink,25);
note(s,'Observed on 18 October 2026 in the current retained UAT. Source comparison validates exact successful archive/source/configuration receipt. review.diff omits import offset lines and generated Manifest comments only; raw.diff retains every exported difference. Other source/export differences remain in the report.');

s=slide('H: the Product Owner chooses restoration',['progress/E.1/cicd-walkthrough.md','docs/srs.md']);
body(s,['Undo: restore the published Title and region Name in Page Designer, then Save.','Keep: retain the export, capture/review it in Git and deliver a new release.','Deployment remains blocked while unexpected drift remains.'],65,175,1140,30,110);
command(s,'bash scripts/cicd-protection-check.sh drift',525);
label(s,'Restoration passes only when the check returns NO DRIFT against the original receipt.',65,605,1140,C.teal,25);
note(s,'Current manual restoration is pending the Product Owner decision. Do not report it complete. Synthetic H has its own saved-definition restoration and must not be interleaved with the manual edit. No automatic adoption or overwrite of unexpected edits.');

s=slide('Verification and recovery limits',['progress/E.1/sprint_E.1_tests.md','scripts/cicd-walkthrough-E_promotion.sh']);
body(s,['Missing VERIFIER greeting: publication stops, then the prompt allows correction.','Post-publication fixture failure: delivery stays successful and history stays saved.','A bounded continuation resumes the matching checkpoint without reinstalling.'],65,175,1140,29,110);
command(s,'bash scripts/cicd-walkthrough-E_promotion.sh --resume-examples',540,24);
label(s,'Checkpoint continuation is distinct from the additive-DDL repair shown next.',65,615,1140,C.red,24);
note(s,'Observed E failures were ORA-20619 missing runtime snapshot and ORA-20304 fixture relying on an unset World default. Fixes: checkpoint-bound verification resume/missing-data retry, and explicit active-entry selections with post-publication example continuation. No new application release or general recovery contract was implied.');

s=slide('I: repair a failed additive deployment',['scripts/cicd-walkthrough-I_repair.sh','progress/E.1/tests/recovery_proof_20261018.txt']);
const failed=box(s,'First DDL commits\nSecond step fails',65,185,330,120,29);
const inspect=box(s,'Inspect retained state\nApprove its exact hash',475,185,330,120,29);
const repaired=box(s,'Apply reviewed repair\nPublish ready state',885,185,330,120,29);
link(s,failed,inspect);link(s,inspect,repaired);
body(s,['Failure keeps ownership and blocks ordinary runtime access.','Repair preserves prior DDL, all history and configuration.','Repeated repair is a no-op; changed partial state is rejected.'],65,360,1140,27,72);
command(s,'bash scripts/cicd-walkthrough-I_repair.sh',605,25);
note(s,'Bounded integration_test experiment only. A deliberately failed Liquibase changeset follows one successful additive index. A separate source-bound repair archive retains the first successful changeset identity and adds forward completion. Observation hash approval and database recheck precede repair. No checksum clearing, rollback of business history or arbitrary recovery claim.');

s=slide('Evidence and remaining work',['PROGRESS_BOARD.md','progress/E.1/sprint_E.1_tests.md'],true);
text(s,'The selected journey works.\nThe broader architecture still needs proof.',65,240,1130,180,46,C.white,true);
text(s,'Prototype results and full sprint acceptance are separate decisions',65,515,1130,75,28,'#DCE7EB');

s=slide('Delivered evidence and official status',['PROGRESS_BOARD.md','progress/E.1/sprint_E.1_assessment.md']);
body(s,['PBI-011.1 and 011.3: tested on the board','PBI-011.2, 011.4, 011.6 and 011.7: under construction','PBI-011.5: under construction, with concurrent integration still unproved','PBI-011.8: bounded additive failure/repair proved; broader acceptance remains open'],65,170,1140,28,90);
label(s,'PBI-012–016 remain under_design. This handover proposes conclusions and follow-up, not status changes.',65,570,1140,C.red,25);

s=slide('The remaining Elaboration proofs',['progress/E.1/sprint_E.1_design.md','docs/test-profile.md']);
body(s,['Atomic contention: synchronized Hello competitors, exactly one winner','Parallel work: independent Hello/World contributions and safe integration','Maintenance: stale workers, in-flight sessions and verifier revocation','Recovery: broader schema drift and unsupported partial database states'],65,170,1140,28,108);
note(s,'Existing scope: PBI-011.2/.5/.7/.8, validation under PBI-012; original IT-6/7/8/9/12. These are registered child definitions, not newly scheduled sprints. Dedicated measurements and all full-suite gates remain incomplete.');

s=slide('Recommended next step',['progress/E.1/sprint_E.1_assessment.md','ROADMAP.md']);
body(s,['Retain the demonstrated delivery and protection slice as E.1 evidence.','Run one bounded Elaboration follow-up for concurrency, fencing and broader drift controls.','Reassess Lifecycle Architecture before committing to full Construction.'],65,185,1140,31,115);
label(s,'A follow-up sprint and revised scope require Product Owner selection. No new sprint is activated here.',65,600,1140,C.muted,24);

s=slide('Product Owner review decision',['progress/E.1/sprint_E.1_handover.md'],true);
body(s,['Does the handover explain and demonstrate the selected A–I outcomes?','Should the current manual edit be restored or retained for Git review?','Which remaining proofs should the next Elaboration increment prioritize?'],65,200,1140,31,115);
// Dark slide body contrast.
// Explicitly restyle body text on the dark ending.
for(const sh of s.shapes.items){if(sh.position.top>=190 && sh.position.top<650) sh.text.color=C.white;}
text(s,'E.1 remains open pending review and scope decisions',65,610,1130,60,29,'#DCE7EB',true);

await fs.mkdir(build,{recursive:true});
await fs.writeFile(path.join(build,'slide-map.json'),JSON.stringify(slideMap,null,2));
for(let i=0;i<P.slides.items.length;i++){
 const b=await P.export({slide:P.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));
}
const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(P)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=process.env.PRESENTATION_FINAL_PATH || path.join(root,'progress/E.1/sprint_E.1_increment_demo.pptx');
const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','18'],
 requiredNativeTableOwnerSlides:[18],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Arial']},
 verifyArtifactToolImport:true,receiptPath:process.env.PRESENTATION_RECEIPT_PATH || path.join(build,'presentation.validation.json')});
console.log(JSON.stringify({slides:slideMap.length,finalPath,result}));
