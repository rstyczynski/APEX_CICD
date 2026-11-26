'use strict';
const {check}=require('../checks.cjs');const fs=require('node:fs');
try {const input=Object.fromEntries(['changed', 'report', 'sql'].map(k=>[k,process.env['INPUT_'+k.toUpperCase()]]));check('review',input);fs.appendFileSync(process.env.GITHUB_OUTPUT,'validated=true\n');console.log('PASS review');}catch(e){console.error('Check rejected: '+e.message);process.exitCode=1;}
