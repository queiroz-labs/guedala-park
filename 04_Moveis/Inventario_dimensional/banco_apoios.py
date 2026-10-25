import FreeCAD as A, Part, pathlib, json, math
out=pathlib.Path(__file__).parent/'Banco_estrutura';out.mkdir(exist_ok=True)
root=out.parents[3]
s=A.getDocument('Guedala_Park_R44_Consolidado')
def w(n):
 o=s.getObject(n);q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
inv=json.loads((root/'outputs/estudo-dimensional-2026-10-23/banco_visivel.json').read_text(encoding='utf8'))
supports=[r for r in inv if abs(r['bbox'][5]-400)<1e-5]
contact=[]
for ln in ['BancoR43_Painel1','BancoR43_Painel2']:
 for r in supports:
  q=w(ln);q.translate(A.Vector(0,0,-0.001));c=q.common(w(r['name']))
  if c.Volume>.000001:contact.append({'tampa':ln,'apoio':r['name'],'area_contato_estimada_mm2':c.Volume/0.001,'metodo':'penetração virtual 0,001 mm no apoio; modelo não alterado'})
old=root/'guedala-park/03_Ambientes/Sala_e_jantar/Retirada_ponta/Calculo_hibrido_R02.json'
schedule=json.loads(old.read_text(encoding='utf8'))['bolt_schedule']
items=[r for r in inv if r['name'].startswith('PecaBancoR0') and ('gabarito' in r['label'] or r['name'] in ['PecaBancoR036','PecaBancoR037'])]
hits=[]
for dep in [5.6,13]:
 for i,b in enumerate(schedule):
  x=512 if b['side']=='front' else 136
  sign=-1 if b['side']=='front' else 1
  q=Part.makeCylinder(10,dep,A.Vector(x,5550-b['x'],b['z']),A.Vector(sign,0,0))
  for r in items:
   z=w(r['name'])
   if q.BoundBox.intersect(z.BoundBox):
    v=q.common(z).Volume
    if v>.001:hits.append({'projecao_hipotetica_mm':dep,'indice_parafuso':i,'lado':b['side'],'centro':[x,5550-b['x'],b['z']],'objeto':r['name'],'volume_mm3':v})
calc=[]
for E in [2500,4780,5500,5580,5960]:
 for t in [17.1,18,20]:
  P=80*9.80665;L=376;b=200
  calc.append({'E_MPa':E,'espessura_estrutural_mm':t,'forca_N':P,'vao_mm':L,'largura_faixa_mm':b,'tensao_servico_MPa':1.5*P*L/(b*t*t),'flecha_servico_mm':P*L**3/(4*E*b*t**3)})
data={'contatos':contact,'fixacao_sensibilidade':hits,'flexao_sensibilidade':calc,'aviso':'Cilindros D20 x5,6/13 são envelopes hipotéticos de fixação, não CAD de produto. Padrão M6 histórico espelhado para banco atual: Y=5550-x. Não valida parafuso nem resistência. Flecha é viga simplificada, não certificação de assento.'}
(out/'Conferencia_apoios_fixacoes.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
result={'contatos':len(contact),'interferencias_fixacao':len(hits),'amostra':hits[:8]}
