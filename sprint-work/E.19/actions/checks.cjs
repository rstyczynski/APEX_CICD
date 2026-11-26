'use strict';
const fs = require('node:fs');
const crypto = require('node:crypto');
const BUILD = '25.4.1.022.0618';
function file(path) {
  if (!path || !fs.lstatSync(path).isFile() || fs.lstatSync(path).isSymbolicLink()) throw Error('required regular file');
  return fs.readFileSync(path);
}
function required(value, name) {
  if (typeof value !== 'string' || !value.trim()) throw Error(`missing ${name}`);
  return value;
}
function check(kind, input) {
  if (kind === 'tool') {
    const text = file(input.log).toString();
    if (!text.includes(`Release 25.4.1.0 Production Build: ${BUILD}`)) throw Error('tool mismatch');
    const config = JSON.parse(file(input.config));
    if (config.sqlcl?.version !== '25.4.1.0') throw Error('metadata version mismatch');
  } else if (kind === 'output') {
    const text = file(input.log).toString().replace(/\x1b\[[0-9;]*m/g, '');
    if (!text.trim()) throw Error('empty native output');
    if (/Errors:\s*[1-9]|^\s*(?:ORA-|PLS-|SP2-|ERROR\b|Error starting|Unknown Command)|Expected a subcommand/im.test(text)) throw Error('native output contains errors');
  } else if (kind === 'provenance') {
    const receipt = JSON.parse(file(input.receipt));
    const source = required(input.source, 'source');
    if (!/^[a-f0-9]{40}$/.test(source) || receipt.source !== source) throw Error('source mismatch');
    if (receipt.build !== BUILD || input.build !== BUILD) throw Error('tool mismatch');
    const digest = crypto.createHash('sha256').update(file(input.archive)).digest('hex');
    if (receipt.sha256 !== digest) throw Error('artifact mismatch');
  } else throw Error('unknown check');
  return true;
}
module.exports = {check};
if (require.main === module) {
  try {
    const input = Object.fromEntries(['log','config','receipt','source','build','archive'].map(k => [k, process.env[`INPUT_${k.toUpperCase()}`]]));
    check(process.argv[2], input);
    if (process.env.GITHUB_OUTPUT) fs.appendFileSync(process.env.GITHUB_OUTPUT, 'validated=true\n');
    console.log('PASS support check');
  } catch (error) {
    console.error(`Support check rejected: ${error.message}`);
    process.exitCode = 1;
  }
}
