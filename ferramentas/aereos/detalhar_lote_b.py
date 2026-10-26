"""Metas de Elias: caixa preferida, ligacoes internas e demandas globais.

Sem produto de suspensao, capacidade de junta ou alteracao CAD.
"""
from pathlib import Path
from collections import Counter
import csv,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontes import sha,HASH_RULE
from reconciliar_lote_b import META,contact

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao';G=9.80665
sys.path.insert(0,str(ROOT/'ferramentas/cinematica'))
from cinematica import Engine
def read(p):return json.loads(p.read_text(encoding='utf-8'))

def canonical(code,world,old):
    if code=='P04':return np.array([2872-world[1],7390-world[0],world[2]-2132])
    m=old['modules'][code];q=np.array(m['module_inverse_matrix']).reshape(4,4)@np.r_[world,1];o=m['canonical_origin']
    return np.array([q[0]-o['u0_module_mm'],o['rear_module_mm']-q[1],q[2]-o['z0_module_mm']])

def joints(module):
    code=module['code'];m=META[code];w,h=m['w'],m['h']
    selected=next(v for v in module['variants'] if v['preferred_for_study'])
    p={n:np.array(b) for n,b in selected['boxes_uvz_mm'].items()};rows=[]
    verticals=[(n,b) for n,b in p.items() if abs(b[3]-b[0]-18)<1e-6 and b[4]-b[1]>100 and b[5]-b[2]>100]
    for name,b in verticals:
        side=b[0]<0 or b[3]>w;u=(b[0]+b[3])/2
        # Acesso ao lado livre: nao entre divisores pareados nem no vao7 deP04.
        access_sign=1
        if name in ['ApoioComumR001','ApoioComumR004','ApoioComumR003','ApoioComumR11','ApoioComumR002']:access_sign=-1
        for horizontal,z in [(m['base'],18.),(m['top'],h-18)]:
            bottom=horizontal==m['base']
            for v in ([90.,158.] if code=='P04' else [90.,258.]):
                if side:
                    left=b[0]<0;point=np.array([0 if left else w,v,9 if bottom else h-9])
                    cam=np.array([34 if left else w-34,v,18 if bottom else h-18])
                    direction=np.array([0,0,-1 if bottom else 1]);cam_part=horizontal;axis='u'
                else:
                    point=np.array([u,v,z]);cam=np.array([u+9*access_sign,v,52 if bottom else h-52])
                    direction=np.array([-access_sign,0,0]);cam_part=name;axis='z'
                kind,area,_=contact(p[name],p[horizontal]);assert kind=='face' and area>0
                # Caixa envolvente do furo cego, incluindo +0,5 na profundidade.
                end=cam+14*direction;lo=np.minimum(cam,end);hi=np.maximum(cam,end)
                for j in range(3):
                    if abs(direction[j])<.5:lo[j]-=7.5;hi[j]+=7.5
                host=p[cam_part];assert np.all(lo>=host[:3]-1e-6) and np.all(hi<=host[3:]+1e-6),(code,name,cam)
                # Corredor de chave20x20x30, so contra madeira, ate a face do caneco.
                lo2=cam.copy();hi2=cam.copy();tip=cam-30*direction
                lo2=np.minimum(lo2,tip);hi2=np.maximum(hi2,tip)
                for j in range(3):
                    if abs(direction[j])<.5:lo2[j]-=10;hi2[j]+=10
                hits=[n for n,bx in p.items() if np.all(np.minimum(hi2,bx[3:])-np.maximum(lo2,bx[:3])>1e-6)]
                rows.append(dict(code=code,id=f'{horizontal}_{name}_{v:g}',a=name,b=horizontal,axis=axis,
                    interface_uvz_mm=point.tolist(),cam_part=cam_part,cam_access_uvz_mm=cam.tolist(),drill_inward=direction.tolist(),
                    blind_bore_bbox_mm=np.r_[lo,hi].tolist(),tool_corridor_bbox_mm=np.r_[lo2,hi2].tolist(),
                    access='interior',bore_inside_host=True,tool20_wood_clear=not hits,tool20_interferences=hits,
                    local_straight_tool_diameter_limit_mm=18 if hits else None,hardware_clearance_verified=False,
                    family='Minifix15 262.26.034+pinoB34 262.28.920 candidatos',
                    underside_face_unbroken=True,nominal_skin_at_max_drill_depth_mm=4.,purchase_quantity=False))
    return rows

