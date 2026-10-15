'use strict';
const fs = require('fs');
const path = require('path');
const source = JSON.parse(fs.readFileSync(path.join(__dirname, 'Contas_conferidas.json'), 'utf8').replace(/^\uFEFF/, ''));
const formulas = {
 banheiro_frente_nominal: ['124 - 59', 124 - 59],
 banheiro_frente_com_tolerancia_positiva_louca: ['124 - (59 + 1)', 124 - 60],
 tampo: ['90 - 13.5', 90 - 13.5],
 varoes: ['2 * (97.3 + 33.2)', 2 * (97.3 + 33.2)],
 ganho_varoes_pct: ['100 * (261 - 186.4) / 186.4', 100 * (261 - 186.4) / 186.4],
 largura_armario: ['2 * 97.3 + 3 * 1.8', 2 * 97.3 + 3 * 1.8],
 passagem_protegida_queen160: ['295 - 61 - 160 - 20', 295 - 61 - 160 - 20],
 passagem_protegida_queen158: ['295 - 61 - 158 - 20', 295 - 61 - 158 - 20],
 aereo_antigo_cm3: ['7 * 36 * 36 * 31', 7 * 36 * 36 * 31],
 aereo_atual_cm3: ['5 * 36 * 51 * 31', 5 * 36 * 51 * 31],
 aereo_variacao_pct: ['100 * (284580 / 281232 - 1)', 100 * (284580 / 281232 - 1)],
 escritorio_porta_margem: ['220 - 75 - 142', 220 - 75 - 142],
 escritorio_arco: ['sqrt(78^2 + 3^2) - 75', Math.sqrt(78 ** 2 + 3 ** 2) - 75],
 escritorio_recuo_comparativo: ['sqrt(80^2 - 78^2)', Math.sqrt(80 ** 2 - 78 ** 2)],
 folha_raio: ['sqrt(15^2 + 37.5^2)', Math.sqrt(15 ** 2 + 37.5 ** 2)],
 folha_parede: ['55 - 10 - sqrt(15^2 + 37.5^2)', 55 - 10 - Math.sqrt(15 ** 2 + 37.5 ** 2)],
 coluna_limite_comparativo: ['2 * (10.7 - 3)', 2 * (10.7 - 3)]
};
const checks = Object.entries(formulas).map(([key, [formula, actual]]) => ({ key, formula, actual, reported: source[key], pass: Math.abs(actual - source[key]) < 1e-9 }));
if (checks.some(x => !x.pass)) throw new Error('Divergencia aritmetica');
fs.writeFileSync(path.join(__dirname, 'Verificacao_contas.json'), JSON.stringify({date:'2026-10-06', scope:'Arithmetic only; hypotheses are not measured geometry or installation approval.', count: checks.length, checks}, null, 2));
process.stdout.write(`${checks.length} conferencias aritmeticas passaram\n`);
