import FreeCAD as A, Part, FreeCADGui as G, json, pathlib, hashlib
P=pathlib.Path(__file__).resolve().parent
src=A.getDocument('Guedala_Park_R44_Consolidado')
source_hash=hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest()
def box(x,y,z,w,d,h): return Part.makeBox(w,d,h,A.Vector(x,y,z))
def world(o):
    s=o.Shape.copy()
    if hasattr(o,'getGlobalPlacement'): s.Placement=o.getGlobalPlacement()
    return s
def feature(d,name,label,s,color=(.65,.65,.65),trans=0):
    o=d.addObject('PartDesign::Feature' if False else 'Part::Feature',name);o.Label=label;o.Shape=s
    o.ViewObject.ShapeColor=color;o.ViewObject.Transparency=trans
    return o
def copy(d,n):
    q=src.getObject(n)
    return feature(d,n,q.Label,world(q),q.ViewObject.ShapeColor)
def hit(a,b): return round(a.common(b).Volume,3) if a.BoundBox.intersect(b.BoundBox) else 0
def finish(d,file):
    d.recompute();G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();d.saveAs(str(P/file))
    return {'file':str(P/file),'invalid_shapes':[o.Name for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isValid()]}

k=A.newDocument('Apurema_atras_ESTUDO_20261023');k.Label='ESTUDO — Apurema atrás da Dora; montagem pendente'
refs=['Peca135','Peca140','Peca141','Peca308','Peca324','Peca325','Peca326','Peca327','Peca278','Peca279','Peca280','Peca276']
for n in refs:copy(k,n)
for n in ['Peca324','Peca325','Peca326','Peca327']:k.getObject(n).ViewObject.Transparency=85
# A cuba do consolidado é apenas uma caixa rasa: representação corrigida no estudo,
# preservando envelope externo e sem alterar o documento principal.
k.Peca135.ViewObject.Visibility=False
dora=box(2380,6500,735,430,370,185).cut(box(2395,6515,736,400,340,190))
feature(k,'Dora','Dora — envelope nominal; sem gabarito de fabricação',dora,(.65,.70,.73))
# Elementos são envelopes dimensionais, não reprodução industrial da torneira.
stem=Part.makeCylinder(27,250,A.Vector(2595,6925,920))
upper=box(2568,6692,1170,54,260,210.7)
feature(k,'ApuremaBase','Apurema — base Ø54 no eixo x2595/y6925',stem,(.12,.12,.12))
feature(k,'ApuremaCurva','Envelope superior 260 × 54; topo1380,7',upper,(.2,.2,.2),65)
command=box(2560,6795,962,70,130,94.5)
feature(k,'ComandoFrontal','Reserva de comando voltado à frente — curso real pendente',command,(.9,.6,.15),70)
service=Part.makeCylinder(40,682,A.Vector(2595,6925,218))
feature(k,'PercursoHipotetico','HIPÓTESE Ø80 — mangueira/contrapeso; não validada',service,(.9,.35,.2),80)
k.PercursoHipotetico.ViewObject.Visibility=False
tests=[]
for name,s in [('base',stem),('superior',upper),('comando_hipotetico',command)]:
    tests.append({'element':name,'overlaps':[{'object':n,'volume_mm3':v} for n in refs if (v:=hit(s,world(src.getObject(n))))>.1]})
kr=finish(k,'Apurema_atras_ESTUDO.FCStd')
kr.update({'test_type':'Envelopes estáticos; não valida curso da mangueira ou resistência da pedra','tests':tests,'axis_mm':[2595,6925,920],
 'strip_behind_sink_mm':110,'base_diameter_mm':54,'base_clearance_each_depth_side_mm':28,
 'base_axis_to_backsplash_mm':55,'top_to_upper_cabinet_mm':151.3,
 'hole_diameter':None,'thread_diameter_drawing_mm':31,
 'hypothetical_service_hits':[{'object':n,'volume_mm3':v} for n in refs if (v:=hit(service,world(src.getObject(n))))>.1],
 'storage':'Sem mudança da caixa ou das prateleiras no principal. Percurso real pode exigir recorte já pendente; não comprovado mesmo armazenamento utilizável.',
 'purifier_discrepancy':'CAD contém PE12G; orçamento recente refere PE11X. Nenhum foi substituído; posição à esquerda não disputa a faixa traseira da cuba.'})

