import FreeCAD as A, Part, json, pathlib, hashlib, itertools, traceback

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'Montagem_vertical_R02'
OUT.mkdir(exist_ok=True)
DATA = json.loads((ROOT / 'Geometria_extraida_R42.json').read_text(encoding='utf-8-sig'))
SRC = pathlib.Path(DATA['source'])

def bounds(s):
    b=s.BoundBox
    return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]

def box(b):
    return Part.makeBox(b[3]-b[0],b[4]-b[1],b[5]-b[2],A.Vector(*b[:3]))

def main():
    source_for_fronts=next(doc for doc in A.listDocuments().values() if doc.FileName and pathlib.Path(doc.FileName)==SRC)
    def exact_front(name):
        o=source_for_fronts.getObject(name);s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
    d=A.newDocument('Escritorio_Montagem_Vertical_R02')
    original=d.addObject('App::DocumentObjectGroup','Referencia_R42')
    car=d.addObject('App::DocumentObjectGroup','Carcaca_470x248')
    storage=d.addObject('App::DocumentObjectGroup','Volumes_uteis_comparacao')
    carc={}; before={}; drawers=[]; metrics=[]
    def add(group,name,label,s,color=(0.72,0.63,0.46)):
        o=d.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=s;group.addObject(o)
        o.ViewObject.ShapeColor=color
        return o
    for n in ['Peca367','Peca368','Peca369','Peca370','Peca371']:
        b=list(DATA['objects'][n]['bbox_world']);s=box(b);before[n]=s
        add(original,'Antes_'+n,DATA['objects'][n]['label']+' — referência',s)
        if n in ['Peca367','Peca368']:
            b[1]-=20;b[2]-=8
        elif n=='Peca369':
            b[1]-=20;b[4]-=20;b[2]-=8
        elif n=='Peca370':
            b[1]-=20;b[2]-=8;b[5]-=8
        else:b[1]-=20
        carc[n]=box(b)
        add(car,'Novo_'+n,DATA['objects'][n]['label']+' — proposta',carc[n])
    for i,(name,side,front) in enumerate([
        ('Gaveta008','GavetaComumR072','GavetaComumR077'),
        ('Gaveta009','GavetaComumR084','GavetaComumR089')]):
        g=d.addObject('App::Part','Caixa_'+name)
        g.Label=('Inferior' if i==0 else 'Superior')+' — caixa e frente; curso de estudo'
        g.addProperty('App::PropertyLength','Extensao','Movimento');g.Extensao=0
        g.addProperty('App::PropertyString','Limite','Movimento');g.Limite='0 a 375 mm nominal; ensaio geométrico, sem perfil/engate físico'
        g.setExpression('Placement.Base.y','Extensao')
        z=DATA['objects'][side]['bbox_world'][2]-[8,4][i]
        # Madeira reconstruída, sem escalar ferragens ou sólidos oficiais.
        left=box([4323.5,282,z,4338.5,682,z+80])
        right=box([4661.5,282,z,4676.5,682,z+80])
        floor=box([4333.5,282,z+12,4666.5,682,z+27])
        left=left.cut(floor);right=right.cut(floor)
        pieces={
            'Lateral_E':left,'Lateral_D':right,'Fundo':floor,
            'Traseira':box([4338.5,282,z+27,4661.5,297,z+80]),
            'Dianteira':box([4338.5,666,z+27,4661.5,682,z+80]),
            'Frente':exact_front(front)}
        for key,s in pieces.items():add(g,name+'_'+key,key+' — '+name,s,(0.8,0.7,0.49) if key!='Frente' else (0.36,0.46,0.39))
        drawers.append(pieces)
        h=60.4 if i==0 else 54.0
        prism=box([4338.5,297,z+27,4661.5,666,z+27+h])
        pv=add(storage,'Util_'+name,'Volume de referência preservado — '+name,prism,(0.15,0.75,0.42));pv.ViewObject.Transparency=70
        metrics.append({'drawer':name,'before_internal_mm':[322,359,h],
            'candidate_internal_mm':[323,369,h],
            'before_reference_volume_l':322*359*h/1e6,
            'candidate_reference_volume_l':prism.Volume/1e6,
            'side_height_mm':80,'height_above_floor_mm':53,
            'floor_top_z_mm':z+27,'storage_prism':bounds(prism),
            'guide_lower_plane_inferred_mm':z+12-27,
            'note':'Reference useful height from R42 properties, not certified usable capacity. Guide/clip profile pending.'})
    # Check real new wooden solids, including grooves, not only enclosing boxes.
    collisions=[];pairs=0
    allparts=list(carc.items())+[(str(i)+'_'+k,s) for i,p in enumerate(drawers) for k,s in p.items()]
    for (na,sa),(nb,sb) in itertools.combinations(allparts,2):
        pairs+=1;v=sa.common(sb).Volume
        if v>0.001:collisions.append({'a':na,'b':nb,'volume_mm3':v})
    storage_hits=[]
    for i,m in enumerate(metrics):
        p=box(m['storage_prism'])
        for n,s in allparts:
            v=p.common(s).Volume
            if v>0.001:storage_hits.append({'drawer':i,'part':n,'volume_mm3':v})
    # Sample the whole nominal course plus the documented +3mm course tolerance.
    motion_hits=[];motion_checks=0
    for i,items in enumerate(drawers):
        fixed=list(carc.items())+[(str(1-i)+'_'+k,s) for k,s in drawers[1-i].items()]
        compound=Part.makeCompound(list(items.values()))
        for course in list(range(0,376,5))+[378]:
            moving=compound.copy();moving.translate(A.Vector(0,course,0))
            for n,s in fixed:
                motion_checks+=1
                if not moving.BoundBox.intersect(s.BoundBox):continue
                v=moving.common(s).Volume
                if v>0.001:motion_hits.append({'drawer':i,'course':course,'part':n,'volume_mm3':v})
    external=[];external_checked=0;source_doc=None
    for doc in A.listDocuments().values():
        if doc.FileName and pathlib.Path(doc.FileName)==SRC:source_doc=doc;break
    if source_doc:
        for n,s in carc.items():
            delta=s.cut(before[n])
            if delta.isNull() or delta.Volume<0.001:continue
            for o in source_doc.Objects:
                if o.Name in carc or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull():continue
                q=o.Shape.copy()
                if hasattr(o,'getGlobalPlacement'):q.Placement=o.getGlobalPlacement()
                if not delta.BoundBox.intersect(q.BoundBox):continue
                external_checked+=1;v=delta.common(q).Volume
                if v>0.001:external.append({'new':n,'other':o.Name,'label':o.Label,'volume_mm3':v})
    note=d.addObject('App::FeaturePython','Limites_do_estudo')
    note.addProperty('App::PropertyString','Escopo');note.Escopo='Madeira e espaço útil em estudo. Não contém guias/engates FGVTN oficiais nem furação liberada. Caixa inferior -8mm e superior -4mm; base -8mm, traseira +20mm. Frentes fixas; junta 2mm.'
    note.addProperty('App::PropertyString','Regulagem');note.Regulagem='Folga superior 5mm permite subida da caixa +3mm com 2mm residual. Frentes exigem alinhamento final independente: regulagens diferenciais podem consumir junta de 2mm.'
    for o in original.Group:o.Visibility=False
    original.Visibility=False
    storage.Visibility=False
    for o in storage.Group:o.Visibility=False
    d.recompute()
    invalid=[o.Name for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
    output=OUT/'Escritorio_montagem_vertical_R02_ESTUDO.FCStd'
    d.saveAs(str(output))
    report={'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'source_unchanged':hashlib.sha256(SRC.read_bytes()).hexdigest()==DATA['sha256'],
        'carcass_external_before_mm':[400,450,240],'carcass_external_after_mm':[400,470,248],
        'front_positions_unchanged':True,'front_gap_mm':2,'top_clearance_before_after_mm':[1,5],
        'base_clearance_inferred_before_after_mm':[4,4],
        'metrics':metrics,'wood_pair_checks':pairs,'wood_collisions':collisions,
        'storage_prism_collisions_wood':storage_hits,'motion_checks':motion_checks,'motion_hits':motion_hits,
        'external_source_loaded':source_doc is not None,'external_pair_checks':external_checked,'external_collisions':external,
        'invalid_shapes':invalid,'output':str(output),
        'limits':['No exact runner/clip geometry; guide datum inferred from drawing.',
                  'No released holes, rear notches, load or manufacturing approval.',
                  '8mm extra exterior projection below cabinet; front alignment must be retained.',
                  'Motion checks sampled at 5mm and end 378; not continuous collision proof.']}
    (OUT/'Verificacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    import FreeCADGui as G
    G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll()
    G.activeDocument().activeView().saveImage(str(OUT/'Montagem_fechada.png'),1400,1000,'White')
    return d

try:main()
except Exception:
    (OUT/'erro.txt').write_text(traceback.format_exc(),encoding='utf-8')
    raise

