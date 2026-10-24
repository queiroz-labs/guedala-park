import json,pathlib,math
P=pathlib.Path(__file__).parent
A={r['name']:r for r in json.loads((P/'Solidos_finitos_ativos_R44.json').read_text(encoding='utf-8'))}
T={r['name']:r for r in json.loads((P/'Arvore_R44.json').read_text(encoding='utf-8'))}
# Face contact of rectangular panel envelopes is a geometric interface, never a load rating.
mods=[];contacts=[]
for i in range(20):
 n='Modulo' if i==0 else 'Modulo%03d'%i
 if i==17:n='BC43_Madeira'
 ps=[A[c] for c in T[n]['group'] if c in A and c.startswith(('Peca','BasePlana','ApoioComum','ApoioOposto','Prateleira','BC43_')) and not any(k in A[c]['label'].lower() for k in ['reserva','gabarito','objeto','tanque externo','vazio útil'])]
 rect=[]
 for r in ps:
  v=math.prod(r['dim']); ratio=r['volume']/v if v else 0
  if ratio>.995:rect.append(r)
 for j,a in enumerate(rect):
  for b in rect[j+1:]:
   aa=a['bbox'];bb=b['bbox']
   for axis in range(3):
    if min(abs(aa[axis+3]-bb[axis]),abs(bb[axis+3]-aa[axis]))<.001:
     axes=[k for k in range(3) if k!=axis];ol=[min(aa[k+3],bb[k+3])-max(aa[k],bb[k]) for k in axes]
     if min(ol)>.001:contacts.append(dict(module=n,a=a['name'],b=b['name'],axis='XYZ'[axis],contact_dimensions_mm=ol,area_mm2=math.prod(ol),interpretation='contato horizontal; sentido da gravidade compatível, caminho de carga não verificado' if axis==2 else 'contato de borda vertical; necessita ligação mecânica, não é apoio vertical por gravidade'))
 mods.append(dict(module=n,physical_direct_panels=len(ps),rectangular_panels=len(rect),excluded_nonrectangular=[r['name'] for r in ps if r not in rect]))
(P/'Interfaces_retangulares.json').write_text(json.dumps(dict(method='bboxes globais; somente painéis com volume >=99,5% da caixa; contato nominal tolerância0,001mm; não inclui ferragens e descendentes',modules=mods,interfaces=contacts),ensure_ascii=False,indent=2),encoding='utf-8')
out=['# Interfaces de painéis — auditoria geométrica','', 'Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação.','', '| Módulo | Peças | Plano do contato | Dimensões mm | Leitura |','|---|---|---|---|---|']
for c in contacts:out.append(f"| {c['module']} | {c['a']} / {c['b']} | {c['axis']} | {c['contact_dimensions_mm'][0]:g} × {c['contact_dimensions_mm'][1]:g} | {c['interpretation']} |")
(P/'Interfaces_retangulares.md').write_text('\n'.join(out),encoding='utf-8')
print(len(contacts))
