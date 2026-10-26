"""Implantacao candidata P17/P12: envelopes e demandas, sem capacidade atribuida.

Usa somente fontes persistidas. Executar --movel P17 ou --movel P12.
"""
from pathlib import Path
import argparse, csv, gzip, itertools, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontes import sha, HASH_RULE

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Aereos_suspensao'
META={'P17':('Modulo016','Peca385','Peca384',20,8),
      'P12':('Modulo011','Peca343','Peca342',10,4)}

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def overlap(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-7 for i in range(3))

def calcos(code,objects,reference):
    parent=META[code][0];matrix=np.array(reference['module_inverse_matrix']).reshape(4,4)
    origin=reference['canonical_origin'];result=[]
    for name,obj in objects.items():
        if not name.startswith('Calco') or not obj['visivel'] or not obj.get('caixa_global'):continue
        ancestor=name;seen=set()
        while ancestor in objects and ancestor not in seen and ancestor!=parent:
            seen.add(ancestor);ancestor=objects[ancestor].get('pai')
        if ancestor!=parent:continue
        box=obj['caixa_global'];points=[]
        for corner in itertools.product(*[(box[i],box[i+3]) for i in range(3)]):
            q=matrix@np.r_[corner,1]
            points.append([q[0]-origin['u0_module_mm'],origin['rear_module_mm']-q[1],q[2]-origin['z0_module_mm']])
        points=np.array(points)
        result.append(dict(name=name,box_uvz_mm=np.r_[points.min(0),points.max(0)].tolist()))
    assert len(result)==META[code][4]
    return result

def corridor(point,axis,outward,length,diameter):
    p=np.array(point,dtype=float);tip=p.copy();tip[axis]+=outward*length
    lo=np.minimum(p,tip);hi=np.maximum(p,tip)
    for i in range(3):
        if i!=axis:lo[i]-=diameter/2;hi[i]+=diameter/2
    return np.r_[lo,hi].tolist()

