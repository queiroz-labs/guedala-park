"""Gera PDF e pacote de oficina a partir do caderno, sem preencher medições.

Executar com Python que disponha de ReportLab e pypdf. Fontes explícitas;
sem CAD, documentos personalizados ou busca recursiva de dependências.
"""
from pathlib import Path
from html import escape
from urllib.parse import unquote, urlsplit, quote
import csv
import hashlib
import io
import json
import posixpath
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '04_Moveis/Ensaios_oficina'
OUT = ROOT / '06_Entregas/Ensaios_oficina'
LINK = re.compile(r'(!?)\[([^\]]+)\]\(([^)]+)\)')
EXTRAS = '''
04_Moveis/Aereos_suspensao/P04_ensaios_laboratorio.pdf
04_Moveis/Aereos_suspensao/P04_acesso_e_suspensao.png
04_Moveis/Aereos_suspensao/P04_preparacao_ensaios.json
04_Moveis/Aereos_suspensao/Lote_B_ligacoes_internas.csv
04_Moveis/Aereos_suspensao/Lote_B_ligacoes_traseiras.csv
04_Moveis/Aereos_suspensao/Lote_B_mapa_reconciliado.csv
04_Moveis/Aereos_suspensao/Lote_B_fontes_Minifix.json
04_Moveis/Aereos_suspensao/P12_mapa_juntas.csv
04_Moveis/Aereos_suspensao/P12_eixos_fixadores.csv
04_Moveis/Aereos_suspensao/P12_suspensao.png
04_Moveis/Aereos_suspensao/P17_mapa_juntas.csv
04_Moveis/Aereos_suspensao/P17_eixos_fixadores.csv
04_Moveis/Aereos_suspensao/P17_suspensao.png
04_Moveis/P20/Assento_fechado/Interfaces_montagem.csv
04_Moveis/P20/Assento_fechado/Mapa_contatos.png
04_Moveis/P20/Assento_fechado/Montagem_aberta.png
04_Moveis/P14/Reacoes_e_operacao/Montagem_nominal.json
04_Moveis/P14/Reacoes_e_operacao/Reacoes_parada_55.png
04_Moveis/P08/Apoios.png
04_Moveis/P16/Gavetas_estabilidade/Planta_movimento_apoios.png
04_Moveis/P16/Interface_guia_fundo/Mapa_intersecoes.png
04_Moveis/P16/Interface_guia_fundo/Referencia_G2_e_furos_P16.json
04_Moveis/Inventario_dimensional/Gavetas/Ajuste_vertical_e_retirada.md
04_Moveis/Avanco_pendencias/Ferragens/FGVTN_Oculta_ET_montagem_Set24.png
04_Moveis/Inventario_dimensional/Gavetas/Alternativas_escritorio/Blum_MOVENTO_oficial.pdf
04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia/Fontes/Omega_7379.pdf
04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia/Fontes/Mahler_54_2000.pdf
04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia/Fontes/Bigfer_112.pdf
09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/Bigfer_suportes_aereos.pdf
'''.strip().splitlines()


def select_sources():
    names = {'04_Moveis/Ensaios_oficina/Caderno.md', '04_Moveis/Ensaios_oficina/README.md'}
    for entry in ('Caderno.md', 'README.md'):
        for _, _, url in LINK.findall((BASE / entry).read_text(encoding='utf8')):
            part = urlsplit(url)
            if part.scheme or not part.path:
                continue
            path = (BASE / unquote(part.path)).resolve()
            if path.is_relative_to(OUT):
                continue  # A entrega não inclui a si mesma como fonte.
            if path.suffix in {'.md', '.csv', '.txt', '.svg', '.png', '.pdf'} and path != BASE/'Registro.csv':
                names.add(path.relative_to(ROOT).as_posix())
    names.update(EXTRAS)
    for name in names:
        if not (ROOT/name).is_file():
            raise FileNotFoundError(name)
        if any(x in name.lower() for x in ('guedala-pessoal', 'blum_g2_pagina', 'contrato')):
            raise ValueError('Fonte não pública: '+name)
    return sorted(names)


def destination(name):
    return 'Fontes/'+name+('.html' if name.endswith('.md') else '')


def clean(text):
    return text.replace('—', '-').replace('–', '-').replace('\u2011', '-')


