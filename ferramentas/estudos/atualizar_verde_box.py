"""Reproduz B09 do fechamento: decisão de duas paredes, sem alterar luz ou orçamento."""
from html import escape
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
AREA=ROOT/'03_Ambientes/Banheiro/Fechamento_pre_entrega'
RESULTADO=('Duas paredes verdes no box: chuveiro e janela em Portobello Vivant Sauge Mate 7×24,4; '
           'a outra parede interna segue clara. Piso Travertino Reale Greige; Branco Itaúnas; '
           'Algodão Egípcio e teto branco. Alturas, paginação e recorte da janela dependem de levantamento. '
           'Não copiar a altura da cozinha para a cuba do banheiro.')


def main():
    source=AREA/'Situacao.json'
    data=json.loads(source.read_text(encoding='utf-8-sig'))
    item=next(s for s in data['sections'] if s['id']=='B09')
    old=item['result'];item['result']=RESULTADO
    item['source']='Elias, 30/10/2026: quer verde também na parede da janela; decisão nesta conversa'
    source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    page=AREA/'Fechamento.html';html=page.read_text(encoding='utf-8')
    # Mantém demais seções e substitui somente o resultado da linha correspondente.
    row=re.search(r'<tr id="B09">.*?</tr>',html,re.S)
    if not row:raise ValueError('Linha B09 ausente')
    revised=row[0].replace(escape(old),escape(RESULTADO)).replace(old,escape(RESULTADO))
    if escape(RESULTADO) not in revised:raise ValueError('Resultado B09 não localizado')
    page.write_text(html[:row.start()]+revised+html[row.end():],encoding='utf-8',newline='\n')


if __name__=='__main__':main()
