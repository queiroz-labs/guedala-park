"""Guia de campo offline: textos revisados, geometria nominal e fotos existentes."""
import base64
import csv
import io
import json
from pathlib import Path
import re
from html import escape
from build_field_data import rows,ROOT

HERE=Path(__file__).resolve().parent


def protocol_html(text):
    """Texto de campo legível offline; fontes nomeadas, sem links locais quebrados."""
    result=[]
    for i,block in enumerate(text.split('```')):
        if i%2:
            result.append('<pre>'+escape(block.split('\n',1)[-1].rstrip())+'</pre>')
            continue
        for paragraph in block.split('\n\n'):
            if not paragraph.strip():continue
            paragraph=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',paragraph.strip())
            heading=paragraph.startswith('# ')
            paragraph=escape(paragraph[2:] if heading else paragraph)
            paragraph=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',paragraph)
            result.append(('<h3>'+paragraph+'</h3>') if heading else '<p>'+paragraph+'</p>')
    return ''.join(result)


def guide_data():
    guides=json.loads((HERE/'guias_campo.json').read_text(encoding='utf-8'))
    codes=[p['codigo'] for r in rows() for p in r['partes']]
    if sorted(g['codigo'] for g in guides)!=sorted(codes):raise ValueError('Guia e formulário precisam dos mesmos códigos únicos')
    with (ROOT/'07_Imovel/Medidas_e_impactos.csv').open(encoding='utf-8-sig',newline='') as f:
        measures={r['codigo_medida']:r for r in csv.DictReader(f)}
    plans=json.loads((ROOT/'06_Entregas/Planta_cotada/Cotas.json').read_text(encoding='utf-8'))['pranchas']
    def mm(code):
        match=re.fullmatch(r'(-?\d+(?:\.\d+)?) mm',measures[code]['valor_nominal_atual'])
        if not match:raise ValueError('Geometria nominal sem cota escalar: '+code)
        return float(match[1])/10
    targets={}
    needed={g['onde']['alvo'] for g in guides if g['onde']['alvo']}
    for item in plans['openings']:
        if item['id'] not in needed:continue
        x,y,w,d,z,h=map(mm,item['refs'])
        targets[item['id']]=dict(room=item['room'],x=x,y=y,w=w,d=d,kind=item['kind'])
    for item in plans['points']:
        if item['id'] not in needed:continue
        x,y=map(mm,item['refs'][:2])
        targets[item['id']]=dict(room=item['room'],x=x,y=y,kind='ponto')
    overlay=[]
    for key,t in targets.items():
        shape=(f'<circle cx="{t["x"]}" cy="{t["y"]}" r="7"/>' if t['kind']=='ponto' else
               f'<rect x="{t["x"]}" y="{t["y"]}" width="{t["w"]}" height="{t["d"]}"/>')
        overlay.append(f'<g class="field-plan-target" data-fp-target="{escape(key)}" data-fp-r="{t["room"]}">{shape}</g>')
    for guide in guides:
        target=guide['onde']['alvo']
        if target is not None and target not in targets:raise ValueError('Alvo do guia sem geometria: '+str(target))
        if target is None and 'só cômodo' not in guide['onde']['orientacao']:raise ValueError('Declarar limite de geometria: '+guide['codigo'])
    photos={}
    # Quadros inspecionados nesta tarefa: sem rosto, retrato, placa ou marca visível.
    # Não alterar evidência: somente redução/compressão, sem recorte nem retoque.
    from PIL import Image
    for photo in sorted({g['foto'] for g in guides if g['foto']}):
        source=(ROOT/photo).resolve()
        if ROOT not in source.parents or not source.is_file():raise ValueError('Foto fora do acervo: '+photo)
        im=Image.open(source).convert('RGB');im.thumbnail((800,800))
        stream=io.BytesIO();im.save(stream,format='JPEG',quality=65,optimize=True)
        photos[photo]='data:image/jpeg;base64,'+base64.b64encode(stream.getvalue()).decode('ascii')
    protocol=(ROOT/'07_Imovel/Roteiro_dia_das_chaves_R01.md').read_text(encoding='utf-8').split('\n---\n')[0]
    return dict(guias=guides,targets=targets,overlay=''.join(overlay),photos=photos,protocolo_html=protocol_html(protocol))


def build():
    data=guide_data()
    with (HERE/'Cobertura_guias.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['codigo','comodo','geometria','alvo','foto'])
        for guide in data['guias']:
            writer.writerow([guide['codigo'],guide['onde']['comodo'],'alvo nominal' if guide['onde']['alvo'] else 'só cômodo',guide['onde']['alvo'] or '',guide['foto'] or 'sem foto'])
    # Evitar repetir as mesmas instruções e chaves 162 vezes no HTML autônomo.
    methods=[];packed=[]
    for g in data.pop('guias'):
        if g['como'] not in methods:methods.append(g['como'])
        packed.append([g['codigo'],g['titulo_simples'],g['onde']['comodo'],g['onde']['alvo'],g['onde']['orientacao'],methods.index(g['como']),g['instrumento'],g['altura_ref_mm'],g['foto']])
    data['itens']=packed;data['metodos']=methods
    js='// Gerado: guias revisados, Cotas.json e quadros existentes.\n'
    js+='globalThis.GUEDALA_FIELD_GUIDE='+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    js+="{const d=globalThis.GUEDALA_FIELD_GUIDE;d.guias=d.itens.map(g=>({codigo:g[0],titulo_simples:g[1],onde:{comodo:g[2],alvo:g[3],orientacao:g[4]},como:d.metodos[g[5]],instrumento:g[6],altura_ref_mm:g[7],foto:g[8]}));delete d.itens;delete d.metodos;}\n"
    (HERE/'src/field-guide-data.js').write_text(js,encoding='utf-8')
    return js


def standalone():
    """Cópia leve da mesma interface, sem CAD/dossiês volumosos, toda offline."""
    src=HERE/'src'
    svg=(ROOT/'06_Entregas/Planta_cotada/Planta_cotada.svg').read_text(encoding='utf-8')
    bootstrap='globalThis.GuedalaFloorplan={data:{svg:'+json.dumps(svg,ensure_ascii=False).replace('<','\\u003c')+'}};'
    css='\n'.join((src/p).read_text(encoding='utf-8') for p in ('app.css','field.css'))
    scripts='\n'.join((src/p).read_text(encoding='utf-8') for p in ('field-data.js','field-guide-data.js','field-core.js','field-ui.js'))
    html='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · Dia das chaves</title><style>'+css+'</style><main id="chaves" class="field-page active"></main><script>'+bootstrap+'\n'+scripts+'</script></html>'
    if len(html.encode('utf-8'))>1024*1024:raise ValueError('Guia offline ultrapassou 1 MB; reduzir mídia')
    (HERE/'Dia_das_chaves.html').write_text(html,encoding='utf-8')


if __name__=='__main__':build();standalone()
