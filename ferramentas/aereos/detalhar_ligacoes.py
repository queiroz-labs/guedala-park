"""LoteP09/P11/P15: juntas, acesso e solicitacoes de uma implantacao nominal.

Sem CAD, furos definitivos ou capacidade de suspensao atribuida a produto.
Recalcula os pesos/CG com portasR52 e reconcilia dimensoes das fichas atuais.
"""
from pathlib import Path
import csv,hashlib,itertools,json,math,re,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao';G=9.80665
sys.path.insert(0,str(ROOT/'ferramentas/cinematica'))
from cinematica import Engine
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ENGINE=Engine(ROOT/'04_Moveis/Proximas_decisoes/Cinematica/Snapshot_R52.json')
OLD=read(OUT/'Geometria_R51.json');OTHER=read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Geometria_e_portas_R51.json')
W={'P09':614.,'P11':661.,'P15':799.};H={'P09':592.,'P11':610.,'P15':580.};D=330.

def profiles(code,variant='current'):
    w,h=W[code],H[code]
    names={'P09':['Peca316','Peca315','Peca317','Peca318','Peca319'],
           'P11':['Peca335','Peca334','Peca336','Peca337','Peca338'],
           'P15':['Peca360','Peca359','Peca361','Peca362','Peca363']}[code]
    boxes=[[-18,0,0,0,D,h],[w,0,0,w+18,D,h],[0,0,18,w,18,h-18],[0,18,0,w,D,18],[0,18,h-18,w,D,h]]
    if code=='P09':names+=['Peca320'];boxes+=[[w/2-9,18,18,w/2+9,D,h-18]]
    if code=='P11':names+=['Peca339'];boxes+=[[0,18,276,w,D,294]]
    if variant=='wood_study':
        assert code=='P15'
        boxes[0][2]=boxes[1][2]=-18
        boxes[2][2]=-18;boxes[2][5]=h
        names+=['P15_camada_inferior_ESTUDO'];boxes+=[[0,18,-18,w,D,0]]
    return {n:np.array(b,float) for n,b in zip(names,boxes)}

def canonical(code,world):
    if code=='P15':return np.array([world[0]-3563,7000-world[1],world[2]-1650])
    m=OLD['modules'][code];p=(np.array(m['module_inverse_matrix']).reshape(4,4)@np.r_[world,1])[:3];o=m['canonical_origin']
    return np.array([p[0]-o['u0_module_mm'],o['rear_module_mm']-p[1],p[2]-o['z0_module_mm']])

def masses(case):
    code=case['code'];variant=case.get('variant','current');rho=case['rho_kg_m3'];items=[]
    for b in profiles(code,variant).values():items.append((float(np.prod(b[3:]-b[:3])*rho/1e9*18.3/18),(b[:3]+b[3:])/2))
    leaves=OTHER['modules']['P15']['doors'] if code=='P15' else OLD['modules'][code]['leaves']
    for leaf,angle in zip(leaves,case['door_angles_deg']):
        for name,cg in ENGINE.centers(leaf['leaf'],angle).items():
            wanted=[leaf['name']] if code=='P15' else leaf['fronts']
            if name not in wanted:continue
            front=next(f for f in ENGINE.data['leaves'][leaf['leaf']]['fronts'] if f['name']==name)
            items.append((front['volume_mm3']*rho/1e9*18.3/18,canonical(code,cg)))
    total_wood=sum(m for m,_ in items)
    oldtotal=case.get('wood_plus_content_kg',case.get('total_wood_plus_content_kg'))
    # Conteudo e posicao conservados; desconte as madeiras calculadas da
    # resultante antiga para recuperar o ponto de conteudo, sem contar duas vezes.
    oldfirst=oldtotal*np.array(case['center_uvz_mm']);woodfirst=sum((m*c for m,c in items),np.zeros(3))
    kg=case['payload_kg']
    if kg:
        # Os tres programas antigos usam posicaoZ0 para o conteudo gravitacional.
        # u/v sao declarados nas etiquetas e parametros do estudo original.
        label=case['payload_case'];w=W[code]
        if label in ['distributed','5_center','10_center','20_center']:u,v=w/2,174.
        elif label in ['front','5_front','10_front','20_front']:u,v=w/2,D-25
        elif label in ['near_u0','5_near_u0','10_near_u0','20_near_u0']:u,v=.05*w,D-25
        elif label in ['near_uL','5_near_uL','10_near_uL','20_near_uL']:u,v=.95*w,D-25
        else:raise ValueError(label)
        items.append((kg,np.array([u,v,0.])))
    assert abs(total_wood+kg-oldtotal)<1e-8
    recomputed=sum((m*c for m,c in items),np.zeros(3))
    # Z pode diferir nas tabelas antigas pelo CG de volumes alem do datum;
    # a conta de suspensao gravitacional usa apenasu/v, conferidos abaixo.
    assert np.max(np.abs(recomputed[:2]-oldfirst[:2]))<1e-6,(code,variant,recomputed,oldfirst)
    # Reserva1kg de ferragens fixas no centro, ainda sem pesagem/CG reais.
    items.append((1.,np.array([W[code]/2,174.,H[code]/2])))
    mass=sum(m for m,_ in items);first=sum((m*c for m,c in items),np.zeros(3))
    return mass,first