b=A.newDocument('Cornalina_Verona_ESTUDO_20261023');b.Label='ESTUDO — Cornalina com torneira na louça'
for n in ['Peca399','Peca188','Peca400','Peca401','Peca402','Peca403','Peca404','EspelhoAplicadoR12','EspelhoAplicadoR001']:copy(b,n)
for n in ['Peca400','Peca401','Peca402','Peca403','Peca404','EspelhoAplicadoR12','EspelhoAplicadoR001']:b.getObject(n).ViewObject.Transparency=75
# Cuba centralizada na profundidade: margens75 frente/fundo,100 laterais.
# Interior e eixo do furo são apenas esquemáticos onde a ficha não cota.
cx,cy=3060,5172
shell=box(2860,4915,765,400,300,130).cut(box(2870,4925,785,380,280,120))
deck=box(3020,5129,785,80,86,110)
shell=shell.fuse(deck).cut(Part.makeCylinder(18.5,150,A.Vector(cx,cy,760)))
feature(b,'Cornalina','Cornalina400×300×130 — interior e eixo esquemáticos',shell,(.95,.95,.94))
medium=Part.makeCylinder(18,225,A.Vector(cx,cy,895)).fuse(box(cx-18,cy-187,1040,36,187,15))
feature(b,'VeronaMedia','Verona MÉDIA — 225; saída145; fixação NÃO validada',medium,(.12,.12,.12))
high=Part.makeCylinder(18,325,A.Vector(cx,cy,895)).fuse(box(cx-18,cy-187,1140,36,187,15))
feature(b,'VeronaAlta','Verona ALTA sobre a cuba — hipótese com interferência',high,(.9,.2,.15),50)
b.VeronaAlta.ViewObject.Visibility=False
support=Part.makeCylinder(18,2,A.Vector(cx,cy,895))
br=finish(b,'Cornalina_Verona_ESTUDO.FCStd')
br.update({'cuba_mm':[400,300,130],'rim_level_mm':895,'margins_mm':{'sides':100,'front':75,'rear':75},
 'hole_mm':37,'drawn_tap_body_mm':36,'support_overlap_if_only_body_mm':(36-37)/2,
 'actual_base_and_seal_diameter_confirmed':False,'tap_hole_axis_assumption':'43 mm da borda traseira, apenas para estudo; ficha cota mesa86 mas não o eixo.',
 'medium':{'overall_top_mm':1120,'outlet_mm':1040,'outlet_above_rim_mm':145,'top_to_cabinet_mm':30,
 'collisions':[{'object':n,'volume_mm3':v} for n in ['Peca188','Peca403','EspelhoAplicadoR12','EspelhoAplicadoR001'] if (v:=hit(medium,world(src.getObject(n))))>.1]},
 'high':{'overall_top_mm':1220,'outlet_mm':1140,'outlet_above_rim_mm':245,
 'collisions':[{'object':n,'volume_mm3':v} for n in ['Peca188','Peca403','EspelhoAplicadoR12','EspelhoAplicadoR001'] if (v:=hit(high,world(src.getObject(n))))>.1]},
 'status':'Furo na louça é funcionalmente apropriado. Verona alta não aprovada nesta posição; média depende de apoio/vedação e acesso ao comando sob o armário.'})
r={'date':'2026-10-23','source':src.FileName,'source_sha256':source_hash,'kitchen':kr,'bathroom':br,'budget_updated':False,'Bonnie':'Mantido',
 'unchanged_source_file':source_hash==hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest()}
(P/'Verificacao.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
