from pathlib import Path
import json,runpy
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
p=(Path(__file__).resolve().parent / 'Guedala_Park_R14_Correr_Simples.FCStd').resolve()
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==p)
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R14.json').resolve()).read_text(encoding='utf-8'))
def descendants(o):
 out=[]
 for q in getattr(o,'Group',[]):out.append(q);out+=descendants(q)
 return out
def visible(o):
 if o.Name.startswith('Ambiente_'):return True
 if hasattr(o,'Visibility') and not o.Visibility:return False
 return all(visible(a) for a in o.InList if a.TypeId in ['App::Part','App::DocumentObjectGroup'])
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def volume(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
sheet=next(o for o in d.Objects if o.Name.startswith('ControleSimplesR04'))
row=data['rows'][1]
corner=[o for o in descendants(d.getObject('CantoSimplesR04')) if 'Shape' in o.PropertiesList and o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina'))]
corner += [d.getObject(n) for n in ['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal']]
maleiro=[o for o in descendants(d.getObject('Modulo002')) if 'Shape' in o.PropertiesList and o.Shape.Volume>0 and visible(o)]
cases=[]
for angle in [0,45,86]:
 sheet.set('B2',str(angle)+' deg');sheet.set('B3',str(angle)+' deg')
 for side in [0,1]:
  for n in row['controls']:d.getObject(n).Deslocamento=0
  d.getObject(row['controls'][side]).Deslocamento=row['course'];d.recompute();hits=[]
  for o in maleiro:
   for q in corner:
    v=volume(shape(o),shape(q))
    if v>.1:hits.append({'maleiro':o.Name,'corner':q.Name,'mm3':v})
  cases.append({'corner_deg':angle,'sliding_open_leaf':side+1,'hits':hits})
sheet.set('B2','0 deg');sheet.set('B3','0 deg')
for row in data['rows']:
 for n in row['controls']:d.getObject(n).Deslocamento=0
d.recompute();d.save()
# Reopen only once; a later scope correction must not repeat an already-valid reopen.
if not ((Path(__file__).resolve().parent / 'Canto_reabertura_R14.json').resolve()).exists():
 assert d.isSaved() and p.exists() and p.stat().st_size>100000
 App.closeDocument(d.Name);d=App.openDocument(str(p))
checks=[]
for row in data['rows']:
 for i,n in enumerate(row['controls']):
  c=d.getObject(n);c.Deslocamento=row['course'];d.recompute();driver=d.getObject(row['drivers'][i]);leaf=d.getObject(row['leaves'][i]);pos=list(driver.Placement.Base)
  expected=row['right']-row['course'] if i else 20+row['course']
  checks.append({'control':n,'input_mm':float(c.Deslocamento),'placement_mm':pos,'expected_x':expected,'expression_ok':abs(pos[0]-expected)<1e-7,'leaf_valid':leaf.Shape.isValid(),'leaf_state':list(leaf.State)})
  c.Deslocamento=0
d.recompute();d.save()
out={'file':str(p),'corner_vs_changed_maleiro':cases,'corner_targets':len(corner),'maleiro_targets':len(maleiro),'reopening_checks':checks,'inputs_final_mm':[float(d.getObject(n).Deslocamento) for row in data['rows'] for n in row['controls']], 'limits':'Seis cenários de encontro com canto R04, somente contra novo maleiro. Não repetição da cinemática R04 nem confirmação dos mecanismos/gabaritos.'}
((Path(__file__).resolve().parent / 'Canto_reabertura_R14.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');result=out
