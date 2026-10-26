"""Cortes locais, CSV, chapaL e caminho divisoria/base/soco; gera sintese."""
import csv,hashlib,json,math,os
from pathlib import Path
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from casca_linear import System
from casca_em_L import LPanel

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P03'

def check_L():
    s=System();p=LPanel(s,'L',[0,0,0],step=95);K=s.matrix();f=np.zeros(s.ndof);mass=p.own_weight(f)
    resultant=sum(f[p.ids[:,2]]);mx=sum(p.coords[:,1]*f[p.ids[:,2]]);my=-sum(p.coords[:,0]*f[p.ids[:,2]])
    cg=np.array([-my/resultant,mx/resultant]);expected=np.array([365.0829875518675,634.7925311203317])
    assert np.max(np.abs(cg-expected))<1e-9
    rigid=[]
    for e in np.eye(3):
        v=np.array([np.r_[np.cross(e,r),e] for r in p.coords]).flatten()
        rigid.append(float(abs(v@K@v)/max(np.linalg.norm(K)*np.linalg.norm(v)**2,1)))
    assert max(rigid)<1e-12
    # A malha usa um so ID em cada vertice compartilhado, inclusive no recorte.
    assert len(np.unique(p.coords,axis=0))==len(p.coords)
    return dict(area_mm2=p.area,center_xy_mm=cg.tolist(),mass_kg=mass,rigid_normalized_energy=rigid)