def rear_joints(module):
    code=module['code']
    if code=='P12':return [] # Fundo atual encontra base/topo somente por aresta.
    m=META[code];p={n:np.array(b) for n,b in next(v for v in module['variants'] if v['preferred_for_study'])['boxes_uvz_mm'].items()};rows=[]
    # Mesmas12 estacoes u dos estudos parciais; marcador antigo estava emv9,
    # aqui registramos a interfacev18 e a entrada real nominal na traseirav0.
    for u in np.linspace(72,m['w']-72,12):
        for horizontal,z in [(m['base'],9),(m['top'],m['h']-9)]:
            point=np.array([u,18,z]);entry=np.array([u,0,z]);end=np.array([u,50,z])
            assert contact(p[m['back']],p[horizontal])[0]=='face'
            for name,lo,hi in [(m['back'],entry,point),(horizontal,point,end)]:
                a=np.minimum(lo,hi);b=np.maximum(lo,hi);a[[0,2]]-=3.5;b[[0,2]]+=3.5
                assert np.all(a>=p[name][:3]-1e-6) and np.all(b<=p[name][3:]+1e-6)
            rows.append(dict(code=code,id=f'{horizontal}_fundo_{u:.6f}',a=m['back'],b=horizontal,axis='v',
                interface_uvz_mm=point.tolist(),rear_entry_uvz_mm=entry.tolist(),nominal_tip_uvz_mm=end.tolist(),
                family='Confirmat7x50 candidato',nominal_length_beyond_back_mm=32,
                nominal_wood_to_base_underside_mm=5.5 if z==9 else None,
                head_access='traseira;cabeca precisa embutimento compativel com apoio na parede',
                head_pilot_or_capacity_selected=False,purchase_quantity=False,
                source='12estacoes do estudo parcialP17/P04;nao somar como ferragens existentes'))
    return rows

