'use strict';
const {check}=require('../checks.cjs');const fs=require('node:fs');
try {const input=Object.fromEntries(['event'].map(k=>[k,process.env['INPUT_'+k.toUpperCase()]]));check('candidate',input);fs.appendFileSync(process.env.GITHUB_OUTPUT,'validated=true\n');console.log('PASS candidate');}catch(e){console.error('Check rejected: '+e.message);process.exitCode=1;}