def main():
    d=json.loads((OUT/'Ligacao_P02_P03.json').read_text(encoding='utf-8'));rr=d['configurations']
    assert len(rr)==18 and all(len(r['cases'])==96 for r in rr)
    cad=ROOT/'02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd'
    assert hashlib.sha256(cad.read_bytes()).hexdigest()==d['source_sha256'] and d['source_unchanged']
    with (OUT/'Ligacao_C01_solicitacoes.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    assert len(rows)==sum(r['options']['c01_n']*96 for r in rr)
    for idx,r in enumerate(rr):
        assert max(abs(x) for x in r['equilibrium_max_residual_N_Nmm_Nmm'])<.1
        assert max(r['P02_cut_max_residual_N_Nmm'][:3])<.001 and max(r['P02_cut_max_residual_N_Nmm'][3:])<.1
        assert r['divider_vertical_cut_max_residual_N']<.001
        rs=[x for x in rows if int(x['configuration'])==idx]
        for ic,c in enumerate(r['cases']):
            cs=[x for x in rs if int(x['case'])==ic]
            assert len(cs)==r['options']['c01_n']
            assert abs(sum(float(x['Fy_N']) for x in cs)-c['C01_force_on_P02_N'][1])<1e-8
            assert abs(sum(float(x['Fz_N']) for x in cs)-c['C01_force_on_P02_N'][2])<1e-8
            assert abs(max(float(x['tension_N']) for x in cs)-c['max_C01_tension_N'])<1e-8
            assert abs(max(float(x['shear_N']) for x in cs)-c['max_C01_shear_N'])<1e-8
    summary=[]
    for idx,r in enumerate(rr):
        # Requisito principal: P03 com malas20kg;P02 vazio de conteudo,
        # mas inclui madeira,faixas,portas e todas as poses de estudo.
        primary=[c for c in r['cases'] if c['P02_content_kg']==0]
        summary.append(dict(configuration=idx,options=r['options'],
            primary_P03_down_mm=max(c['P03_base_down_mm'] for c in primary),
            primary_P02_down_mm=max(c['P02_base_down_mm'] for c in primary),
            primary_C01_tension_N=max(c['max_C01_tension_N'] for c in primary),
            primary_C01_shear_N=max(c['max_C01_shear_N'] for c in primary),
            primary_divider_foot_N=max(c['divider_foot_force_N'] for c in primary),
            primary_base_under_divider_mm=max(c['P01_base_below_divider_down_mm'] for c in primary),
            primary_base_under_divider_min_mm=min(c['P01_base_below_divider_down_mm'] for c in primary),
            primary_floor_peak_MPa=max(c['floor_peak_pressure_MPa'] for c in primary),
            primary_soco_center_force_N=max(c['floor_under_divider_N'] for c in primary),
            primary_linear_screen_count=sum(c['small_displacement_screen_ok'] for c in primary),
            combined_max_P03_down_mm=max(c['P03_base_down_mm'] for c in r['cases']),
            combined_max_P02_down_mm=max(c['P02_base_down_mm'] for c in r['cases']),
            all_linear_screen_count=sum(c['small_displacement_screen_ok'] for c in r['cases'])))
    # Caminho nominal por volumes simples; nao substitui medida/nivel.
    area=18*550;parts=[dict(name='Soco_frente_base',length_y_mm=18),dict(name='Soco_transversal_4_caixa',length_y_mm=514),dict(name='Soco_traseiro',length_y_mm=18)]
    assert sum(r['length_y_mm'] for r in parts)==550
    path=dict(divider_x_mm=[6381,6399],divider_y_mm=[3372,3922],divider_bottom_Z=80,
        base_Z_mm=[62,80],soco_Z_mm=[0,62],support_parts=parts,nominal_complete_contact_mm2=area,
        limitation='Contato nominal formado por tres pecas do soco;continuidade real e nivelamento ainda pendentes.')
    product=dict(status='Familia candidata,nao conjunto comprado/dimensionado',source='https://www.hafele.si/en/product/threaded-sleeve-with-m4-internal-thread-steel/P-00861539/',
        sleeve_internal_thread='M4',bore_reference_mm=5,
        variants=[dict(code='267.00.914',length_mm=25,stack_range_mm=[31,36]),dict(code='267.00.916',length_mm=30,stack_range_mm=[36,40])],
        two_panels_nominal_mm=36,conditional_stack_range_mm=[35.4,36.6],
        note='Luva e parafusos/cabecas correspondentes formam o conjunto. Medir espessuras;os intervalos se encontram em36,sem cobrir ambos com umSKU. Cabecas,parafusos,aperto e resistenciasMDF nao definidos.')
    report=dict(cases=18*96,csv_rows=len(rows),sha256=d['source_sha256'],L_validation=check_L(),summary=summary,divider_path=path,candidate_connector=product,
        mesh_primary_P03_relative_change_1_to1_5=abs(summary[16]['primary_P03_down_mm']/summary[13]['primary_P03_down_mm']-1),
        mesh_primary_P03_relative_change_1_5_to2_upper=abs(summary[17]['primary_P03_down_mm']/summary[16]['primary_P03_down_mm']-1),
        C01_candidate_points_world_mm=[[6740,y,z] for y in [3430,3646,3862] for z in [2180,2392]],
        status='Cortes,geometria e aritmetica conferidos;rigidezes/capacidades fisicas e fabricacao pendentes.')
    (OUT/'Verificacao_ligacao_P02_P03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    draw(summary)
    print(json.dumps(dict(cases=report['cases'],csv_rows=len(rows),mesh_change=report['mesh_primary_P03_relative_change_1_5_to2_upper'],status=report['status']),ensure_ascii=False))

def draw(summary):
    im=Image.new('RGB',(1500,1120),'#f4f1eb');q=ImageDraw.Draw(im)
    def text(x,y,t,size=23,b=False,c='#28382e'):
        q.text((x,y),t,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),size),fill=c)
    text(45,28,'P03 ↔ P02 | ligação e apoio da divisória',36,True)
    text(45,80,'Proposta de estudo • duas chapas separadas de 18 mm • sem alteração da R52',24)
    q.rounded_rectangle((35,132,880,690),18,fill='white');text(60,150,'1. Seis posições candidatas na face comum',28,True)
    x0,y0=90,250;w,h=612,272
    q.rectangle((x0,y0,x0+w,y0+h),fill='#cbb99f',outline='#28382e',width=3)
    for y in [120,336,552]:
        for z in [30,242]:
            x=x0+y;yy=y0+h-z;q.ellipse((x-8,yy-8,x+8,yy+8),fill='#396951')
    text(95,207,'Vista da face 612 × 272 mm',24)
    text(92,545,'Frente: 120 mm  |  Trás: 60 mm  |  Bordas: 30 mm',23)
    text(60,600,'Grupo inicial4 → candidato6 com maior afastamento.',23)
    text(60,638,'Posições ainda dependem de ferragens, cabeças e ensaio.',23)
    q.rounded_rectangle((905,132,1465,690),18,fill='#e4ebe4');text(930,150,'2. Caminho até o piso',28,True)
    q.rectangle((1140,230,1180,430),fill='#cbb99f',outline='#28382e',width=2)
    q.rectangle((1000,430,1330,468),fill='#cbb99f',outline='#28382e',width=2)
    q.rectangle((1140,468,1180,590),fill='#cbb99f',outline='#28382e',width=2)
    q.line((980,590,1360,590),fill='#28382e',width=5)
    for yy in [270,350,505,550]:q.polygon([(1155,yy),(1165,yy),(1165,yy+15),(1173,yy+15),(1160,yy+30),(1147,yy+15),(1155,yy+15)],fill='#396951')
    text(1210,285,'Divisória18',22);text(1210,386,'Z80',22);text(1210,475,'Z62',22);text(1210,550,'Soco62',22)
    text(930,625,'Contato nominal: 18 × 550 = 9.900 mm².',23)
    q.rounded_rectangle((35,715,1465,1080),18,fill='white')
    text(60,735,'3. Resultados condicionais: malas20kg em P03, P02 sem conteúdo',26,True)
    a,b=summary[1],summary[13]
    text(65,795,'Tração máxima por pontoC01',24);text(650,795,f"4 pontos: {a['primary_C01_tension_N']:.0f} N",24,True);text(1020,795,f"6 pontos: {b['primary_C01_tension_N']:.0f} N",24,True)
    text(65,840,'Deslizamento: força máxima',24);text(650,840,f"4 pontos: {a['primary_C01_shear_N']:.0f} N",24,True);text(1020,840,f"6 pontos: {b['primary_C01_shear_N']:.0f} N",24,True)
    text(65,900,f"Base sob a divisória com soco: até {a['primary_base_under_divider_mm']:.2f} mm no modelo de referência.",24)
    text(65,950,'São solicitações, sem capacidade homologada do conector ou do MDF.',24,True)
    text(65,995,'Apoio real/nivelamento, juntas e deformação da caixa superior continuam condicionados.',23)
    im.save(OUT/'Ligacao_P02_P03.png')

if __name__=='__main__':main()
