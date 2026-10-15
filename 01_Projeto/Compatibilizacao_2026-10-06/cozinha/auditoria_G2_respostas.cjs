const fs=require('fs'),path=require('path');const r=x=>Math.round(x*1e6)/1e6;
const raw=[
['concha_Rosle100006',[31,7,6],[26,6.7,5],'candidata_geometria; sopa_feijao_nao_explicitos;40ml'],
['peneira_Westmark12812270',[26,8,4.2],[20.5,7,3],'candidata_documental'],
['escumadeira_Rosle100050',[32,8,2.5],[33,10,6.2],'reprovada'],
['escumadeira_Westmark28502270',[32,8,2.5],[32.2,11.8,8],'reprovada'],
['vazada_Westmark20352270',[30,6,2.5],[28.3,7,2],'reprovada'],
['vazada_Westmark20152270',[30,6,2.5],[26,7.4,1.6],'reprovada'],
['peneira_Kuhn24346',[26,8,4.2],[26.8,8,5],'reprovada'],
['citrico_Westmark50002260',[19,7,6.5],[23.7,11.6,6.9],'reprovado'],
['citrico_Westmark30932280',[19,7,6.5],[7.2,7.2,7.7],'reprovado'],
['citrico_Westmark90882280',[19,7,6.5],[8.5,7.1,1.9],'reprovado;fatias'],
['citrico_OXO1057962',[19,7,6.5],[10.5*2.54,4.24*2.54,1.5*2.54],'reprovado'],
['ralador_Westmark10022270',[21,7.5,4],[24.3,10.3,1],'reprovado'],
['ralador_MicroplaneSpice',[21,7.5,4],[21.5,3,2],'reprovado'],
['ralador_Westmark11532270',[21,7.5,4],[15,5.3,2.6],'geometria_contida;formato_curvo_nao_selecionado']
];
const out={data:'2026-10-06',unidade:'cm',resposta_usuario:'concha para sopa/feijao;molho nao atende',descartado_por_funcao:'Tramontina25159100',escopo:'comparacoes documentais;nao compra ou liberacao executiva',comparacoes:raw.map(([id,limite,envelope,status])=>({id,limite,envelope:envelope.map(r),folga:limite.map((n,i)=>r(n-envelope[i])),contido:envelope.every((n,i)=>n<=limite[i]),status})),condicionais:{H_faixa1:r(5+.2+2.5+.4+1),H_faixa2:r(1.65+.2+2.5+.2+3+.4+1),H_governante_original:11.1,porcoes_ilustrativas_40ml:[250,300].map(volume=>({volume_ml:volume,numero:Math.ceil(volume/40)}))},lacunas:['Fackelmann680938 sem envelope primario','alho25601100 fechado nao explicito','concha Rosle100006 nao descreve sopa/feijao explicitamente','escumadeira citrico ralador plano sem candidato apto nesta rodada','H real pega retirada estabilidade tolerancias']};
fs.writeFileSync(path.join(__dirname,'auditoria_G2_respostas.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify({casos:out.comparacoes.length,H:out.condicionais}));
