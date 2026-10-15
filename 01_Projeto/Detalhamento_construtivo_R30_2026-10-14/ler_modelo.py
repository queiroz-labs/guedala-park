"""Executar na sessão FreeCAD: leitura localizada, sem recompute ou save."""
import FreeCAD as App
from pathlib import Path
import json,hashlib
here=Path(__file__).resolve().parent
d=App.ActiveDocument
assert d and d.Name=='Guedala_Park_R30_Juntas_Rotulos'
base=here.parent/'Modelo_FreeCAD/02_Revisoes_e_estudos'
bank=json.loads((base/'Banco_R16_2026-10-14/Montagem_R16.json').read_text(encoding='utf-8'))
basket=json.loads((base/'Cesto_R15_2026-10-14/Montagem_R15.json').read_text(encoding='utf-8'))
groups={
 'banco':('Modulo019',list(dict.fromkeys(bank['structure']+[x['lid'] for x in bank['lids']]+[x['cushion'] for x in bank['lids']]))),
 'cesto':('Modulo013',list(dict.fromkeys(basket['fixed']+basket['frame']+[basket['front'],basket['upper'],'Peca352','Peca353','FundoTanqueR29']))),
}
out={}
for title,(module,names) in groups.items():
    m=d.getObject(module);rows=[]
    for name in names:
        o=d.getObject(name)
        if not o or not hasattr(o,'Shape') or o.Shape.isNull():continue
        shape=o.Shape.copy()
        shape.Placement=m.getGlobalPlacement().inverse().multiply(o.getGlobalPlacement())
        b=shape.BoundBox
        rows.append({'name':name,'label':o.Label,'bbox_local_mm':[round(x,4) for x in [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]],'volume_mm3':o.Shape.Volume})
    out[title]={'module':module,'parts':rows}
out['meta']={'file':d.FileName,'sha256':hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest(),'method':'Geometria das peças selecionadas, no referencial local de cada módulo. Sem mudança de posição, movimento, recompute, auditoria global ou save. Nomes de seleção herdados de R15/R16, geometria lida na R30.'}
(here/'Geometria_atual.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
result={'bank_parts':len(out['banco']['parts']),'basket_parts':len(out['cesto']['parts']),'saved':str(here/'Geometria_atual.json')}
