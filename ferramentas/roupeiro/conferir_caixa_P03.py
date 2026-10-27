"""Audita saidas, registra encontros/impedimento e desenha sintese sem abrir CAD."""
import csv, hashlib, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/P03'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    d=read(OUT/'Caixa_20kg.json');configs=d['configurations']
    assert len(configs)==29 and all(len(r['cases'])==16 for r in configs)
    assert d['source_unchanged']
    cad=ROOT/'02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd'
    assert sha(cad)==d['source_sha256']
    force_res=[];moment_res=[];count=0;invalid=0
    for r in configs:
        masses=r['mass_hypotheses']
        total=sum(masses['panel_mass_kg'].values())+masses['door_mass_kg']+masses['fixed_accessory_reserve_kg']+masses['P01_front_mass_kg']+20
        for c in r['cases']:
            count+=1;invalid+=not c['small_displacement_screen_ok']
            assert math.isfinite(c['base_max_down_mm'])
            assert c['contact_min_active_reaction_N']>=-1e-6
            assert c['max_inactive_penetration_mm']<1e-7
            equilibrium=c['equilibrium_residual_N_Nmm_Nmm']
            force_res.append(abs(equilibrium[0]));moment_res+=list(map(abs,equilibrium[1:]))
            assert abs(sum(v['vertical_reaction_N'] for v in c['root_reactions'].values())-total*9.80665)<1e-3
        for j in r['joint_envelopes']:
            assert j['max_resultant_N']>=0 and j['max_relative_translation_mm']>=0
    assert max(force_res)<.001 and max(moment_res)<.1
    with (OUT/'Caixa_20kg_juntas.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    assert len(rows)==4*16*32
    for idx in [1,21,22,24]:
        for j in configs[idx]['joint_envelopes']:
            rr=[r for r in rows if int(r['configuration'])==idx and r['joint']==j['name']]
            assert len(rr)==16
            assert abs(max(float(r['resultant_N']) for r in rr)-j['max_resultant_N'])<1e-9
            for r in rr:
                assert abs(np.linalg.norm([float(r[k]) for k in ['Fx_N','Fy_N','Fz_N']])-float(r['resultant_N']))<1e-9
    def peak(i):return max(c['base_max_down_mm'] for c in configs[i]['cases'])
    mesh_change=abs(peak(25)/peak(21)-1)
    penalty_change=abs(peak(26)/peak(21)-1)
    assert mesh_change<.01 and penalty_change<.01
    # Guia da folha traseira fechada: root(5390,3290,0), driver(985,44,90),
    # local guia(30,-5,1997), retencao(30,18,1987). Reservas hipoteticas.
    rail=[5408,3354,2034,7372,3372,2114]
    reserves={'guia_flex_traseira':[6405,3329,2087,6490,3357,2102],
              'retencao_traseira':[6405,3352,2077,6460,3365,2089]}
    overlap={}
    for name,b in reserves.items():
        dims=[max(0,min(rail[a+3],b[a+3])-max(rail[a],b[a])) for a in range(3)]
        assert min(dims)>0
        overlap[name]=dict(bbox_mm=b,overlap_xyz_mm=dims,overlap_mm3=math.prod(dims))
    summary=[]
    for idx,label in [(0,'A18, encontro de aresta'),(1,'A18, base/topo prolongados18'),(2,'A18, mais apoio traseiro'),
                      (4,'A18, longarina80 equivalente INCOMPATIVEL'),(21,'Base25, caixa fechada'),
                      (22,'Base25, mais apoio traseiro'),(24,'Base25+traseiro, junta com rigidez rotacional suposta')]:
        r=configs[idx];m=r['mass_hypotheses'];c=max(r['cases'],key=lambda c:c['base_max_down_mm'])
        summary.append(dict(configuration=idx,label=label,max_base_down_mm=peak(idx),
            P03_plus_content_mass_kg=sum(m['panel_mass_kg'].values())+m['door_mass_kg']+m['fixed_accessory_reserve_kg']+20,
            max_joint_N=max(j['max_resultant_N'] for j in r['joint_envelopes']),
            max_seam_moment_Nm=max(j['max_absolute_seam_moment_Nm'] for j in r['joint_envelopes']),
            critical_base_case=[c['pose'],c['packing']],base_location_relative_mm=c['base_max_down_location_relative_mm']))
    report=dict(cases=count,configurations=len(configs),joint_csv_rows=len(rows),source_sha256=sha(cad),
        numerical_validation=d['numerical_validation'],max_global_force_residual_N=max(force_res),
        max_global_moment_residual_Nmm=max(moment_res),outside_small_displacement_screen_cases=invalid,
        base25_mesh12_to16_relative_change=mesh_change,base25_contact100_to1000_relative_change=penalty_change,
        summary=summary,back_geometry=dict(current_contact_area_mm2=0,closed_contact_area_each_mm2=1314*18,
            current_base_y_mm=[3310,3922],closed_base_y_mm=[3310,3940],back_y_mm=[3922,3940],
            meaning='Area geometrica apenas; nao comprova resistencia ou apoio no P01.'),
        incompatible_front_rail=dict(bbox_mm=rail,reservations=overlap,
            sources=['ferramentas/componentes/Portas_de_correr/montar_correr.py',
                     'ferramentas/componentes/Portas_de_correr/ajustar_vias.py'],
            limitation='Reservas hipoteticas de montagem, nao STEP real. Conflito ja na folha traseira fechada; nao simula varredura completa.'),
        status='Verificacao numerica condicional; capacidade20kg ainda nao demonstrada; CAD preservado.')
    (OUT/'Verificacao_caixa_20kg.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    draw(summary)
    print(json.dumps({k:report[k] for k in ['cases','joint_csv_rows','max_global_force_residual_N','max_global_moment_residual_Nmm','base25_mesh12_to16_relative_change','status']},ensure_ascii=False))

def draw(summary):
    im=Image.new('RGB',(1500,1100),'#f4f1eb');q=ImageDraw.Draw(im)
    def font(s,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),s)
    def txt(x,y,s,size=24,fill='#293831',b=False):q.text((x,y),s,font=font(size,b),fill=fill)
    txt(50,32,'P03 | caixa e ligações para 20 kg de conteúdo',36,b=True)
    txt(50,85,'Estudo separado • Arenza • duas portas de abrir • R52 preservada',24)
    q.rounded_rectangle((40,135,1460,530),18,fill='white')
    txt(65,153,'1. Dar área de encontro ao fundo',29,b=True)
    txt(80,206,'Antes: encontro de aresta',24,b=True)
    txt(790,206,'Proposta: base/topo +18 mm atrás',24,b=True)
    # Secao esquematica na parte traseira. Espessuras exageradas para leitura.
    for x,closed in [(100,False),(810,True)]:
        q.rectangle((x+380,270,x+415,380),fill='#b4a38a',outline='#293831',width=2)
        q.rectangle((x,380,x+(415 if closed else 380),415),fill='#ccbfa9',outline='#293831',width=2)
        if closed:q.line((x+380,380,x+415,380),fill='#27826c',width=8)
        else:q.ellipse((x+374,374,x+386,386),fill='#b85d40')
        txt(x,440,'1314 × '+('630' if closed else '612')+' × 18 mm',23)
    txt(65,485,'Envelope externo e vão interno preservados na proposta em 18 mm. Sem apoio traseiro automático no P01.',21)
    q.rounded_rectangle((40,550,920,1058),18,fill='white')
    txt(65,570,'2. Comparação condicional do deslocamento da base',26,b=True)
    labels={1:'18 mm, caixa fechada',2:'18 mm + apoio atrás',21:'25 mm, caixa fechada',22:'25 mm + apoio atrás'}
    for n,r in enumerate([s for s in summary if s['configuration'] in labels]):
        y=635+n*76;txt(65,y,labels[r['configuration']],23)
        w=r['max_base_down_mm']*35
        q.rectangle((435,y,435+w,y+28),fill='#a67b57')
        txt(450+w,y-1,f"{r['max_base_down_mm']:.2f} mm",24,b=True)
    txt(65,955,'Hipóteses: juntas e apoios com rigidez não medida.',22)
    txt(65,990,'20 kg + peso da caixa + 8 kg de portas + reserva.',22)
    q.rounded_rectangle((940,550,1460,1058),18,fill='#e5ece6')
    txt(965,575,'3. O que impede fechar',27,b=True)
    lines=['• Longarina frontal cruza reservas', '  de guia/retenção das portas P01.',
           '• Base de 25 mm deixa vão de', '  265 mm: sobra 15 para mala250.',
           '• Rigidez real de juntas, apoio', '  da divisória e caminho ao piso.',
           '• Acoplamento P02/C01 e cargas', '  simultâneas do conjunto em L.',
           '• Ferragens e manuseio reais.', '', '20 kg ainda não demonstrados.']
    for i,line in enumerate(lines):txt(965,635+i*32,line,22,b=i==10)
    im.save(OUT/'Caixa_20kg.png')

if __name__=='__main__':main()
