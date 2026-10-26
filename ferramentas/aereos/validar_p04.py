"""P04: acesso especial SW4, implantacao candidata e requisitos de validacao.

Envelopes conservadores e equilibrio, sem abrir CAD ou atribuir resistencia.
"""
from pathlib import Path
import csv,gzip,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontes import sha,HASH_RULE
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao'
G=9.80665
def read(p):return json.loads(p.read_text(encoding='utf8'))
def overlap(a,b):return np.all(np.minimum(a[3:],b[3:])-np.maximum(a[:3],b[:3])>1e-7)
def segment_box(a,b,box,pad):
    """Segmento contra interior da caixa expandida; tangencia nao e penetracao."""
    lo=box[:3]-pad;hi=box[3:]+pad;v=b-a;t0,t1=0.,1.
    for k in range(3):
        if abs(v[k])<1e-10:
            if a[k]<=lo[k]+1e-8 or a[k]>=hi[k]-1e-8:return False
        else:
            t=(lo[k]-a[k])/v[k];u=(hi[k]-a[k])/v[k]
            t0=max(t0,min(t,u));t1=min(t1,max(t,u))
            if t1-t0<=1e-8:return False
    return t1-t0>1e-8

def saved_hardware(base):
    objects=base['objetos'];items=[]
    def belongs(n):
        seen=set()
        while n in objects and n not in seen:
            if n=='Modulo003':return True
            seen.add(n);n=objects[n].get('pai')
        return False
    # CLIP retirado: calcos fixos ficam. Caixas globaisR52 sao conservadoras.
    for n,v in objects.items():
        if not n.startswith('Calco') or not belongs(n) or not v['visivel'] or not v.get('caixa_global'):continue
        b=v['caixa_global'];box=np.array([2872-b[4],7390-b[3],b[2]-2132,2872-b[1],7390-b[0],b[5]-2132])
        items.append(dict(name=n,label=v['rotulo'],box_uvz_mm=box.tolist()))
    assert len(items)==8
    return items

def tool_access(joint,obstacles):
    cam=np.array(joint['cam_access_uvz_mm']);out=-np.array(joint['drill_inward']);sign=out[2]
    # Chave80x22. Perfil4 entre faces cabe em4/cos30=4,619 entre vertices.
    # Envelope10 cobre perfil e dobra; grip30x30x20 e reserva,nao mao medida.
    # Curso de reencaixe: ponta ate8 dentro ou2 fora; cotas internas do encaixe
    # nao foram medidas. Exterior de todos esses estados e envolvido abaixo.
    radius=5.;arc_guard=2*80*math.sin(math.radians(.25));pad=radius+arc_guard
    shaft_end=cam+24*out;shaft_box=np.r_[np.minimum(cam,shaft_end),np.maximum(cam,shaft_end)]
    shaft_box[[0,1]]-=pad;shaft_box[[3,4]]+=pad
    assert not any(overlap(shaft_box,b) for b in obstacles.values())
    rows=[];minimum=None
    for angle in range(-35,36):
        a=math.radians(angle);end=cam+np.array([80*math.cos(a),80*math.sin(a),0])
        # ExtrusaoZ inclui continuamente engates0..8 e retirada ate2.
        z1,z2=sorted([cam[2]+sign*9,cam[2]+sign*29])
        root=cam.copy();tip=end.copy();root[2]=tip[2]=(z1+z2)/2
        hits=[]
        for n,b in obstacles.items():
            bb=b.copy();bb[2]=max(bb[2],z1);bb[5]=min(bb[5],z2)
            if bb[5]-bb[2]>1e-7:
                # TesteXY exato da linha;Z foi envolvido pela extrusao acima.
                bb[2]=root[2]-1;bb[5]=root[2]+1
                if segment_box(root,tip,bb,np.array([pad,pad,0.])):hits.append(n)
        z3,z4=sorted([cam[2]+sign*4,cam[2]+sign*34])
        grip=np.r_[end[:2]-15-arc_guard,z3,end[:2]+15+arc_guard,z4]
        hits += [n for n,b in obstacles.items() if overlap(grip,b)]
        assert not hits,(joint['id'],angle,hits)
        rows.append(dict(access_id=joint['id'],angle_deg=angle,cam_uvz_mm=cam.tolist(),
            key_end_uv_mm=end[:2].tolist(),grip_swept_bbox_mm=grip.tolist(),collisions=[]))
    # Introducao/retirada pela frente, chave fora do encaixe2mm e orientada+u.
    c=cam.copy();c[1]=230.;at=cam+2*out;end=cam+24*out
    shaft=np.r_[min(cam[0],c[0])-pad,min(cam[1],c[1])-pad,min(at[2],end[2]),
                max(cam[0],c[0])+pad,max(cam[1],c[1])+pad,max(at[2],end[2])]
    arm=np.array([cam[0]-pad,cam[1]-pad,min(cam[2]+19*sign,cam[2]+29*sign),
                  cam[0]+80+pad,230+pad,max(cam[2]+19*sign,cam[2]+29*sign)])
    grip=np.array([cam[0]+80-15-arc_guard,cam[1]-15-arc_guard,min(cam[2]+14*sign,cam[2]+34*sign),
                   cam[0]+80+15+arc_guard,230+15+arc_guard,max(cam[2]+14*sign,cam[2]+34*sign)])
    for bb in [shaft,arm,grip]:assert not any(overlap(bb,b) for b in obstacles.values()),joint['id']
    return dict(id=joint['id'],cam_uvz_mm=cam.tolist(),key_sku='05133154001',sweep_deg=[-35,35],
        reindex_increment_deg=60,shaft_envelope_diameter_mm=10,
        continuous_angle_guard_mm=arc_guard,insertion_envelope_mm=[-2,8],
        grip_reserve_mm=[30,30,20],wood_and_fixed_calcos_clear=True,
        shaft_to_near_divider_mm=cam[0]-pad-25,
        entry_swept_boxes_mm=[b.tolist() for b in [shaft,arm,grip]],rows=rows)

