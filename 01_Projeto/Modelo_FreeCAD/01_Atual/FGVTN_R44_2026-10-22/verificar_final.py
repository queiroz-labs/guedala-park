import FreeCAD as A,pathlib,json,hashlib
p=pathlib.Path(__file__).parent;f=p/'Guedala_Park_R44_Consolidado.FCStd';d=A.openDocument(str(f))
r={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'official':[],'berlin':[],'bank':[],'bathroom':[]}
for o in d.Objects:
 if not hasattr(o,'Shape') or hasattr(o,'Group'):continue
 target='official' if o.Name.startswith('FGVTN_R44_') else 'berlin' if o.Name.startswith(('Fechada_','Aberta_')) else 'bank' if o.Name in ['BancoR43_Painel1','BancoR43_Painel2'] else 'bathroom' if o.Name.startswith('BC43_') else None
 if target:r[target].append({'name':o.Name,'null':o.Shape.isNull(),'valid':o.Shape.isValid(),'solids':len(o.Shape.Solids)})
assert len(r['official'])==12 and all(not x['null'] and x['valid'] for x in r['official'])
assert len(r['berlin'])==15 and all(not x['null'] and x['valid'] for x in r['berlin'])
assert len(r['bank'])==2 and all(not x['null'] and x['valid'] for x in r['bank'])
assert all(not x['null'] and x['valid'] for x in r['bathroom'])
(p/'Validacao_formas_R44.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf8')
print('OK', {k:len(v) for k,v in r.items() if isinstance(v,list)})
