"""Leitura offline dos parâmetros salvos. Não recalcula nem grava o FCStd."""
from pathlib import Path
import zipfile, xml.etree.ElementTree as ET, json, hashlib
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
MODEL=PROJECT/'Modelo_FreeCAD/01_Cadeiras/Guedala_Park_R30_Juntas_Rotulos.FCStd'
raw=MODEL.read_bytes()
xml=ET.fromstring(zipfile.ZipFile(MODEL).read('Document.xml'))
objects={o.get('name'):o for o in xml.findall('./ObjectData/Object')}
def props(name):
    return {p.get('name'):p for p in objects[name].findall('./Properties/Property')}
def position(name):
    p=props(name)['Placement'][0]
    assert all(abs(float(p.get(q)))<1e-10 for q in ['Q0','Q1','Q2'])
    assert abs(float(p.get('Q3'))-1)<1e-10
    return [float(p.get(k)) for k in ['Px','Py','Pz']]
names=['Peca133','Peca134','Peca305','Peca306','Peca307','Peca308','Peca152','Peca357']
rows={}
for name in names:
    p=props(name)
    assert p['ExpressionEngine'][0].get('count')=='0'
    dims=[float(p[k][0].get('value')) for k in ['Length','Width','Height']]
    xyz=position(name)
    if name in ['Peca305','Peca306','Peca307']:
        assert name in [e.get('value') for e in props('Modulo006')['Group'][0]]
        xyz=[a+b for a,b in zip(xyz,position('Modulo006'))]
    # Transformação do apartamento espelhado documentada no coletor da R28.
    bbox=[7400-xyz[0]-dims[0],xyz[1],xyz[2],7400-xyz[0],xyz[1]+dims[1],xyz[2]+dims[2]]
    rows[name]={'rotulo':p['Label'][0].get('value'),'dimensoes_mm':dims,'bbox_espelhado_mm':bbox}
b=lambda n: rows[n]['bbox_espelhado_mm']
oven=b('Peca133'); right=b('Peca305'); left=b('Peca306'); top=b('Peca308'); cross=b('Peca307')
results={
    'vao_interno_mm':right[0]-left[3],
    'folgas_envelope_laterais_mm':[oven[0]-left[3],right[0]-oven[3]],
    'folga_envelope_parede_mm':7000-oven[4],
    'folga_envelope_travessa_mm':cross[2]-oven[5],
    'folga_lg_lateral_mm':b('Peca152')[0]-right[3],
    'desvio_eixos_forno_cooktop_mm':(oven[0]+oven[3]-b('Peca134')[0]-b('Peca134')[3])/2,
    'lateral_sob_pedra_lavanderia_mm':right[3]-b('Peca357')[0],
    'limite_d_para_separacao_200_mm':top[5]-oven[5]-200,
    'separacao_vertical_mm_por_d':{str(d):top[5]-d-oven[5] for d in [40,50,60,70,80]},
    'folga_corpo_485_centralizado_condicional_mm':(right[0]-left[3]-485)/2,
}
assert results['vao_interno_mm']==577
assert results['folgas_envelope_laterais_mm']==[30,30]
assert results['folga_envelope_parede_mm']==15
assert results['folga_envelope_travessa_mm']==0
assert results['folga_lg_lateral_mm']==67
assert results['desvio_eixos_forno_cooktop_mm']==6.5
assert results['lateral_sob_pedra_lavanderia_mm']==13
assert results['limite_d_para_separacao_200_mm']==60
report={'data':'2026-10-14','arquivo':str(MODEL),'sha256':hashlib.sha256(raw).hexdigest(),
 'metodo':'Parâmetros XML salvos de oito caixas; translação do módulo e espelhamento X=7400-X documentado na R28. Sem FreeCAD ativo, recompute, leitura de BREP, inspeção dos vínculos ou nova auditoria de colisões. Não valida montagem real.',
 'referencias':'Parede Y=7000 e transformação herdadas do estudo, sem levantamento físico.',
 'objetos':rows,'resultados':results}
(HERE/'Conferencia_parametros_R30.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
