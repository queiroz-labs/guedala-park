'use strict';
const fs = require('fs');
const path = require('path');
const checks = [
 {formula:'(600 - 400) / 2',actual:(600-400)/2,expected:100,unit:'mm',scope:'nominal lateral reserve each side'},
 {formula:'100 + 300 + 50',actual:100+300+50,expected:450,unit:'mm',scope:'nominal countertop depth budget'},
 {formula:'600 / 2',actual:600/2,expected:300,unit:'mm',scope:'nominal common transverse axis'}
].map(x=>({...x,pass:Math.abs(x.actual-x.expected)<1e-9}));
if(checks.some(x=>!x.pass)) throw new Error('Nominal arithmetic failed');
fs.writeFileSync(path.join(__dirname,'Verificacao_arion_nominal.json'),JSON.stringify({date:'2026-10-06',limitations:'Arion base, outlet, handle and hole unknown. No installation or fabrication approval.',count:checks.length,checks},null,2));
process.stdout.write(`${checks.length} contas nominais passaram\n`);
