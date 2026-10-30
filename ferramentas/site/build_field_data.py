"""Lista móvel das chaves derivada do CSV vigente; não grava valores de campo."""
import csv
import json
from pathlib import Path
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[2]
SELECT=re.compile(r'^(PD-|DIM-|MOV-|ANC(?:-|$)|PISO(?:-|$)|COMP(?:-|$)|LAV-TEC(?:-|$)|COZ-|SAL-COND(?:-|$))')
ROOMS={'quarto':'Quarto','cozinha':'Cozinha','lavanderia':'Lavanderia','escritorio':'Escritório',
       'banho':'Banheiro','sala':'Sala e jantar','circulacao':'Circulação','all':'Geral'}


def room_id(text):
    text=''.join(c for c in unicodedata.normalize('NFD',text.lower()) if not unicodedata.combining(c))
    return {'banheiro':'banho','sala/jantar':'sala','todos':'all'}.get(text,text)


def nominal_parts(code,text):
    """Sem extrair um número de uma descrição como se fosse uma cota.

    DIM já admite eixos /0, /1 na resolução existente das pranchas.
    Fora de DIM, só se aceita um valor escalar isolado com unidade.
    """
    if code.startswith('DIM-'):
        tokens=re.findall(r'(-?\d+(?:[.,]\d+)?)\s*(mm|cm|m)?',text)
        if not tokens:return [dict(codigo=code,nominal_mm=None,label='Medida')]
        last_unit=next((u for _,u in reversed(tokens) if u),'')
        values=[float(n.replace(',','.'))*{'mm':1,'cm':10,'m':1000}[u or last_unit] for n,u in tokens] if last_unit else []
        if not values:return [dict(codigo=code,nominal_mm=None,label='Medida')]
        return [dict(codigo=f'{code}/{i}' if len(values)>1 else code,nominal_mm=v,
                     label=f'Medida {i+1}' if len(values)>1 else 'Medida') for i,v in enumerate(values)]
    match=re.fullmatch(r'\s*(-?\d+(?:[.,]\d+)?)\s*(mm|cm|m)\s*',text)
    value=float(match[1].replace(',','.'))*{'mm':1,'cm':10,'m':1000}[match[2]] if match else None
    return [dict(codigo=code,nominal_mm=value,label='Medida')]


def rows(root=ROOT):
    with (root/'07_Imovel/Medidas_e_impactos.csv').open(encoding='utf-8-sig',newline='') as f:source=list(csv.DictReader(f))
    result=[]
    for r in source:
        code=r['codigo_medida']
        if not SELECT.match(code):continue
        room=room_id(r['ambiente'])
        if room not in ROOMS:raise ValueError('Ambiente sem grupo: '+r['ambiente'])
        clean=lambda s:re.sub(r'laminado','vinílico Olmo',s,flags=re.I)
        result.append(dict(codigo=code,ambiente=room,ambiente_nome=ROOMS[room],
            descricao=clean(r['medida_ou_verificacao']),nominal=clean(r['valor_nominal_atual']),
            tolerancia=r['tolerancia_que_afeta_projeto'],partes=nominal_parts(code,r['valor_nominal_atual']),
            moveis=r['moveis_afetados']))
    codes=[p['codigo'] for r in result for p in r['partes']]
    if len(codes)!=len(set(codes)):raise ValueError('Código de campo duplicado')
    return result


def build(root=ROOT):
    text='// Gerado de Medidas_e_impactos.csv; não editar valores aqui.\n'
    text+='globalThis.GUEDALA_FIELD_ROWS='+json.dumps(rows(root),ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    (root/'ferramentas/site/src/field-data.js').write_text(text,encoding='utf-8')


if __name__=='__main__':build()
