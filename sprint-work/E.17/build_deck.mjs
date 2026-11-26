import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const {makeNativeBulletParagraphs}=await import(process.env.PRESENTATION_UTILS);
const p=Presentation.create({slideSize:{width:1280,height:720}});
const run=process.env.E17_RUN_ID||'pending';
const slides=[
 ['Clean-host native delivery','Sprint E.17 · PBI-085\nReproduce the reviewed Oracle delivery journey'],
 ['Agenda','1. Scope and architecture\n2. Fresh host and native delivery\n3. Observed failures and recovery\n4. Verification and next decisions'],
 ['Scope and architecture','One independent hosted reproduction\nDeclared tools and new private inputs'],
 ['Native responsibilities','GitHub Actions: visible phase sequencing and outcomes\nOracle Database: author and independent target\nAPEX and ORDS: application access over native data\nSQLcl PROJECT: export, stage, verify, release and deploy\nGit: reviewed source and generated release history'],
 ['Fresh-host journey','Start from a new Ubuntu job\nGenerate private inputs in RUNNER_TEMP'],
 ['Provision the platform','Remove unused SDKs before Oracle consumes disk.\nStart digest-pinned full Oracle Database containers.\nVerify APEX archive checksum; install through apexins.sql.\nCreate workspace and a fresh application account.\nInstall ORDS using a PDB-local administrator.'],
 ['Prepare and install the native release','project init -name native16 -schemas AUTHOR16\nproject export -schemas AUTHOR16\nproject stage -branch-name baseline\nproject verify -compared-branch-name baseline -verbose\nproject release -version 1.0.0\nproject gen-artifact -name native16 -version 1.0.0\nproject deploy -file <verified 1.0.0 archive>'],
 ['Retain data through upgrade and repeat',"insert into preserved values\n  (1,'retained across upgrade');\ncommit;\nalter table preserved add (extra varchar2(80));\n\nPrepare 1.1.0 through the same native Actions steps.\nDeploy 1.1.0 and repeat the identical verified archive."],
 ['Inspect the application and cleanup','Log in through actual ORDS/APEX as fresh LAB_USER.\nThe fixture page reads the native preserved table.\nExpected: Row 1: retained across upgrade.\nRetain browser capture, SQL logs, receipts and Git bundle.\nRemove job-private connections and owned containers.\nFinal qualification remains pending.'],
 ['Reviewed candidate and protected merge','PR 1: trusted Review and real Oracle run 45819877026.\nBefore validation: ordinary protected merge refused.\nAfter exact-head success publication: ordinary merge passed.\nPR 2: changed bytes rejected as stale Review.\nCandidate SQL skipped; ordinary merge remained refused.'],
 ['Failures and recovery','Retain failed observations\nQualify repairs through real hosted execution'],
 ['Hosted disk and XML DB failures','Trial 45818534213 exhausted hosted runner disk.\nUnused SDK removal allowed the next trial to progress.\nTrial 45819313293 found XDB INVALID during apexins.\nA zero process exit concealed ORA-20001.\nFull Oracle image and explicit native-output checks repair\nthe observed prerequisite and error-detection gaps.'],
 ['PDB-local installation authority','Trial 45820349969 reached ORDS preparation.\nChanging common SYS from a PDB failed: ORA-65066.\nUse newly supplied PDB-local E17_ADMIN instead.\nPass fresh installer/runtime passwords through stdin.\nMatch container uid/gid to private configuration ownership.\nDo not reuse a prepared-host credential.'],
 ['Verification and next decisions','Acceptance against PBI-085\nClosure requires the complete verified result'],
 ['Current verification','Reviewed candidate journey: verified in E.17 repositories.\nDedicated reader contracts and source smoke: passing.\nNative platform and authenticated data path: pending.\nFull acceptance/regression gates: pending final source.\nDemo, final audit and recorded closure: pending.\nCapacity measurements remain E.18 scope.'],
 ['Q&A','Inspect the actual named Actions steps and retained data.\nPBI-085 remains under construction until all gates pass.']
];
await fs.mkdir('.local-apex/e17/deck',{recursive:true});
for(let i=0;i<slides.length;i++){
 const s=p.slides.add();s.background.fill='#102638';
 const code=[6,7].includes(i);const bullets=[3,5,8,9,11,12,14].includes(i);
 for(const [txt,y,h,size] of [[slides[i][0],48,100,42],[slides[i][1],185,465,code?24:28],[String(i+1),670,28,18]]){
  const sh=s.shapes.add({geometry:'textbox',position:{left:60,top:y,width:1160,height:h},fill:'none',line:{fill:'none',width:0}});
  sh.text=y===185&&bullets?makeNativeBulletParagraphs(txt.split('\n'),{marginLeftPoints:18,hangingPoints:9,spaceAfterPoints:10}):txt;
  sh.text.style={fontSize:size,typeface:y===185&&code?'Courier New':'Arial',color:'#FFFFFF',autoFit:'none',insets:0};
 }
 s.speakerNotes.text='Sources: progress/E.17/sprint_E.17_checklist.md; sprint_E.17_implementation.md; sprint_E.17_bugs.md; sprint-work/E.17/.github/workflows/native.yml. Native run: '+run+'. Source/SQL details belong in the complete walkthrough. Pending labels are intentional until actual qualification.';
 const b=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`.local-apex/e17/deck/slide-${i+1}.png`,new Uint8Array(await b.arrayBuffer()));
}
await(await PresentationFile.exportPptx(p)).save('.local-apex/e17/deck/candidate.pptx');
