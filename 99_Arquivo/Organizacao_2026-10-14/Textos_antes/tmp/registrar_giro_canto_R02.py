from pathlib import Path
from pypdf import PdfReader
import os,json
root=Path(__file__).resolve().parents[1]
pdf=root/'output/pdf/Quarto_conferencia_giro_R02_2026-10-12.pdf'
note='**12/10/2026 - conferência do giro do canto, R02:** após acolher R01, Elias pediu conferir ferragens e evitar choques com os vizinhos. Catálogo confirma conjunto candidato CLIP top 71T7550 + 79T8500 e limitador 70T7553.09 de 92°. Modelo de eixos fixos e painéis de 18 mm encontrou risco de retorno da folha B ao maleiro em aberturas maiores e cruzamento com a primeira porta do aéreo em abertura simultânea (canto 10°, articulação 0°, vizinha ~11°). R01 não está liberada. Nova proposta, ainda não aprovada: faixa frontal fixa de 15 cm após o canto, seguida por quatro faixas móveis de 41,25 cm com a primeira dobradiça no extremo afastado; interior atrás da faixa pode integrar primeiro compartimento de 56,25. Triagem de 88.929 posições dá separação do disco envolvente da vizinha >=4,82 cm após limite de amostragem, SOMENTE no modelo de pivôs fixos. Isso não é folga real garantida: faltam deslocamentos multilink, calços, recobrimentos, ajustes, puxadores, carga, quantidade/fixação e teste com portas de correr. Preservados profundidades 65/25, alturas alinhadas, canto nominal 65 × 105 e programa inferior. Não adotar faixa 15 como decisão do usuário nem anunciar giro sem colisão validado.'
for rel in ['README.md','01_Projeto/Registro_de_decisoes.md','01_Projeto/Painel_de_decisoes.md','01_Projeto/Resumo.md','01_Projeto/Portas_e_quarto/README.md','01_Projeto/Portas_e_quarto/Aereos_continuos_quarto_2026-09-25.md','01_Projeto/Portas_e_quarto/Guarda_roupa_interior_R02.md']:
 p=root/rel;s=p.read_text(encoding='utf-8-sig')
 if 'conferência do giro do canto, R02' in s:continue
 h,r=s.split('\n',1);link=os.path.relpath(pdf,p.parent).replace('\\','/')
 p.write_text(h+'\n\n'+note+' [Conferência em quatro páginas]('+link+').\n'+r,encoding='utf-8')
data=root/'01_Projeto/Portas_e_quarto/Conferencia_giro_canto_R02.json'
d=json.loads(data.read_text(encoding='utf-8'))
d['sources']=[{'url':'https://publications.blum.com/2024/catalogue/en/84/','supports':'dobradiça 71T7550 e limitadores 92/110'}, {'url':'https://publications.blum.com/2024/catalogue/en/117/','supports':'posição de canecos da articulação na folha principal'}, {'url':'https://ea.blum.com/en/opening-angle-stops-155-hinges/','supports':'limitador 70T7553.09 de 92 graus'}, {'local':'../../02_Plantas_e_manuais/Manuais/Ferragens_maleiro/Blum_Canto_bifold_catalogo_2025.pdf','pages':[31,32,47],'supports':'planejamento, movimento a 90, dobradiças e limitadores'}]
d['proposal_R02']={'fixed_front':15,'moving_front_bands':[41.25]*4,'first_aerial_body_nominal':56.25,'approval':'proposta não aprovada; apenas a conferência solicitada por Elias'}
data.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
r=PdfReader(pdf);assert len(r.pages)==4
assert all(len(p.extract_text())>500 for p in r.pages)
assert abs(15+4*41.25-180)<1e-9
print('R02 salva como proposta; quatro páginas verificadas; R01 preservada.')
