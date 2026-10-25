"""Estudo de sensibilidade; nao substitui geometria industrial nem aprova o produto."""
import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, hashlib, math
P=pathlib.Path(__file__).resolve().parent
source=A.getDocument('Guedala_Park_R45_EM_REVISAO')
before=hashlib.sha256(pathlib.Path(source.FileName).read_bytes()).hexdigest()
def world(o):
 s=o.Shape.copy()
 if hasattr(o,'getGlobalPlacement'): s.Placement=o.getGlobalPlacement()
 return s
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,A.Vector(x,y,z))
def add(doc,name,shape,color,trans=0):
 o=doc.addObject('Part::Feature',name);o.Shape=shape;o.ViewObject.ShapeColor=color;o.ViewObject.Transparency=trans;return o
names=['Peca188','Peca403','EspelhoAplicadoR12','EspelhoAplicadoR001']
refs={n:world(source.getObject(n)) for n in names}
cx,cy,zbase=3060.,5172.,895.
# Dimensoes externas publicadas; corpo/base/furo alinhados por hipotese.
fixed=box(cx-22.5,cy-22.5,zbase,45,45,6).fuse(box(cx-17.5,cy-17.5,zbase+6,35,35,121)).fuse(box(cx-17.5,cy-152.5,zbase+112,35,170,15))
# Caixa envolvente da alavanca: volutariamente inclui vazios da peca.
closed=box(cx-17.5,cy-70.5,zbase+127,35,88,28)
def clearance(s,n):
 return {'distance_mm':round(s.distToShape(refs[n])[0],3),'overlap_mm3':round(s.common(refs[n]).Volume,3)}
cases=[]
for pz in [127,141,155]:
 for py in [-17.5,0,17.5]:
  pivot=A.Vector(cx,cy+py,zbase+pz)
  for pitch in [0,15,30,45,60]:
   for yaw in [-45,0,45]:
    s=closed.copy();s.rotate(pivot,A.Vector(1,0,0),-pitch);s.rotate(pivot,A.Vector(0,0,1),yaw)
    cases.append({'pivot_z_above_base_mm':pz,'pivot_y_offset_mm':py,'pitch_deg':pitch,'yaw_deg':yaw,'top_mm':round(s.BoundBox.ZMax,3),'tests':{n:clearance(s,n) for n in names}})
doc=A.newDocument('Purangi_R45_SENSIBILIDADE_20261023');doc.Label='Purangi na Cornalina - ESTUDO NAO APROVADO'
for n in ['Peca399','Peca188','Peca400','Peca401','Peca402','Peca403','Peca404','EspelhoAplicadoR12','EspelhoAplicadoR001']:
 o=source.getObject(n);add(doc,n,world(o),o.ViewObject.ShapeColor,75 if n!='Peca188' else 0)
old=A.getDocument('Cornalina_Verona_ESTUDO_20261023')
add(doc,'CornalinaHipotese',world(old.getObject('Cornalina')),(.9,.9,.9),35)
add(doc,'PurangiCorpoEnvelope',fixed,(.08,.08,.08))
add(doc,'AlavancaFechadaEnvelope',closed,(.1,.1,.1),30)
opening=closed.copy();opening.rotate(A.Vector(cx,cy,zbase+127),A.Vector(1,0,0),-45)
add(doc,'HIPOTESE_45graus_pivo127',opening,(.95,.55,.08),45)
doc.addObject('App::FeaturePython','Premissas')
for key,val in {'Status':'NAO APROVADO: pivo, curso, vedacao e eixo do furo sem cotas oficiais','Metodo':'Caixa envolvente; pitch0/15/30/45/60 e yaw-45/0/45; pivos hipoteticos','Fonte':'Purangi HTC0757; desenho155x170x35, base45x45, alavanca88x28','Referencia':'R45 preservada; Cornalina na implantacao hipotetica anterior'}.items():
 doc.Premissas.addProperty('App::PropertyString',key);setattr(doc.Premissas,key,val)
doc.recompute();doc.saveAs(str(P/'Purangi_R45_SENSIBILIDADE.FCStd'))
G.activeDocument().activeView().viewRight();G.activeDocument().activeView().fitAll()
G.activeDocument().activeView().saveImage(str(P/'Purangi_sensibilidade.png'),1300,1000,'White')
report={'status':'PENDENTE, NAO INCORPORAR','source_file':source.FileName,'source_sha256_before':before,'source_sha256_after':hashlib.sha256(pathlib.Path(source.FileName).read_bytes()).hexdigest(),'assumptions':{'base_z':zbase,'hole_axis':[cx,cy],'pivot_range_z':[127,155],'pivot_range_y':[-17.5,17.5],'envelope':[35,88,28],'certified_opening':False},'context':{n:[s.BoundBox.XMin,s.BoundBox.YMin,s.BoundBox.ZMin,s.BoundBox.XMax,s.BoundBox.YMax,s.BoundBox.ZMax] for n,s in refs.items()},'closed':{n:clearance(closed,n) for n in names},'fixed':{n:clearance(fixed,n) for n in names},'case_count':len(cases),'cases':cases,'invalid_study_shapes':[o.Name for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isValid()]}
(P/'Purangi_abertura_R45.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