def main():
    geom=read(OUT/'Lote_B_geometria.json');choices=read(OUT/'Lote_B_premissas.json');catalog=read(OUT/'Lote_B_fontes_Minifix.json')
    engine=Engine(ROOT/'04_Moveis/Proximas_decisoes/Cinematica/Snapshot_R52.json');old=read(OUT/'Geometria_R51.json')
    other=read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Geometria_e_portas_R51.json')
    assert engine.data['sha256']==geom['cad_sha256']
    cases=read(OUT/'Resultados.json')['cases']+read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Resultados.json')['cases']
    sources=[];rows=[];summary=[];jrows=[];rear=[];cache={};max_old_error=0.
    for module in geom['modules']:
        code=module['code'];m=META[code];target=choices['payload_targets_kg'][code]
        chosen=next(v for v in module['variants'] if v['preferred_for_study'])
        p={n:np.array(b) for n,b in chosen['boxes_uvz_mm'].items()}
        p0={n:np.array(b) for n,b in module['variants'][0]['boxes_uvz_mm'].items()}
        leaves=other['modules'][code]['doors'] if code=='P04' else old['modules'][code]['leaves']
        source_cases=[c for c in cases if c['code']==code and c['payload_kg'] in [0,target] and c.get('variant','current')=='current']
        for c in source_cases:
            rho=c['rho_kg_m3'];items=[];olditems=[]
            for n,b in p.items():items.append((np.prod(b[3:]-b[:3])*rho/1e9*18.3/18,(b[:3]+b[3:])/2))
            for b in p0.values():olditems.append((np.prod(b[3:]-b[:3])*rho/1e9*18.3/18,(b[:3]+b[3:])/2))
            for leaf,angle in zip(leaves,c['door_angles_deg']):
                key=(code,leaf['leaf'],angle)
                if key not in cache:
                    wanted=[leaf['name']] if code=='P04' else leaf['fronts'];cache[key]=[]
                    for n,world in engine.centers(leaf['leaf'],angle).items():
                        if n not in wanted:continue
                        f=next(f for f in engine.data['leaves'][leaf['leaf']]['fronts'] if f['name']==n)
                        pos=canonical(code,world,old)
                        if code=='P04':
                            ref=next(s['center_uvz_mm'] for s in leaf['samples'] if s['angle_deg']==angle)
                            assert np.max(np.abs(pos-ref))<1e-6
                        cache[key].append((f['volume_mm3'],pos))
                for vol,pos in cache[key]:
                    item=(vol*rho/1e9*18.3/18,pos);items.append(item);olditems.append(item)
            label=c['payload_case'];u=m['w']/2;v=(18+m['d'])/2
            if code=='P04':u=(5*(25+876.5)/2+2.5*(912.5+1320.25)/2+2.5*(1338.25+1764)/2)/10
            if 'front' in label or 'near_' in label:v=m['d']-25
            if 'near_u0' in label:u=.05*m['w']
            if 'near_uL' in label:u=.95*m['w']
            if c['payload_kg']:
                item=(c['payload_kg'],np.array([u,v,0.]));items.append(item);olditems.append(item)
            oldmass=sum(x for x,_ in olditems);oldfirst=sum((x*q for x,q in olditems),np.zeros(3))
            historicalmass=c.get('wood_plus_content_kg',c.get('total_wood_plus_content_kg'))
            err=np.max(np.abs(oldfirst[:2]-historicalmass*np.array(c['center_uvz_mm'])[:2]));max_old_error=max(max_old_error,float(err))
            assert err<1e-5 and abs(oldmass-historicalmass)<1e-7,(code,c['id'],err)
            mass=float(sum(x for x,_ in items));first=sum((x*q for x,q in items),np.zeros(3))
            rows.append(dict(code=code,source_case_id=c['id'],rho_kg_m3=rho,variant=chosen['variant'],
                payload_kg=c['payload_kg'],payload_case=label,doors_deg=c['door_angles_deg'],mass_wood_contents_kg=mass,
                center_uvz_mm=(first/mass).tolist(),V_N=mass*G,M_Nm=float(first[1]*G/1000),S_Nmm=float(first[0]*G),
                accessory_mass_included=False,payload_distribution_selected=False,
                T_formula='T_total_N=1000*M_Nm/braco_vertical_real_mm;sem partilha ou produto escolhido'))
        z=[r for r in rows if r['code']==code and r['payload_kg']==target];maxm=max(z,key=lambda r:r['M_Nm']);maxs=max(z,key=lambda r:r['S_Nmm'])
        jrows+=joints(module)
        rear+=rear_joints(module)
        summary.append(dict(code=code,target_contents_kg=target,case_count=sum(r['code']==code for r in rows),
            mass_range_kg=[min(r['mass_wood_contents_kg'] for r in z),max(r['mass_wood_contents_kg'] for r in z)],
            max_V_N=max(r['V_N'] for r in z),max_M_case=maxm,max_lateral_first_moment_case=maxs,
            full_back_mass_delta_range_kg=[module['full_back_additional_volume_mm3']*rho/1e9*18.3/18 for rho in [650,900]],
            per_accessory_kg_at_v200mm=dict(V_N=G,M_Nm=G*.2),
            nominal_MF_positions=sum(r['code']==code for r in jrows)))
    paths=[OUT/n for n in ['Lote_B_geometria.json','Lote_B_premissas.json','Lote_B_fontes_Minifix.json','Resultados.json','Geometria_R51.json']]
    paths += [ROOT/n for n in ['04_Moveis/P04/Suspensao_P04_P15/Resultados.json','04_Moveis/P04/Suspensao_P04_P15/Geometria_e_portas_R51.json','04_Moveis/Proximas_decisoes/Cinematica/Snapshot_R52.json','ferramentas/cinematica/cinematica.py','ferramentas/aereos/reconciliar_lote_b.py']]
    result=dict(scope='LoteB condicionado:massas/demandas e proposta nominal de acessoMinifix,nao capacidade.',
        cad_sha256=geom['cad_sha256'],cad_changed=False,summary=summary,cases=rows,joints=jrows,rear_joints=rear,
        old_case_max_first_moment_error_kgmm=max_old_error,
        minifix_catalog=catalog,hash_rule=HASH_RULE,sources_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in paths},
        script_sha256=sha(Path(__file__)),hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')),
        rear_reconciliation='R00 continua separado:CF18/12/9 emP17/P04/P12;48pontos base/topo-fundo herdam as estacoes dos estudos parciais,nao compras nem capacidade. Se adotados:CF42/36/9 como contagem candidata,R00+24/+24/+0. P04 preserva2CF por divisor doR00;nao acrescentar tambem o terceiro marcador de cada divisor do estudo parcial. Face-a-face4+4 e cavilhas continuam separados/sem posicoes novas ou credito de capacidade.',
        limits=['Metas globais20/10/10,nao por nicho. Distribuicao5/2,5/2,5P04 e concentracoes sao cenarios anteriores,nao escolha de Elias.',
        'Densidades650/800/900 e fator18,3/18 sao hipoteses de massa;sem pesagem ou massa/CG de ferragens.',
        'P04 inclui faixa7 ja no acervo apenas como massa nominal;nao adotada ou usada como reforco.',
        '60posicoes Minifix reconciliam24/24/12 doR00,nao60conectores adicionais. Confirmat inferior antigo nao pode permanecer como furo passante.',
        'Corredor20x20x30 verifica apenas madeira. Quatro acessosP04 lateral esquerda interferem1mm no divisor:u34-10=24 contra faceu25;diametro reto maximo18 nesta zona,sem ferramenta selecionada. Nao corpos de dobradicas,calcos,parafusos,maos ou montagem completa.',
        'Furo13,5+0,5 deixa4mm nominais em18;espessura real,pilotos,embutimento8 e resistencia/rigidez ainda pendentes.',
        'Flechas locais anteriores dependem de rigidez hipotetica das juntas;nao transferir resultado para novo Minifix.',
        'Nenhum numero de suportes,partilha,produto de suspensao,ancoragem ou resistencia da caixa escolhidos;nao dividirV por furos.'])
    (OUT/'Lote_B_detalhamento.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for name,data in [('Lote_B_ligacoes_internas.csv',jrows),('Lote_B_ligacoes_traseiras.csv',rear),('Lote_B_demandas.csv',rows)]:
        with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]),delimiter=';');writer.writeheader();writer.writerows(data)
    draw(summary)
    print(json.dumps(dict(cases=len(rows),internal_minifix_positions=len(jrows),summary=[{k:s[k] for k in ['code','mass_range_kg','max_V_N','nominal_MF_positions']} for s in summary])))

