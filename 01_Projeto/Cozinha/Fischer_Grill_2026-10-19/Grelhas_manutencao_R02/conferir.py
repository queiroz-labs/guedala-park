"""Grelhas removíveis e retirada: complemento isolado da R01, sem salvar fontes."""
from pathlib import Path
import sys,math,json,hashlib,itertools
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App,Part
here=Path(__file__).resolve().parent
r01=here.parent/'Apoios_ventilacao_R01'
rep=json.loads((r01/'Conferencia.json').read_text(encoding='utf-8'))
srcpath=Path(json.loads((here.parent/'Conferencia_Fischer.json').read_text(encoding='utf-8'))['source'])
paths=[srcpath,r01/'Apoios_Ventilacao_R01.FCStd']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
previous=App.openDocument(str(paths[1])); original=App.openDocument(str(srcpath))
doc=App.newDocument('Grelhas_Manutencao_R02');shapes={};kinds={};rows={}
def add(n,s,kind,note):
 assert s.isValid(),n
 obj=doc.addObject('Part::Feature',n);obj.Shape=s
 obj.addProperty('App::PropertyString','Limite','Estudo');obj.Limite=note
 shapes[n]=s;kinds[n]=kind
 rows[n]={'kind':kind,'volume_mm3':round(s.Volume,5),'note':note}
 return s
for n,row in rep['objects'].items():
 if n=='ArSaida':continue
 add(n,previous.getObject(n).Shape.copy(),row['kind'],row['limit'])
# O acabamento superior fica recuado26 desde a frente do forno. O caminho
# termina agora na face da grelha, sem fingir passagem através de chapa sólida.
add('ArSaida',Part.makeBox(560,596,60,App.Vector(2946.5,6404,705)),'ar','Passagem até a grelha recuada; saída na faceY6402,5.')
def rounded_box(x,y,z,w,h,r,t):
 s=Part.makeBox(w-2*r,t,h,App.Vector(x+r,y,z))
 s=s.fuse(Part.makeBox(w,t,h-2*r,App.Vector(x,y,z+r)))
 for xx in [x+r,x+w-r]:
  for zz in [z+r,z+h-r]:
   s=s.fuse(Part.makeCylinder(r,t,App.Vector(xx,y,zz),App.Vector(0,1,0)))
 return s.removeSplitter()
slot_area=134*17-(4-math.pi)*3**2
slots=[];mounting=[]
for name,y,z0 in [('Inferior',6406.5,15),('Superior',6402.5,690)]:
 plate=rounded_box(2926.5,y,z0,600,90,2,1.5)
 cutters=[]
 for i in range(4):
  for j in range(3):
   void=rounded_box(2926.5+23+140*i,y,z0+17+19.5*j,134,17,3,1.5)
   cutters.append(void);slots.append(void)
   plate=plate.cut(void)
 for xx in [3026.5,3426.5]:
  for zz in [z0+7.5,z0+82.5]:
   plate=plate.cut(Part.makeCylinder(2.25,1.5,App.Vector(xx,y,zz),App.Vector(0,1,0)))
 add('Grelha'+name,plate.removeSplitter(),'proposta','Peça candidata inox1,5;600x90,12 rasgos134x17R3,4furos4,5. Sem liberação de corte, cor ou compra; não recebe peso do forno.')
 # Réguas do acabamento ficam fora do vão de ar60, com furação alinhada.
 for pos,z in [('Baixa',z0-3),('Alta',z0+75)]:
  rail=Part.makeBox(577,18,18,App.Vector(2938,y+1.5,z))
  zz=z0+7.5 if pos=='Baixa' else z0+82.5
  for xx in [3026.5,3426.5]:
   rail=rail.cut(Part.makeCylinder(2.25,18,App.Vector(xx,y+1.5,zz),App.Vector(0,1,0)))
  add('Regua'+name+pos,rail,'proposta','Régua de acabamento18x18 ligada às laterais; furo4,5 para montagemM4 com retenção mecânica a detalhar. Não é apoio do forno.')
 mounting.append({'grille':name,'plane_front_y_mm':y,'z_range_mm':[z0,z0+90],
                  'fixing_x_mm':[3026.5,3426.5],'fixing_z_mm':[z0+7.5,z0+82.5],
                  'rail_z_ranges_mm':[[z0-3,z0+15],[z0+75,z0+93]]})
airparts=[shapes[n] for n in shapes if kinds[n]=='ar']+slots
air=airparts[0]
for a in airparts[1:]:air=air.fuse(a)
air=air.removeSplitter();assert air.isValid() and len(air.Solids)==1
kernel_area=sum(s.Volume for s in slots[:12])/1.5/100
assert abs(kernel_area-12*slot_area/100)<1e-6,(kernel_area,12*slot_area/100)
solids=[n for n in shapes if kinds[n] in ['referencia','proposta']]
pairs=[]
for a,b in itertools.combinations(solids,2):
 if kinds[a]==kinds[b]=='referencia':continue
 v=round(shapes[a].common(shapes[b]).Volume,5)
 pairs.append({'a':a,'b':b,'overlap_mm3':v})
