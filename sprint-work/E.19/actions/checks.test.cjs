const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const crypto=require('node:crypto');
const {check}=require('./checks.cjs');
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'e19-check-'));
function write(name,text){const p=path.join(dir,name);fs.writeFileSync(p,text);return p;}
process.on('exit',()=>fs.rmSync(dir,{recursive:true,force:true}));
test('tool requires log and matching native metadata',()=>{
 const log=write('tool','SQLcl: Release 25.4.1.0 Production Build: 25.4.1.022.0618');
 const config=write('config',JSON.stringify({sqlcl:{version:'25.4.1.0'}}));
 assert.equal(check('tool',{log,config}),true);
 assert.throws(()=>check('tool',{log}));
 assert.throws(()=>check('tool',{log,config:write('badconfig','{}')}));
 assert.throws(()=>check('tool',{log:write('wrongtool','25.3'),config}));
});
test('output rejects error signatures and empty/missing files',()=>{
 assert.equal(check('output',{log:write('ok','Successful native operation')}),true);
 for(const text of ['','ORA-00942: missing','\x1b[31mPLS-00103','SP2-001','ERROR failure','Error starting at line','Unknown Command','Expected a subcommand','Errors: 2']) assert.throws(()=>check('output',{log:write('error',text)}));
 assert.throws(()=>check('output',{}));
});
test('provenance explicit checks reject substitutions and malformed evidence',()=>{
 const archive=write('artifact','qualified bytes');
 const source='a'.repeat(40),build='25.4.1.022.0618';
 const receipt=write('receipt',JSON.stringify({source,build,sha256:crypto.createHash('sha256').update('qualified bytes').digest('hex')}));
 const input={archive,receipt,source,build};
 assert.equal(check('provenance',input),true);
 for(const patch of [{source:'b'.repeat(40)},{source:''},{build:'wrong'},{archive:write('altered','changed')},{receipt:write('malformed','{')},{receipt:undefined}]) assert.throws(()=>check('provenance',{...input,...patch}));
});
