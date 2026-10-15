from pathlib import Path
import os, shutil
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
pdf=root/'output/pdf/Quarto_canto_independente_R01_2026-10-12.pdf'
note='**12/10/2026 - canto independente articulado, estudo R01:** Elias acolheu a ideia e pediu aprofundar. Desenvolvida proposta de um compartimento em L, com envelope nominal 65 × 105 cm (não retangular), duas faixas de frente de 40 cm e sem montante na quina de acesso. Restam 135 × 65 cm no maleiro reto e 180 × 25 cm no aéreo raso, este estudado com quatro faixas de 45. Preservados profundidades 65/25, face inferior 213,2, topo de estudo 244, altura interna geométrica 27,2, varão 205 e passagem nominal 49. Dentro da nova proposta, a antiga junta de 3 cm é substituída pelo canto integrado; folgas das portas a detalhar. Blum 79T8500 + dobradiça de caixa 155°/170° é referência comercial, não seleção final. Esquema com giros ilustrativos 90°/60°, sem validação cinemática, de carga, limitador ou colisão. Ferragem do maleiro de correr continua pendente. Conceito acolhido não equivale a aprovação das novas medidas ou fabricação; render anterior ainda não mostra esta divisão de portas.'
paths=['README.md','01_Projeto/Registro_de_decisoes.md','01_Projeto/Painel_de_decisoes.md','01_Projeto/Resumo.md','01_Projeto/Portas_e_quarto/README.md','01_Projeto/Portas_e_quarto/Aereos_continuos_quarto_2026-09-25.md','01_Projeto/Portas_e_quarto/Guarda_roupa_interior_R02.md']
for rel in paths:
    p=root/rel
    s=p.read_text(encoding='utf-8-sig')
    if 'canto independente articulado, estudo R01' in s: continue
    head,rest=s.split('\n',1)
    link=os.path.relpath(pdf,p.parent).replace('\\','/')
    p.write_text(head+'\n\n'+note+' [Prancha de estudo, três páginas]('+link+').\n'+rest,encoding='utf-8')
dest=root/'02_Plantas_e_manuais/Manuais/Ferragens_maleiro/Blum_Canto_bifold_catalogo_2025.pdf'
shutil.copy2(root/'tmp/pdfs/canto_articulado/Blum.pdf',dest)
assert len(PdfReader(pdf).pages)==3
assert abs((65+135)-200)<1e-9
assert abs((105+180)-285)<1e-9
assert abs((244-1.8)-215-27.2)<1e-9
assert all(PdfReader(pdf).pages[i].extract_text() for i in range(3))
print('Registros atualizados; PDF com 3 páginas; cotas de composição conferidas.')
