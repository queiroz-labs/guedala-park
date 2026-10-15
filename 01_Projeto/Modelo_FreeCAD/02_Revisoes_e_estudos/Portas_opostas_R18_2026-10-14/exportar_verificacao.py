from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();a=json.loads(((Path(__file__).resolve().parent / 'Montagem_R18.json').resolve()).read_text(encoding='utf-8'));p=Path(a['file'])
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
def matrix(o):
 m=o.getGlobalPlacement().Matrix
 return [[m.A11,m.A12,m.A13,m.A14],[m.A21,m.A22,m.A23,m.A24],[m.A31,m.A32,m.A33,m.A34],[m.A41,m.A42,m.A43,m.A44]]
def box(o):return {'name':o.Name,'label':o.Label,'matrix':matrix(o),'dimensions':[float(o.Length),float(o.Width),float(o.Height)]}
rows=[]
for r in a['doors']:
 m=d.getObject(r['module']);g=d.getObject(r['door']);panel=d.getObject(r['old_panel'])
 rows.append(dict(r,module_matrix=matrix(m),closed_leaf_base=list(g.Placement.Base),front_local_box=[panel.Placement.Base.x,0,0,panel.Placement.Base.x+float(panel.Length),float(panel.Width),float(panel.Height)],front_height=float(panel.Height),front_plan_closed=box(panel)))
targets=[]
for o in d.Objects:
 if o.TypeId=='Part::Box' and o.Name.startswith('Peca') and o.Name[4:].isdigit() and int(o.Name[4:])<235 and getattr(o,'TipoPeca','')!='Parede em corte':targets.append(box(o))
for mn in ['Modulo016','Modulo003']:
 for o in d.getObject(mn).Group:
  if o.TypeId=='Part::Box':targets.append(box(o))
for n in ['DivisorApoioVizinhaR03','FaixaFixaEstudo','ApoioPortaBR04','FaixaQuinaAR04','FaixaQuinaBR04']:
 o=d.getObject(n)
 if o is not None:targets.append(box(o))
arch=[x for x in targets if x['label'].startswith('Parede ·')]
report={'file':str(p),'rows':rows,'targets':targets,'axes_file':str((Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/Eixos_71B3550.json').resolve()),'changed_doors':a['changed_doors'],'architecture_walls':arch,'note':'Exportação numérica sem operações booleanas de ferragens. Auditoria nativa anterior foi interrompida pelo fechamento do aplicativo, sem resultado completo.'}
((Path(__file__).resolve().parent / 'Dados_plano_R18.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'rows':len(rows),'targets':len(targets),'file':str((Path(__file__).resolve().parent / 'Dados_plano_R18.json').resolve())}