def main(code):
    geometry=read(OUT/'Lote_B_geometria.json');detail=read(OUT/'Lote_B_detalhamento.json')
    prior=read(OUT/'Geometria_R51.json');product=read(OUT/'Selecao_ferragem.json')
    release=read(ROOT/'ferramentas/site/current_release.json')
    basepath=ROOT/'02_Modelo_3D/Base_verificacao.json.gz';base=json.loads(gzip.decompress(basepath.read_bytes()))
    assert sha(ROOT/release['cadPath'])==release['cadSHA256']==base['sha256']==detail['cad_sha256']==geometry['cad_sha256']
    dims=product['preferred_candidate']['dimensions']
    assert [dims[k] for k in ['arm_keyhole_mm','arm_side_mm','strip_width_mm','small_rear_hole_from_outer_corner_mm']]==[49.5,37.8,16,9.5]
    module=next(m for m in geometry['modules'] if m['code']==code)
    selected=next(v for v in module['variants'] if v['preferred_for_study'])
    wood=selected['boxes_uvz_mm'];fixed=calcos(code,base['objetos'],prior['modules'][code])
    obstacles={**wood,**{c['name']:c['box_uvz_mm'] for c in fixed}}
    w=module['width_internal_mm'];height=module['height_mm'];depth=module['depth_mm']
    # H-58, herdado do loteA, alinha o acesso auxiliar aos calcos superiores.
    # Subir22 deixa10 ate o tampo para o metal e acesso reto com calcos fixos.
    upper_z=height-36;lower_z=90.;arm=upper_z-lower_z
    mounts=[];access=[];rejected=[]
    for side in [0,1]:
        corner=0. if side==0 else w;sign=1 if side==0 else -1
        old=corridor([corner+sign*9.5,19.5,height-58],1,1,depth-19.5,12)
        old_hits=[c['name'] for c in fixed if overlap(old,c['box_uvz_mm'])]
        assert len(old_hits)==1
        rejected.append(dict(side=side,old_upper_z_mm=height-58,auxiliary12_bbox_mm=old,calco_interferences=old_hits))
        u=corner+sign*40.5
        box=[0 if side==0 else w-49.5,18,upper_z-8,49.5 if side==0 else w,55.8,upper_z+8]
        assert not any(overlap(box,b) for b in obstacles.values())
        mounts.append(dict(side=side,carrier=META[code][1+side],corner_u_mm=corner,upper_u_mm=u,
            upper_z_mm=upper_z,envelope_uvz_mm=box,wood_and_fixed_calcos_clear=True,
            screw_reference_only=True,product_mounting_confirmed=False))
        targets=[('wall_anchor',[u,19.5,upper_z],1,1,depth-19.5),
                 ('rear_auxiliary',[corner+sign*9.5,19.5,upper_z],1,1,depth-19.5),
                 ('side_1',[corner,30.8,upper_z],0,sign,100.),
                 ('side_2',[corner,42.8,upper_z],0,sign,100.)]
        for role,at,axis,outward,length in targets:
            generic=corridor(at,axis,outward,length,20)
            hits=[n for n,b in obstacles.items() if overlap(generic,b)]
            # O furo auxiliar a9.5 da lateral nao admite envolvente20:0.5 de invasao.
            candidate_diameter=12 if role=='rear_auxiliary' else 20
            chosen=corridor(at,axis,outward,length,candidate_diameter)
            assert not any(overlap(chosen,b) for b in obstacles.values()),(role,side)
            access.append(dict(side=side,role=role,reference_uvz_mm=at,
                generic20_bbox_mm=generic,generic20_interferences=hits,
                candidate_diameter_mm=candidate_diameter,candidate_bbox_mm=chosen,
                candidate_wood_and_calcos_clear=True,actual_bit_head_grip_verified=False,
                limit='Corredor nominal;nao inclui corpo da ferramenta,mao,cabeca ou chapa do proprio suporte. Ferramenta escolhida apos fixadores.'))
    assert sum(bool(a['generic20_interferences']) for a in access)==2
    # Os canecos e seus corredores internos continuam acessiveis sem os corpos das portas.
    cams=[j for j in detail['joints'] if j['code']==code]
    for j in cams:
        assert j['tool20_wood_clear']
        assert not any(overlap(j['tool_corridor_bbox_mm'],b) for b in [c['box_uvz_mm'] for c in fixed]+[m['envelope_uvz_mm'] for m in mounts])
        assert not any(overlap(j['blind_bore_bbox_mm'],m['envelope_uvz_mm']) for m in mounts)
    a,b=40.5,w-40.5;la,lb=-9.,w+9.
    cases=[c for c in detail['cases'] if c['code']==code];vectors=[];lower=[];certificates=[]
    for c in cases:
        total=c['V_N'];moment=c['M_Nm']*1000;first=c['S_Nmm']
        vertical=[(b*total-first)/(b-a),(first-a*total)/(b-a)]
        for share in [0.,.5,1.]:
            normal=[share*moment/arm,(1-share)*moment/arm]
            normal_first=a*normal[0]+b*normal[1];normal_total=sum(normal)
            comp=[(lb*normal_total-normal_first)/(lb-la),(normal_first-la*normal_total)/(lb-la)]
            force=np.array([0.,0.,-total]);mom=np.cross(c['center_uvz_mm'],force)
            for side in [0,1]:
                u=[a,b][side];f=np.array([0.,-normal[side],vertical[side]]);point=[u,0.,upper_z]
                force+=f;mom+=np.cross(point,f)
                local=np.cross(np.array(point)-[mounts[side]['corner_u_mm'],18,upper_z],f)
                assert vertical[side]>0 and comp[side]>0
                vectors.append(dict(case_id=c['source_case_id'],rho=c['rho_kg_m3'],payload_kg=c['payload_kg'],
                    payload_case=c['payload_case'],doors_deg=c['doors_deg'],share_left=share,side=side,
                    u_mm=u,z_mm=upper_z,h_mm=arm,V_N=vertical[side],T_N=normal[side],
                    R_N=math.hypot(vertical[side],normal[side]),local_M_corner_Nmm=local.tolist(),
                    hardware_mass_included=False,capacity_demonstrated=False))
                lower.append(dict(case_id=c['source_case_id'],share_left=share,side=side,u_mm=[la,lb][side],z_mm=lower_z,
                    C_N=comp[side],reference_area_mm2=1080.,mean_pressure_reference_MPa=comp[side]/1080.,actual_contact_measured=False))
                f=np.array([0.,comp[side],0]);force+=f;mom+=np.cross([[la,0,lower_z],[lb,0,lower_z]][side],f)
            err=max(max(abs(force)),max(abs(mom)));assert err<1e-7
            certificates.append(dict(case_id=c['source_case_id'],share_left=share,force_error_N=float(max(abs(force))),moment_error_Nmm=float(max(abs(mom)))))
    critical={}
    for side in [0,1]:
        target=[v for v in vectors if v['side']==side and v['payload_kg']==META[code][3]]
        for field in ['V_N','T_N','R_N']:
            row=max(target,key=lambda r:r[field]);key=(row['case_id'],row['share_left'],side)
            critical.setdefault(key,dict(row,controls=[]))['controls'].append(field)
    target=[r for r in vectors if r['payload_kg']==META[code][3]]
    demands={field:max(r[field] for r in target) for field in ['V_N','T_N','R_N']}
    result=dict(code=code,status='ESTUDO_NOMINAL_PARA_QUALIFICACAO',cad_opened=False,cad_changed=False,cad_sha256=base['sha256'],
        variant=selected['variant'],payload_target_kg=META[code][3],width_internal_mm=w,height_mm=height,depth_mm=depth,
        candidate=product['preferred_candidate'],candidate_source='Selecao_ferragem.json:catalogo Bigfer p235;geometria persistida,sem nova consulta.',
        mounts=mounts,static_calcos=fixed,accesses=access,cam_accesses_checked=len(cams),rejected_old_height=rejected,
        mounting=dict(upper_z_mm=upper_z,lower_z_hypothesis_mm=lower_z,couple_mm=arm,upper_u_mm=[a,b],lower_u_mm=[la,lb],
            bracket_count_hypothesis=2,metal_bounding_pair_ml=59.8752,back_shift_mm=0,body_dimensions_changed=False,
            single_translation_mirrored_keyholes=False,method='Com gabinete sustentado/nivelado,inserir e apertar fixacoes por dentro;retirar com apoio. Metodo sujeito a confirmacao de produto.',
            height_change_vs_lote_A_mm=22,top_metal_gap_mm=10,
            door_access='Montar antes das portas. Para manutencao,desclipar/remover portas;calcos fixos permanecem. Sem validacao dinamica de dobradicas/portas.'),
        cases=len(cases),vectors=vectors,lower_reactions=lower,certificates=certificates,qualification_cases=list(critical.values()),
        target_separate_maxima=demands,accessory_unit=dict(mass_kg=1,at_u_mm=w/2,at_v_mm=200,additional_V_N=9.80665,
            additional_M_Nm=1.96133,additional_total_T_N=1961.33/arm,interpretation='Sensibilidade por1kg,nao massa de ferragens selecionada;partilha recalculada pelo centro real.'),
        load_path='Base/divisorias/tampo/portas -> juntas e fundo/laterais -> suportes superiores -> ancoragens. Compressao inferior fecha momento. Sem credito a cavilhas/atrito ou composicao monolitica de divisores.',
        limits=[
            'Dois suportes e partilha0/50/100 sao hipoteses;nao quantidade suficiente nem rigidez/capacidade demonstrada.',
            'Cantos e acessos conferidos contra caixas de madeira e calcosR52 salvos. Sem furos/raios/tolerancias ou ferramenta real;nenhum CNC.',
            'Furos auxiliares traseirosu9.5:envolvente20 invade0.5 a lateral. Envolvente12 cabe com3.5 de folga nominal,sem escolher ponta/cabeca ou comprovar ergonomia.',
            'Contatos inferiores nas arestas existentes18x60,Z60..120 sao referencia. Fundo/laterais coplanares:area/centroZ90 reais desconhecidos. Sem calco inferior novo.',
            'Massa madeira+conteudo inclui portas e fundo da variante;sem massa/CG reais de ferragens,fita ou tolerancias alem das hipoteses herdadas.',
            'Momentos locaisrxF reduzem a mesma forca ao canto;nao adicionar ao equilibrio global nem dividir por parafusos sem modelo de juntas.',
            'MetodoBigfer,MDF18,pilotos,passo12/borda9.5,cabeca/arruela/rasgo,retencao,durabilidade e V/T simultaneos ainda exigem dados/ensaio.',
            'Caixa completa,rigidez do fundo/caminho ate os cantos e juntas nao provadas;resultados de placa local nao validam a suspensao.',
            'Sem fatores/ciclos/carga de prova definidos. Ancoragem depende da parede/revestimento e instalacoes reais;nenhum ensaio fisico.'
        ])
    paths=[OUT/'Lote_B_geometria.json',OUT/'Lote_B_detalhamento.json',OUT/'Selecao_ferragem.json',OUT/'Geometria_R51.json',basepath]
    result.update(hash_rule=HASH_RULE,sources_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in paths},script_sha256=sha(Path(__file__)),hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')))
    (OUT/f'{code}_suspensao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for suffix,rows in [('demandas_suspensao',vectors),('reacoes_inferiores',lower),('qualificacao_suspensao',list(critical.values()))]:
        with (OUT/f'{code}_{suffix}.csv').open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    brief=[f'{code} - REQUISITOS DE QUALIFICACAO DA SUSPENSAO',
        'Consulta local preparada;nao enviada. Nenhum ensaio fisico executado.',
        f'Caixa: W interno{w:g};H{height:g};D{depth:g}mm;variante{selected["variant"]};conteudo-alvo{META[code][3]}kg.',
        f'Candidata Bigfer04.02.058 nos cantos laterais/fundo18;2suportes apenas como hipotese. u40.5/{w-40.5:g},Z{upper_z:g};centro inferiorZ90 e braco{arm:g}mm hipoteticos.',
        'Posicao22mm acima da referencia do loteA evita os calcos superiores;metal deixa10mm ate o tampo. Portas desclipadas na manutencao;calcos fixos permanecem.',
        'Entrada dos rasgos espelhados nao permite translacao unica. Confirmar montagem com gabinete sustentado,nivelado e parafusos inseridos/apertados pela frente;remocao tambem com apoio.',
        'Confirmar cabeca/arruela/rasgo5 e passagem por fundo18,pilotos,parafusosMDF,pitch12 e borda9.5,profundidade util,torque,esmagamento/flexao,retencao e durabilidade.',
        'Parafuso auxiliar traseiro:corredor20 invade0.5 a lateral;reserva12 cabe com3.5 ate a lateral e sem atingir calcos. Ponta/cabeca,corpo da ferramenta e mao reais precisam de verificacao.',
        f'Aplicar os {len(critical)} vetores simultaneos preservados em {code}_qualificacao_suspensao.csv. Momentos rxF estao reduzidos ao canto,nao sao cargas extras;nao dividir V pelo numero de parafusos.',
        'Amostras com o painelBP18 real e juntas representativas da caixa. Definir antes protocolo,replicacao,fatores,ciclos,duracao e criterios de deslocamento/rotacao,residual e danos com fabricante/laboratorio/RT.',
        'Demonstrar rigidez da caixa/fundo e caminho ate os cantos. Medir area e centro inferior;coplanaridade nao garante Z90/1080mm2. Nenhuma cavilha/atrito creditado.',
        'Somar massas e centros reais de ferragens antes do ensaio do conjunto. Parede/revestimento,instalacoes e ancoragens definitivas dependem de levantamento.',
        f'Reproducao:python -B ferramentas/aereos/suspender_lote_b.py --movel {code};python -B ferramentas/aereos/conferir_suspensao_b.py --movel {code}.']
    (OUT/f'{code}_qualificacao_suspensao.txt').write_text('\n'.join(brief)+'\n',encoding='utf-8')
    draw(result,wood)
    print(json.dumps(dict(code=code,cases=len(cases),vectors=len(vectors),qualifications=len(critical),generic20_auxiliary_failures=2,**demands)))

def draw(d,wood):
    im=Image.new('RGB',(1500,1080),'#f4f1eb');q=ImageDraw.Draw(im)
    def text(x,y,s,n=23,bold=False):q.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),n),fill='#263c36')
    text(40,24,f"{d['code']} | suspensão compacta em estudo",36,True)
    text(40,80,f"Conteúdo-alvo {d['payload_target_kg']} kg • caixa {d['width_internal_mm']+36:g} × {d['depth_mm']:g} × {d['height_mm']:g} mm • sem mudança de vãos",24)
    q.rounded_rectangle((35,130,1465,660),18,fill='white')
    text(60,151,'VISTA FRONTAL INTERNA — portas retiradas; profundidade omitida',24,True)
    scale=min(1220/(d['width_internal_mm']+36),.68);ox=115;oy=610
    def x(u):return ox+(u+18)*scale
    def y(z):return oy-z*scale
    w=d['width_internal_mm'];h=d['height_mm']
    q.rectangle((x(-18),y(h),x(w+18),y(0)),fill='#ece9e1',outline='#7b776d',width=2)
    for name,b in wood.items():
        if b[4]-b[1]>100:
            q.rectangle((x(b[0]),y(b[5]),x(b[3]),y(b[2])),fill='#d2c7b4',outline='#8d806a',width=2)
    for m in d['mounts']:
        b=m['envelope_uvz_mm'];q.rectangle((x(b[0]),y(b[5]),x(b[3]),y(b[2])),fill='#3a806f',outline='#244e43',width=2)
        xx=x(m['upper_u_mm']);yy=y(m['upper_z_mm']);q.line((xx,yy-55,xx,yy-8),fill='#3a806f',width=4)
        q.polygon([(xx,yy-8),(xx-7,yy-20),(xx+7,yy-20)],fill='#3a806f')
    for u in [-9,w+9]:q.line((x(u)-9,y(120),x(u)+9,y(120)),fill='#bf7d47',width=7)
    text(70,616,f"u superiores: 40,5 / {w-40.5:g} mm; Z {h-36:g}; contato inferior Z90 hipotético; braço {h-126:g} mm.",22)
    q.rounded_rectangle((35,685,1465,1038),18,fill='white')
    text(60,706,'ACESSO E QUALIFICAÇÃO',27,True)
    text(60,757,'2 suportes candidatos: envelope do metal ≈60 mL/par; fundo na posição original.',24)
    text(60,798,'Auxiliar traseiro junto à lateral: Ø20 não cabe; reserva Ø12 cabe nominalmente.',24)
    text(60,839,'Escolher fixadores e ferramenta reais; método e capacidade Bigfer continuam pendentes.',24)
    m=d['target_separate_maxima']
    text(60,887,f"Máximos separados por suporte: V {m['V_N']:.1f} N / T {m['T_N']:.1f} N / R {m['R_N']:.1f} N.",24,True)
    text(60,929,'Usar os vetores simultâneos do CSV; sem massa real de ferragens ou carga de prova.',24)
    text(60,981,'R52 preservada • juntas/caixa, contatos inferiores, parede e ensaios ainda pendentes.',23)
    im.save(OUT/f'{d["code"]}_suspensao.png')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--movel',choices=list(META),required=True)
    main(parser.parse_args().movel)