hits=[p for p in pairs if p['overlap_mm3']>.1];assert not hits,hits
airhits={n:round(air.common(shapes[n]).Volume,5) for n in solids+['Cooktop131']}
assert not any(v>.1 for v in airhits.values()),airhits
# Retirada horizontal ideal: dois volumes separados respeitam a diferença
# de cotas frente/chassi. A caixa única do conjunto criaria falsos conflitos.
front_sweep=Part.makeBox(595,626,447,App.Vector(2929,5778,123))
body_sweep=Part.makeBox(560,1147,432,App.Vector(2946.5,5804,138))
withdrawal=front_sweep.fuse(body_sweep)
new_hits={n:round(withdrawal.common(shapes[n]).Volume,5) for n in solids if n not in ['Frente','CorpoConservador']}
assert not any(v>.1 for v in new_hits.values()),new_hits
native_count=0;native_hits=[];nearby=[]
for obj in original.Objects:
 if not obj.Name.startswith('Peca') or obj.Name in ['Peca133','Peca307'] or not hasattr(obj,'Shape') or obj.Shape.isNull():continue
 s=obj.Shape.copy();s.Placement=obj.getGlobalPlacement();m=App.Matrix();m.A11=-1;m.A14=7400;s=s.transformGeometry(m)
 b=s.BoundBox
 # Inventário do vizinho para não prometer acesso por gavetas/LG.
 if b.XMin<2920 and b.XMax>2100 and b.YMin<7020 and b.YMax>6350 and b.ZMin<920:
  nearby.append({'name':obj.Name,'label':obj.Label,'bbox':[round(v,3) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]})
 if b.XMax<2850 or b.XMin>3650 or b.YMax<5700 or b.YMin>7020 or b.ZMax<0 or b.ZMin>920:continue
 native_count+=1
 for n,p in [('RETIRADA',withdrawal),('AR',air)]+[(n,shapes[n]) for n in shapes if n.startswith(('Grelha','Regua'))]:
  bb=p.BoundBox
  if all(min(getattr(b,k+'Max'),getattr(bb,k+'Max'))-max(getattr(b,k+'Min'),getattr(bb,k+'Min'))>1e-5 for k in 'XYZ'):
   v=p.common(s).Volume
   if v>.1:native_hits.append({'proposal':n,'source':obj.Name,'overlap_mm3':round(v,5)})
assert not native_hits,native_hits
doc.recompute();doc.saveAs(str(here/'Grelhas_Manutencao_R02.FCStd'))
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};assert after==hashes
data={'date':'2026-10-20','reference_hashes_before':hashes,'reference_hashes_after':after,
 'grille':{'quantity':2,'outer_mm':[600,90],'candidate_thickness_mm':1.5,'candidate_material':'inox304; acabamento final a compatibilizar',
 'slot_count':12,'slot_mm':[134,17],'corner_radius_mm':3,'slot_x_mm':[23,163,303,443],
 'slot_z_mm':[17,36.5,56],'mount_holes_x_mm':[100,500],'mount_holes_z_mm':[7.5,82.5],'mount_hole_diameter_mm':4.5,
 'free_area_cm2':round(12*slot_area/100,6),'project_minimum_cm2':252,
 'free_area_from_cad_cm2':round(kernel_area,6),
 'margin_percent':round((12*slot_area/25200-1)*100,4),
 'example_slots_0_2mm_smaller_area_cm2':round(12*((134-.2)*(17-.2)-(4-math.pi)*9)/100,6),
 'limit':'Área ideal da face, sem tela/guarnição invadindo rasgos. Tolerância simulada não é especificação industrial nem ensaio térmico.'},
 'mounting':mounting,'solid_pair_count':len(pairs),'solid_checks':pairs,'solid_overlaps':hits,
 'air_connected_solids':len(air.Solids),'air_overlaps_mm3':airhits,
 'withdrawal_translation_mm':600,'withdrawal_overlaps_new_and_refs_mm3':new_hits,
 'native_region_count':native_count,'native_hits':native_hits,'left_neighbor_inventory':nearby,
 'limits':['Não valida fixação de réguas/insertos ou capacidade de apoio; apenas reserva paraM4 retido e quatro furos por grelha.',
 'Retirada600 é cenário de serviço com envelopes: não mede cabo real, puxador, mão, carrinho, pessoa, gás, porta real ou circulação de obra.',
 'A região usa apenasPeca*. Forno e travessa históricos excluídos. Não é auditoria global do apartamento.',
 'Não se escolheu acesso pelo módulo vizinho nem se reservou uma passagem em gavetas. Posição real de tomada/registro e rota continuam pendentes.',
 'Sem confirmação nova de datums Fischer ou projeção inferior KE4GC. Envelopes conservadores daR01 preservados.']}
(here/'Conferencia.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:data[k] for k in ['grille','solid_pair_count','solid_overlaps','air_connected_solids','native_region_count','native_hits']},ensure_ascii=False))
for d in [doc,original,previous]:App.closeDocument(d.Name)