def joints(code,variant='current'):
    p=profiles(code,variant);w,h=W[code],H[code];rows=[]
    left,right,back,base,top=list(p)[:5]
    def add(name,a,b,point,axis,family,existing=False):
        rows.append(dict(code=code,variant=variant,id=name,a=a,b=b,u_mm=point[0],v_mm=point[1],z_mm=point[2],
                         axis=axis,family=family,existing=existing,status='Ponto nominal de interface,nao CNC/piloto ou capacidade'))
    if code=='P09':
        div='Peca320'
        for horizontal,z in [(base,9),(top,h-9)]:
            for side,u in [(left,0),(right,w)]:
                for v in [90,258]:add(f'{horizontal}_{side}_{v}',side,horizontal,[u,v,z],'u','Confirmat7x50 candidato')
                add(f'{horizontal}_{side}_cavilha',side,horizontal,[u,174,z],'u','Cavilha8x30 posicionamento')
        for side,u in [(left,0),(right,w)]:
            for z in [90,h/2,h-90]:add(f'{back}_{side}_{z}',side,back,[u,9,z],'u','Confirmat7x50 candidato')
            for z in [193,399]:add(f'{back}_{side}_cav_{z}',side,back,[u,9,z],'u','Cavilha8x30 posicionamento')
        for horizontal,z in [(base,18),(top,h-18)]:
            for v in [90,258]:add(f'{div}_{horizontal}_{v}',horizontal,div,[w/2,v,z],'z','Confirmat7x50 candidato:retencao axial')
            add(f'{div}_{horizontal}_cav',horizontal,div,[w/2,174,z],'z','Cavilha8x30 posicionamento')
        for z in [90,h-90]:add(f'{div}_{back}_{z}',back,div,[w/2,18,z],'v','Confirmat7x50 candidato')
        add(f'{div}_{back}_cav',back,div,[w/2,18,h/2],'v','Cavilha8x30 posicionamento')
    else:
        horizontals=[(base,9),(top,h-9)]+([('Peca339',285)] if code=='P11' else [])
        for horizontal,z in horizontals:
            for side,u in [(left,0),(right,w)]:
                for v in [78,270]:add(f'{horizontal}_{side}_{v}',horizontal,side,[u,v,z],'u','Minifix262.26.034+pino262.28.920 existente',True)
        heights=[90,305,520] if code=='P11' else ([54,281,508] if variant=='wood_study' else [90,290,490])
        for side,u in [(left,0),(right,w)]:
            for z in heights:add(f'{back}_{side}_{z}',side,back,[u,9,z],'u','Confirmat7x50 candidato')
        if code=='P11':
            for u in [72,244,417,589]:add(f'prateleira_fundo_{u}',back,'Peca339',[u,18,285],'v','Confirmat7x50 candidato')
            for u in [158,330.5,503]:add(f'prateleira_cavilha_{u}',back,'Peca339',[u,18,285],'v','Cavilha8x30 posicionamento')
        elif variant=='wood_study':
            for name,z in [(base,9),(top,571)]:
                for u in [72,203,334,465,596,727]:add(f'{name}_fundo_{u}',back,name,[u,18,z],'v','Confirmat7x50 candidato')
    return rows

