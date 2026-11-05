"""Transcreve inventário nominal das fichas atuais para cotação, sem calcular corte.
Histórico da consolidação anterior no git; não envia nem altera CAD.
"""
# MEDIDAS: nao se aplica - transcrição de quantidades documentais, sem dimensionamento
from pathlib import Path
from html import escape
import csv
import json

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT/'06_Entregas/Cotacao/Quantidades_referencia.csv'
FIELDS = ['grupo','item','movel','padrao','espessura_mm','formato','quantidade',
          'unidade','quantidade_com_perda','base','fonte','observacao']


def read(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=';'))


def write(path, rows, fields=None):
    with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter=';')
        w.writeheader();w.writerows(rows)


def expanded_fichas(root=ROOT):
    panels={}
    for path in sorted((root/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')):
        for n,r in enumerate(read(path),2):
            ids=[x.strip() for x in r['IDs CAD'].split('|')]
            if len(ids)!=int(r['Qtd']):
                raise ValueError(f'{path.name}:{n}: Qtd diferente dos IDs')
            for ident in ids:
                key=(path.name[:3],ident)
                if key in panels:raise ValueError(f'ID repetido: {key}')
                panels[key]=dict(c=float(r['C nominal mm']),l=float(r['L nominal mm']),
                    t=float(r['Esp. envelope mm']),fonte=f'{path.relative_to(root).as_posix()}:{n}')
    return panels


def current_rows():
    """Transcreve as fichas atuais; não recalcula corte, fita ou capacidade."""
    panels=expanded_fichas()
    manifest=json.loads((ROOT/'06_Entregas/Fichas_fabricacao/manifest.json').read_text(encoding='utf-8'))
    if len(panels)!=manifest['panels']:
        raise ValueError('Contagem de painéis diverge do manifesto das fichas')
    tech_path='06_Entregas/Fichas_fabricacao/Tecnica_R15.json'
    tech=json.loads((ROOT/tech_path).read_text(encoding='utf-8'))
    rows=[]
    def add(**values):
        rows.append(dict.fromkeys(FIELDS,'') | values)
    for mod in sorted({k[0] for k in panels}):
        stage='futura; fora da etapa inicial' if mod in ('P16','P17') else 'etapa inicial'
        add(grupo='paineis',item=mod,movel=mod,quantidade=sum(k[0]==mod for k in panels),
            unidade='painel',base='inventário nominal das fichas atuais',
            fonte=f'06_Entregas/Fichas_fabricacao/{mod}-pecas.csv',observacao=stage+'; não é quantidade de chapas; medidas reais pendentes')
        for h in tech['modules'][mod]['hardwareRows']:
            quantity=h.get('quantity')
            add(grupo='ferragens',item=h['item'],movel=mod,
                quantidade='' if quantity is None else quantity,unidade=h.get('unit',''),
                base='documental; confirmar produto e composição do kit',fonte=tech_path,
                observacao=stage+'; '+str(h.get('reference',''))+'; '+str(h.get('status','')))
    for label,note in [
        ('Chapas, formatos e perdas','Quantidade a definir pela oficina com as peças atuais; não reutilizar o plano histórico de 249 painéis/14 chapas.'),
        ('Fita de borda','Definir por peça atual, cor, espessura, aresta e processo; metragem anterior não é compra vigente.'),
        ('Conectores e fixadores','Quantidades das fichas são referências documentais, sem soma ao mapa de juntas; P19: 12 Minifix documentais versus 8 do mapa, decisão pendente.'),
        ('Complementos e serviços','C01 a C06 e S01 a S06 estão no formulário; não estão completos neste inventário de painéis/ferragens.')]:
        add(grupo='pendencia',item=label,base='pendente; vazio não é zero',
            fonte='05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md',observacao=note)
    return rows


def annex(path=CSV):
    rows=read(path)
    panels=[r for r in rows if r['grupo']=='paineis']
    rails=[r for r in rows if r['grupo']=='ferragens' and r['item'].startswith('Corrediças laterais')]
    body=''.join('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in [r['movel'],r['item'],r['quantidade'],r['unidade'],r['observacao'].split(';')[0]])+'</tr>' for r in rails)
    total=sum(int(r['quantidade']) for r in panels)
    return f'''<section><h2>Inventário para cotação — revisão 04/11/2026</h2>
<p><b>ESTIMATIVA NOMINAL: {total} painéis nas fichas atuais dos 20 móveis.</b> Inclui P16/P17 adiados. As peças e ferragens por móvel estão no CSV; a oficina deve separar integral e etapa inicial.</p>
<table><thead><tr><th>Móvel</th><th>Corrediça</th><th>Qtd.</th><th>Unidade</th><th>Etapa</th></tr></thead><tbody>{body}</tbody></table>
<p>Corrediças laterais com amortecimento: 7 pares de 500 mm na etapa inicial e 2 pares de 400 mm no P16 futuro. SKU, fixadores, capacidade e furação pendentes. Não cotar as antigas guias ocultas nem seus engates como conjunto vigente.</p>
<p><b>Chapas e fita: quantidade a confirmar pela oficina.</b> O plano histórico de 249 painéis/14 chapas e a metragem anterior de fita não acompanham as caixas atuais; não usá-los como compra. Informar formato, produto, perdas, bordas e cobertura completa da proposta.</p>
<p>P19: 12 Minifix documentais versus 8 no mapa, sem decisão; não somar bases. Quantidade ausente não é zero; componentes incluídos em kits não geram compra duplicada.</p>
<p>Modelo de referência R55. As fichas R15 incorporam atualizações, mas conservam rótulos/metadados históricos R53/R45 e mapas anteriores. Não constituem nova extração integral nem gabarito de fabricação. Em divergência, a oficina deve apontar o item antes de fechar preço ou executar.</p>
<p><a href="Quantidades_referencia.csv">Inventário atual, fontes e pendências</a>. Complementos e serviços permanecem no formulário de resposta.</p></section>'''


def main():
    rows=current_rows()
    write(CSV,rows,FIELDS)
    print(f'{len(rows)} linhas atuais; sem cálculo de corte, fita ou cargas')


if __name__=='__main__':main()
