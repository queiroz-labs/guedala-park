const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const models = [
 {id:'Ou_PFL200', ml:725, l:17, w:12, h:7.5, g:550, url:'https://www.ou.com.br/products/pote-de-vidro-hermetico-ou-725ml-linha-fresh-lock'},
 {id:'Luminarc_V5495', ml:820, l:17.9, w:13.5, h:6.7, g:550, url:'https://www.latabledarc.com/products/boite-de-conservation-rectangulaire-82-cl-pure-box-active'},
 {id:'Luminarc_P0740', ml:820, l:17.9, w:13.3, h:6.2, g:530, url:'https://www.latabledarc.com/products/boite-de-conservation-rectangulaire-82-cl-keepn-box'},
 {id:'Invicta_101528291770', ml:1000, l:20.4, w:15.3, h:6.9, g:732, url:'https://www.invictaonline.com.br/kit-com-6-potes-de-vidro-hermetico-1000ml-retangular-invicta/p'},
 {id:'Ou_PFL300', ml:1200, l:19.5, w:14, h:9, g:788, url:'https://www.ou.com.br/products/pote-de-vidro-hermetico-ou-1-2l-linha-fresh-lock'}
];
const round = x => Math.round(x*1000)/1000;
const assumptions = {count:6, content_mass_g_each:[300,500,700], illustrative_headspace_fraction:0.2, horizontal_gap_cm:1, interlayer_protection_cm:0.2, base_protection_cm:0.2, top_clearance_cm:0.5, hand_clearance_cm:3, no_nesting_credit:true, tray_available_area_cm2:26.2*18+19.2*12, old_bank_unit_height_limit_cm:8.5, empty_R1_cm:[12.8,22.3,22.8], R1_with_mixer_additional_pots:0};
const results = models.map(m => ({...m,
 dimension_status:'Campos comerciais do produto com tampa incluída; desenho do envelope fechado com travas não publicado. Não são cotas de embalagem.',
 mass_status:'Massa comercial nominal; repartição corpo/tampa e pesagem independente ausentes.',
 six_volume_L:round(6*m.ml/1000), six_empty_kg:round(6*m.g/1000),
 illustrative_volume_with_20pct_headspace_ml:round(m.ml*0.8),
 content_scenarios:assumptions.content_mass_g_each.map(c=>({content_g_each:c, unit_total_kg:round((m.g+c)/1000), six_total_kg:round(6*(m.g+c)/1000), volume_fit:'Não inferido: densidade e receita desconhecidas.'})),
 six_one_layer_2by3_cm:[round(2*m.l+1),round(3*m.w+2),m.h],
 three_columns_two_layers_cm:[round(3*m.w+2),m.l,round(2*m.h+0.2)],
 two_layers_total_clearance_cm:round(2*m.h+0.2+0.2+0.5+3),
 three_layers_total_clearance_cm:round(3*m.h+0.4+0.2+0.5+3),
 six_footprint_area_cm2:round(6*m.l*m.w),
 six_in_old_trays_area_lower_bound_pass:6*m.l*m.w <= assumptions.tray_available_area_cm2,
 one_pot_old_bank_height_pass:m.h <= assumptions.old_bank_unit_height_limit_cm,
 empty_R1_static_unit_footprint_pass:Math.min(m.l,m.w)<=12.8 && Math.max(m.l,m.w)<=22.3,
 empty_R1_three_layer_conservative_height_pass:3*m.h+0.4+0.2+0.5+3 <=22.8,
 stacking_status:'Alturas são soma de envelopes sem crédito de encaixe. Não demonstram estabilidade ou autorização do fabricante.'
}));
assert.equal(round(assumptions.tray_available_area_cm2),702);
assert(results.every(r=>r.six_in_old_trays_area_lower_bound_pass===false));
assert.equal(results.find(r=>r.id==='Ou_PFL300').one_pot_old_bank_height_pass,false);
assert.equal(results.find(r=>r.id==='Ou_PFL200').six_empty_kg,3.3);
assert.equal(results.find(r=>r.id==='Invicta_101528291770').six_empty_kg,4.392);
assert.equal(results.find(r=>r.id==='Ou_PFL300').content_scenarios[1].six_total_kg,7.728);
const out={date:'2026-10-06', units:{dimensions:'cm',mass:'g / kg',capacity:'mL / L'},status:'Estudo nominal não adotado, sem compra ou aprovação técnica.', assumptions, results, checks:'PASS: área disponível, rejeição das cinco referências nas bandejas antigas, altura de 1,2 L, massas e cenário de conteúdo.'};
fs.writeFileSync(path.join(__dirname,'Resultados_potes_refeicoes_individuais.json'),JSON.stringify(out,null,2)+'\n','utf8');
const csv=['id,consultado,capacidade_ml,comprimento_cm,largura_cm,altura_cm,massa_g,url',...models.map(m=>[m.id,'2026-10-06',m.ml,m.l,m.w,m.h,m.g,m.url].join(','))].join('\n')+'\n';
fs.writeFileSync(path.join(__dirname,'Fontes_potes_refeicoes_individuais.csv'),csv,'utf8');
console.log(out.checks);
