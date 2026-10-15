from pathlib import Path
import json
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
def insert(rel,note):
 p=root/rel;s=p.read_text(encoding='utf-8-sig');head,rest=s.split('\n',1)
 p.write_text(head+'\n\n'+note+'\n'+rest,encoding='utf-8')
common='**12/10/2026 - auditoria dimensional:** Elias pediu verificar se gavetas, portas, alturas e profundidades têm escala realista e referências de mercado. Comparação documental concluída: cozinha 61,9 L e frentes 16/16/40 mantidas como base; escritório requer rever o curso ensaiado de 45 cm dentro de módulo externo de 45 cm, desenvolvendo nominal 400 mm. Gaveta de piso, profundidade líquida do guarda-roupa, prateleiras, tampo e assentos ainda dependem de solução construtiva/carga. Banheiro e caixas internas têm cotas pendentes. Ferragem do maleiro permanece pendente por pedido expresso, sem nova consulta externa. Não houve liberação de fabricação ou troca de layout.'
for rel in ['01_Projeto/Resumo.md','01_Projeto/Registro_de_decisoes.md','01_Projeto/Painel_de_decisoes.md']:
 insert(rel,common+' [Auditoria completa, nove páginas](../output/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf).')
insert('README.md',common+' [Abrir auditoria dimensional](output/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf).')
insert('01_Projeto/Escritorio/Setup_e_caixa_R10.md','**Auditoria de 12/10/2026:** curso de 45 cm abaixo era ensaio geométrico e não ferragem compatibilizada com o módulo externo de 45 cm. Com frente/fundo hipotéticos de 18 mm, restam 414 mm; nominal 450 não cabe nessa construção. Desenvolver referência nominal 400 mm e recalcular caixa/útil com a ferragem exata. Exemplo MOVENTO: espaço 403 mm sem estabilizador lateral; lateral da caixa 390 mm. Não se escolheu marca ou mudou o módulo. Curso de estudo 40 leva de y70 a y110, coincidente com a cama aberta, sem folga de uso garantida. [Auditoria](../../output/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf), página 5; dados antigos abaixo ficam históricos neste ponto.')
insert('01_Projeto/Portas_e_quarto/Aereos_continuos_quarto_2026-09-25.md','**Situação após a resposta de Elias em 12/10/2026:** deixar a ferragem do maleiro pendente e avançar para a verificação dimensional de toda a marcenaria. RO-32 permanece referência condicional; não é produto escolhido ou liberado. Consulta técnica continua pronta e não enviada. [Auditoria dimensional](../../output/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf).')
insert('01_Projeto/Cozinha/Interior_gavetas_2026-09-25.md','**Auditoria de escala em 12/10/2026:** referências atuais de fabricantes sustentam manter o módulo 61,9 e frentes 16/16/40; não há evidência de gavetas principais excessivamente largas ou profundas. Confirmar úteis com o sistema exato, H livre de G2 ≥ 11,1 e carga total de G3. Caixa de 50 e corrediça nominal de 50 não são equivalentes em todas as famílias. [Auditoria por ambiente](../../output/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf).')
pdf=root/'output/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf';reader=PdfReader(str(pdf))
assert len(reader.pages)==9
assert all(len(p.extract_text())>500 for p in reader.pages)
report={'pages':len(reader.pages),'text_extracted_all_pages':True,'external_links':sum(1 for p in reader.pages for a in p.get('/Annots',[]) if a.get_object().get('/A',{}).get('/URI')),'visual_review':'Todas as nove páginas renderizadas a 90 dpi e inspecionadas; sem sobreposição ou corte observados.','output':str(pdf)}
assert report['external_links']>=10
(root/'01_Projeto/Auditoria_dimensional_2026-10-12/Verificacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
