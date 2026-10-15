from pathlib import Path
import json,shutil
from datetime import datetime
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve();root.mkdir(exist_ok=True)
src=(Path(__file__).resolve().parent / '../Canto_2026-10-13/Canto_simples_R04/Guedala_Park_R04_Canto_Simples.FCStd').resolve()
original=next((d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Canto_2026-10-13/Canto_simples_R04/Guedala_Park_R04_Canto_Simples.FCStd').resolve()),None)
if original is None:original=App.openDocument(str(src))
original.save()
dest=(Path(__file__).resolve().parent / 'Guedala_Park_R05_Caixas_Gavetas.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(src,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R05 - caixas padronizadas, ferragens em conferencia'
rows=[]
for g in [o for o in doc.Objects if hasattr(o,'Extensao') and o.Label!='Gaveta baixa']:
    m=next(p for p in g.InList if p.TypeId=='App::Part')
    floor=next(o for o in g.Group if o.TypeId=='Part::Box' and o.Label.startswith('Fundo da caixa'))
    sides=sorted([o for o in g.Group if o.TypeId=='Part::Box' and o.Label.startswith('Lateral da caixa')],key=lambda o:o.Placement.Base.x)
    ends=sorted([o for o in g.Group if o.TypeId=='Part::Box' and o.Label.startswith('Travessa da caixa')],key=lambda o:o.Placement.Base.y)
    front=next(o for o in g.Group if o.TypeId=='Part::Box' and o.Label.startswith('Frente'))
    old={'outer_width_mm':float(floor.Length),'internal_width_mm':float(ends[0].Length),'depth_mm':float(floor.Width),'bottom_z_mm':floor.Placement.Base.z,'floor_thickness_mm':float(floor.Height),'nominal_travel_mm':float(g.CursoNominal)}
    midpoint=g.Placement.Base.x+floor.Placement.Base.x+float(floor.Length)/2
    support=[]
    for o in m.Group:
        if o.TypeId=='Part::Box' and float(o.Length)<=18.01 and float(o.Width)>300 and o.Placement.Base.z<=g.Placement.Base.z+80<=o.Placement.Base.z+float(o.Height):
            support.append((o.Placement.Base.x,o.Placement.Base.x+float(o.Length),o.Label))
    left=max(q for q in support if q[1]<midpoint);right=min(q for q in support if q[0]>midpoint)
    opening=right[0]-left[1];inside=opening-42;outside=inside+30
    nl=400 if 'escritório' in m.Label else 500
    depth=nl-10
    height=float(sides[0].Height)+float(floor.Height)
    sidebase=36 if g.Placement.Base.z<10 else 20
    x=(float(front.Length)-outside)/2;y=floor.Placement.Base.y
    for i,o in enumerate(sides):
        o.Placement.Base=App.Vector(x if i==0 else x+outside-15,y,sidebase)
        o.Length=15;o.Width=depth;o.Height=height
    for i,o in enumerate(ends):
        o.Placement.Base=App.Vector(x+15,y if i==0 else y+depth-15,sidebase+12)
        o.Length=inside;o.Width=15;o.Height=height-12
    floor.Placement.Base=App.Vector(x+15,y+15,sidebase+12)
    floor.Length=inside;floor.Width=depth-30;floor.Height=15
    for name,ptype in [('NLProposto','App::PropertyLength'),('VaoInternoMedido','App::PropertyLength'),('LarguraInternaProposta','App::PropertyLength'),('LarguraExternaProposta','App::PropertyLength'),('RebaixoFundoProposto','App::PropertyLength'),('AlturaUtilProposta','App::PropertyLength'),('StatusR05','App::PropertyString')]:
        if name not in g.PropertiesList:g.addProperty(ptype,name,'Conferencia R05')
    g.NLProposto=nl;g.VaoInternoMedido=opening;g.LarguraInternaProposta=inside;g.LarguraExternaProposta=outside;g.RebaixoFundoProposto=12;g.AlturaUtilProposta=height-27
    g.Ferragem='Candidata MOVENTO760H, caixa NL-10 e largura INTERNA LW-42. Ferragem ainda nao instalada nem curso real validado.'
    g.StatusR05='Caixa proposta para conferencia dimensional. Fixacao do fundo, travas, gancho traseiro, carga e conteudo pendentes. CursoNominal anterior preservado.'
    body_y=g.Placement.Base.y+y
    rear=float(m.Profundidade)-18
    rows.append({'drawer':g.Label,'name':g.Name,'module':m.Label,'old':old,'opening_mm':opening,'opening_supports':[left,right],
        'candidate':{'NL_mm':nl,'body_length_mm':depth,'inside_width_mm':inside,'outer_width_mm':outside,'side_thickness_mm':15,'bottom_recess_mm':12,'floor_thickness_mm':15,'box_side_height_mm':height,'usable_height_mm':height-27,'side_base_local_z_mm':sidebase},
        'depth_available_from_body_front_mm':rear-body_y,'runner_NL_plus3_margin_mm':rear-body_y-(nl+3),
        'notes':'Fundo entre laterais, ainda sem detalhe de encaixe/estrutura. Altura util geometricamente proposta; nao comprova conteudo. NL500 no roupeiro nao autoriza novo curso500, a verificar com cama e portas de correr.'})
office=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label=='Gaveteiro do escritório')
office.Placement=App.Placement(App.Vector(3100,700,480),App.Rotation(App.Vector(0,0,1),180))
if 'CorrecaoOrientacaoR05' not in office.PropertiesList:office.addProperty('App::PropertyString','CorrecaoOrientacaoR05','Conferencia R05')
office.CorrecaoOrientacaoR05='Mesmo envelope x2700..3100/y250..700; frente em y700, abertura para+Y, conforme Setup_e_caixa_R10. A orientacao anterior abriu para parede.'
ward=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('Guarda-roupa'))
right=next(o for o in ward.Group if o.Label=='Porta de correr inferior 2')
right.setExpression('Placement.Base.x','985 mm - Deslocamento')
doc.recompute();doc.save()
report={'file':str(dest),'drawer_count':len(rows),'source':'https://publications.blum.com/2024/catalogue/en/413/',
    'scope':'Conferencia dimensional de caixas com referencias MOVENTO. Nao representa montagem de corrediças ou validacao do movimento real. Gaveta baixa de limpeza preservada com mecanismo proprio pendente.',
    'critical_correction':'LW-42 e a largura INTERNA, nao externa. Com laterais15, largura externa=LW-12.',
    'drawers':rows,'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]}
((Path(__file__).resolve().parent / 'Caixas_dimensoes_R05.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'file':str(dest),'drawers':[{'drawer':r['drawer'],'LW':r['opening_mm'],'new':r['candidate'],'depth_margin':r['runner_NL_plus3_margin_mm']} for r in rows],'invalid':report['invalid']},ensure_ascii=False)
