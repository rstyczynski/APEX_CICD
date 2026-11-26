import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const {makeNativeBulletParagraphs}=await import(process.env.PRESENTATION_UTILS);
const p=Presentation.create({slideSize:{width:1280,height:720}});
const run=process.env.E17_RUN_ID||'pending';
const slides=[
  [
    "Clean-host native delivery",
    "Sprint E.17 · PBI-085\nReproduce the reviewed Oracle delivery journey"
  ],
  [
    "Agenda",
    "1. Scope and architecture\n2. Fresh host and native delivery\n3. Observed failures and recovery\n4. Verification and next decisions"
  ],
  [
    "Scope and architecture",
    "One independent hosted reproduction\nDeclared tools and new private inputs"
  ],
  [
    "Native responsibilities",
    "GitHub Actions: visible phase sequencing and outcomes\nOracle Database: author and independent target\nAPEX and ORDS: application access over native data\nSQLcl PROJECT: export, stage, verify, release and deploy\nGit: reviewed source and generated release history"
  ],
  [
    "Fresh-host journey",
    "Start from a new Ubuntu job\nGenerate private inputs in RUNNER_TEMP"
  ],
  [
    "Provision the platform",
    "Remove unused SDKs before starting pinned databases.\nQualify AMD64 ORDS and private config access first.\nVerify APEX checksum; install with native apexins.sql.\nCreate workspace and a fresh application account.\nInstall native ORDS with freshly supplied SYS input."
  ],
  [
    "Prepare and install the native release",
    "project init -name native16 -schemas AUTHOR16\nproject export -schemas AUTHOR16\nproject stage -branch-name baseline\nproject verify -compared-branch-name baseline -verbose\nproject release -version 1.0.0\nproject gen-artifact -name native16 -version 1.0.0\nproject deploy -file $GITHUB_WORKSPACE/result/native16-1.0.0.zip"
  ],
  [
    "Retain data through upgrade and repeat",
    "-- target after 1.0.0 installation\ninsert into preserved values\n  (1,'retained across upgrade');\ncommit;\n-- author change for native 1.1.0 preparation\nalter table preserved add (extra varchar2(80));\n-- target: deploy verified 1.1.0, then identical archive"
  ],
  [
    "Inspect the application and cleanup",
    "Sign in through actual ORDS/APEX as fresh LAB_USER.\nThe fixture page reads the native preserved table.\nExpected: Row 1: retained across upgrade.\nInspect browser receipt, SQL logs and native Git bundle.\nRemove job-private connections and owned containers.\nFinal qualification remains pending."
  ],
  [
    "Reviewed candidate and protected merge",
    "PR 1: trusted Review and real Oracle run 45819877026.\nBefore validation: ordinary protected merge refused.\nAfter exact-head success publication: ordinary merge passed.\nPR 2: changed bytes rejected as stale Review.\nCandidate SQL skipped; ordinary merge remained refused."
  ],
  [
    "Failures and recovery",
    "Retain failed observations\nQualify repairs through real hosted execution"
  ],
  [
    "Hosted runner disk exhaustion",
    "Trial 45818534213 exhausted runner disk.\nThe worker could not retain normal logs or artifacts.\nIts authoritative check annotation preserves the error.\nRemove unused hosted SDK payloads before provisioning.\nLater hosts progressed beyond this failure.\nApply this cleanup only to disposable hosted jobs."
  ],
  [
    "APEX prerequisite and error detection",
    "Trial 45819313293 found XML DB INVALID.\nNative apexins reported ORA-20001 but exited zero.\nA successful process exit did not prove installation.\nUse the same Oracle release’s pinned full image.\nReject reported native errors as well as failed exits.\nLater trials completed actual native APEX installation."
  ],
  [
    "PDB-local installer authority",
    "Changing common SYS inside a PDB failed ORA-65066.\nThe attempted local DBA lacked ORDS grant authority.\nA later SQL*Plus input-line bug returned ORA-03405.\nSeparate CREATE USER and GRANT onto native input lines.\nUse native resetPassword, then install ORDS as SYS.\nPass fresh installer/runtime passwords through stdin."
  ],
  [
    "Executable architecture on a new host",
    "Trial 45824130390 rejected ARM64 ORDS on AMD64.\nNo ORDS installation occurred: exec format error.\nInspect and pin AMD64 ORDS of the same 25.3.0 release.\nQualify native version and private config before Oracle.\nThe early native CLI/configuration checks now pass.\nFull server/application qualification remains pending."
  ],
  [
    "Verification and next decisions",
    "Acceptance against PBI-085\nClosure requires the complete verified result"
  ],
  [
    "Current verification",
    "Reviewed candidate journey: verified in E.17 repositories.\nDedicated reader contracts and source smoke: passing.\nAPEX installation and early ORDS preflight: observed.\nComplete native delivery/application path: pending.\nFull acceptance/regression and final audit: pending."
  ],
  [
    "Assigned work and next decisions",
    "PBI-085: under construction in E.17.\nComplete platform, release, application and cleanup proof.\nFinish live demonstration and documentation audit.\nRecord closure only after every selected gate passes.\nPBI-086 remains planned in E.18 for capacity measurements.\nNo production readiness or PO satisfaction is inferred."
  ],
  [
    "Q&A",
    "Inspect the actual named Actions steps and retained data.\nPBI-085 remains under construction until all gates pass."
  ]
];
await fs.mkdir('.local-apex/e17/deck',{recursive:true});
for(let i=0;i<slides.length;i++){
 const s=p.slides.add();s.background.fill='#102638';
 const code=[6,7].includes(i);const bullets=[3,5,8,9,11,12,13,14,16,17].includes(i);
 for(const [txt,y,h,size] of [[slides[i][0],48,100,42],[slides[i][1],185,465,code?24:28],[String(i+1),670,28,18]]){
  const sh=s.shapes.add({geometry:'textbox',position:{left:60,top:y,width:1160,height:h},fill:'none',line:{fill:'none',width:0}});
  sh.text=y===185&&bullets?makeNativeBulletParagraphs(txt.split('\n'),{marginLeftPoints:18,hangingPoints:9,spaceAfterPoints:10}):txt;
  sh.text.style={fontSize:size,typeface:y===185&&code?'Courier New':'Arial',color:'#FFFFFF',autoFit:'none',insets:0};
 }
 s.speakerNotes.text='Sources: progress/E.17/sprint_E.17_checklist.md; sprint_E.17_implementation.md; sprint_E.17_bugs.md; sprint-work/E.17/.github/workflows/native.yml. Native run: '+run+'. Source/SQL details belong in the complete walkthrough. Pending labels are intentional until actual qualification.';
 const b=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`.local-apex/e17/deck/slide-${i+1}.png`,new Uint8Array(await b.arrayBuffer()));
}
await(await PresentationFile.exportPptx(p)).save('.local-apex/e17/deck/candidate.pptx');
