const fs=require('fs'),path=require('path');
const casos=[
 ['concha_molho_25159100',[31,7,6],[19.6,6.5,5.5],'adequacao_funcional_pendente'],
 ['escumadeira_25158100',[32,8,2.5],[29.9,8.9,6.2],'reprovada'],
 ['lisa_25855160',[30,6,2.5],[27.3,5,1.65],'apta_documental'],
 ['vazada_25155100',[30,6,2.5],[30.2,7.4,4.2],'reprovada'],
 ['peneira_25680101',[26,8,4.2],[25.2,9.7,4.5],'reprovada'],
 ['alho_25601100_conservador',[19,7,6.5],[16,4.7,4.7],'posicao_fechada_pendente'],
 ['citrico_25609100',[19,7,6.5],[20.5,6.8,3.5],'reprovada'],
 ['ralador_25685100',[21,7.5,4],[33,3.5,1.9],'reprovado']
];
const round=n=>Math.round(n*1e6)/1e6;
const resultado={data:'2026-10-06',unidade:'cm',escopo:'conferencia documental; nao libera compra ou obra',comparacoes:casos.map(([id,limite,envelope,status])=>({id,limite,envelope,status,folgas:limite.map((n,i)=>round(n-envelope[i])),contido:envelope.every((n,i)=>n<=limite[i])})),contas_condicionais:{faixa1:round(5.5+.2+2.5+.4+1),faixa2:round(1.65+.2+2.5+.2+4.2+.4+1),H_original_governante:11.1},oxo_peneira_sob_hipotese_polegadas:{entrada:[7.85,3.1,1.75],convertido:[7.85,3.1,1.75].map(n=>round(n*2.54)),altura_excede:round(1.75*2.54-4.2),unidade_fonte_nao_explicitada:true}};
fs.writeFileSync(path.join(__dirname,'auditoria_G2.json'),JSON.stringify(resultado,null,2)+'\n');
console.log(JSON.stringify({comparacoes:resultado.comparacoes.length,contidos:resultado.comparacoes.filter(x=>x.contido).length,contas_condicionais:resultado.contas_condicionais}));
