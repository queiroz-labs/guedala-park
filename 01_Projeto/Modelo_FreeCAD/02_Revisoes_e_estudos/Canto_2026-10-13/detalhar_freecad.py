from pathlib import Path
import json
import math
import shutil
import FreeCAD as App
import FreeCADGui as Gui
import Part
HERE=(Path(__file__).resolve().parent / '.').resolve()
MODEL=(Path(__file__).resolve().parent / '../../03_Recursos/output/Guedala_Park_R01.FCStd').resolve()
DEST=(Path(__file__).resolve().parent / 'Guedala_Park_R02_Canto.FCStd').resolve()
for existing in list(App.listDocuments().values()):
    if existing.FileName and Path(existing.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R02_Canto.FCStd').resolve():
        App.closeDocument(existing.Name)
shutil.copy2(MODEL,DEST)
doc=App.openDocument(str(DEST))
doc.Label='Guedala Park · R02 · canto em conferência'
corner=next(o for o in doc.Objects if o.Label.startswith('Canto integrado em L') and o.TypeId=='App::Part')
maleiro=next(o for o in doc.Objects if o.Label.startswith('Maleiro reto') and o.TypeId=='App::Part')
aerial=next(o for o in doc.Objects if o.Label.startswith('Aéreo raso da cabeceira') and o.TypeId=='App::Part')
room=next(o for o in doc.Objects if o.Name.startswith('Ambiente_quarto'))
A=next(o for o in corner.Group if o.Label.startswith('Frente articulada A'))
B=next(o for o in corner.Group if o.Label.startswith('Frente articulada B'))
controls=doc.addObject('Spreadsheet::Sheet','ControleCanto')
controls.Label='Canto · ângulos e variantes · giro ideal'
for i,(label,value,alias) in enumerate([
    ('Principal: domínio de estudo 0 a 92°','0 deg','Alpha'),
    ('Articulação: domínio de estudo 0 a 60°','0 deg','Beta'),
    ('Porta vizinha: 0 a 90°','0 deg','Vizinha'),
    ('Faixa fixa: proposta 150 mm; zero reproduz R01','150 mm','Faixa'),
    ('Junta horizontal: hipótese para detalhar','3 mm','Junta'),
    ('Nominal da folha de canto: não é corte acabado','400 mm','Folha'),
    ('Recuo da faixa fixa: proposta de estudo','40 mm','Recuo')],2):
    controls.set('A'+str(i),label);controls.set('B'+str(i),value);controls.setAlias('B'+str(i),alias)
controls.setColumnWidth('A',420);controls.setColumnWidth('B',140)
corner.addProperty('App::PropertyString','ModeloDeMovimento','Conferência')
corner.ModeloDeMovimento='Dois eixos ideais independentes; não reproduz o mecanismo multilink Blum.'
corner.addProperty('App::PropertyLink','Controles','Conferência');corner.Controles=controls
N=controls.Name
for o in [A,B]:
    o.setExpression('Length',N+'.Folha - 2 * '+N+'.Junta')
    o.Width=18
    o.Height=306
    o.addProperty('App::PropertyString','FerragemCandidata','Conferência')
    o.addProperty('App::PropertyString','Corte','Conferência')
    o.Corte='400 mm é faixa nominal. Junta 3 mm e painel 394 mm são hipótese; aplicar fórmula Blum após fechar calços e recobrimentos.'
A.FerragemCandidata='71T7550 + limitador 70T7553.09 de 92°, sem amortecimento integrado'
B.FerragemCandidata='79T8500, articulação 60°, caneco fixado na folha A'
A.setExpression('Placement.Base.x','650 mm - '+N+'.Junta * cos('+N+'.Alpha) - 18 mm * sin('+N+'.Alpha)')
A.setExpression('Placement.Base.y','-650 mm - '+N+'.Junta * sin('+N+'.Alpha) + 18 mm * cos('+N+'.Alpha)')
A.setExpression('Placement.Rotation.Angle','180 deg + '+N+'.Alpha')
B.setExpression('Placement.Base.x','650 mm - 400 mm * cos('+N+'.Alpha) + '+N+'.Junta * sin('+N+'.Alpha + '+N+'.Beta) - 18 mm * cos('+N+'.Alpha + '+N+'.Beta)')
B.setExpression('Placement.Base.y','-650 mm - 400 mm * sin('+N+'.Alpha) - '+N+'.Junta * cos('+N+'.Alpha + '+N+'.Beta) - 18 mm * sin('+N+'.Alpha + '+N+'.Beta)')
B.setExpression('Placement.Rotation.Angle',N+'.Alpha + '+N+'.Beta - 90 deg')
A.ViewObject.ShapeColor=(.17,.47,.57);B.ViewObject.ShapeColor=(.81,.55,.25)
leafgroups=[o for o in aerial.Group if o.TypeId=='App::Part' and hasattr(o,'Abertura')]
leafgroups.sort(key=lambda o:float(o.Placement.Base.x))
for i,p in enumerate(leafgroups):
    p.setExpression('Placement.Base.x','(1800 mm - '+N+'.Faixa) * '+str(i)+' / 4 + 1 mm')
    p.setExpression('Abertura','-'+N+'.Vizinha' if i==3 else '0 deg')
    front=next(o for o in p.Group if o.TypeId=='Part::Box')
    front.setExpression('Length','(1800 mm - '+N+'.Faixa) / 4 - 2 mm')
    if i==3:
        front.ViewObject.ShapeColor=(.66,.26,.24)
neighbour=next(o for o in leafgroups[3].Group if o.TypeId=='Part::Box')
fixed=doc.addObject('Part::Box','FaixaFixaEstudo');aerial.addObject(fixed)
fixed.Label='Faixa fixa · proposta, não aprovada'
fixed.Length=132;fixed.Width=18;fixed.Height=272;fixed.Placement.Base=App.Vector(1650,40,18)
fixed.setExpression('Length','max(1 mm, '+N+'.Faixa - ('+N+'.Recuo == 0 mm ? 0 mm : 18 mm))')
fixed.setExpression('Placement.Base.x','1800 mm - '+N+'.Faixa')
fixed.setExpression('Placement.Base.y',N+'.Recuo')
fixed.setExpression('Height',N+'.Recuo == 0 mm ? 306 mm : 272 mm')
fixed.setExpression('Placement.Base.z',N+'.Recuo == 0 mm ? 1 mm : 18 mm')
fixed.ViewObject.ShapeColor=(.78,.67,.48)
fixed.addProperty('App::PropertyString','Status');fixed.Status='Somente variante de estudo; NÃO registrar como medida aprovada.'

# Hardware references are translucent clearance markers, not imported manufacturer CAD.
hardware=doc.addObject('App::DocumentObjectGroup','ReferenciasFerragens');room.addObject(hardware)
hardware.Label='Ferragens · referências de montagem, sem CAD real'
for z in [51,255]:
    for panel,edge,label,depth in [(A,'principal','71T7550 · caneco candidato',13),(A,'articulacao','79T8500 · caneco na A',11)]:
        marker=doc.addObject('Part::Cylinder','ReferenciaCaneco');hardware.addObject(marker)
        marker.Label=label;marker.Radius=17.5;marker.Height=depth
        marker.addProperty('App::PropertyString','Status')
        marker.Status='Gabarito visual Ø35; posição/furação não liberadas. Confirmar eixos e recobrimentos no configurador.'
        # Both cups are on A. Boring of the bi-fold cup is not fixed from an uncertain diagram.
        marker.ViewObject.ShapeColor=(.48,.50,.52);marker.ViewObject.Transparency=55
        marker.Placement=App.Placement(App.Vector(10+(627.5 if edge=='principal' else 272.5),3940-645,2132+z),App.Rotation(App.Vector(1,0,0),90))
hardware.ViewObject.Visibility=False

def pose(alpha,beta,adj,filler,recess=40):
    controls.set('B2',str(alpha)+' deg');controls.set('B3',str(beta)+' deg')
    controls.set('B4',str(adj)+' deg');controls.set('B5',str(filler)+' mm')
    controls.set('B8',str(recess)+' mm')
    if filler==0:
        fixed.ViewObject.Visibility=False
    else:
        fixed.ViewObject.Visibility=True
    doc.recompute();Gui.updateGui()

def shape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s

for o in doc.Objects:
    if o.Name.startswith('Ambiente_'):
        o.ViewObject.Visibility=(o==room)
for key in ['ParedesInteiras','ParedesCortadas']:
    o=doc.getObject(key)
    if o:o.ViewObject.Visibility=False
for o in room.Group:
    o.ViewObject.Visibility=o in [corner,maleiro,aerial]
hardware.ViewObject.Visibility=False
for o in corner.Group:
    if o.Label.startswith('Suporte geométrico'):o.ViewObject.Visibility=False
Gui.activeDocument().activeView().viewAxonometric()
poses=[]
for name,alpha,beta,adj,filler,recess in [
    ('R01_colisao',10,0,11.055,0,40),
    ('Faixa_alinhada_bate',1,0,0,150,0),
    ('Faixa_recuada_inicio',1,0,0,150,40),
    ('R02_mesma_abertura',10,0,11.055,150,40),
    ('R02_posicao_critica',23.75,0,24,150,40),
    ('R02_abertura_maxima',92,60,90,150,40),
    ('R03_faixa20_abertura',92,60,90,200,40),
    ('Sem_limitador_155',155,60,0,150,40)]:
    pose(alpha,beta,adj,filler,recess)
    sa,sb,sn=shape(A),shape(B),shape(neighbour)
    intersection=sa.common(sn).Volume+sb.common(sn).Volume
    distance=min(sa.distToShape(sn)[0],sb.distToShape(sn)[0])
    maleiro_parts=[o for o in maleiro.Group if hasattr(o,'Shape') and o.Label.startswith('Frente de correr')]
    overlap_maleiro=sum(sb.common(shape(o)).Volume for o in maleiro_parts)
    fixed_collision=0 if filler==0 else sa.common(shape(fixed)).Volume+sb.common(shape(fixed)).Volume
    poses.append({'name':name,'alpha':alpha,'beta':beta,'neighbour':adj,'filler_mm':filler,
        'neighbour_intersection_mm3':round(intersection,3),'distance_to_neighbour_mm':round(distance,3),
        'recess_mm':recess,'intersection_with_fixed_strip_mm3':round(fixed_collision,3),
        'intersection_with_maleiro_fronts_mm3':round(overlap_maleiro,3)})
    A.ViewObject.ShapeColor=(.17,.47,.57);B.ViewObject.ShapeColor=(.81,.55,.25)
    if intersection or overlap_maleiro or fixed_collision:B.ViewObject.ShapeColor=(.85,.18,.18)
    Gui.activeDocument().activeView().fitAll();Gui.updateGui()
    Gui.activeDocument().activeView().saveImage(str(HERE/(name+'.png')),1600,1100,'White')
pose(0,0,0,150)
Gui.activeDocument().activeView().fitAll()
doc.recompute()
invalid=[o.Name for o in doc.Objects if 'Invalid' in o.State]
report={'file':str(DEST),'poses':poses,'invalid_objects':invalid,
        'manufacturer_linkage_imported':False,'default_variant':'Faixa nominal 150 mm, recuada 40 mm: proposta, não aprovada.',
        'scope':'Colisões 3D em poses selecionadas + varredura 2D independente. Giro ideal, não modelo cinemático das dobradiças reais.'}
doc.saveAs(str(DEST))
((Path(__file__).resolve().parent / 'Conferencia_FreeCAD.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