def pdf(caderno, names):
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    fontdir = Path('C:/Windows/Fonts')
    for name, file in [('Oficina','arial.ttf'), ('Oficina-Bold','arialbd.ttf'), ('Oficina-Italic','ariali.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(fontdir/file)))
    pdfmetrics.registerFontFamily('Oficina', normal='Oficina', bold='Oficina-Bold', italic='Oficina-Italic', boldItalic='Oficina-Bold')
    body = ParagraphStyle('corpo', fontName='Oficina', fontSize=10, leading=13, spaceAfter=7, textColor=colors.HexColor('#243b36'))
    small = ParagraphStyle('tabela', parent=body, fontSize=8, leading=11, spaceAfter=0)
    heading = ParagraphStyle('secao', parent=body, fontName='Oficina-Bold', fontSize=17, leading=22, spaceAfter=15, keepWithNext=True)
    sub = ParagraphStyle('sub', parent=heading, fontSize=12, leading=16, spaceBefore=10, spaceAfter=8)
    title = ParagraphStyle('titulo', parent=heading, fontSize=32, leading=38)
    def inline(text):
        chunks=[]; last=0
        for match in LINK.finditer(text):
            chunks.append(escape(clean(text[last:match.start()])))
            _, label, url = match.groups(); parsed=urlsplit(url)
            href=url if parsed.scheme in ('http','https') else None
            if not parsed.scheme:
                path=(BASE/unquote(parsed.path)).resolve()
                try: name=path.relative_to(ROOT).as_posix()
                except ValueError: name=''
                if path==BASE/'Registro.csv': href='Registro.csv'
                elif name in names: href=destination(name)
            chunks.append(f'<link href="{escape(quote(href,safe="/:?#=&%"),quote=True)}" color="#216956">{escape(clean(label))}</link>' if href else escape(clean(label)))
            last=match.end()
        chunks.append(escape(clean(text[last:])))
        result=''.join(chunks)
        result=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',result)
        result=re.sub(r'`([^`]+)`',r'\1',result)
        return result
    story=[Spacer(1,65),Paragraph('GUEDALA PARK',sub),Paragraph('Ensaios<br/>de oficina',title),Spacer(1,22),
           Paragraph('Caderno de preparação, montagem e registro',heading),
           Paragraph('<b>Pendente de execução</b>',heading),
           Paragraph('13 frentes de oficina. Conferências de instalação após o levantamento do apartamento.',body),
           Paragraph('Nenhum resultado físico registrado. Cargas, desenhos e critérios ainda indefinidos devem ser fechados antes da respectiva prova.',body),
           Paragraph('No pacote: abra COMECE_AQUI.html, consulte as fontes e preencha somente Registro.csv. Extraia o ZIP inteiro para usar os links locais.',body),
           Spacer(1,30),Paragraph('Preparação documental - 28/10/2026',body),PageBreak()]
    lines=caderno.splitlines(); i=0
    while i<len(lines):
        line=lines[i].strip(); i+=1
        if not line or line.startswith('# ') or line.startswith('28/10/2026'):continue
        if line.startswith('## '):
            if len(story)>1 and not isinstance(story[-1],PageBreak):story.append(PageBreak())
            story.append(Paragraph(inline(line[3:]),heading));continue
        if line.startswith('### '):
            if line.startswith('### A01'):story.append(PageBreak())
            story.append(Paragraph(inline(line[4:]),sub));continue
        if line.startswith('|'):
            rows=[line]
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip());i+=1
            data=[]
            for row in rows:
                cells=row.strip('|').split('|')
                if all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in cells):continue
                data.append([Paragraph(inline(c.strip()),small) for c in cells])
            n=len(data[0]); ratios=([.07,.12,.34,.32,.15] if n==5 and 'Quem fornece' in rows[0] else [.16,.37,.17,.30] if n==4 and 'Ordem' in rows[0] else [1/n]*n)
            table=Table(data,colWidths=[489*r for r in ratios],repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1ebe5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#547363')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f3')])]))
            if 'Ordem' in rows[0]:
                table.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
            story.extend([table,Spacer(1,12)]);continue
        story.append(Paragraph(inline(line),body))
    def furniture(canvas,doc):
        canvas.setFont('Oficina',8);canvas.setFillColor(colors.HexColor('#547363'))
        canvas.drawString(53,811,'GUEDALA PARK / ENSAIOS DE OFICINA')
        canvas.drawRightString(542,811,'PENDENTE DE EXECUÇÃO')
        canvas.line(53,800,542,800)
        canvas.drawString(53,28,'Medidas nominais em mm. Conferir produtos e plano antes de executar.')
        canvas.drawRightString(542,28,str(doc.page))
    stream=io.BytesIO()
    doc=SimpleDocTemplate(stream,pagesize=A4,leftMargin=53,rightMargin=53,topMargin=56,bottomMargin=48,title='Guedala Park - Caderno de ensaios de oficina',author='Guedala Park',invariant=1)
    doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
    return stream.getvalue()


def build():
    from pypdf import PdfReader
    from verificar_ensaios_oficina import verificar
    if any(status!='sem dados' for _,status,_ in verificar(BASE/'Registro.csv')):
        raise ValueError('Distribuição pública exige o registro inteiramente sem dados')
    names=select_sources()
    sys.path.insert(0,str(ROOT/'ferramentas/site'))
    from build_workshop_docs import markdown
    payload={}
    omitted=[]
    def html_page(title,body):
        return ('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>body{font:16px/1.6 system-ui;color:#243b36;max-width:1100px;margin:auto;padding:32px;background:#fafaf7}a{color:#216956;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #dce4dd;padding:9px;vertical-align:top}img{max-width:100%}pre{white-space:pre-wrap}nav{display:grid;gap:12px}h1,h2{line-height:1.2}li{margin:6px 0}</style>'+body+'</html>').encode('utf8')
    for name in names:
        raw=(ROOT/name).read_bytes();payload['Fontes/'+name]=raw
        if name.endswith('.md'):
            content=markdown(raw.decode('utf-8-sig'))
            def rewrite(m):
                attr,delim,url=m.group(1,2,3);part=urlsplit(unquote(url))
                if part.scheme in ('https','http','data') or url.startswith('#'):return m[0]
                resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),part.path))
                target=destination(resolved) if resolved in names else 'Registro.csv' if resolved=='04_Moveis/Ensaios_oficina/Registro.csv' else None
                if target:
                    rel=posixpath.relpath(target,posixpath.dirname(destination(name)))
                    return attr+'='+delim+quote(rel,safe='/')+delim
                omitted.append({'fonte':name,'referencia':url})
                return 'data-referencia-complementar='+delim+escape(url,quote=True)+delim
            content=re.sub(r'\b(href|src)\s*=\s*(["\'])(.*?)\2',rewrite,content)
            payload[destination(name)]=html_page(Path(name).stem,'<p><b>Documento de origem.</b> Execução e registro seguem o caderno. Referências complementares fora desta seleção não têm link local.</p>'+content)
    payload['Caderno_ensaios_oficina.pdf']=pdf((BASE/'Caderno.md').read_text(encoding='utf8'),names)
    payload['Registro.csv']=(BASE/'Registro.csv').read_bytes()
    payload['verificar_ensaios_oficina.py']=(ROOT/'ferramentas/estudos/verificar_ensaios_oficina.py').read_bytes()
    links=''.join('<li><a href="'+quote(destination(n),safe='/')+'">'+escape(n)+'</a></li>' for n in names)
    body='<h1>Ensaios de oficina</h1><p><strong>Pendente de execução</strong></p><p>Roteiros de montagem, compras e medições para preparar os protótipos. Cargas, desenhos e critérios em aberto precisam ser definidos antes da respectiva prova.</p><nav><a href="Caderno_ensaios_oficina.pdf">Abrir caderno em PDF</a><a href="Registro.csv" download>Registro único de medições - CSV</a></nav><h2>Como usar</h2><ol><li>Extraia todo o ZIP e abra este arquivo.</li><li>Comece pela preparação do caderno e pelo retalho P04 sem carga.</li><li>Preencha somente Registro.csv. Os formulários das fontes são referências; não mantenha registros paralelos.</li><li>Guarde fotos e planos junto da cópia privada e informe seus caminhos relativos no CSV.</li><li>Opcional, com Python: <code>python -B verificar_ensaios_oficina.py Registro.csv</code>.</li></ol><p>O verificador confere completude documental, não aceita nem rejeita o móvel. Resultados e dados pessoais da oficina devem permanecer na cópia privada.</p><h2>Documentos de origem</h2><p>Versões HTML permitem leitura offline; arquivos Markdown originais preservam a fonte. Links externos exigem internet. Referências complementares não incluídas estão no manifesto, sem links quebrados nas versões HTML.</p><ul>'+links+'</ul>'
    payload['COMECE_AQUI.html']=html_page('Ensaios de oficina',body)
    manifest={'estado':'pendente de execução','fontes':names,'referencias_complementares_nao_incluidas':omitted,'arquivos':[{'caminho':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())]}
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    payload['Manifesto.json']=manifest_bytes
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(payload.items()):
            entry=zipfile.ZipInfo('Ensaios_oficina/'+n,date_time=(2026,10,28,12,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(entry,b)
    with zipfile.ZipFile(io.BytesIO(mem.getvalue())) as z:
        assert z.testzip() is None
        for item in manifest['arquivos']:
            assert hashlib.sha256(z.read('Ensaios_oficina/'+item['caminho'])).hexdigest()==item['sha256']
        for n,b in payload.items():
            if not n.endswith('.html'):continue
            for url in re.findall(r'(?:href|src)="([^"]+)"',b.decode('utf8')):
                part=urlsplit(unquote(url))
                if not part.scheme and part.path:
                    assert posixpath.normpath(posixpath.join(posixpath.dirname(n),part.path)) in payload,(n,url)
    reader=PdfReader(io.BytesIO(payload['Caderno_ensaios_oficina.pdf']))
    assert all('PENDENTE DE EXECUÇÃO' in p.extract_text() for p in reader.pages)
    OUT.mkdir(parents=True,exist_ok=True)
    for n in ('Caderno_ensaios_oficina.pdf',): (OUT/n).write_bytes(payload[n])
    public_body='''<p>GUEDALA PARK / MARCENARIA</p><h1>Ensaios de oficina</h1>
<p><strong>Pendente de execução</strong></p>
<p>Roteiros para preparar protótipos, conferir a montagem e registrar medições. O caderno reúne materiais, ferragens, sequência de trabalho, compras e campos de registro.</p>
<nav><a href="Caderno_ensaios_oficina.pdf">Ler o caderno em PDF</a><a href="Pacote_ensaios_oficina.zip" download>Baixar pacote completo para a oficina</a><a href="../../04_Moveis/Ensaios_oficina/Registro.csv" download>Baixar registro de medições em CSV</a></nav>
<h2>O que será conferido</h2><ul><li>Identificação das chapas, ferragens e massas.</li><li>Acesso aos conectores, juntas e suspensão dos armários.</li><li>Base composta da lavanderia, banco com baú e cesto de roupas.</li><li>Rodízios, engates, frentes e retirada das gavetas.</li></ul>
<h2>Como começar</h2><p>Extraia o ZIP inteiro e abra COMECE_AQUI.html. Consulte o plano de preparação e comece pela identificação dos materiais e pelo retalho P04 sem carga.</p>
<p>O pacote contém o PDF, o CSV vazio, documentos de origem e um verificador de preenchimento. Use somente o registro único para as medições e guarde fotos e laudos na cópia privada.</p>
<h2>Antes das provas</h2><p>Os ensaios de oficina podem ser preparados antes da entrega do apartamento. Cada prova depende dos produtos, desenhos e critérios indicados no caderno. Cargas de cálculo não devem ser usadas como pesos de prova.</p>
<p>Piso, parede, ancoragens e folgas de instalação serão conferidos após o levantamento do imóvel. Nenhum resultado físico está registrado.</p>'''
    (OUT/'index.html').write_bytes(html_page('Ensaios de oficina | Guedala Park',public_body))
    (OUT/'Pacote_ensaios_oficina.zip').write_bytes(mem.getvalue())
    (OUT/'Manifesto.json').write_bytes(manifest_bytes)
    print(json.dumps({'paginas':len(reader.pages),'fontes':len(names),'arquivos_zip':len(payload),'zip_bytes':len(mem.getvalue()),'zip_sha256':hashlib.sha256(mem.getvalue()).hexdigest(),'registro':'sem dados','links_html':'OK'},ensure_ascii=False))


if __name__=='__main__':build()