def draw(summaries):
    im=Image.new('RGB',(1450,900),'#f4f1eb');q=ImageDraw.Draw(im)
    def t(x,y,s,n=24,b=False,c='#293a31'):q.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n),fill=c)
    t(40,24,'P17 / P04 / P12 | conteúdo + peso do armário',34,True)
    t(40,80,'Estudo nominal: fundos inteiros P17/P04; base limpa nos três. R52 preservada.',24)
    for i,s in enumerate(summaries):
        x=40+i*470;q.rounded_rectangle((x,140,x+440,490),16,fill='white')
        t(x+20,160,s['code'],31,True);t(x+20,216,f"Conteúdo: {s['target_contents_kg']} kg",28,True)
        lo,hi=s['mass_range_kg'];t(x+20,271,f'Conjunto: {lo:.1f}–{hi:.1f} kg',27)
        t(x+20,319,'Madeira + conteúdo; sem ferragens',20)
        t(x+20,371,f"Momento máximo: {s['max_M_case']['M_Nm']:.1f} Nm",23)
        t(x+20,426,f"{s['nominal_MF_positions']} posições Minifix internas",23)
    q.rounded_rectangle((40,520,1410,870),16,fill='white')
    t(65,545,'Como preservar a face inferior',28,True)
    t(65,600,'Base–laterais: caneco acessível por cima da base, dentro do armário.',24)
    t(65,642,'Base–divisórias: caneco na face interna da divisória; pino na base.',24)
    t(65,684,'Pares de divisórias: acesso pelas faces livres, sem unir as duas chapas como 36 mm.',24)
    t(65,737,'P04: quatro acessos usam Allen curta SW4; conferir o complemento de acesso e suspensão P04.',22,True,c='#a65438')
    t(65,805,'São solicitações e posições de estudo. Juntas, ferragens e suspensão ainda exigem comprovação.',22,True)
    im.save(OUT/'Lote_B_caixa_e_ligacoes.png')

if __name__=='__main__':main()