def main():
    manifest=read(ROOT/'ferramentas/site/current_release.json');cad=ROOT/manifest['cadPath']
    assert sha(cad)==manifest['cadSHA256']==ENGINE.data['sha256']
    audit=[];oldgeoms={**{c:OLD['modules'][c] for c in ['P09','P11']},'P15':OTHER['modules']['P15']}
    for code in W:
        csvpath=ROOT/f'06_Entregas/Fichas_fabricacao/{code}-pecas.csv'
        dimensions={}
        with csvpath.open(encoding='utf-8-sig',newline='') as f:
            for r in csv.DictReader(f,delimiter=';'):
                for name in r['IDs CAD'].split(' | '):dimensions[name]=sorted(float(r[k]) for k in ['C nominal mm','L nominal mm','Esp. envelope mm'])
        oldparts={r['name']:r for r in oldgeoms[code]['body']}
        for name,b in profiles(code).items():
            dims=sorted((b[3:]-b[:3]).tolist());assert dims==dimensions[name],(code,name,dims,dimensions[name])
            assert abs(np.prod(b[3:]-b[:3])-oldparts[name]['volume_mm3'])<1e-5
            assert np.max(np.abs((b[:3]+b[3:])/2-oldparts[name]['center_uvz_mm']))<1e-5
        audit.append(dict(code=code,source_csv=str(csvpath.relative_to(ROOT)),sha256=sha(csvpath),panels=len(profiles(code))))
    oldcases=read(OUT/'Resultados.json')['cases']
    oldcases=[r for r in oldcases if r['code'] in ['P09','P11']]
    oldcases += [r for r in read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Resultados.json')['cases'] if r['code']=='P15']
    loads=[];critical={};equilibrium=[]
    for ic,c in enumerate(oldcases):
        code=c['code'];variant=c.get('variant','current');mass,first=masses(c)
        w,h=W[code],H[code];a,b=72.,w-72;upper=h-90;lower=90.;arm=upper-lower
        V=mass*G;M=first[1]*G;S=first[0]*G
        vertical=[(b*V-S)/(b-a),(S-a*V)/(b-a)];T=M/arm
        for share in [0.,.5,1.]:
            normal=[share*T,(1-share)*T]
            for side in [0,1]:
                row=dict(code=code,variant=variant,source_case_id=c['id'],rho=c['rho_kg_m3'],payload_case=c['payload_case'],payload_kg=c['payload_kg'],
                    doors_deg='|'.join(map(str,c['door_angles_deg'])),traction_share_left=share,side=side,u_mm=[a,b][side],upper_z_mm=upper,
                    lower_z_mm=lower,couple_h_mm=arm,V_N=vertical[side],T_N=normal[side],R_N=math.hypot(vertical[side],normal[side]),
                    total_mass_with_accessory_reserve_kg=mass,total_M_Nm=M/1000,wall_gap_mm=0.,anchors_or_capacity_selected=False)
                loads.append(row);key=(code,variant,c['payload_kg'])
                if key not in critical or row['R_N']>critical[key]['R_N']:critical[key]=row
            err=max(abs(sum(vertical)-V),abs(a*vertical[0]+b*vertical[1]-S),abs(sum(normal)*arm-M))
            equilibrium.append(err);assert err<1e-7
    jrows=[]
    for code,variant in [('P09','current'),('P11','current'),('P15','current'),('P15','wood_study')]:jrows+=joints(code,variant)
    # Conferencia de acesso: quatro zonas36x36x8 internas e corredor nominal
    # de ferramenta20, apenas contra madeira; exclui corpos de ferragens.
    access=[]
    for code in W:
        for u,z in itertools.product([72,W[code]-72],[90,H[code]-90]):
            tool=np.array([u-10,18,z-10,u+10,D,z+10]);zone=np.array([u-18,18,z-18,u+18,26,z+18])
            for name,b in profiles(code).items():
                for bb in [tool,zone]:assert not np.all(np.minimum(bb[3:],b[3:])-np.maximum(bb[:3],b[:3])>1e-7),(code,name)
            access.append(dict(code=code,u_mm=u,z_mm=z,reserve_uvz_mm=zone.tolist(),tool20_bbox_mm=tool.tolist(),wood_clear=True,hardware_clearance_verified=False))
    # Aresta nao virou face para uma ligacao horizontal impossivel.
    contacts=[]
    for code in W:
        p=profiles(code);names=list(p)
        for name in names[3:5]:
            b1,b2=p[names[2]],p[name];over=np.minimum(b1[3:],b2[3:])-np.maximum(b1[:3],b2[:3])
            assert sum(abs(v)<1e-7 for v in over)==2
            contacts.append(dict(code=code,a=names[2],b=name,current='somente_aresta',direct_rear_screw_in_current_box=False))
    alternatives=[]
    for code in W:
        free_height=H[code]-36-(18 if code=='P11' else 0)
        free_width=W[code]-(18 if code=='P09' else 0)
        affected=list(profiles(code))[2:]
        alternatives.append(dict(code=code,kind='reserva_traseira16_ESTUDO',back_relocation_toward_room_mm=16,
            outside_depth_change_mm=0,internal_depth_old_mm=312,internal_depth_new_mm=296,
            storage_volume_reduction_liters=free_height*free_width*16/1e6,
            affected_body_ids=affected,load_capacity_revalidated=False,
            note='Geometria alternativa,nao escolha. Reposicionar fundo e reduzir base/topo/prateleira/divisor;validar produto no fundo18. Nao rasgar16 na espessura18 nem afastar todo o movel silenciosamente.'))
    sources=[OUT/'Resultados.json',OUT/'Geometria_R51.json',
        ROOT/'04_Moveis/P04/Suspensao_P04_P15/Resultados.json',ROOT/'04_Moveis/P04/Suspensao_P04_P15/Geometria_e_portas_R51.json',
        ROOT/'04_Moveis/Proximas_decisoes/Cinematica/Snapshot_R52.json',ROOT/'AGENTS.md',
        *[ROOT/f'06_Entregas/Fichas_fabricacao/{c}-pecas.csv' for c in W]]
    pdfdir=ROOT/'09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao'
    sources += list(sorted(pdfdir.glob('*.pdf')))
    sources += [ROOT/'09_Referencias/Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf']
    report=dict(cad_revision='R52',cad_sha256=sha(cad),cad_opened=False,cad_changed=False,coordinate_system='u:esquerda interna;v:parede0 para frente330;z:base externa original0. Nao coordenadas globais/CNC.',
        input_reconciliation=audit,body_volumes_and_centers_match_saved_R51=True,R52_door_CGs_recomputed=True,
        cases_recomputed=len(oldcases),group_load_rows=len(loads),maximum_equilibrium_residual_N_Nmm=max(equilibrium),
        axes_nominal=jrows,access=access,edge_only_contacts=contacts,critical_groups=list(critical.values()),
        alternative_rear_reserve=alternatives,
        source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sources},generator_sha256=sha(Path(__file__)),
        hardware_existing_counts={'P11_Minifix':12,'P15_Minifix':8},
        accessory_mass_reserve_kg=1.,depurador_included_in_P09=False,
        P15_new_side_pin_base_height_mm=27.,P15_old_side_pin_base_height_mm=9.,
        depurador_geometric_reach=dict(envelope_top_Z=1916,base_bottom_Z=1958,gap_mm=42,manual_screw_mm=30,max_tip_from_envelope_Z=1946,unreached_gap_mm=12,
            limitation='Gabarito nao representa abas reais. Conta so rejeita ponte automatica do gabarito;nao reprova o aparelho ou autoriza parafuso maior.'),
        mounting_status='Fixacao direta e estudo de implantacao;produto/grupos/placas,caixa e parede nao dimensionados. h e partilha precisam ser demonstrados.',
        limits=['Sem curva/capacidade fisica de junta,inercia/ruptura/ancoragem ou ensaio;nao libera cargas.',
            'Corpos de ferragens,furos completos e ferramenta real excluidos da verificacao de madeira.',
            'Reserva1kg nao e pesagem. Valores sem majoracao,impacto ou efeitos de mao.',
            'P15 composto e proposta separada;camadas distintas18+18,sem produto/processo de composicao. TitebondMelamine excluida.',
            '20kg no arquivo sao cenarios globais,nao capacidade local nem20kg por nivel.',
            'Cavilhas so posicionamento;Minifix existentes nao sao novas compras. Pontos nao sao pilotos ouquantitativo adicional.'])
    (OUT/'Detalhamento_P09_P11_P15.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for file,rows in [('Mapa_ligacoes_P09_P11_P15.csv',jrows),('Solicitacoes_fixacao_direta.csv',loads)]:
        with (OUT/file).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    draw(report)
    print(json.dumps(dict(cases=len(oldcases),group_load_rows=len(loads),joints=len(jrows),wood_access_zones=len(access),max_equilibrium_error=max(equilibrium),R52_unchanged=sha(cad)==manifest['cadSHA256']),ensure_ascii=True))

def draw(d):
    im=Image.new('RGB',(1500,1090),'#f4f1eb');q=ImageDraw.Draw(im)
    def txt(x,y,t,size=23,b=False,c='#293a31'):q.text((x,y),t,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),size),fill=c)
    txt(45,28,'P09 / P11 / P15 | juntas e suspensão',36,True)
    txt(45,82,'Implantação de estudo • acesso pela frente • R52 preservada • sem capacidade liberada',23)
    for i,code in enumerate(W):
        x=45+i*490;q.rounded_rectangle((x,140,x+460,590),16,fill='white');txt(x+20,155,code+' | fundo 18 na traseira',24,True)
        w,h=W[code],H[code];sx=400/w;sy=300/h
        q.rectangle((x+30,210,x+430,510),outline='#81725d',width=3)
        if code=='P11':q.line((x+30,510-285*sy,x+430,510-285*sy),fill='#b7a68a',width=5)
        if code=='P09':q.line((x+230,210,x+230,510),fill='#b7a68a',width=6)
        for u,z in itertools.product([72,w-72],[90,h-90]):
            px=x+30+u*sx;py=510-z*sy;q.ellipse((px-8,py-8,px+8,py+8),fill='#356b51')
        txt(x+20,535,f'u=72/{w-72:g}  |  z=90/{h-90:g} mm',22)
    q.rounded_rectangle((45,615,1455,1035),18,fill='white')
    txt(65,635,'O caminho precisa existir em cada encontro',29,True)
    txt(70,695,'P09',25,True);txt(190,695,'Divisor ligado à base, topo e fundo; retorno de 20 mm e depurador pendentes.',23)
    txt(70,750,'P11',25,True);txt(190,750,'Preservar 12 Minifix; 10 Confirmat + 3 cavilhas do estudo, sem duplicar compras.',23)
    txt(70,805,'P15',25,True);txt(190,805,'Composição 18+18 depende de processo/ensaio. Pino: 9 → 27 mm na nova lateral.',23)
    txt(70,870,'Base/topo atuais encontram o fundo só pela aresta: não desenhar parafuso nesse vazio.',24,True)
    txt(70,925,'Zonas verdes são reservas de estudo, não furos/ancoragens executivas.',24)
    txt(70,970,'HB65: página 65 kg × ficha 60 kg; desenho e condições precisam de confirmação do fabricante.',23)
    im.save(OUT/'Ligacoes_P09_P11_P15.png')

if __name__=='__main__':main()
