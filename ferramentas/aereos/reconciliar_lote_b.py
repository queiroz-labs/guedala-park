"""LoteB: geometria,contatos,mapa anterior e premissas respondidas por Elias."""
from collections import Counter
from pathlib import Path
import csv,itertools,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontes import sha,HASH_RULE

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao'
GLOBAL=OUT/'Geometria_R51.json';OTHER=ROOT/'04_Moveis/P04/Suspensao_P04_P15/Geometria_e_portas_R51.json'
META={'P17':dict(w=1964.,h=550.,d=330.,back='Peca386',base='Peca387',top='Peca388'),
      'P04':dict(w=1764.,h=308.,d=230.,back='Peca268',base='Peca269',top='Peca270'),
      'P12':dict(w=765.,h=584.,d=330.,back='Peca344',base='Peca345',top='Peca346')}

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def csvread(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def bodies():
    g=read(GLOBAL);o=read(OTHER);out={};reconciled=[]
    for code,m in META.items():
        fiche=ROOT/f'06_Entregas/Fichas_fabricacao/{code}-pecas.csv';spec={}
        for r in csvread(fiche):
            for name in r['IDs CAD'].split(' | '):spec[name]=sorted(float(r[k]) for k in ['C nominal mm','L nominal mm','Esp. envelope mm'])
        p={};source=o['modules'][code] if code=='P04' else g['modules'][code]
        for item in source['body']:
            name=item['name'];c=np.array(item['center_uvz_mm'],float)
            if 'box_module_mm' in item:
                b=np.array(item['box_module_mm'],float);origin=source['canonical_origin']
                box=np.r_[b[0]-origin['u0_module_mm'],origin['rear_module_mm']-b[4],b[2]-origin['z0_module_mm'],
                          b[3]-origin['u0_module_mm'],origin['rear_module_mm']-b[1],b[5]-origin['z0_module_mm']]
            else:
                if name in ['Peca266','Peca267']:dims=[18,m['d'],m['h']]
                elif name==m['back']:dims=[m['w'],18,m['h']-36]
                elif name in [m['base'],m['top']]:dims=[m['w'],m['d']-18,18]
                elif name=='FaixaFixaEstudo':dims=[7,18,m['h']-36]
                else:dims=[18,m['d']-18,m['h']-36]
                box=np.r_[c-np.array(dims)/2,c+np.array(dims)/2]
            box=np.round(box,7);dims=box[3:]-box[:3]
            assert np.max(np.abs((box[:3]+box[3:])/2-c))<1e-5
            assert abs(np.prod(dims)-item['volume_mm3'])<1e-4
            assert np.max(np.abs(sorted(dims)-np.array(spec[name])))<1e-6,(code,name)
            p[name]=box
        out[code]=p;reconciled.append(dict(code=code,body_parts=len(p),dimension_csv=fiche.relative_to(ROOT).as_posix(),
            dimension_projection_sha256=hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            projection_scope='IDs CAD e tres dimensoes nominais porID;demais colunas nao consumidas pelo calculo.',
            dimensions_match=True,volume_and_CG_match_saved_R51=True,
            R52_body_positions_read_live=False,body_source='GeometriaR51 reconciliada dimensionalmente com fichas locais;nao nova verificacao BREP R52'))
    return out,reconciled

def contact(a,b):
    overlaps=np.minimum(a[3:],b[3:])-np.maximum(a[:3],b[:3]);tol=1e-6
    if min(overlaps)<-tol:return 'separado',0.,None
    n=int(sum(overlaps>tol))
    if n==3:return 'intersecao_volumetrica',float(np.prod(overlaps)),None
    if n==2:
        axis=int(np.argmin(np.abs(overlaps)));return 'face',float(np.prod(overlaps[overlaps>tol])),axis
    return ('aresta' if n==1 else 'ponto'),0.,None

def main():
    choices=read(OUT/'Lote_B_premissas.json')
    release=read(ROOT/'ferramentas/site/current_release.json');cad=ROOT/release['cadPath']
    assert sha(cad)==release['cadSHA256']
    original,recon=bodies();all_contacts=[];modules=[];mapping=[]
    oldmap=csvread(ROOT/'04_Moveis/Mapa_conectores/Mapa_conectores_R00.csv')
    for code,m in META.items():
        variants={'atual':original[code]}
        if code in ['P17','P04']:
            full={k:v.copy() for k,v in original[code].items()};full[m['back']][2]=0;full[m['back']][5]=m['h'];variants['fundo_inteiro_proposto']=full
        summaries=[]
        for variant,p in variants.items():
            hits=[]
            for (na,a),(nb,b) in itertools.combinations(p.items(),2):
                kind,area,axis=contact(a,b)
                if kind=='separado':continue
                assert kind!='intersecao_volumetrica',(code,variant,na,nb)
                row=dict(code=code,variant=variant,a=na,b=nb,kind=kind,contact_area_mm2=area,normal_axis='uvz'[axis] if axis is not None else '',
                    status='Geometria de caixas nominais;nao resistencia,usinagem ou montagem aprovada')
                all_contacts.append(row);hits.append(row)
            back=p[m['back']];pairs=[]
            for h in [m['base'],m['top']]:
                kind,area,axis=contact(back,p[h]);pairs.append(dict(a=m['back'],b=h,kind=kind,area_mm2=area))
                assert kind==('face' if variant=='fundo_inteiro_proposto' else 'aresta')
            summaries.append(dict(variant=variant,proposed=variant!='atual',adopted=False,
                preferred_for_study=(variant=='fundo_inteiro_proposto' if code in choices['full_back_preferred_for_study'] else variant=='atual'),
                boxes_uvz_mm={k:v.tolist() for k,v in p.items()},back_to_base_top=pairs,
                positive_face_contacts=sum(r['kind']=='face' for r in hits),
                volume_mm3=float(sum(np.prod(b[3:]-b[:3]) for b in p.values()))))
        rows=[r for r in oldmap if r['Módulo']==code]
        for r in rows:
            a,b=r['Peça A'],r['Peça B'];assert a in original[code] and b in original[code]
            kind,area,axis=contact(original[code][a],original[code][b])
            mapping.append(dict(code=code,a=a,b=b,family=r['Conector'],old_connector_qty=int(r['Qtd conector']),old_dowel_qty=int(r['Qtd cavilha']),
                current_contact=kind,current_area_mm2=area,purchase_quantity=False,
                interpretation='Quantidade anterior para cotacao,nao existente/aprovada nem somar com marcadores do estudo'))
        newV=(summaries[-1]['volume_mm3']-summaries[0]['volume_mm3']) if len(summaries)>1 else 0.
        modules.append(dict(code=code,width_internal_mm=m['w'],width_external_mm=m['w']+36,height_mm=m['h'],depth_mm=m['d'],
            current_back_height_mm=m['h']-36,proposed_full_back_height_mm=m['h'] if len(summaries)>1 else None,
            full_back_additional_volume_mm3=newV,
            delta_mass_kg_hypothetical_800_18p3=newV*800/1e9*18.3/18,
            external_and_useful_dimensions_change_mm=0,
            historical_connector_quantities={family:sum(int(r['Qtd conector']) for r in rows if r['Conector']==family) for family in sorted(set(r['Conector'] for r in rows))},
            historic_dowels=sum(int(r['Qtd cavilha']) for r in rows),variants=summaries,
            underside_clean_required=True,back_edge_finish=choices.get('back_edge_finish',{}).get(code)))
    p17=read(ROOT/'04_Moveis/P17/Base_fundo_ligacoes/Conferencia_geometrica.json')
    p04axes=[r for r in csvread(ROOT/'04_Moveis/Ligacoes_sem_tubos/Eixos_ligacoes_estudo.csv') if r['id'].startswith('P04')]
    underside={'P17':sum(r['axis_in_module']=='Z' and abs(r['study_uyz_mm'][2])<1e-6 for r in p17['nominal_axes']),
               'P04':sum('Z' in r['axis'] and abs(float(r['Z_mm']))<1e-6 for r in p04axes)}
    assert underside=={'P17':8,'P04':8}
    decisions=[dict(id='uso_carga',state='META_ESCOLHIDA_NAO_CAPACIDADE',subject='Elias,25/10/2026:"20 kg / 10 kg / 10 kg",ordemP17/P04/P12;usos no arquivo de premissas.'),
        dict(id='base_aparente',state='BASE_LIMPA',subject='Elias,25/10/2026:"Base limpa, sem cabeças ou tampinhas aparentes";8posicoes inferiores antigas de cadaP17/P04 precisam de revisao.'),
        dict(id='fundos_inteiros',state='PREFERIDOS_PARA_ESTUDO_SEM_ALTERAR_CAD',subject='Elias,25/10/2026:"Desenvolver os fundos inteiros";P17:514para550;P04:272para308;mesmo envelope/vaos.'),
        dict(id='borda_inferior_fundo',state='FITA_NO_PADRAO_EXTERNO',subject='Elias,25/10/2026:"Fita na borda no padrão externo: Arenza no P04 e off-white no P17";facesBrancoTX preservadas.'),
        dict(id='P04_faixa7',state='PROPOSTA_EXISTENTE_NAO_APROVADA',subject='FaixaFixaEstudo7x18x272 ja listada no acervo;nenhum credito de reforco/decisao nova por esta auditoria.'),
        dict(id='suspensao',state='PRODUTO_NAO_ESCOLHIDO',subject='Nao copiar Bigfer do loteA ou numero de suportes paraP04/P12/P17;definir caminho,produto equantidade depois das decisoes.'),
        dict(id='acabamento_chapa',state='REGRA_VIGENTE_PRESERVADA',subject='Um acabamento nas duas faces por peca;nao inserir segunda caixa. Aparencia das bordas expostas pelo fundo inteiro depende de revisao.')]
    paths=[GLOBAL,OTHER,OUT/'Lote_B_premissas.json',ROOT/'04_Moveis/Mapa_conectores/Mapa_conectores_R00.csv',ROOT/'04_Moveis/P17/Base_fundo_ligacoes/Conferencia_geometrica.json',ROOT/'04_Moveis/Ligacoes_sem_tubos/Eixos_ligacoes_estudo.csv']
    d=dict(scope='Auditoria geometrica e reconciliacao sem assumir decisoes de Elias.',cad_sha256=sha(cad),cad_opened=False,cad_changed=False,
        reconciliation=recon,modules=modules,contacts=all_contacts,historical_map_rows=len(mapping),
        current_mapped_contacts_all_positive=all(r['current_contact']=='face' for r in mapping),historical_map=mapping,
        historical_nominal_axes={'P17':len(p17['nominal_axes']),'P04':len(p04axes)},underside_positions_proposed=underside,
        decisions=decisions,chosen_payloads_kg=choices['payload_targets_kg'],chosen_hardware=None,new_connector_purchase_qty=None,
        sources_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in paths},hash_rule=HASH_RULE,
        script_sha256=sha(Path(__file__)),hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')),
        limits=['Fichas reconciliam dimensoes,nao provam posicao/forma integral do BREP R52;nao houve nova aberturaCAD.',
            'Caixas retangulares,sem ferragens/furos/cabecas/tolerancias ou movimento de portas.',
            'Fundo inteiro pode expor borda inferior/traseira e precisa de acabamento/acesso revisados;nao e aprovacao de usinagem.',
            'Massa incremental hipotetica,nao pesagem/SKU/material aprovado;metas de conteudo escolhidas,capacidade nao demonstrada.'])
    (OUT/'Lote_B_geometria.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,rows in [('Lote_B_contatos.csv',all_contacts),('Lote_B_mapa_reconciliado.csv',mapping)]:
        with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
    draw(d)
    print(json.dumps(dict(modules=3,geometry_variants=sum(len(m['variants']) for m in modules),contacts=len(all_contacts),historical_map_rows=len(mapping),
        historical_contacts_positive=d['current_mapped_contacts_all_positive'],underside_positions=underside,CAD_geometry_applied=0,CAD_preserved=True)))

def draw(d):
    im=Image.new('RGB',(1500,1040),'#f4f1eb');q=ImageDraw.Draw(im)
    def t(x,y,s,n=23,b=False,c='#293a31'):q.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n),fill=c)
    t(40,24,'P17 → P04 → P12 | fundos e base limpa',35,True)
    t(40,79,'Metas de conteúdo: 20 / 10 / 10 kg • estudo separado da R52',24)
    for i,m in enumerate(d['modules']):
        x=40+i*485;code=m['code'];h=m['height_mm'];w=m['width_external_mm'];sx=405/w;sy=280/h
        q.rounded_rectangle((x,135,x+460,690),18,fill='white');t(x+20,155,code,29,True)
        l=x+25;r=x+430;top=240;bottom=520
        q.rectangle((l,top,r,bottom),fill='#e8ece4',outline='#81725d',width=3)
        for b in m['variants'][0]['boxes_uvz_mm'].values():
            if b[3]-b[0]<25 and b[4]-b[1]>100 and b[5]-b[2]>100:
                xx=l+(b[0]+18)*sx;q.rectangle((xx,top,xx+max(2,(b[3]-b[0])*sx),bottom),fill='#b7a68a')
        if len(m['variants'])>1:
            q.rectangle((l+18*sx,top,r-18*sx,top+18*sy),fill='#d7a36c')
            q.rectangle((l+18*sx,bottom-18*sy,r-18*sx,bottom),fill='#d7a36c')
            t(x+20,550,f"Fundo: {h-36:g} → {h:g} mm (estudo)",24,True)
            t(x+20,592,f"Acréscimo ≈ {m['delta_mass_kg_hypothetical_800_18p3']:.2f} kg a ρ800",22)
            t(x+20,637,'Rever 8 posições inferiores anteriores',21,c='#a65438')
        else:
            t(x+20,550,'Fundo atual: 548 mm',24,True)
            t(x+20,592,'Divisória central existente',22)
            t(x+20,637,'Meta: 10 kg de bacias e afins',21,c='#a65438')
        t(x+20,200,f"Caixa {w:g} × {h:g} × {m['depth_mm']:g} mm",22)
    q.rounded_rectangle((40,720,1460,1000),18,fill='white')
    t(65,740,'Preferência de estudo confirmada por Elias em25/10/2026',29,True)
    t(65,794,'Fundos inteiros criam faces de contato com base e tampo, mantendo os vãos e o envelope externo.',23)
    t(65,840,'As faixas em ocre mostram os acréscimos de 18 mm em cima e embaixo; cores apenas didáticas.',23)
    t(65,886,'Borda inferior: fita Arenza no P04 e off-white no P17; faces dos fundos em Branco TX.',23)
    t(65,943,'Conectores, suspensão e aplicação na R52 continuam condicionados.',25,True)
    im.save(OUT/'Lote_B_reconciliacao.png')

if __name__=='__main__':main()
