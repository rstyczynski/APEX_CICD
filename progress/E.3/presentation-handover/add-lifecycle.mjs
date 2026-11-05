import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const root=process.cwd(), skill=process.env.PRESENTATION_SKILL_DIR;
const build=path.join(root,'.local-apex/e3/presentation-build/lifecycle-v2');
await fs.mkdir(build,{recursive:true});
const input=path.join(root,'progress/E.3/sprint_E.3_increment_demo.pptx');
const deck=await PresentationFile.importPptx(await FileBlob.load(input));
if(deck.slides.items.length!==12) throw new Error('Expected original 12-slide deck; refuse duplicate append');
await fs.copyFile(input,path.join(build,'original.pptx'));
const originalTexts=deck.slides.items.map(s=>s.id);
const C={ink:'#14313E',teal:'#126B70',muted:'#52636D',red:'#9E3D2A'};
function text(s,value,x,y,w,h,size=26,color=C.ink,bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};
}
const paper='refs/apex-lifecycle-management-v3.pdf, Understanding the Oracle APEX Application Development Lifecycle, Version 3.2, June 2025. Page numbers are printed pages.';
function slide(title,rows,footer,notes){
 const s=deck.slides.add();s.background.fill='#FFFFFF';
 text(s,title,64,40,1152,105,42,C.ink,true);
 rows.forEach(([heading,body],i)=>{text(s,heading,64,160+i*112,1152,39,28,C.teal,true);text(s,body,92,203+i*112,1124,63,25);});
 text(s,footer,64,635,1152,36,21,C.muted);
 text(s,String(deck.slides.items.length).padStart(2,'0'),1170,675,45,22,16,C.muted);
 s.speakerNotes.text=paper+'\n'+notes;
 return s;
}
slide('Oracle lifecycle mapping: authoring',[
 ['Working Copies and Main checkpoints (pp. 12–14, 32)', 'E.3: edit a Working Copy, compare selected changes, merge into APEX Main.'],
 ['Git source and generated distribution (pp. 18–20, 26–27)', 'E.3: native PROJECT export and stage, review src/dist, then commit to Git.'],
 ['Peer review before Git integration (pp. 32–34)', 'E.3: manually opened PR, hosted checks and reviewed squash merge.'],
 ['Collaboration model: bounded adaptation (pp. 32–34)', 'Shared-Main capture plus Git review. Private branch instances and\nparallel feature isolation remain outside this demonstration.']
 ],'Oracle paper v3.2 · Authoring evidence: E.3 slides 5–8',
 'Oracle p.32 Figure 29 describes Working Copy/Main team checkpoints. Pp.32–34 describe feature-centric private work areas, updates and formal review. E.3 combines the shared-Main capture path with a Git PR, and does not demonstrate the full feature-centric topology. APEX Main is the live author application; Git main is accepted repository source. Evidence: progress/E.3/sprint_E.3_native_correction.md; tests/working-copy-merge.json; tests/working-copy-inspection.png; examples/git-pipeline/sql/capture.sql; sprint_E.3_increment_demo.md sections C–E. Existing retained observations only.');
slide('Oracle lifecycle mapping: automation',[
 ['Automation platform (pp. 40–41)', 'Oracle allows GitHub Actions. E.3 workflows sequence native SQLcl\noperations on the local runner using GitHub configuration and secrets.'],
 ['Release preparation and artifact (pp. 26–27, 41–43)', 'Release Please prepares version/changelog and a tag. Manual release\nverifies and packages the selected Git source with SQLcl PROJECT.'],
 ['Validation before deployment (pp. 42–44)', 'E.3 requires zero native verification errors, then deploys the archive.\nA separate qualification run demonstrates missing-changeset rejection.'],
 ['Deployment timing and evidence (pp. 40, 43–44)', 'E.3 uses explicit tag selection and workflow_dispatch. Retained runs bind\nsource, archive hash and target, followed by browser/preservation checks.']
 ],'Oracle paper v3.2 · Pipeline evidence: E.3 slides 9–11',
 'P.40 explicitly names GitHub Actions as an alternative to Jenkins and permits on-demand jobs. Pp.41–44 illustrate release/artifact creation, testing, gated deployment, archived results and cleanup. E.3 adapts the timing: PR/version preparation cannot deploy; the deployer dispatches a selected tag. Release Please and Conventional Commit classification are project choices, not Oracle requirements. Sources: examples/git-pipeline/.github/workflows/{pr,version,release,qualification}.yml; examples/git-pipeline/.github/actions/setup-native/action.yml; examples/git-pipeline/sql/; progress/E.3/sprint_E.3_github_configuration.md; tests/github-environment-journey.json. Seed v1.0.4 deployment 41679427616 and qualification 41679432928 are retained reference evidence, not new runs.');
slide('Oracle lifecycle mapping: scope and gaps',[
 ['Demonstrated E.3 slice', 'Native APEX authoring, Git capture/review and deliberate native deployment\nmap to the lifecycle building blocks. Evidence covers one serial lab journey.'],
 ['Project choices and version differences', 'Release Please, manual promotion and checksum-pinned SQLcl 25.4.1\nadapt the examples. The paper validates APEX 24.2 / SQLcl 25.1.1 (p. 2).'],
 ['Oracle guidance still beyond this proof (pp. 22–25, 30–34, 45)', 'utPLSQL: PBI-040. UI checks: PBI-034. Audits: PBI-041.\nPrivate branch environments: PBI-056. Mini-app reuse: PBI-044.'],
 ['Accepted mapping and tracked gaps', 'Mapping accepted on 5 November 2026. Remaining capabilities stay in\nbacklog. Deployed APEX release identity is tracked by PBI-057.']
 ],'Oracle paper v3.2 · LC-1 specification: sprint_E.3_pipeline_scope.md',
 'Sources: paper p.2 example versions; pp.22–25 testing, pp.30–31 audits, pp.32–34 collaboration and p.45 recommendations; pp.7,15–16 optional mini-app modularity. E.3 uses SQLcl 25.4.1.022.0618 / Java 21 per sprint_E.3_github_configuration.md. Pinning is project NFR-5 policy rather than following the paper example download-latest helper. Known boundaries: APEX display version remains 1.0.0 while repository release is v1.0.4; native availability restrictions do not prove atomic fencing or DDL recovery; prepared-host credential exception remains explicit. Public seed topology adapts the paper recommendation for a private team repository. Sources: sprint_E.3_handover.md, sprint_E.3_tests.md, sprint_E.3_assessment.md, sprint_E.3_pipeline_scope.md#lc-1--oracle-apex-lifecycle-alignment-validation. The Product Owner accepted LC-1 on 2026-11-05 and directed backlog follow-up. No separate acceptance/report gate remains. This does not claim production qualification.');
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(build,'output','lifecycle-v2.pptx');await fs.mkdir(path.dirname(finalPath),{recursive:true});
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:process.env.PRESENTATION_RUNTIME_PYTHON,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:15,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(const [i,s] of final.slides.items.entries()){
 const png=await final.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
console.log(JSON.stringify({finalPath,slides:final.slides.items.length,originalSlides:originalTexts.length}));
