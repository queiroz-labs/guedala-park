const fs=require('node:fs'),p=require('node:path');
const project=p.resolve(__dirname,'..');
const generator=p.join(__dirname,'montar_prancha.cjs');
let text=fs.readFileSync(generator,'utf8');
const edits=[
 ['Mudança funcional/visual para avaliar. Capacidade em unidades e funcionamento da ventilação não demonstrados.','Direção funcional aceita em 08/10. Capacidade em unidades, ventilação e encaixe final ainda não demonstrados.'],
 ['Poucos alimentos: alternativa junto da fruteira','Poucos alimentos: fruteira com base ventilada escolhida'],
 ['<strong>Proposta para você avaliar:</strong>','<strong>Direção escolhida por Elias em 08/10:</strong>'],
 ['bandeja superior de 5 cm e fundo de 4 mm','bandeja superior com 5 cm úteis e fundo de 4 mm'],
 ['Esta escolha muda a aparência da fruteira e requer concordância funcional; não foi incorporada como decisão.','A escolha funcional foi aceita: “Fruteira com base ventilada”. Medidas, material e produto continuam em desenvolvimento.'],
 ['Se você não quiser essa solução na mesa, o cesto permanece pendente e será preciso comparar outro destino real.','Se a capacidade ou o uso real não atenderem, revisar a peça preservando essa direção ou apresentar o conflito antes de mudar seu destino.'],
 ['fruteira com alimentos é alternativa para decisão.','fruteira com base ventilada tem direção aceita, mas capacidade, ventilação e manobra ainda precisam de conferência.']
];
for(const [before,after] of edits)text=text.replaceAll(before,after);
fs.writeFileSync(generator,text);
const summary='**08/10/2026 — cozinha e banco, atualização vigente:** Elias aprovou a proposta de organização da cozinha e do banco em 08/10, com a resposta “ok, aprovado”, e confirmou térmica guardada vazia e seca, poucas unidades de batatas/cebolas/alho e escolheu fruteira com base ventilada na mesa. Dimensões da fruteira seguem de estudo. Proposta do banco preserva 180 × 55 cm externos, assento com 45 cm de profundidade e topo a 47; os 45 cm antes chamados de profundidade externa foram corrigidos pela fonte. Folha preservada; setores 36,2 / 35 / 19,8 com duas divisórias de 1,8. Fundo a 8 cm somente no setor dos potes é nova hipótese construtiva: preserva reserva inferior 3,5, superior 4 e montagem de apoio testada de 24 mm. Estacionamento estático 67 × 95 na mesa conferido. Continuação técnica: o assento de 7 cm do modelo zera a sobra do balde e interfere com a subida direta da jarra. Alternativa de tampas de 2 cm e almofadas separadas amplia a passagem para 37,8 cm (2,4 cm por lado do corpo do balde); exige retirar almofada também no acesso diário à térmica, rotina aceita em 09/10/2026 por Elias (“entendo q funciona sim”). Dez percursos de potes/apoios/objetos inferiores reconferidos com assento de 7 cm; painéis agora têm 3 mm de montagem lateral. Estrutura, ferragens, acesso real, produtos, estoque e capacidade global não estão concluídos. Organização funcional adotada; construção, cotas executivas e fabricação seguem condicionadas às conferências técnicas.';
const targetFiles=[
 [p.resolve(project,'../README.md'),'01_Projeto/Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'README.md'),'Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'Resumo.md'),'Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'Painel_de_decisoes.md'),'Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'Cozinha/README.md'),'../Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'Sala_e_jantar/README.md'),'../Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'Compatibilizacao_2026-10-06/Estado_atual.md'),'../Compatibilizacao_2026-10-08/Cozinha_e_banco.html'],
 [p.join(project,'Compatibilizacao_2026-10-02/Mapa_do_inventario.md'),'../Compatibilizacao_2026-10-08/Cozinha_e_banco.html']
];
for(const [file,link] of targetFiles){let body=fs.readFileSync(file,'utf8');if(!body.includes('**08/10/2026 — cozinha e banco, atualização vigente:**')){const i=body.indexOf('\n');body=body.slice(0,i+1)+'\n'+summary+' [Prancha e mapa conjunto]('+link+'). Registros anteriores abaixo são históricos onde superados.\n'+body.slice(i+1);fs.writeFileSync(file,body);}}
const log=p.join(project,'Registro_de_decisoes.md');let body=fs.readFileSync(log,'utf8');
if(!body.includes('## 08/10/2026 — fechamento do armazenamento')){
 body+='\n\n## 08/10/2026 — fechamento do armazenamento\n\nPedido: “ok fecharemos o armazenamento da cozinha ebanco”. Autoriza continuar o desenvolvimento e consolidar a proposta; não adota automaticamente os novos detalhes.\n\nRespostas diretas recebidas nesta rodada:\n\n- Térmica de 1,5 L: “Vazia e seca após o uso”. Guarda em móvel preservada.\n- Batatas, cebolas e alho: “nao mt, poucas unidades”. Nenhuma quantidade exata em unidades ou kg presumida.\n- Nova escolha funcional: “Fruteira com base ventilada”, após apresentação de base com três divisões e frutas acima, aproximadamente 18 × 30 cm e 21 cm de altura total na mesa. Direção adotada; produto, material, capacidade e medidas executivas não escolhidos.\n\n'+summary+' [Prancha completa](Compatibilizacao_2026-10-08/Cozinha_e_banco.html). A nova proposta não consome as duas reservas de 3,5 nem apropria espaço de G3/C3; a viabilidade do fundo a 8 cm deve ser demonstrada pela construção real. O apoio temporário da fruteira ao liberar a mesa continua a definir. Sem compra, contato, commit/push ou publicação.\n';fs.writeFileSync(log,body);
}
console.log('Escolhas de 08/10 e proposta condicionada integradas em 9 índices/registros existentes.');
