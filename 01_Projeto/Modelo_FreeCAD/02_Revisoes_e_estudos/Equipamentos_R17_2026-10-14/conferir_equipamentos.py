from pathlib import Path
import json, shutil, hashlib
import FreeCAD as App, Part

root=(Path(__file__).resolve().parent / '.').resolve(); base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Banco_R16_2026-10-14/Guedala_Park_R16_Banco_Simples.FCStd').resolve()
dst=(Path(__file__).resolve().parent / 'Guedala_Park_R17_Equipamentos.FCStd').resolve()
assert not dst.exists(), 'Revisão existente; não reconstruir'
prev=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==src)
assert prev.isSaved() and src.stat().st_size>100000
before_hash=hashlib.sha256(src.read_bytes()).hexdigest()
shutil.copy2(src,dst); d=App.openDocument(str(dst)); App.setActiveDocument(d.Name)
d.Label='Guedala Park - R17 - equipamentos e reservas documentais'
def prop(o,n,v):
    if n not in o.PropertiesList: o.addProperty('App::PropertyString',n,'Conferência R17')
    setattr(o,n,v)
def shape(o):
    s=o.Shape.copy(); s.Placement=o.getGlobalPlacement(); return s
def bounds(o):
    b=shape(o).optimalBoundingBox()
    return [b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
equipment=['Peca133','Peca134','Peca138','Peca139','Peca140','Peca152','Peca154','Peca155','Peca156','Peca157','Peca351']
old={n:bounds(d.getObject(n)) for n in equipment}
micro=d.getObject('Peca351'); assert abs(float(micro.Width)-452)<1e-6
micro.setExpression('Width',None); micro.Width=352
micro.Label='ME23P - corpo documental 461x352x290; folgas separadas R17'
prop(micro,'FonteR17','Guia Electrolux ME23P G0033709/009, página PDF5: 461x290x352 LxAxP. Manual página3: laterais/traseira100, acima300. Micro_C2: posição de estudo e escolha superior100.')
prop(micro,'StatusR17','Corrigido corpo452->352; posição frontal/base1550 preservadas. Layout100 acima não atende manual300. Pés/porta/fixação/acesso/cabos reais pendentes; sem corte/furação/compra.')
purifier=d.getObject('Peca140'); assert abs(purifier.Placement.Base.y-6530)<1e-6
purifier.setExpression('Placement.Base.y',None)
p=purifier.Placement; p.Base.y=6480; purifier.Placement=p
prop(purifier,'FonteR17','PE12G vigente, manual251021JAXM páginaPDF5/impresso4: lados50/traseira100/topo220; páginaPDF10/impresso9:160x350x420. PE11X histórico não rege PE12G.')
prop(purifier,'StatusR17','Proposta: avançar50 na bancada para deixar100 até paredeY7000. PosiçãoX/altura e aparelho preservados. Frente fica520 da parede,110 antes da pedra630. Água/tomada/pega/afastamento de calor e exemplar reais pendentes.')
prop(d.getObject('Peca155'),'StatusR17','Envelope ilustrativo350x157x530 mantido; manual E21 corpo483 alto. Datums e conexões não conhecidos, não encurtar para fingir folga. Laterais200 recomendadas; posição/apoio incombustível/duto reais pendentes.')
prop(d.getObject('Peca156'),'StatusR17','Gabarito quadrado80, não chaminé real. Manual E21 diâmetro60; percurso/terminação/conexões e datums não validados.')
prop(d.getObject('Peca133'),'StatusR17','Envelope total ilustrativo517x615x610 mantido, não forno instalado. Referência traseira no CAD a15 da parede; cenário Corte_coccao pede50 condicionais. Corpo485x560x570 e frente têm datums distintos; Venax3/5 versus10cm conflitantes. Não mover/subdividir sem esclarecer fonte.')
prop(d.getObject('Peca134'),'StatusR17','Caixa superior ilustrativa600x450x15; não inclui volume inferior/grampo/gás. d instalado desconhecido; não usar15 ou altura total131 como d.')
prop(d.getObject('Modulo008'),'StatusR17','Vão614 favorável a603 nominal Suggar, corpo600x300x176. Canal reservado não conectado: base/tampo inteiros e42 entre topo do volume do aparelho e baseD. Abertura superior20 por largura não comprovada; fixação/recortes/retorno ainda sem projeto.')
prop(d.getObject('Peca154'),'StatusR17','Guarda cotidiana na lavanderia; uso temporário na cozinha conforme programa. Reserva100 laterais/traseira/acima é gabarito; gaveta/vapor/cabo/água/calor e pega reais pendentes.')
refs=d.addObject('App::Part','ReferenciasEquipamentosR17'); refs.Label='R17 - reservas de ar/acesso; NÃO peças nem nichos homologados'
zones=[]
def zone(label,xyzwhd,source,status='Reserva documental estacionária; não comprova fluxo, fixação ou operação.',kind='ar'):
    x,y,z,w,p,h=xyzwhd
    o=d.addObject('Part::Box','ReservaEquipamentoR17');refs.addObject(o);o.Label=label
    o.Length=w;o.Width=p;o.Height=h;o.Placement.Base=App.Vector(x,y,z)
    prop(o,'FonteR17',source);prop(o,'StatusR17',status);prop(o,'TipoReservaR17',kind)
    o.ViewObject.ShapeColor=(.92,.48,.22);o.ViewObject.Transparency=80;o.Visibility=False
    zones.append(o);return o
ms='Manual ME23P página3; guia página5. ParedeY7000 hipotética.'
zone('ME23P - traseira100 livre',(5165,6900,1550,461,100,290),ms)
zone('ME23P - lateral100 esquerda',(5065,6548,1550,100,352,290),ms)
zone('ME23P - lateral100 direita',(5626,6548,1550,100,352,290),ms)
zone('ME23P - acima100 escolhidos',(5165,6548,1840,461,352,100),ms,'Escolha de layout; não atende300 do manual.')
zone('ME23P - acima300 exigidos',(5165,6548,1840,461,352,300),ms,'Invasão esperada do aéreo B; evidência de divergência, não alteração de guarda.')
ps='Manual PE12G251021JAXM PDF5/impresso4. Coordenadas propostas; paredeY7000.'
zone('PE12G - traseira100',(5520,6900,920,160,100,350),ps)
zone('PE12G - lateral50 esquerda',(5470,6480,920,50,420,350),ps)
zone('PE12G - lateral50 direita',(5680,6480,920,50,420,350),ps)
zone('PE12G - topo220',(5520,6480,1270,160,420,220),ps)
ib='Guia IB6 G0046764/003 página2; correspondência IB6S documentada27/09.'
zone('IB6S - traseira100',(5849,6900,0,601,100,1866),ib)
zone('IB6S - lateral100 esquerda',(5749,6152.5,0,100,747.5,1866),ib)
zone('IB6S - lateral100 direita',(6450,6152.5,0,100,747.5,1866),ib)
zone('IB6S - topo100',(5849,6152.5,1866,601,747.5,100),ib)
lg='Manual LG CV501***4 páginas10-12; suporte CV5012PC4 correspondente confirmado27/09.'
zone('LG - traseira100',(3200,6900,0,600,100,850),lg)
zone('LG - lateral20 esquerda',(3180,6280,0,20,620,850),lg)
zone('LG - lateral20 direita',(3800,6280,0,20,620,850),lg)
zone('LG - topo5',(3200,6280,850,600,620,5),lg)
af='Folheto RI9252, página2:100 laterais/traseira/acima. Posição cotidiana do CAD.'
zone('RI9252 - traseira100',(3490,6870,920,264,100,295),af)
zone('RI9252 - lateral100 esquerda',(3390,6510,920,100,360,295),af)
zone('RI9252 - lateral100 direita',(3754,6510,920,100,360,295),af)
zone('RI9252 - topo100',(3490,6510,1215,264,360,100),af)
e='Manual E21 176, figura3/recomendação lateral200; usar envelope ilustrativo530 conservador. Não reduzir por aceite de distância.'
zone('E21 - lateral200 esquerda recomendada',(2420,6750,1570,200,157,530),e)
zone('E21 - lateral200 direita recomendada',(2970,6750,1570,200,157,530),e)
zone('E21 - frente600 referência ideal',(2620,6150,1570,350,600,530),e,'Referência600 como limite inferior de distância ideal>600; não nicho, madeira permitida ou recinto homologado.')
d.recompute()
# Explicit static subset: imported room/walls, current carcasses and R10 leaves.
# No visibility filter; no cut-wall duplicates, obsolete historical fronts, boolean inputs or hardware drivers.
target_names=[]
for o in d.Objects:
    if o.Name.startswith('Peca') and o.Name[4:].isdigit() and int(o.Name[4:])<235:
        if getattr(o,'TipoPeca','')!='Parede em corte' and o.Name not in equipment:target_names.append(o.Name)
for mname in ['Modulo004','Modulo005','Modulo006','Modulo008','Modulo009','Modulo010','Modulo011','Modulo012','Modulo014']:
    m=d.getObject(mname)
    target_names.extend(c.Name for c in m.Group if c.TypeId=='Part::Box' and c.Name!='Peca321')
target_names+=['Peca308','Peca357']
r10=json.loads(((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/Montagem_R10.json').resolve()).read_text(encoding='utf-8'))
target_names.extend(r['front'] for r in r10['doors'])
targets=[(d.getObject(n),shape(d.getObject(n))) for n in dict.fromkeys(target_names)]
def hits(s):
    b=s.optimalBoundingBox(); out=[]
    for o,t in targets:
        if b.intersect(t.optimalBoundingBox()):
            v=s.common(t).Volume
            if v>1e-3:out.append({'name':o.Name,'label':o.Label,'volume_mm3':v})
    return out
zh=[{'name':z.Name,'label':z.Label,'bbox':bounds(z),'hits':hits(shape(z)),'valid':z.Shape.isValid()} for z in zones]
# One new swept envelope of the proposed purifier translation; no repeated cabinet movements.
pur_path=Part.makeBox(160,470,350,App.Vector(5520,6480,920))
correction={'purifier_swept_envelope_hits':hits(pur_path),'micro_body_hits':hits(shape(micro)),'purifier_body_hits':hits(shape(purifier))}
assert not any(correction.values()), 'Correção colide: '+str(correction)
assert micro.Shape.isValid() and purifier.Shape.isValid() and all(z.Shape.isValid() for z in zones)
refs.Visibility=False
report={'file':str(dst),'source':str(src),'source_sha256':before_hash,'units':'mm','old_bboxes':old,
        'current_bboxes':{n:bounds(d.getObject(n)) for n in equipment},'zones':zh,'targets':target_names,
        'target_count':len(targets),'corrections':correction,
        'scope':'Interseções estacionárias em subconjunto explícito. Equipamentos proprietários excluídos das reservas; sem portas/gavetas reais de aparelho, fluxo, térmica, conexões/pessoas/hardware. Não valida instalação.'}
((Path(__file__).resolve().parent / 'Conferencia_R17.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
d.recompute();d.save()
assert d.isSaved() and dst.exists() and dst.stat().st_size>100000
assert hashlib.sha256(src.read_bytes()).hexdigest()==before_hash, 'R16 alterada'
result={'file':str(dst),'target_count':len(targets),'corrections':correction,'zone_hits':[{r['label']:[h['name'] for h in r['hits']]} for r in zh if r['hits']]}
