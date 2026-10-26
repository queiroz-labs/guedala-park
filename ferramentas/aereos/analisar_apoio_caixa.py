"""Apoio inferior nominal e corpo de prova fundo-laterais. Nao capacidade fisica.

Usa cargas existentes: nao cria novas varreduras de material/rigidez.
Reacoes do corpo de prova sao solucao de norma minima de equilibrio,nao previsao.
"""
from collections import defaultdict
from pathlib import Path
import csv,hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from detalhar_ligacoes import ROOT,OUT,W,H,profiles,joints

def read(p):return json.loads(p.read_text(encoding='utf-8'))
from fontes import sha,HASH_RULE
def skew(r):
    x,y,z=r
    return np.array([[0,-z,y],[z,0,-x],[-y,x,0.]])

def group_matrix(points,length):
    origin=np.mean(points,axis=0)
    A=np.concatenate([np.vstack([np.eye(3),skew((p-origin)/length)]) for p in points],axis=1)
    return A,origin

def main():
    release=read(ROOT/'ferramentas/site/current_release.json');cad=ROOT/release['cadPath']
    selected=read(OUT/'Selecao_ferragem.json')
    assert sha(cad)==release['cadSHA256']==selected['cad_sha256']
    with (OUT/'Solicitacoes_suporte_L.csv').open(encoding='utf-8-sig',newline='') as f:upper=list(csv.DictReader(f,delimiter=';'))
    with (OUT/'Requisitos_suporte_L.csv').open(encoding='utf-8-sig',newline='') as f:tests=list(csv.DictReader(f,delimiter=';'))
    pairs=defaultdict(list)
    for r in upper:pairs[(r['code'],r['variant'],r['source_case_id'],r['traction_share_left'])].append(r)
    areas=[]
    for code,variant in [('P09','current'),('P11','current'),('P15','current'),('P15','wood_study')]:
        p=profiles(code,variant);names=list(p)
        for side,name in enumerate(names[:2]):
            band=np.array([-18 if side==0 else W[code],0,60,0 if side==0 else W[code]+18,0,120.])
            b=p[name]
            assert all(b[i]<=band[i] and band[i+3]<=b[i+3] for i in [0,2])
            assert b[1]==band[1]==band[4]==0
            back=p[names[2]]
            assert back[1]==0 and back[2]<=60 and back[5]>=120
            areas.append(dict(code=code,variant=variant,side=side,piece=name,reference_rear_face_uz_mm=band.tolist(),
                width_mm=18,height_mm=60,nominal_area_mm2=1080,resultant_u_mm=-9 if side==0 else W[code]+9,
                reference_resultant_z_mm=90,added_volume_mm3=0,
                effective_contact_verified=False,other_back_contacts_present=True))
    lower=[];critical={};max_global_error=0.
    for key,pair in pairs.items():
        assert len(pair)==2
        code,variant,case,share=key;w,h=W[code],H[code]
        T=sum(float(r['T_N']) for r in pair);first=sum(float(r['u_mm'])*float(r['T_N']) for r in pair)
        a,b=-9.,w+9
        comp=[(b*T-first)/(b-a),(first-a*T)/(b-a)]
        assert min(comp)>-1e-8
        V=sum(float(r['V_N']) for r in pair)
        uCG=sum(float(r['u_mm'])*float(r['V_N']) for r in pair)/V
        wall_moment=T*(h-148);vCG=wall_moment/V
        # Certificado3D: peso total equivalente +2grupos superiores +2contatos.
        F=np.array([0.,0.,-V]);M=np.cross([uCG,vCG,0],F)
        for r in pair:
            force=np.array([0.,-float(r['T_N']),float(r['V_N'])]);point=[float(r['u_mm']),0,h-58]
            F+=force;M+=np.cross(point,force)
        for side,u in enumerate([a,b]):
            force=np.array([0.,comp[side],0.]);F+=force;M+=np.cross([u,0,90],force)
            row=dict(code=code,variant=variant,source_case_id=case,traction_share_left=float(share),
                payload_kg=float(pair[0]['payload_kg']),side=side,u_mm=u,z_mm=90,
                C_N=comp[side],nominal_area_mm2=1080,p_mean_nominal_MPa=comp[side]/1080,
                effective_area_verified=False,contact_centroid_verified=False)
            lower.append(row)
            target=20 if code=='P15' else 10
            if row['payload_kg']==target and ((code,variant) not in critical or row['C_N']>critical[(code,variant)]['C_N']):critical[(code,variant)]=row
        err=max(np.max(np.abs(F)),np.max(np.abs(M)));max_global_error=max(max_global_error,float(err));assert err<1e-7
    specimens=[]
    for code,variant in [('P09','current'),('P11','current'),('P15','current'),('P15','wood_study')]:
        p=profiles(code,variant);names=list(p);side=p[names[0]];back=p[names[2]]
        js=[j for j in joints(code,variant) if j['family'].startswith('Confirmat') and j['b']==names[2] and j['axis']=='u']
        z=sorted(set(j['z_mm'] for j in js))
        specimens.append(dict(code=code,variant=variant,side_quantity=2,back_quantity=1,
            side_height_depth_thickness_mm=[float(side[5]-side[2]),float(side[4]-side[1]),float(side[3]-side[0])],
            back_width_height_thickness_mm=[float(back[3]-back[0]),float(back[5]-back[2]),float(back[4]-back[1])],
            side_bottom_z_mm=float(side[2]),back_bottom_z_mm=float(back[2]),
            three_joint_z_from_side_bottom_mm=[float(v-side[2]) for v in z],
            three_joint_z_from_back_bottom_mm=[float(v-back[2]) for v in z],
            nominal_axis_from_rear_mm=9,connector_candidate='6Confirmat7x50,3porlado;sem piloto/cabeca/torque definidos',
            excluded='Sem base/topo/prateleira/divisor,semBigfer e sem suspensao/parede real;laterais presas ao dispositivo de ensaio. P15estudo nao testa composicao18+18.'))
    fixtures=[];fixture_csv=[];fixture_max=0.
    for idx,r in enumerate(tests):
        code,variant=r['code'],r['variant'];p=profiles(code,variant);back=list(p)[2]
        jr=[j for j in joints(code,variant) if j['family'].startswith('Confirmat') and j['b']==back and j['axis']=='u']
        assert len(jr)==6
        points=np.array([[j['u_mm'],j['v_mm'],j['z_mm']] for j in jr]);L=max(W[code],H[code])
        A,origin=group_matrix(points,L);rank=int(np.linalg.matrix_rank(A));assert rank==6
        force=np.array([0.,-float(r['T_N']),float(r['V_N'])]);at=np.array([float(r['u_mm']),18,float(r['upper_z_mm'])])
        moment=np.cross(at-origin,force);rhs=-np.r_[force,moment/L]
        solution=np.linalg.lstsq(A,rhs,rcond=None)[0];reaction=solution.reshape(-1,3)
        err=float(np.max(np.abs(A@solution-rhs)));fixture_max=max(fixture_max,err);assert err<1e-9
        local=[]
        for side in [0,1]:
            col=points[:3] if side==0 else points[3:]
            B,base=group_matrix(col,L)
            test=np.r_[force,np.cross(at-base,force)/L]
            residual=test-B@np.linalg.lstsq(B,test,rcond=None)[0]
            assert np.linalg.matrix_rank(B)==5
            local.append(dict(side=side,rank=5,missing_rotation='z',
                unbalanced_Mz_for_transfer_to_this_column_Nm=float(np.cross(at-base,force)[2]/1000),
                residual_scaled_norm=float(np.linalg.norm(residual)),sole_point_column_sufficient=False))
        rows=[]
        for j,f in zip(jr,reaction):
            row=dict(fixture_id=idx+1,code=code,variant=variant,source_case_id=r['source_case_id'],
                source_upper_side=int(r['side']),controls=r['controls'],joint_id=j['id'],u_mm=j['u_mm'],v_mm=j['v_mm'],z_mm=j['z_mm'],
                N_axis_u_N=float(f[0]),Q_v_N=float(f[1]),Q_z_N=float(f[2]),R_min_norm_solution_N=float(np.linalg.norm(f)),
                actual_joint_force_predicted=False)
            rows.append(row);fixture_csv.append(row)
        fixtures.append(dict(id=idx+1,code=code,variant=variant,source_case_id=r['source_case_id'],controls=r['controls'],
            upper_side=int(r['side']),load_application_uvz_mm=at.tolist(),applied_F_uvz_N=force.tolist(),
            applied_M_at_group_center_Nmm=moment.tolist(),group_center_uvz_mm=origin.tolist(),length_scale_mm=L,
            matrix_rank=rank,one_column_checks=local,reactions_min_norm_only=rows,
            necessary_lower_bound_on_any_max_joint_resultant_N=float(np.linalg.norm(solution)/np.sqrt(6)),
            scaled_equilibrium_residual=err,
            physical_interpretation='Corpo de prova:forca superior inteira introduzida no fundo;seis ligacoes as laterais no dispositivo de ensaio. Nao e previsao de reparticao no gabinete com demais juntas/contatos.'))
    data=dict(scope='Apoio geometrico nominal e requisitos de transferencia fundo-laterais,sem capacidade liberada.',
        cad_sha256=sha(cad),cad_opened=False,cad_changed=False,
        reference_lower_areas=areas,lower_group_pairs=len(pairs),lower_reaction_rows=len(lower),
        reference_content_critical_lower=list(critical.values()),global_equilibrium_max_error_N_Nmm=max_global_error,
        specimens=specimens,fixtures=fixtures,fixture_configuration_count=4,fixture_load_case_count=len(fixtures),fixture_joint_rows=len(fixture_csv),fixture_equilibrium_max_scaled_error=fixture_max,
        fixture_case_coverage='Oito casos globais controladoresV/T/R da pre-selecao. Servem a caracterizacao desta rota;nao sao envelope de todas as juntas em todos os casos ou protocolo de homologacao.',
        contact_rules=[
            'Faixas18x60,Z60..120 sao zonas de referencia na traseira das laterais existentes,nao calcos/pads ou furos novos. CentroZ90 e hipotese,nao contato medido.',
            'Fundo e laterais compartilham plano traseirov0;nao ha como garantir duas zonas ativas apenas desenhando-as. Contatos fora da faixa podem alterar o braco e a tracao.',
            'Sem aumentar afastamento do movel ou reduzir armazenamento. Nao adicionar calco isolado que incline a caixa;qualquer compensacao exige estudo de prumo/posicoes/fixacao.',
            'PressaoC/1080 e media sobre area nominal,nao pico nem resistencia admissivel. Se areaefetiva=A, recalcularC/A;sem A medida nao comparar com limite do material.',
            'Reacoes inferiores repartidas pela soma e momento de guinada;nao copiar a tracao de cada suporte para a lateral do mesmo lado.',
            'Sem credito a atrito ou fixacao a parede real. Apoio direto inferior na lateral evita atribuir essa compressao ao grupo de parafusos do fundo.'],
        joint_rules=[
            'Preservar6Confirmat candidatos fundo-laterais,3por lado,sem duplicar Minifix/cavilhas ou permitir pilotos/CNC.',
            'Uma coluna de3ligacoes pontuais colineares tem posto5;nao reage momentoMz em torno da propria coluna. Precisa de caminho pelo fundo e outra lateral ou rigidez de junta/contato demonstrada.',
            'Seis pontos em duas colunas tem posto6 para equilibrio;isso nao comprova resistencia/flexibilidade do fundo ou das juntas.',
            'Solucao de norma minima e certificado matematico de equilibrio e limite inferior L2 para a maior reacao,nao forca de projeto por Confirmat. Autoequilibrios/rigidezes reais podem elevar muito os esforcos.',
            'Corpo de prova testa uma rota com toda a forca superior entrando no fundo. Parafusos lateraisBigfer,demais juntas,atrito e apoio inferior estao excluidos;somar resultados destes modelos daria dupla contagem.',
            'Para dimensionar o gabinete,medir/modelar rigidez do fundo,juntas e partilha nos parafusos da ferragem em um sistema acoplado;sem atribuir rigidez por conveniencia.'],
        next_checks=[
            'Oficina:montar corpo de prova com fundo18 inteiro,laterais18 e seis conectores/furos/cabecas reais. Instrumentar movimento relativo em cada borda e deformacao do fundo.',
            'Definir introducao da carga no fundo sem criar engaste/apoio extra ou reforcar artificialmente sua largura;desenhar garra/distribuidor e separar deformacao/falha local da aplicacao e da junta.',
            'Aplicar cada vetor do corpo de prova no ponto indicado sem combinar maximos de casos diferentes;avaliar ambos os lados. Responsavel define fatores,duracao,ciclos e limites antes do ensaio.',
            'No local:mapear contato traseiro com caixa sustentada,confirmar prumo,areaefetiva,centro de pressao e parede/instalacoes antes de ancoragem. Nao usar contato presumido para fechar carga.',
            'Conferir acesso/manutencao e retencao inferior com produto/fixadores reais;prototipo integrado da caixa continua necessario.'],
        input_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [OUT/'Selecao_ferragem.json',OUT/'Solicitacoes_suporte_L.csv',OUT/'Requisitos_suporte_L.csv',ROOT/'ferramentas/aereos/detalhar_ligacoes.py']},
        script_sha256=sha(Path(__file__)),hash_rule=HASH_RULE,hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')),physical_tests=0)
    (OUT/'Apoio_e_caixa.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,rows in [('Reacoes_apoio_inferior.csv',lower),('Corpos_prova_fundo_laterais.csv',fixture_csv)]:
        with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');wr.writeheader();wr.writerows(rows)
    notes=['ROTEIRO NOMINAL — APOIO INFERIOR E JUNTA FUNDO/LATERAIS',
        '25/10/2026. Preparacao tecnica,nao instrucao de fabricacao ou ensaio liberados.',
        'Objetivo:medir acomodacao das juntas e deformacao do fundo inteiro sem depender daBigfer.',
        'Substrato/BP/espessura efetivos e parafusos devem representar as pecas do projeto.',
        'A distancia9mm da traseira localiza o eixo;nao e diametro de furo. Piloto,escareamento,cabeca e torque dependem do produto real.',
        '', 'GEOMETRIA DO CORPO DE PROVA (mm)']
    for s in specimens:
        notes += [f"{s['code']} {s['variant']}:2laterais altura/profundidade/espessura={s['side_height_depth_thickness_mm']};1fundo largura/altura/espessura={s['back_width_height_thickness_mm']}.",
            f"3eixos por lado desde base da lateral={s['three_joint_z_from_side_bottom_mm']};desde base do fundo={s['three_joint_z_from_back_bottom_mm']};9da traseira."]
    notes += ['', 'DATUM E VETORES APLICADOS',
        'u=0 na esquerda interna,v=0 traseira externa para frente,z=0 base externa ORIGINAL.',
        'P15study desce18:a base fisica da lateral/fundo eZ-18;nao usarZoriginal como cota desde nova borda.',
        'ForcaF=(0,-T,+V) aplicada no fundo emv18;laterais fixas no dispositivo. +z=cima,-v=para parede.',
        'Cada linha e um caso separado do grupo superior,nao oito cargas simultaneas. Avaliar ambos os lados.']
    for f in fixtures:
        s=next(s for s in specimens if (s['code'],s['variant'])==(f['code'],f['variant']))
        force=f['applied_F_uvz_N'];point=f['load_application_uvz_mm']
        notes.append(f"Caso{f['id']} {f['code']} {f['variant']},fonte{f['source_case_id']},controle{f['controls']}:F={np.round(force,3).tolist()}N;u={point[0]:g},v=18,Zoriginal={point[2]:g},altura desde base do fundo={point[2]-s['back_bottom_z_mm']:g}.")
    notes += ['', 'O QUE MEDIR E O QUE NAO CONCLUIR',
        'Medir movimento relativo em cada grupo fundo/lateral e deformacao do fundo;descontar movimento/flexibilidade do dispositivo.',
        'Definir garra/distribuidor para introduzir a resultante no fundo sem criar engaste/apoio extra ou reforcar sua largura. Registrar deformacao/falha local do aplicador separadamente.',
        'Registrar fissura,abertura,escorregamento,impressao local,ciclos,carga mantida e recuperacao.',
        'Responsavel pelo ensaio define fatores,duracao,ciclos e limites de aceitacao antes de testar.Sem criterios nao ha aprovacao.',
        'Reacoes de norma minima doCSV sao certificado matematico,nao forcas admissiveis ou reais por parafuso.',
        'Nao extrapolar este corpo de prova para prateleiraP11,composicaoP15 ou capacidade do gabinete/suspensao.',
        '', 'APOIO INFERIOR A CONFERIR NO CONJUNTO E NO LOCAL',
        'Zonas18x60 na aresta traseira das laterais,Z60..120,sem calco novo. Fundo coplanar tambem pode tocar.',
        'Confirmar prumo,contato efetivo e centro de pressao.Nao assumir1080mm2 ativos nem adicionar calco isolado.',
        'Ancoragem depende da parede real;nao usar pessoa como carga de ensaio. R52 preservada.', '']
    (OUT/'Roteiro_apoio_caixa.txt').write_text('\n'.join(notes),encoding='utf-8')
    draw(data)
    print(json.dumps(dict(lower_rows=len(lower),nominal_area_per_side_mm2=1080,fixtures=len(fixtures),fixture_joint_rows=len(fixture_csv),
        single_column_rank=5,two_columns_rank=6,max_global_error=max_global_error,max_fixture_error=fixture_max,CAD_preserved=True)))

def draw(data):
    im=Image.new('RGB',(1480,1100),'#f4f1eb');p=ImageDraw.Draw(im)
    def t(x,y,s,n=23,b=False,c='#293a31'):
        p.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n),fill=c)
    t(40,25,'Apoio inferior e caminho fundo–laterais',36,True)
    t(40,80,'Estudo nominal • sem novos calços • espaço interno e R52 preservados',24)
    for i,code in enumerate(W):
        x=40+480*i;w,h=W[code],H[code];sx=390/(w+36);sy=300/h
        p.rounded_rectangle((x,135,x+450,680),18,fill='white');t(x+20,155,code,29,True)
        l=x+30;r=x+420;top=225;bottom=525
        p.rectangle((l,top,r,bottom),fill='#eee8dd',outline='#81725d',width=3)
        p.rectangle((l+18*sx,top+18*sy,r-18*sx,bottom-18*sy),fill='#faf8f4')
        for side in [0,1]:
            u=40.5 if side==0 else w-40.5;px=l+(u+18)*sx;py=bottom-(h-58)*sy
            p.ellipse((px-7,py-7,px+7,py+7),fill='#356b51')
            edge=l if side==0 else r-18*sx
            p.rectangle((edge,bottom-120*sy,edge+18*sx,bottom-60*sy),fill='#bd603f')
        t(x+20,552,'Faixas existentes: 18 × 60 mm',24,True)
        t(x+20,590,'Z = 60…120 | centro hipotético 90',22)
        t(x+20,631,'Fundo também pode tocar a parede',21,c='#bd603f')
    p.rounded_rectangle((40,710,1440,1065),18,fill='white')
    t(65,735,'O que o estudo resolveu',29,True)
    t(65,790,'A pressão nominal usa 1.080 mm² por lado; área real e centro de contato precisam de verificação.',23)
    t(65,837,'Três parafusos numa única coluna não fecham sozinhos o momento de torção dessa rota.',23)
    t(65,884,'Oito casos de ensaio usam seis ligações e forças/posições identificadas em quatro configurações.',23)
    t(65,931,'Equilíbrio matemático não demonstra resistência das juntas, do fundo ou da suspensão.',23,c='#bd603f')
    t(65,1000,'Sem fabricação, ensaio físico ou ancoragem liberados.',24,True)
    im.save(OUT/'Apoio_e_caixa.png')

if __name__=='__main__':main()
