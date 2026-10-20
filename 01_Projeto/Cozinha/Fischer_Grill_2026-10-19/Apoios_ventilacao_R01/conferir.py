"""R01 localizada: apoio até o piso e percurso de ar. Não modifica R30."""
import sys,json,hashlib,itertools
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App, Part
here=Path(__file__).resolve().parent
old=json.loads((here.parent/'Conferencia_Fischer.json').read_text(encoding='utf-8'))
source=Path(old['source']); before=hashlib.sha256(source.read_bytes()).hexdigest()
src=App.openDocument(str(source)); out=App.newDocument('Apoios_Ventilacao_R01')
shapes={}; rows={}; kinds={}
def bounds(s):
 b=s.BoundBox
 return [round(v,4) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]
def add(n,s,kind,note):
 assert s.isValid(),n
 o=out.addObject('Part::Feature',n);o.Shape=s
 o.addProperty('App::PropertyString','Limite','Estudo');o.Limite=note
 shapes[n]=s;kinds[n]=kind;rows[n]={'bbox_mm':bounds(s),'kind':kind,'limit':note}
 return s
def box(n,x,y,z,w,d,h,kind='proposta',note='Cota candidata, sem liberação de fabricação.'):
 return add(n,Part.makeBox(w,d,h,App.Vector(x,y,z)),kind,note)
for n in ['Peca134','Peca305','Peca306','Peca308','Peca152','Peca357']:
 o=src.getObject(n); s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
 m=App.Matrix();m.A11=-1;m.A14=7400
 add('R30_'+n,s.transformGeometry(m),'referencia','Cópia estática espelhada; fonte intacta.')
box('Frente',2929,6378,123,595,26,447,note='Envelope conservador. Topo570; posição relativa ao apoio por confirmar no exemplar.')
box('CorpoConservador',2946.5,6404,138,560,547,432,note='L560 é abertura, não chassi. P547 conservador; datum base/corpo/frente não é oficial.')
box('BasePlana',2938,6410,120,577,535,18,note='Base18 candidata, plana e contínua; fundo termina55 antes da parede. Material/uniões/carga a especificar pelo fabricante do móvel.')
for name,x in [('Esquerdo',2938),('Central',3217.5),('Direito',3497)]:
 box('Apoio'+name,x,6440,0,18,505,120,note='Nervura18 até o piso; recuada30 da frente da base e fora do canal traseiro. Nivelamento final e material não dimensionados.')
for name,x,wingx in [('Esquerdo',2938,2920),('Direito',3506.5,3515)]:
 # Acerto nominal ligado à lateral18 existente; não apoia o peso do forno.
 a=Part.makeBox(8.5,100,512,App.Vector(x,6404,138))
 b=Part.makeBox(18,6,512,App.Vector(wingx,6404,138))
 add('Contramarco'+name,a.fuse(b),'proposta','Envelope de contramarco26,5 na frente (18 da lateral +8,5 de ajuste). União à lateral existente e parafusos do kit dependem dos furos reais; não usar tira8,5 isolada como estrutura.')
box('Travessa',2938,6743,660,577,212,30,note='Deslocamento27 para frente; termina no início do canal traseiro. Material e ligações originais não homologados.')
box('Cooktop131',2920,6460,789,600,450,131,'reserva','Teste:131 totais para baixo; não inclui grampos, gás ou cabo reais.')
box('RecorteCooktop',2960,6490,900,520,390,20,'reserva','Recorte520x390 no eixo atual; raio/grampos e resistência da pedra pendentes.')
rear=box('ArTraseiro',2946.5,6955,30,560,45,870,'ar','Canal reservado45x560, sem fundo/travessas/conexões.')
front=box('ArEntrada',2946.5,6408,30,560,32,60,'ar','Entrada inferior livre; acabamento frontal recuado30 do início da base.')
left=box('ArInferiorEsquerdo',2956,6440,30,261.5,515,60,'ar','Canal sob base; segue atrás das nervuras até o canal traseiro.')
right=box('ArInferiorDireito',3235.5,6440,30,261.5,515,60,'ar','Segundo canal sob base.')
upper=box('ArSaida',2946.5,6378,705,560,622,60,'ar','Saída frontal60 de altura; substitui45 preliminares para aceitar área ocupada por grelha.')
# Percurso unido por faces e volume no topo. Contagem de sólidos testa conexão,
# não vazão, pressão, temperatura ou ausência de recirculação.
path=front.fuse(left).fuse(right).fuse(rear).fuse(upper).removeSplitter()
assert path.isValid() and len(path.Solids)==1,(path.isValid(),len(path.Solids))
solid=[n for n in shapes if kinds[n] in ['proposta','referencia']]
checks=[]
for a,b in itertools.combinations(solid,2):
 if kinds[a]==kinds[b]=='referencia':continue
 v=shapes[a].common(shapes[b]).Volume
 checks.append({'a':a,'b':b,'overlap_mm3':round(v,5)})
