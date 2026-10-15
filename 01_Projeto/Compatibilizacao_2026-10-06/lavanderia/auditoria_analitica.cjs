// Auditoria documental independente. Centimetros, exceto volume em litros.
// Nao confirma medidas, carga, ergonomia ou instalacao.
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const r=x=>+x.toFixed(5), sin=Math.sin(55*Math.PI/180),cos=Math.cos(55*Math.PI/180);
const maxCesto=12+Math.hypot(25,45);
const frente=56+7*cos+55.1*sin;
const frenteAlta=56+7*cos+77.7*sin;
const piso=12-7*sin+3*cos;
const result={data:'2026-10-06',natureza:'Contas com premissas dos estudos locais; nao liberacao',
 cesto:{picoZ:r(maxCesto),anguloPico:r(Math.atan2(25,45)*180/Math.PI),folgaPainel:r(67.5-maxCesto),saldoAlemReserva3:r(67.5-maxCesto-3),frenteMaxY:r(frente),frenteAltaMaxY:r(frenteAlta),economia:r(frenteAlta-frente),pisoMin:r(piso)},
 saco:{volumeEnvelopeExternoL:40*20*40/1000,aroInterno:[42,22],corpo:[40,20],crescimentoPorLado:[0,.5,1].map(delta=>({delta,folgaPorLado:r(1-delta)})),limiteTranslacaoVertical:r(1/sin)},
 tanque:{volumeRetangularAteBordaL:38*35*20/1000,cenariosBordaLivre:[0,2,5].map(borda=>({borda,volumeGeometricoL:r(38*35*(20-borda)/1000)}))},
 ambiente:{volumeIsoladoM3:r(1.29*1.54*2.47),deficitAte6M3:r(6-1.29*1.54*2.47)},
 chapa:[50,100,150,200,250].map(a=>({distancia:a,queda:r(247-(160+(232-160)*a/(a+110)))})),
 banquinho:{faixaAposFrente:r(123-frente),deficitReserva45:r(45-(123-frente)),deficitProduto39_5:r(39.5-(123-frente)),folgaManobraSofa:r(205-(87+Math.hypot(45,70)))}};
assert.ok(Math.abs(result.cesto.frenteMaxY-105.15031)<.00001);
assert.ok(Math.abs(result.cesto.picoZ-63.47815)<.00001);
assert.ok(result.cesto.saldoAlemReserva3>1);
assert.equal(result.saco.volumeEnvelopeExternoL,32);
assert.ok(result.banquinho.deficitReserva45>27);
fs.writeFileSync(path.join(__dirname,'auditoria_analitica.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