def main():
    geometry=read(OUT/'Lote_B_geometria.json');detail=read(OUT/'Lote_B_detalhamento.json')
    release=read(ROOT/'ferramentas/site/current_release.json');cad=ROOT/release['cadPath'];cadsha=sha(cad)
    basepath=ROOT/'02_Modelo_3D/Base_verificacao.json.gz';base=json.loads(gzip.decompress(basepath.read_bytes()))
    assert cadsha==base['sha256']==geometry['cad_sha256']==detail['cad_sha256']
    m=next(m for m in geometry['modules'] if m['code']=='P04');variant=next(v for v in m['variants'] if v['preferred_for_study'])
    boxes={n:np.array(b) for n,b in variant['boxes_uvz_mm'].items()};hardware=saved_hardware(base)
    oldbox=np.array([0,18,242,49.5,55.8,258]);bad=[n for n,b in boxes.items() if overlap(oldbox,b)]
    assert bad==['ApoioOpostoR002']
    # Candidata esquerda na face direita do divisor existenteu7..25;
    # desloca ferragem25,sem deslocar madeira ou adicionar chapa.
    brackets=[dict(side=0,carrier='ApoioOpostoR002',corner_u_mm=25.,upper_u_mm=65.5,envelope_uvz_mm=[25,18,242,74.5,55.8,258]),
              dict(side=1,carrier='Peca266',corner_u_mm=1764.,upper_u_mm=1723.5,envelope_uvz_mm=[1714.5,18,242,1764,55.8,258])]
    obstacles={**boxes,**{h['name']:np.array(h['box_uvz_mm']) for h in hardware}}
    for b in brackets:
        bb=np.array(b['envelope_uvz_mm']);assert not any(overlap(bb,x) for x in obstacles.values())
        u=b['upper_u_mm'];corridor=np.array([u-10,19.5,240,u+10,230,260])
        assert not any(overlap(corridor,x) for x in obstacles.values())
        b['tool20_bbox_mm']=corridor.tolist();b['product_mounting_confirmed']=False
        obstacles['Bigfer_ESTUDO_'+str(b['side'])]=bb
    old_accesses=[r for r in detail['joints'] if r['code']=='P04' and not r['tool20_wood_clear']];assert len(old_accesses)==4
    access=[tool_access(r,obstacles) for r in old_accesses]
    vectors=[];lower=[];certificates=[];cases=[c for c in detail['cases'] if c['code']=='P04']
    a,b=65.5,1723.5;la,lb=-9.,1773.;h=160.
    for c in cases:
        V=c['V_N'];M=c['M_Nm']*1000;S=c['S_Nmm'];vertical=[(b*V-S)/(b-a),(S-a*V)/(b-a)];T=M/h
        for share in [0.,.5,1.]:
            normals=[share*T,(1-share)*T];first=a*normals[0]+b*normals[1]
            comp=[(lb*T-first)/(lb-la),(first-la*T)/(lb-la)]
            assert min(vertical)>0 and min(comp)>0
            F=np.array([0.,0.,-V]);moment=np.cross(c['center_uvz_mm'],F)
            for side in [0,1]:
                u=[a,b][side];f=np.array([0.,-normals[side],vertical[side]]);point=np.array([u,0.,250.])
                F+=f;moment+=np.cross(point,f)
                corner=np.array([brackets[side]['corner_u_mm'],18.,250.]);local=np.cross(point-corner,f)
                vectors.append(dict(case_id=c['source_case_id'],rho=c['rho_kg_m3'],payload_kg=c['payload_kg'],payload_case=c['payload_case'],
                    doors_deg=c['doors_deg'],share_left=share,side=side,u_mm=u,z_mm=250.,h_mm=h,
                    V_N=vertical[side],T_N=normals[side],R_N=math.hypot(vertical[side],normals[side]),
                    local_M_corner_Nmm=local.tolist(),force_uvz_N=f.tolist(),mass_kg=c['mass_wood_contents_kg'],
                    capacity_selected=False,hardware_mass_included=False))
                force=np.array([0.,comp[side],0.]);F+=force;moment+=np.cross([[la,0,90],[lb,0,90]][side],force)
                lower.append(dict(case_id=c['source_case_id'],share_left=share,side=side,u_mm=[la,lb][side],z_mm=90.,
                    C_N=comp[side],reference_area_mm2=1080.,mean_pressure_on_reference_MPa=comp[side]/1080.,actual_area_verified=False))
            err=max(float(max(abs(F))),float(max(abs(moment))));assert err<1e-7
            certificates.append(dict(case_id=c['source_case_id'],share_left=share,force_error_N=max(abs(F)),moment_error_Nmm=max(abs(moment))))
    chosen={}
    for side in [0,1]:
        rows=[r for r in vectors if r['side']==side and r['payload_kg']==10]
        for field in ['V_N','T_N','R_N']:
            r=max(rows,key=lambda r:r[field]);key=(r['case_id'],r['share_left'],side)
            chosen.setdefault(key,dict(r,controls=[]))['controls'].append(field)
    tests=list(chosen.values())
    # Rigidez da memoria local e requisito de medicao,nao atribuido aoMinifix.
    local=read(ROOT/'04_Moveis/Ligacoes_sem_tubos/Resultados.json')
    reference=next(r for r in local['cases'] if r['case'].startswith('P04'))
    result=dict(scope='P04:acessos especiais resolvidos nominalmente,ligacoes e suspensao em qualificacao.',cad_sha256=cadsha,cad_opened=False,cad_changed=False,
        source_tool=read(OUT/'P04_fontes_validacao.json'),accesses=access,static_hardware=hardware,
        sequence='Montar caixa e apertarMinifix antes de portas/dobradicas. Para manutencao,desclipar/remover portas,manter calcos,usar braco curtoSW4 reto,cursos ate60graus,retirar e reencaixar60graus ate travamento conforme fabricante. Sem torque ou profundidade de engate prescritos.',
        old_corner_bracket=dict(rejected=True,box_uvz_mm=oldbox.tolist(),wood_interferences=bad),
        proposed_brackets=brackets,upper_z_mm=250,lower_z_hypothesis_mm=90,couple_mm=h,
        no_body_dimensions_or_storage_changed=True,bracket_count_hypothesis=2,bracket_occupancy_ml=2*49.5*37.8*16/1000,
        cases=len(cases),vectors=vectors,lower_reactions=lower,certificates=certificates,qualification_cases=tests,
        max_equilibrium_error=max(max(r['force_error_N'],r['moment_error_Nmm']) for r in certificates),
        local_reference=dict(case=reference['case'],deflection_plus_reserve_mm=reference['deflection_plus_reserve_mm'],
            criterion_mm=reference['criterion_mm'],joint_K_initial_required_N_mm=1000,
            applicability='Referencia local anterior,nao validacao doMinifix nem da suspensao que agora introduz forca no divisor esquerdo.'),
        limits=['Envelopes de ferramenta incluem guarda angular continua0,6982mm;engates0..8 apenas envolvente exterior,nao profundidade real de encaixe.',
            'Perfil/dobra envolvido por10mm;reserva de dedos30x30x20 nao e ergonomia medida. Conferir chave/caneco reais e aperto/retirada em retalho.',
            'So calcos fixos na manutencao;nenhuma colisao dinamica com portas/dobradicas em movimento foi homologada. Portas desclipadas como sequencia.',
            'Dois suportes sao hipotese de qualificacao. Esquerdo no divisor18 muda o caminho;fundo inteiro/divisor/juntas e caixa completa precisam de prova.',
            'Contato inferiorZ90/1080mm2 nao foi medido;fundo e laterais coplanares podem mudar centro de contato/braco e tracao.',
            'Madeira+conteudo ate46,209kg,sem massas/CG de ferragens. Cada1kg adicional emv200 acrescenta9,80665N e1,96133Nm;T_total cresce12,2583N parah160.',
            'Partilhas0/50/100 sao demandas condicionais,nao rigidez real. Momento local rXF e reducao da mesma forca,nao soma extra.',
            'Sem resistencia/rigidez atribuidas a produto,carga de prova/fatores normativos ou ancoragem definidos;parede real depende de levantamento.'])
    paths=[OUT/'Lote_B_detalhamento.json',OUT/'Lote_B_geometria.json',OUT/'P04_fontes_validacao.json',OUT/'Selecao_ferragem.json',basepath,
           ROOT/'04_Moveis/Ligacoes_sem_tubos/Resultados.json']
    result.update(hash_rule=HASH_RULE,sources_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in paths},script_sha256=sha(Path(__file__)),hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')))
    (OUT/'P04_validacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for name,rows in [('P04_demandas_suspensao.csv',vectors),('P04_casos_qualificacao.csv',tests),('P04_reacoes_inferiores.csv',lower)]:
        with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    draw(result)
    print(json.dumps(dict(accesses=4,angular_states=4*71,cases=len(cases),vectors=len(vectors),qualification_cases=len(tests),
        max_V_N=max(r['V_N'] for r in vectors),max_T_N=max(r['T_N'] for r in vectors),max_R_N=max(r['R_N'] for r in vectors),equilibrium_error=result['max_equilibrium_error'])))

def draw(d):
    im=Image.new('RGB',(1500,1100),'#f4f1eb');q=ImageDraw.Draw(im)
    def t(x,y,s,n=24,b=False,c='#293a31'):q.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n),fill=c)
    t(40,24,'P04 | acesso pela chave curta e suspensão candidata',34,True)
    t(40,82,'Estudo nominal • base limpa • mesma madeira e vãos • R52 intacta',25)
    q.rounded_rectangle((40,140,735,690),18,fill='white');t(65,160,'Base e tampo: acesso aos 4 canecos',27,True)
    ox,oy,scale=110,660,2
    def xy(u,v):return ox+u*scale,oy-v*scale
    q.rectangle((*xy(7,230),*xy(25,18)),fill='#b7a68a')
    for v in [90,158]:
        x,y=xy(34,v);q.ellipse((x-15,y-15,x+15,y+15),fill='#9bbfac',outline='#293a31',width=2)
        for a in [-35,0,35]:
            end=xy(34+80*math.cos(math.radians(a)),v+80*math.sin(math.radians(a)))
            q.line((x,y,*end),fill='#467c66',width=6)
    t(355,245,'Allen SW4: 80 × 22 mm',24,True);t(355,290,'Braço curto no caneco',22)
    t(355,334,'Cursos de até 60°',22);t(355,378,'Retirar e reencaixar',22)
    t(355,435,'Sem mover o divisor',22);t(355,478,'Sem furos por baixo',22)
    t(65,646,'Base ilustrada; tampo espelhado; calços conferidos.',21)
    q.rounded_rectangle((765,140,1460,690),18,fill='white');t(790,160,'Suspensão: esquema sem escala',27,True)
    ox2,oy2=815,565
    q.rectangle((ox2,240,ox2+550,oy2),fill='#e8ece4',outline='#81725d',width=3)
    q.rectangle((ox2+5,240,ox2+22,oy2),fill='#b7a68a')
    for xx in [ox2+30,ox2+542]:q.rectangle((xx-8,278,xx+8,318),fill='#467c66')
    t(805,594,'Esquerda no divisor18; direita na lateral18.',22)
    t(805,635,'Hipótese de 2 suportes, ainda sem capacidade.',22,c='#a65438')
    q.rounded_rectangle((40,720,1460,1060),18,fill='white')
    t(65,745,'Validação preparada para produto e oficina',28,True)
    t(65,802,'46,21 kg estimados com conteúdo10 kg, antes das ferragens; braço de estudo160 mm.',24)
    t(65,846,f"Demanda por suporte: até V {max(r['V_N'] for r in d['vectors']):.1f} N e T {max(r['T_N'] for r in d['vectors']):.1f} N em casos distintos.",24)
    t(65,890,'Aplicar os vetores simultâneos do CSV. Não combinar máximos de casos diferentes.',24)
    t(65,952,'Próximo requisito físico: ferramenta real, juntas, contato inferior e suporte no fundo/divisor18.',23,True)
    im.save(OUT/'P04_acesso_e_suspensao.png')

if __name__=='__main__':main()
