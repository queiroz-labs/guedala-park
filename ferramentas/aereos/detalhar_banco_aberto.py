"""P20 aberto: sentido do articulador, reacoes da piano e requisitos de montagem.
Fontes persistidas; eixo/pontos do estudo continuam condicionais, sem editar CAD.
"""
from pathlib import Path
import csv, gzip, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontes import sha, HASH_RULE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'04_Moveis/P20/Assento_fechado'
REF = ROOT/'04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia'
G = 9.80665


def read(p): return json.loads(p.read_text(encoding='utf-8'))


def rotate(p, axis, deg):
    t = math.radians(deg);x,z = np.array(p)-axis
    return np.array(axis)+[x*math.cos(t)-z*math.sin(t), x*math.sin(t)+z*math.cos(t)]


def distance(sc, deg):
    return float(np.linalg.norm(rotate(sc['mobile'], sc['axis'], deg)-sc['fixed']))


def main():
    geom = read(OUT/'Geometria_R51.json');prior = read(REF/'Resultados.json')
    basepath = ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base = json.loads(gzip.decompress(basepath.read_bytes()))
    release = read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath']) == base['sha256']
    for lid in geom['lids']:
        assert np.allclose(lid['box'], base['objetos'][lid['name']]['caixa_global'], atol=1e-6)
    rows, operation, lock = [], [], []
    for lid, scid in zip(geom['lids'], ['banco_tampa1','banco_tampa2']):
        sc = next(r for r in prior['articuladores'] if r['id']==scid)
        b = lid['box'];axis = sc['axis'];ymid=(b[1]+b[4])/2;ys=sum(sc['side'])/2
        cgclosed=[(b[0]+b[3])/2,(b[2]+b[5])/2]
        cgopen=rotate(cgclosed, axis, 90);mobile=rotate(sc['mobile'], axis, 90)
        origin=np.array([axis[0],ymid,axis[1]])
        cg=np.array([cgopen[0],ymid,cgopen[1]])
        at=np.array([mobile[0],ys,mobile[1]])
        fixed=np.array([sc['fixed'][0],ys,sc['fixed'][1]])
        tension=(fixed-at)/np.linalg.norm(fixed-at)
        ends=[np.array([axis[0],b[y],axis[1]]) for y in [1,4]]
        # Uma forca axial no articulador e quatro componentes nas duas
        # extremidades equivalentes da linha da piano. Nao sao parafusos.
        basis=[(at,tension),(ends[0],np.array([1.,0,0])),(ends[0],np.array([0.,0,1.])),
               (ends[1],np.array([1.,0,0])),(ends[1],np.array([0.,0,1.]))]
        columns=[np.r_[f,np.cross(p-origin,f)] for p,f in basis]
        A=np.array(columns).T;idx=[0,2,3,4,5]
        for rho in [650.,800.,900.]:
            mass=lid['volume_mm3']*rho/1e9;weight=np.array([0.,0.,-mass*G])
            gravity=np.r_[weight,np.cross(cg-origin,weight)]
            solved=np.linalg.solve(A[idx],-gravity[idx])
            forces=[solved[i]*f for i,(_,f) in enumerate(basis)]
            residual=A@solved+gravity
            assert np.max(np.abs(residual))<1e-8 and solved[0]<0
            hinge=[forces[1]+forces[2],forces[3]+forces[4]]
            rows.append(dict(lid=lid['name'],rho_kg_m3=rho,wood_envelope_mass_kg=mass,angle_deg=90,
                origin_mm=origin.tolist(),cg_open_mm=cg.tolist(),mobile_terminal_mm=at.tolist(),fixed_terminal_mm=fixed.tolist(),
                gravity_force_N=weight.tolist(),tension_positive_N=float(solved[0]),compression_N=float(-solved[0]),
                force_articulator_on_lid_N=forces[0].tolist(),force_lid_on_articulator_N=(-forces[0]).tolist(),
                fixed_terminal_receives_N=(-forces[0]).tolist(),hinge_equivalent_points_mm=[p.tolist() for p in ends],
                hinge_forces_on_lid_N=[f.tolist() for f in hinge],hinge_forces_on_body_N=[(-f).tolist() for f in hinge],
                hinge_resultant_N=sum(hinge,np.zeros(3)).tolist(),side_offset_from_CG_mm=ys-ymid,
                gravity_moment_about_hinge_Nm=float(gravity[4]/1000),equilibrium_residual=residual.tolist(),
                capacity_demonstrated=False,scope='Tampa sem almofada/mao; massa de metais ausente. Grupos equivalentes de linha, nao esforcos por parafuso.'))
            for angle in [0,15,30,45,60,75,90]:
                p=rotate(cgclosed,axis,angle)
                handle_radius=math.hypot(b[3]-axis[0],cgclosed[1]-axis[1])
                operation.append(dict(lid=lid['name'],rho_kg_m3=rho,angle_deg=angle,
                    gravity_closing_moment_Nm=mass*G*(p[0]-axis[0])/1000,
                    tangent_hand_force_ideal_N=mass*G*(p[0]-axis[0])/handle_radius,
                    energy_above_closed_J=mass*G*(p[1]-cgclosed[1])/1000,
                    terminal_distance_mm=distance(sc,angle),
                    articulator_axial_force_during_folded_motion=None))
        for target in [280.,285.,288.,290.,291.]:
            lo,hi=0.,90.
            for _ in range(70):
                mid=(lo+hi)/2
                if distance(sc,mid)<target:lo=mid
                else:hi=mid
            angle=(lo+hi)/2
            assert abs(distance(sc,angle)-target)<1e-7
            lock.append(dict(lid=lid['name'],hypothetical_lock_distance_mm=target,angle_deg=angle,
                shortfall_to_90_deg=90-angle,extra_straight_extension_after_291_mm=0.,
                product_lock_distance_confirmed=False))
    known=dict(piano_reference='Mahler Ref.54 desenho arquivado',length_mm=1991,length_tolerance_mm=1,
        width_open_mm=30.8,sheet_mm=.8,pin_mm=2.,segments_mm=[971,825],
        remainder_min_before_saw_and_end_trimming_mm=1990-971-825,
        source='Fontes/Mahler_54_2000.pdf,pagina1; cotas visuais conferidas em26/10',
        axis_to_mount_face_mm=None,outer_knuckle_diameter_confirmed_mm=None,pilot_and_screw_pattern_selected=False)
    actions=[
        dict(id='B02_piano',part='Eixo e abas da piano',nominal='X100/Z423.1 e tampasZ400..420; junta2mm ao encosto',
             missing='Perfil completo eixo-face/no externo; suporte fixo ligado ao corpo; rebaixo/apoio e acomodacao sob almofada.',
             next='Montar retalho de secao com o produto real e documentar eixo/apoio/parafusos antes de girar o conjunto.',physical_result=None),
        dict(id='B03_terminal_maior',part='Terminal movel da tampa971',nominal='EixoZ378:22mm abaixo da face inferiorZ400',
             missing='Terminal capaz de realizar22mm,base de fixacao e ferramenta;espaco da jarra.',
             next='Medir produto e conferir conjunto montado no setor do liquidificador.',physical_result=None),
        dict(id='B03_terminal_menor',part='Terminal movel da tampa825',nominal='EixoZ370:30mm abaixo da face inferiorZ400',
             missing='Terminal capaz de realizar30mm,base de fixacao e ferramenta;prateleiraZ310.',
             next='Medir produto e preservar a prateleira;folga27.54 do estudo de barras nao inclui terminais.',physical_result=None),
        dict(id='B04_trava',part='Travamento e liberacao',nominal='Distancia291mm a90graus nos dois estudos',
             missing='Distancia real ao travar,modo/curso de liberacao e capacidade em compressao.',
             next='Exigir dados ou medir amostra;nao dar mais curso por suposicao nem usar carga humana.',physical_result=None),
        dict(id='B04_torcao',part='Piano e fixacao do corpo',nominal='Articulador fora do centro lateral;reacoes nas extremidades equivalentes calculadas',
             missing='Rigidez de torcao da tampa,piano e apoio fixo;distribuicao pelos parafusos.',
             next='Verificar junta completa e retencao no prototipo,com deformacao/residual e protocolo definidos.',physical_result=None),
    ]
    sources=[OUT/'Geometria_R51.json',REF/'Resultados.json',REF/'Fontes/Mahler_54_2000.pdf',REF/'Fontes/Bigfer_112.pdf',basepath]
    d=dict(status='P20_ABERTO_NOMINAL_SEM_CAPACIDADE',cad_sha256=base['sha256'],cad_opened=False,cad_changed=False,
        physical_tests_executed=0,known_piano=known,load_cases=rows,operation=operation,lock_sensitivity=lock,interfaces=actions,
        limits=['Eixo/pontos sao hipoteses do estudo anterior;perfil real da piano e terminais nao montados.',
            'Forca axial do articulador vale somente na parada reta idealizada;nao aplicar ao mecanismo dobrado.',
            'Massas por volume acabado e densidade hipotetica;pesagem/camadas/metais podem mudar as demandas.',
            'Apoio fixo nao pode ser atribuido ao volume de reserva do encosto;precisa ligar ao corpo resistente.',
            'Comprimento da piano atende nominalmente,mas corte/extremidades,perfil e fixacao permanecem pendentes.',
            'Nao houve nova varredura de colisoes nem liberacao de90graus com produto real;sem prova de carga/impacto.'],
        hash_rule=HASH_RULE,sources_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in sources},
        generator_sha256=sha(Path(__file__)))
    (OUT/'Montagem_aberta.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,data in [('Reacoes_abertas.csv',rows),('Trava_distancia_angulo.csv',lock),('Interfaces_montagem.csv',actions)]:
        with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]),delimiter=';');writer.writeheader()
            for r in data:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
    draw(d)
    print(json.dumps([dict(lid=r['lid'],compression_N=r['compression_N'],hinge=r['hinge_resultant_N']) for r in rows if r['rho_kg_m3']==900]))


