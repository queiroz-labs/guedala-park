"""Pre-selecao compacta: envelope de catalogo, implantacao hipotetica e demandas.

Nao demonstra montagem autorizada, resistencia da ferragem/juntas ou ancoragem.
"""
from collections import defaultdict
from pathlib import Path
import csv,hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from detalhar_ligacoes import ROOT,OUT,W,H,D,profiles

PDFDIR=ROOT/'09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    original=json.loads((OUT/'Detalhamento_P09_P11_P15.json').read_text(encoding='utf-8'))
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    assert sha(ROOT/release['cadPath'])==original['cad_sha256']==release['cadSHA256']
    # CatalogoBigfer p235: 49.5 e37.8 sao bracos;16 e a largura da tira.
    # A orientacao nos dois planos verticais e uma proposta nossa, nao manual.
    dimensions=dict(arm_keyhole_mm=49.5,arm_side_mm=37.8,strip_width_mm=16,steel_thickness_mm=1.5,
        keyhole_entry_center_from_outer_corner_mm=32,slot_end_center_from_outer_corner_mm=49.5-9,
        small_rear_hole_from_outer_corner_mm=32-22.5,slot_width_mm=5,entry_diameter_mm=10,
        side_small_hole_pitch_mm=12)
    one_box=49.5*37.8*16/1e6
    mounts=[]
    for code in W:
        w,h=W[code],H[code];z=h-58
        for side in [0,1]:
            u=40.5 if side==0 else w-40.5
            box=np.array([0 if side==0 else w-49.5,18,z-8,49.5 if side==0 else w,55.8,z+8])
            overlaps=[]
            for name,b in profiles(code).items():
                overlap=np.minimum(box[3:],b[3:])-np.maximum(box[:3],b[:3])
                if np.all(overlap>1e-7):overlaps.append(name)
            assert not overlaps,(code,side,overlaps)
            assert h-18-box[5]==32 and z-(h-90)==32
            tool=np.array([u-10,19.5,z-10,u+10,D,z+10])
            assert all(not np.all(np.minimum(tool[3:],b[3:])-np.maximum(tool[:3],b[:3])>1e-7) for b in profiles(code).values())
            mounts.append(dict(code=code,side=side,envelope_uvz_mm=box.tolist(),
                hypothetical_upper_resultant_u_mm=u,upper_z_mm=z,lower_z_mm=90,couple_h_mm=z-90,
                old_rear_Confirmat_vertical_separation_mm=32,old_top_Minifix_vertical_separation_mm=49,
                wood_clear=True,actual_product_clearance_verified=False,
                side_hole_reference_v_mm=[30.8,42.8],rear_small_hole_reference_u_mm=9.5 if side==0 else w-9.5,
                note='Cotas referencia de catalogo;nao pilotos/CNC. Furo traseiro perto da borda e passos exigem validacaoMDF.'))
    with (OUT/'Solicitacoes_fixacao_direta.csv').open(encoding='utf-8-sig',newline='') as f:old=list(csv.DictReader(f,delimiter=';'))
    groups=defaultdict(list)
    for r in old:groups[(r['code'],r['variant'],r['source_case_id'],r['traction_share_left'])].append(r)
    rows=[];critical={};worst=0.
    for key,pair in groups.items():
        assert len(pair)==2
        code,variant,case,share=key;w,h=W[code],H[code];a,b=40.5,w-40.5;arm=h-148
        vertical=sum(float(r['V_N']) for r in pair)
        first=sum(float(r['V_N'])*float(r['u_mm']) for r in pair)
        moment=sum(float(r['T_N'])*float(r['couple_h_mm']) for r in pair)
        V=[(b*vertical-first)/(b-a),(first-a*vertical)/(b-a)]
        T=[float(share)*moment/arm,(1-float(share))*moment/arm]
        errors=[abs(sum(V)-vertical),abs(a*V[0]+b*V[1]-first),abs(sum(T)*arm-moment)]
        worst=max(worst,*errors);assert max(errors)<1e-7
        for side in [0,1]:
            src=pair[0]
            row=dict(code=code,variant=variant,source_case_id=case,rho=float(src['rho']),
                payload_kg=float(src['payload_kg']),payload_case=src['payload_case'],doors_deg=src['doors_deg'],
                traction_share_left=float(share),side=side,u_mm=[a,b][side],upper_z_mm=h-58,
                lower_z_mm=90,couple_h_mm=arm,V_N=V[side],T_N=T[side],R_N=math.hypot(V[side],T[side]),
                reference_corner_Mu_Nm=-18*V[side]/1000,
                reference_corner_Mv_Nm=(-1 if side==0 else 1)*40.5*V[side]/1000,
                reference_corner_Mz_Nm=(-1 if side==0 else 1)*40.5*T[side]/1000,
                equal_vertical_shear_three_fixings_moment_residual_Nm=abs(V[side]*(40.5-9.5/3))/1000,
                product_capacity_verified=False,mounting_approved_by_manufacturer=False)
            rows.append(row);k=(code,variant,row['payload_kg'])
            if k not in critical or row['R_N']>critical[k]['R_N']:critical[k]=row
    assert len(rows)==4176 and len(mounts)==6
    sources={
        'Bigfer_suportes_aereos.pdf':'https://www.bigfer.com.br/wp-content/uploads/sites/6/2023/03/Catalogo-Produto-Ferragens-em-geral-pg.-235.pdf',
        'Hettich_SAH130_montagem.pdf':'https://web2.hettich.com/hbh/addon/montage/MTA_74387_SAH_130_Sprachneutral.pdf',
        'Hettich_SAH116_montagem.pdf':'https://web2.hettich.com/hbh/addon/montage/MTA_19476_SAH_116.pdf'}
    data=dict(status='Pre-selecao de desenvolvimento;nao produto fechado para compra/montagem',
        preference_source='Elias,25/10/2026: de preferencia sem perder espaco interno',
        preferred_candidate=dict(manufacturer='Bigfer',code='04.02.058',sku='0402058411',
            name='Suporte Aereo L para Armarios',source='https://www.bigfer.com.br/suporte-aereo-l-armarios/',
            dimensions=dimensions,product_load_published=False,mounting_with_back18_confirmed=False),
        occupancy=dict(per_hardware_bounding_box_liters=one_box,pair_bounding_boxes_liters=2*one_box,
            pair_bounding_boxes_milliliters=2*one_box*1000,storage_depth_old_mm=312,storage_depth_proposed_mm=312,
            back_relocation_mm=0,wall_standoff_change_mm=0,
            limits='Somente envelope metalico sem capa/cabeca/acesso. Montagem direta sobre face interna do fundo18 e hipotese,nao encaixe comercial demonstrado.'),
        mounts=mounts,cases=696,vectors=len(rows),group_pairs=len(groups),max_equilibrium_error=worst,
        critical_groups=list(critical.values()),
        mounting_assessment=dict(entry_u_from_corner_mm=32,working_u_from_corner_mm=40.5,
            travel_mm=8.5,left_cabinet_translation_mm=-8.5,right_cabinet_translation_mm=8.5,
            common_translation_for_two_mirrored_keyholes_exists=False,
            proposed_method='Gabinete sustentado e nivelado por apoio temporario;fixacoes inseridas/apertadas por dentro na posicao de trabalho. Nao pendurar os dois rasgos espelhados por uma translacao unica.',
            method_confirmed_by_manufacturer=False,
            shank_head_washer='Validar passagem no rasgo5,assento/retencao da cabeca e montagem no fundo18.Sem diametro,parafuso ou bucha selecionados.',
            removal='Suportar gabinete e retirar fixadores pela frente;nao presumir retirada conjunta pelos rasgos.',
            lower_support='Compressao inferiorZ90 e partilha continuam hipoteticas;sem pad/retencao inferior dimensionados.'),
        source_reading_correction='Entradau32 nao e assento do rasgo:u40.5=49.5-9. Pequeno furo:u9.5=32-22.5=1.5+8;8 e medido apos a aba,nao da borda externa do fundo.',
        local_demand_limits='Momentos r x F sao reducao da mesma forca da parede ao canto(u0/W,v18,zH-58),nao momentos extras somados ao equilibrio global nem solicitacoes isoladas do parafuso. Contatos/parafusosMDF precisam realizar essa resultante;V/3 arbitrario nao equilibra o momento.',
        qualification_requirements=[
            dict(item='Metodo',requirement='Confirmar orientacao de dois planos verticais,passagem pelo fundo18 e montagem com gabinete sustentado,sem encaixe simultaneo espelhado.'),
            dict(item='FixadoresMDF',requirement='Definir parafusos,pilotos,profundidade e torque por chapa/substrato reais. Diametros5 na ferragem nao sao pilotos5 no MDF;validar passo12 e borda9.5.'),
            dict(item='Cabeca e rasgo',requirement='Desenho do assento/cabeca/arruela no rasgo5 e entrada10,largura16 da tira e retencao contra abertura/deslocamento;sem recomendar diametro de ancoragem.'),
            dict(item='Contatos e momentos',requirement='Demonstrar reparticao com apoio no fundo18 e na lateral,flexao/esmagamento,ligacoes e momentos locais r x F. Nao V/3 ou V/2 sem rigidez/caminho.'),
            dict(item='Ensaio de conjunto',requirement='Montagem representativa com chapaBP18 real e fixadores escolhidos,sem credito a atrito nao controlado. Aplicar V/T simultaneos nos casos identificados;fabricante/RT define coeficientes,duracao,ciclos e limites de deslocamento/creep/ruptura. Sem criterio de aceitacao nao ha aprovacao.'),
            dict(item='Inferior e retirada',requirement='Detalhar compressao inferior e retencao,apoio temporario e acesso para apertar/retirar;envelope nao inclui capas,cabecas ou ferramenta real.'),
            dict(item='Parede',requirement='So apos identificar substrato,revestimento e instalacoes definir tipo/profundidade da ancoragem. Nao atribuir a ferragem capacidade da parede.')],
        comparison=[
            dict(product='Bigfer04.02.058',conclusion='Preferida para qualificar:compacta,aco1.5;sem carga/metodo comprovados para esta montagem'),
            dict(product='Bigfer04.02.007/008',conclusion='Reserva:aco1.9,42x58x20,pinos/parafusos e capacidade nao demonstrados;volumepar0.09744L'),
            dict(product='HettichSAH130/116',conclusion='Nao substituicao direta:manual mostra fundo3-5/max5 e recorte. Medida16 ate face frontal do fundo nao e reserva livre16 atras dele'),
            dict(product='FGVTNHB65;HettichSAH215/216',conclusion='Montagem atras do fundo;reserva inexistente na caixa atual,perda total se fundo deslocado;nao prioritarios'),
            dict(product='Camar807VP',conclusion='Alternativa de consulta,nao escolhida:desenho consultadoindicaBP16,casos de carga807IN nao se transferem paraVP;implantacao comfundo18 e oferta local nao demonstradas')],
        cad_sha256=original['cad_sha256'],cad_opened=False,cad_changed=False,
        source_pdfs=[dict(path=str((PDFDIR/n).relative_to(ROOT)),url=url,sha256=sha(PDFDIR/n)) for n,url in sources.items()],
        source_input_sha256={str(p.relative_to(ROOT)):sha(p) for p in [OUT/'Detalhamento_P09_P11_P15.json',OUT/'Solicitacoes_fixacao_direta.csv']},
        script_sha256=sha(Path(__file__)),
        limits=['Corpo emL idealizado,sem furos/raios/capa e tolerancias reais.',
            'u40.5 ezH-58 correspondem a implantacao proposta;u32 era entrada do rasgo e foi corrigido. Nao transplantar numeros antigosu72/u32.',
            '18mm entre chapa metalica interna e parede sao vencidos pela ancoragem proposta;ha excentricidade local. Fabricante deve confirmar,sem espaçador ou parafuso escolhido.',
            'Zonas antigas36x36x8 nao contem este produto. Novos envelopes49.5x37.8x16 so foram conferidos contra madeira.',
            'Validar passo12 e distancia de borda9.5 no MDF,pressao/esmagamento,flexao da chapa,parafusos,retencao e acessos de montagem.',
            'Dois suportes superiores sao numero da hipotese,nao quantidade suficiente comprovada;apoios/retencao inferiores ainda devem ser detalhados.',
            'Sem ensaio/material real,majoracao/impacto ou capacidade de uso/ancoragem demonstrada.'])
    (OUT/'Selecao_ferragem.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'Solicitacoes_suporte_L.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    qualification=[]
    for code,variant in [('P09','current'),('P11','current'),('P15','current'),('P15','wood_study')]:
        subset=[r for r in rows if r['code']==code and r['variant']==variant and r['payload_kg']==(20 if code=='P15' else 10)]
        chosen={}
        for quantity in ['R_N','V_N','T_N']:
            r=max(subset,key=lambda x:(x[quantity],x['R_N']))
            key=(r['source_case_id'],r['traction_share_left'],r['side'])
            if key not in chosen:chosen[key]=dict(r,controls=[])
            chosen[key]['controls'].append(quantity)
        qualification.extend(dict(r,controls='|'.join(r['controls'])) for r in chosen.values())
    with (OUT/'Requisitos_suporte_L.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])+['controls'],delimiter=';');writer.writeheader();writer.writerows(qualification)
    data['qualification_case_count']=len(qualification)
    data['qualification_cases']=qualification
    (OUT/'Selecao_ferragem.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    draw(data)
    print(json.dumps(dict(candidate='Bigfer04.02.058',pair_envelope_ml=2*one_box*1000,wood_clear_envelopes=len(mounts),
        vectors=len(rows),max_equilibrium_error=worst,manufacturer_mounting_confirmed=False,cad_preserved=True)))

def draw(data):
    im=Image.new('RGB',(1450,1020),'#f4f1eb');p=ImageDraw.Draw(im)
    def t(x,y,s,n=24,b=False,c='#293a31'):
        p.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n),fill=c)
    t(42,28,'Suspensão compacta | candidata Bigfer 04.02.058',35,True)
    t(42,80,'Proposta para qualificação • não é montagem homologada ou furação executiva',23)
    p.rounded_rectangle((40,130,820,700),18,fill='white')
    t(62,150,'Vista de cima de um canto | esquema sem escala',26,True)
    p.rectangle((110,265,735,300),fill='#b7a68a');p.rectangle((110,300,148,635),fill='#b7a68a')
    t(285,218,'Fundo MDF 18 mantido na posição',23)
    t(72,655,'A prateleira mantém 312 mm de profundidade útil',24)
    p.line((95,250,735,250),fill='#888888',width=4);t(585,190,'Parede',22)
    p.rectangle((148,300,420,311),fill='#356b51');p.rectangle((148,300,160,510),fill='#356b51')
    t(450,328,'49,5 mm no fundo',23,c='#356b51')
    t(185,535,'37,8 mm junto à lateral',23,c='#356b51')
    p.line((371,245,371,330),fill='#bd603f',width=8)
    t(365,400,'Passagem até a parede:',22,c='#bd603f')
    t(365,435,'18 mm de fundo no caminho.',22,c='#bd603f')
    t(365,470,'Fixação e método a confirmar.',22,c='#bd603f')
    p.rounded_rectangle((845,130,1410,700),18,fill='white')
    t(870,155,'Ocupação local estimada',28,True)
    t(870,212,'2 envelopes de 49,5 × 37,8 × 16 mm',24)
    t(870,265,'≈ 60 mL por armário',34,True,c='#356b51')
    t(870,325,'Sem recuar o fundo inteiro.',25)
    t(870,372,'Não inclui capas, cabeças e acesso.',22)
    t(870,438,'Aço de 1,5 mm publicado.',24)
    t(870,485,'Capacidade não publicada na fonte.',23,c='#bd603f')
    t(870,532,'Fundo 18: montagem não confirmada.',23,c='#bd603f')
    t(870,604,'Preferência para desenvolvimento;',23,True)
    t(870,637,'compra e instalação condicionadas.',23)
    p.rounded_rectangle((40,730,1410,980),18,fill='white')
    t(65,755,'Montagem a qualificar | rasgos espelhados',28,True)
    t(65,808,'Entrada a 32 mm; assento a 40,5 mm. Cada lado pede deslizamento de 8,5 mm em sentido oposto.',23)
    t(65,853,'Proposta: gabinete sustentado, fixação e aperto por dentro. Método ainda depende do fabricante.',23)
    t(65,903,'Os esforços incluem excentricidade local; não dividir a carga igualmente pelos três furos no MDF.',23)
    im.save(OUT/'Selecao_ferragem.png')

if __name__=='__main__':main()