hits=[r for r in checks if r['overlap_mm3']>.1];assert not hits,hits
air_checks={n:round(path.common(shapes[n]).Volume,5) for n in solid+['Cooktop131']}
assert not any(v>.1 for v in air_checks.values()),air_checks
native_hits=[];native_count=0
for o in src.Objects:
 if not o.Name.startswith('Peca') or o.Name in ['Peca133','Peca307'] or not hasattr(o,'Shape') or o.Shape.isNull():continue
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();m=App.Matrix();m.A11=-1;m.A14=7400;s=s.transformGeometry(m)
 b=s.BoundBox
 if b.XMax<2850 or b.XMin>3650 or b.YMax<5900 or b.YMin>7020 or b.ZMax<0 or b.ZMin>920:continue
 native_count+=1
 for n in [n for n in solid if kinds[n]=='proposta']+['PERCURSO_AR']:
  p=path if n=='PERCURSO_AR' else shapes[n];bb=p.BoundBox
  if all(min(getattr(b,k+'Max'),getattr(bb,k+'Max'))-max(getattr(b,k+'Min'),getattr(bb,k+'Min'))>1e-5 for k in 'XYZ'):
   vol=p.common(s).Volume
   if vol>.1:native_hits.append({'proposal':n,'source':o.Name,'overlap_mm3':round(vol,4)})
assert not native_hits,native_hits
out.recompute();out.saveAs(str(here/'Apoios_Ventilacao_R01.FCStd'))
after=hashlib.sha256(source.read_bytes()).hexdigest();assert before==after
report={'date_local':'2026-10-19','source_sha256_before':before,'source_sha256_after':after,
 'method':'FreeCAD1.1.4; cópias estáticas espelhadas. Envelopes ideais, sem detalhes ausentes. R30 não recomputada/salva.',
 'objects':rows,'solid_pairs':checks,'overlaps':hits,'air_solid_count':len(path.Solids),
 'air_overlap_mm3':air_checks,'native_region_count':native_count,'native_hits':native_hits,
 'sections_cm2':{'rear_45x560':252,'lower_two_261_5x60':313.8,'opening_560x60_gross':336,'grille_concept_four_ties_4mm':326.4},
 'grille_min_free_ratio':.75,'grille_min_actual_free_area_cm2':252,
 'support_free_spans_mm':[261.5,261.5],'support_front_overhang_mm':30,
 'support_rear_to_wall_mm':55,'nominal_body_rear_to_wall_mm':49,
 'upper_path_gap_to_cross_mm':15,'upper_path_gap_to_stress131_mm':24,
 'structural_service_load_target_kg':50,
 'limits':['50kg é meta para especificação do conjunto, não capacidade calculada/comprovada. Inclui forno, base, recipientes e alimentos; não inclui pessoa nem comprova carga de porta aberta.',
 'Sem cálculo térmico, vazão, validação de junta/chapas/pedra, ligações, parafusos, gás/elétrica, produto real ou campo.',
 'Grade proposta: abertura útil560x60, quatro montantes4, sem tela/lâminas adicionais. Área geométrica ideal; produto final precisa comprovar área efetiva >=252cm².',
 'Contramarcos são reservas ligadas às laterais; sem coordenadas de furos e sem fixação segura demonstrada. Apoio pode exigir ajuste após conferir datums.',
 'A triagem de38 Peca* não cobre outros nomes, elementos ausentes nem movimentos. Porta aberta não revalidada nesta R01.']}
(here/'Conferencia.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pairs':len(checks),'overlaps':hits,'air_solid_count':len(path.Solids),'air_overlap_mm3':air_checks,'native_region_count':native_count,'native_hits':native_hits,'source_unchanged':before==after},ensure_ascii=False))
App.closeDocument(out.Name);App.closeDocument(src.Name)
