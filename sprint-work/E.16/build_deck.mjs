import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const {makeNativeBulletParagraphs}=await import(process.env.PRESENTATION_UTILS);
const p=Presentation.create({slideSize:{width:1280,height:720}});
const slides=[
['Native release provenance','Sprint E.16 · PBI-084\nReviewed source, qualified bytes and retained data'],
['Agenda','1. Scope and execution boundary\n2. Native installation, upgrade and repeat\n3. Rejections, evidence and remaining decisions'],
['Scope and architecture','Disposable Elaboration experiment\nSQLcl PROJECT 25.4.1.022.0618 · Java 21'],
['Execution boundary','GitHub workflow runs Python orchestration on Ubuntu.\nTwo independent Oracle services use AUTHOR16.\nSQLcl exports source and prepares native archives.\nThe guard binds source commit, build and archive digest.'],
['Native delivery journey','A fresh workflow creates source and target schemas.\nThe target starts empty; a seeded row follows installation.'],
['Prepare the first release','project export -schemas AUTHOR16\nproject stage -branch-name baseline\nproject verify -compared-branch-name baseline -verbose\nproject release -version 1.0.0\nproject gen-artifact -name native16 -version 1.0.0'],
['Install and seed','project deploy -file <verified native16-1.0.0.zip>\ninsert into preserved values\n  (1,\'retained across upgrade\');\ncommit;\n\nThe installed table begins with ID and MESSAGE.'],
['Upgrade and repeat','alter table preserved add (extra varchar2(80));\n\nExport, stage, verify and package release 1.1.0.\nDeploy verified 1.1.0, then deploy the identical archive.\nCheck ID=1 and the retained message after each step.'],
['Inspect the evidence','gh run view 45802390235 --repo rstyczynski/APEX_CICD_E.16\n\nReceipts bind Git source, workflow and archive SHA-256.\nThe Git bundle retains exported SQL and release history.\nOracle logs show retained rows and native deployment.'],
['Failures and refusal paths','Observed native failures and their repairs\nNegative cases must fail before deployment is invoked.'],
['Native schema and connection repairs','Cross-schema install failed with ORA-01031.\nSeparate databases with identical schema names fixed it.\nRepeated connection saving failed initialization.\nSave once, then connect by name; no version bypass.'],
['Reject changed inputs','The guard refuses changed digest, source identity or archive bytes.\nAn actual SQLcl 25.3 executable supplies the wrong build.\nCompare target observations before and after refusal.'],
['Verification and decisions','PBI-084: Done — verified bounded native provenance.\nNew gates: 1/1 smoke, 1/1 unit, 1/1 integration.\nFull regression: 15/15 smoke, 17/17 unit, 25/25 integration.\nPBI-085 (E.17) and PBI-086 (E.18): Planned.'],
['Q&A','E.16 closed in YOLO after verified gates and audit.\nNext planned: E.17 independent-host reproduction.\nProduction readiness remains outside this experiment.']];
for (let i=0;i<slides.length;i++) {const s=p.slides.add();s.background.fill='#102638';for(const [txt,y,h,size] of [[slides[i][0],48,100,42],[slides[i][1],185,465,[5,6,7,8].includes(i)?24:29],[String(i+1),670,28,18]]) {const sh=s.shapes.add({geometry:'textbox',position:{left:60,top:y,width:1160,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=(y===185 && [3,10,11,12].includes(i))?makeNativeBulletParagraphs(txt.split('\n'),{marginLeftPoints:18,hangingPoints:9,spaceAfterPoints:10}):txt;sh.text.style={fontSize:size,typeface:[5,6,7,8].includes(i)?'Courier New':'Arial',color:'#FFFFFF',autoFit:'none',insets:0};}s.speakerNotes.text='Sources: sprint-work/E.16/lifecycle.py; progress/E.16/sprint_E.16_checklist.md. Gate status is read from the current verification report.';const b=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`.local-apex/e16/deck/slide-${i+1}.png`,new Uint8Array(await b.arrayBuffer()));}
await (await PresentationFile.exportPptx(p)).save('progress/E.16/sprint_E.16_increment_demo.pptx');