def draw(d):
    im=Image.new('RGB',(1500,860),'#f6f3ed');q=ImageDraw.Draw(im)
    def t(x,y,s,size=23,bold=False):q.text((x,y),s,fill='#263d35',font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size))
    t(42,25,'P20 | montagem aberta e interfaces pendentes',35,True)
    t(42,82,'Parada90° no eixo hipotético atual. Ferragem, terminais e apoio fixo ainda precisam de prova.',23)
    for i,r in enumerate(x for x in d['load_cases'] if x['rho_kg_m3']==900):
        x0=65+i*730;q.rounded_rectangle((x0,140,x0+680,540),radius=15,fill='white')
        t(x0+22,160,'Tampa maior971' if i==0 else 'Tampa menor825',29,True)
        t(x0+22,218,f"Madeira hipotética: {r['wood_envelope_mass_kg']:.3f} kg",24)
        t(x0+22,265,f"Articulador: {r['compression_N']:.2f} N em compressão",25,True)
        t(x0+22,315,f"Deslocamento lateral do apoio: {r['side_offset_from_CG_mm']:.1f} mm",23)
        t(x0+22,365,'Reação da piano: dois grupos equivalentes.',23)
        for j,force in enumerate(r['hinge_forces_on_lid_N']):
            t(x0+22,410+j*40,f"Extremo{j+1}: X{force[0]:+.2f} / Z{force[2]:+.2f} N",23)
    t(42,580,'Montar primeiro o apoio fixo e a piano em retalho de seção; medir o eixo real.',25,True)
    t(42,630,'Terminais móveis:22mm abaixo da tampa maior e30mm abaixo da menor no estudo.',24)
    t(42,678,'Distância291mm é hipótese de barras alinhadas; não confirma engate nem curso de liberação.',23)
    t(42,726,'Retirar almofadas antes de abrir. Pega, mãos, massas de ferragens e impacto não incluídos.',23)
    t(42,774,'As reações não são cargas admissíveis, forças por parafuso ou autorização de ensaio.',23,True)
    im.save(OUT/'Montagem_aberta.png')


if __name__=='__main__':main()
