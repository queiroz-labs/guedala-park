"""Estudo integrado A–D: sol, luz, vapor e conforto térmico anual.

Executar da raiz com Python local e -B. Nenhum download automático e nenhuma
abertura/salvamento de FCStd. Climas obrigatórios e verificados por SHA256.
Os CSVs compactos são regeneráveis; séries e gráficos ficam fora do Git.
"""
import argparse
import copy
import math
from pathlib import Path
import numpy as np
from conforto_fisica import solar,day_number,local_sun,clear_sky,incidence
from conforto_geometria import (aperture,reveal,obstruction,patch,daylight_grid,
                               sky_component,sun_at_points,tower_horizon,directions_az)
from conforto_clima import sha,read_csv,write_csv,dump,load_era,load_epw,climate_tables
from conforto_calor import window_radiation,ventilation_table,simulate,heating_options
from conforto_umidade import surface_tables,moisture_tables,glaser_tables

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'03_Ambientes/Conforto_ambiental'
CONFIG=ROOT/'ferramentas/estudos/modelos/Conforto_hipoteses.json'
EXTERNAL=ROOT.parent/'outputs/Codex_sol_e_umidade'


def north_vector(pdf):
    import pdfplumber
    with pdfplumber.open(pdf) as doc:
        lines=[l for l in doc.pages[0].lines if 788<l['x0']<790 and 796<l['x1']<799 and 85<l['top']<88 and 90<l['bottom']<93]
        if len(lines)!=1:raise ValueError('Vetor de norte não reconhecido; rever fonte')
        line=lines[0];a,b=line['pts'];dx=b[0]-a[0];dy=b[1]-a[1]
        angle=math.degrees(math.atan2(dy,dx))
        return dict(fonte=str(pdf.relative_to(ROOT)),sha256=sha(pdf),pagina=1,
                    inicio_pontos=a,fim_pontos=b,dx_pontos=dx,dy_pontos=dy,
                    angulo_imagem_graus=angle,azimute_alto_graus=270-angle,
                    incerteza_leitura_graus=2,azimute_adotado_graus=245,incerteza_adotada_graus=4,
                    limite='Barra grossa colinear com a linha extraída; incerteza2° é conservadora por traço/registro, não erro estatístico. Satélite de Elias30/10/2026 não arquivado.')


def hh(hour):
    if hour is None:return ''
    minute=int(round(hour*60));return f'{minute//60:02d}:{minute%60:02d}'


def exposure(w,month,config,top=245,scenario='livre',step_min=6):
    day=23 if month==9 else 21
    hours=np.arange(step_min/120,24,step_min/60)
    alt,az=solar(day_number(month,day),hours,config['latitude'],config['longitude'],config['fuso_h'])
    sun=local_sun(alt,az,top);normal=-sun[:,w['eixo']]
    safe=np.maximum(normal,1e-12);thick=config['parede']['espessura_vano_m']
    reveal_fraction=np.maximum(0,1-abs(thick*sun[:,1-w['eixo']]/safe)/w['largura_m'])*np.maximum(0,1-abs(thick*sun[:,2]/safe)/w['altura_m'])
    visible=(alt>obstruction(w,az,config,scenario))&(normal>0)&(reveal_fraction>0)
    indices=np.flatnonzero(visible)
    return dict(mes=month,dia=day,janela=w['id'],ambiente=w['ambiente'],azimute_face=top+w['normal_relativa'],cenario=scenario,
                h_sol_geometrico=round(float(visible.sum()*step_min/60),2),
                primeiro_sol=hh(hours[indices[0]]-step_min/120) if len(indices) else '',
                ultimo_sol=hh(hours[indices[-1]]+step_min/120) if len(indices) else '',
                incidencia_min_graus=round(float(np.degrees(np.arccos(np.clip(normal[visible],-1,1))).min()),1) if len(indices) else '',
                limite='intervalos6min; alguma área útil do vão; não garante céu sem nuvens')


def solar_tables(g,config,out,external):
    import estudo_fotometrico as photo
    cases=['livre','hospital10','hospital20','torres','torre155','combinado'];monthly=[];detail=[];reference=[]
    solids=photo.room_solids(g);plot_points=[]
    for month in range(1,13):
        day=23 if month==9 else 21
        for top in config['azimutes_sensibilidade']:
            for w in config['janelas']:
                monthly.extend(exposure(w,month,config,top,case) for case in cases)
                for hour in range(6,20):
                    alt,az=solar(day_number(month,day),hour,config['latitude'],config['longitude'],config['fuso_h'])
                    geom=patch(w,float(alt),float(az),solids,g['floors'],config,top)
                    if top==245 and w['id']=='J-S' and month==12 and hour in (15,17):plot_points.append((hour,geom['pontos_piso']))
                    for case in cases:
                        valid=alt>obstruction(w,az,config,case)
                        row=dict(mes=month,dia=day,hora_UTC_menos3=hour,janela=w['id'],ambiente=w['ambiente'],azimute_topo=top,cenario=case,
                                 altura_sol_graus=round(float(alt),2),azimute_sol_graus=round(float(az),2),
                                 incidencia_graus=round(float(np.degrees(np.arccos(np.clip(incidence(alt,az,top+w['normal_relativa']),-1,1)))),2),
                                 piso_m2=round(geom['piso_m2'] if valid else 0,3),parede_m2=round(geom['parede_m2'] if valid else 0,3),
                                 moveis_m2=round(geom['moveis_m2'] if valid else 0,3),profundidade_recortada_m=round(geom['profundidade_m'] if valid else 0,2),
                                 profundidade_sem_recorte_m=round(geom['profundidade_sem_recorte_m'] if valid else 0,2),
                                 atingidos=geom['atingidos'] if valid else '',tapete='implantacao_nao_confirmada',metodo='quadratura16x12_primeiro_impacto')
                        detail.append(row)
                        if top==245 and month in (3,6,9,12) and case in ('livre','hospital20','torres'):reference.append(row)
    write_csv(out/'Sol_mensal.csv',monthly);write_csv(out/'Manchas_referencia.csv',reference)
    write_csv(external/'Sol_horario.csv',detail)
    obstructions=[]
    for w in config['janelas']:
        for az in (120,135,145,155,165,175,239,249,259,325,335):
            h=tower_horizon(w,np.array([az]),config)[0]
            low=tower_horizon(w,np.array([az]),config,.7)[0];high=tower_horizon(w,np.array([az]),config,1.3)[0]
            obstructions.append(dict(janela=w['id'],azimute=az,horizonte_torres_graus=round(float(h),1),
                           horizonte_escala_menos30_graus=round(float(low),1),horizonte_escala_mais30_graus=round(float(high),1),
                           hospital10_graus=10 if 239<=az<=259 else 0,hospital20_graus=20 if 239<=az<=259 else 0,
                           fonte='planta SEM ESCALA, polígonos e alturas hipotéticos; hospital setor fornecido, não medido'))
    write_csv(out/'Obstrucoes.csv',obstructions)
    return monthly,plot_points


def solar_gains(climates,config,out,external):
    rows=[];byhour=[]
    for climate in climates:
        for top in config['azimutes_sensibilidade']:
            raw=window_radiation(climate,config,top)
            for month in range(1,13):
                ix=climate['month']==month
                for j,w in enumerate(config['janelas']):
                    for protection,coeff in config['protecao'].items():
                        if not isinstance(coeff,dict):continue
                        gain=raw[ix,j]*config['vidro']['shgc']*coeff['solar']
                        rows.append(dict(clima=climate['name'],mes=month,janela=w['id'],azimute_topo=top,protecao=protection,
                                  area_vidro_hipotese_m2=round(w['largura_m']*w['altura_m']*config['vidro']['fracao_vidro'],3),
                                  ganho_medio_W=round(float(gain.mean()),1),ganho_max_W=round(float(gain.max()),1),
                                  energia_kWh_mes_medio=round(float(gain.sum()/1000/climate['years']),2),
                                  energia_faixa_shgc_min_kWh=round(float(gain.sum()/1000/climate['years']*config['vidro']['shgc_faixa'][0]/config['vidro']['shgc']),2),
                                  energia_faixa_shgc_max_kWh=round(float(gain.sum()/1000/climate['years']*config['vidro']['shgc_faixa'][1]/config['vidro']['shgc']),2)))
        raw=window_radiation(climate,config)
        np.savez_compressed(external/('Ganho_solar_'+climate['name']+'.npz'),W_sem_protecao=raw*config['vidro']['shgc'],janelas=[w['id'] for w in config['janelas']],tempo=[t.isoformat() for t in climate['time']])
    write_csv(out/'Ganhos_solares.csv',rows)
    for month,day in [(12,21),(3,21),(6,21),(9,23)]:
        for hour in np.arange(6,20,.5):
            alt,az=solar(day_number(month,day),hour,config['latitude'],config['longitude']);ghi,dni,dhi=clear_sky(alt)
            from conforto_fisica import plane_irradiance
            for w in config['janelas']:
                irradiance=plane_irradiance(alt,az,245+w['normal_relativa'],ghi,dni,dhi)
                byhour.append(dict(mes=month,dia=day,hora=hour,janela=w['id'],irradiancia_plano_W_m2=round(float(irradiance),1),
                             ganho_ceu_claro_sem_revelo_W=round(float(irradiance)*w['largura_m']*w['altura_m']*config['vidro']['fracao_vidro']*config['vidro']['shgc'],1),
                             limite='HaurwitzGHI, DHI15% hipótese; ganho superior sem recorte do vão nem obstáculos'))
    write_csv(out/'Ceu_claro.csv',byhour)


def light_tables(g,config,epw,out,external):
    rows=[];datasets={}
    variants=[('mobiliado',True,False,1.,None),('sem_moveis',False,False,1.,None),('fechamento_teto',True,True,1.,None),
              ('tecido',True,True,config['protecao']['tecido_compacto']['visivel'],None),
              ('blackout',True,True,config['protecao']['blackout_claro']['visivel'],None),
              ('parede_escura',True,False,1.,.45),('parede_clara',True,False,1.,.80)]
    for label,furniture,ceiling,curtain,rho in variants:
        summary,data=daylight_grid(g,config,furniture,ceiling,curtain,rho,config['luz']['grade_m'])
        rows.extend(dict(cenario=label,**r) for r in summary);datasets[label]=data
    write_csv(out/'Luz_natural.csv',rows)
    detail=[];integration=[];clear=[];base=datasets['mobiliado'];artificial=read_csv(out.parent/'Iluminacao/Grades_lux.csv')
    for room,d in base.items():
        points=d['points'];area=d['areas'];relevant=[r for r in artificial if r['caso']==room+'_geral']
        if not relevant:
            # Casos AS/cozinha/banho usam nomes específicos no estudo existente.
            candidates=sorted({r['caso'] for r in artificial if r['caso'].startswith(room+'_')})
            preferred=next((c for c in candidates if 'geral' in c),candidates[0] if candidates else None)
            relevant=[r for r in artificial if r['caso']==preferred]
        if not relevant:art=None
        else:
            positions=np.array([[float(r[k]) for k in ('x_m','y_m','z_m')] for r in relevant]);lux=np.array([float(r['lux_total_central']) for r in relevant])
            art=lux[np.argmin(((points[:,None,:]-positions[None,:,:])**2).sum(axis=2),axis=1)]
        for i,point in enumerate(points):detail.append(dict(ambiente=room,x_m=round(float(point[0]),4),y_m=round(float(point[1]),4),z_m=.75,
                   area_m2=round(float(area[i]),5),SC_lux=round(float(d['sc'][i]),2),IRC_lux=round(float(d['irc']),2),natural_lux=round(float(d['lux'][i]),2),
                   artificial_existente_lux='' if art is None else round(float(art[i]),2)))
        for month in range(1,13):
            ix=epw['month']==month
            # Série anual de suficiência usa SOMENTE componente difusa. Feixe
            # solar não contado como luz confortável; reflexão direta omitida.
            outdoor=epw['dhi'][ix]*config['luz']['eficacia_difusa_lm_W']
            natural=outdoor[:,None]/config['luz']['externa_lux']*d['lux'][None,:]
            ndays=ix.sum()/24
            for target in config['luz']['metas_lux']:
                sufficient=((natural>=target)*area).sum(axis=1)/area.sum()
                combined='' if art is None else round(float(((((natural+art)>=target)*area).sum(axis=1)/area.sum()>=config['luz']['fracao_grade_meta']).sum()/ndays),2)
                integration.append(dict(mes=month,ambiente=room,meta_hipotese_lux=target,fracao_area_alvo=config['luz']['fracao_grade_meta'],
                         h_dia_so_natural_difusa=round(float((sufficient>=config['luz']['fracao_grade_meta']).sum()/ndays),2),
                         h_dia_natural_mais_artificial=combined,artificial_media_lux='' if art is None else round(float(np.average(art,weights=area)),1),
                         limite='meta de estudo não normativa; luz artificial preexistente interpolada; só céu difuso anual'))
        for month,day in [(12,21),(6,21)]:
            for hour in (9,15,17):
                alt,az=solar(day_number(month,day),hour,config['latitude'],config['longitude']);_,dni,dhi=clear_sky(alt)
                diffuse=d['lux']*float(dhi)*config['luz']['eficacia_difusa_lm_W']/config['luz']['externa_lux']
                direct=sun_at_points(points,config['janelas'],d['solids'],config,float(alt),float(az),float(dni)*config['luz']['eficacia_direta_lm_W'])
                clear.append(dict(mes=month,dia=day,hora=hour,ambiente=room,lux_medio_difuso=round(float(np.average(diffuse,weights=area)),1),
                       lux_medio_feixe=round(float(np.average(direct,weights=area)),1),lux_max_total=round(float((diffuse+direct).max()),1),
                       limite='céu claro simplificado; distribuição difusa CIE encoberta escalada, não céu claro CIE/Perez; sem IRC do feixe'))
    write_csv(out/'Luz_grade.csv',detail);write_csv(out/'Luz_artificial_integracao.csv',integration);write_csv(out/'Luz_ceu_claro.csv',clear)
    # Horizonte e sensibilidade de área/reflectância ficam mensuráveis sem
    # instalar Radiance; a diferença de método não vira erro percentual falso.
    sensitivity=[]
    for label in ('livre','hospital20','torres','combinado'):
        for room,d in base.items():
            sc=sky_component(d['points'],config['janelas'],d['solids'],config,scenario=label)
            sensitivity.append(dict(ambiente=room,obstrucao=label,SC_media_lux=round(float(np.average(sc,weights=d['areas'])),2)))
    write_csv(out/'Luz_obstrucoes.csv',sensitivity)
    return rows,base


def measure_proposals(out):
    items=[
      ('AMB-01','fachadas','Bússola longe de alumínio/armadura; cruzar fotos/sol','SW245±5°; SSE155±5°','PQ-001|PQ-033','azimute e norte real'),
      ('AMB-02','cinco janelas','Largura/altura transparentes, peitoril, espessura vidro, SHGC/tau/U com fabricante','cinco vãos gráficos; não medir largura do cômodo','PQ-001|PQ-007|PQ-033','documento de esquadria/vidro'),
      ('AMB-03','três SW e duas SSE','Identificar correr/maxim-ar, área livre100%/50%; persiana inclusive sala, caixa/frestas','correr50% e maxim-ar35% são hipóteses','PQ-001|PQ-007|PQ-033','tipo e abertura efetiva'),
      ('AMB-04','envoltória','Perguntar bloco/espessura/graute, reboco, cor, laje e níveis de pavimento','bloco equivalente140mm; piso23,2m hipótese','PQ-008|PQ-033|PQ-034','composição térmica/fachada'),
      ('AMB-05','banho','Verificar duto/shaft, saída, retorno e admissão antes de exaustor; medir vazão instalada','ensaiar15/25/40 L/s sem fixar produto','PQ-013|PQ-018|PQ-003','exaustão disponível'),
      ('AMB-06','janela sala/AS','Foto nivelada do horizonte, inclinação e distância/altura hospital/T01/T03','hospital249±10° alturas0/10/20°','PQ-001|PQ-033','perfil angular real'),
      ('AMB-07','sala/quarto/banho/AS','Data logger T/UR5min por7dias no verão e inverno; registrar pessoas/banhos/janelas','não são medições já feitas','PQ-001|PQ-017','perfis internos'),
      ('AMB-08','sala/quarto/escritório','Fotos do sol15h/17h com data, persianas abertas; temperatura do piso sombreado/sol','controlar sol baixo; confirmar posição tapete','PQ-019|PQ-029|PQ-001','mancha e superfícies'),
      ('AMB-09','AS/portas internas','Fita leve/anemômetro na janela; portas abertas/fechadas, varal carregado','comparar sentido SE/NW e gargalos','PQ-001|PQ-017','vento na janela/caminho'),
      ('AMB-10','SW/SSE','Termômetro IR manhã/tarde/noite; corrigir emissividade e evitar vidro refletivo','parede livre e atrás de armário acessível','PQ-001|PQ-026','temperatura superficial'),
      ('AMB-11','janelas/caixas','Teste qualitativo de frestas com fita; se fumaça, sem chama e com RT/ventilação','ACH0,2–1,0 não medido','PQ-001|PQ-007','infiltração/vedação'),
      ('AMB-12','condomínio/RT','Resolver memorial§5.9 x convençãoart58; alimentação, dreno e instalação','split/aquecimento/piso condicionado;127V','PQ-017|PQ-012|PQ-004','viabilidade legal/técnica')]
    write_csv(out/'Medidas_propostas.csv',[dict(codigo_medida_proposto=k,ambiente=r,medida_ou_verificacao=q,valor_nominal_atual=v,PQ_existente=p,
                      pergunta_complementar=extra,valor_medido='',evidencia_campo='',situacao='PROPOSTA; não incluída no pipeline de chaves') for k,r,q,v,p,extra in items])


def plots(config,g,solar_points,daylight,surfaces,external):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig,ax=plt.subplots(figsize=(8,4.5))
    for m,d,label in [(12,21,'21/dez'),(3,21,'21/mar'),(6,21,'21/jun'),(9,23,'23/set')]:
        h=np.arange(5,20,.05);alt,az=solar(day_number(m,d),h,config['latitude'],config['longitude']);mask=alt>0
        a=az[mask].copy();e=alt[mask].copy();jumps=np.r_[False,abs(np.diff(a))>180];a[jumps]=np.nan;e[jumps]=np.nan
        ax.plot(a,e,label=label)
    ax.add_patch(Rectangle((239,0),20,20,color='gray',alpha=.2,label='Hospital20° hipotético'))
    ax.axvline(245,color='black',ls=':',label='NormalSW245°');ax.set(xlabel='Azimute desde norte (°)',ylabel='Altura geométrica (°)',title='Sol e horizonte hipotético — UTC−3');ax.legend(fontsize=8,ncol=2);fig.tight_layout();fig.savefig(external/'Carta_solar.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,6))
    for rects in g['floors'].values():
        for x,y,X,Y in rects:ax.add_patch(Rectangle((x,y),X-x,Y-y,fill=False,lw=.7))
    for hour,points in solar_points:
        if points:
            a=np.array(points);ax.scatter(a[:,0],a[:,1],s=7,label=f'21/dez {hour}h')
    ax.set(xlim=(-.2,7.6),ylim=(7.2,-.2),aspect='equal',title='Primeiro impacto no piso — janela da sala\nPontos ponderados, não contorno contínuo');ax.legend();fig.tight_layout();fig.savefig(external/'Mancha_sol.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,6));allpoints=np.concatenate([d['points'] for d in daylight.values()]);alllux=np.concatenate([d['lux'] for d in daylight.values()])
    sc=ax.scatter(allpoints[:,0],allpoints[:,1],c=alllux/100,marker='s',s=14,cmap='viridis');fig.colorbar(sc,ax=ax,label='DF (%) — Eext10000lux')
    ax.set(xlim=(-.2,7.6),ylim=(7.2,-.2),aspect='equal',title='Luz natural a0,75m, mobiliado\nAproximação, sem validação Radiance');fig.tight_layout();fig.savefig(external/'Mapa_DF.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4))
    from conforto_fisica import surface_rh
    # Séries TMY ordenadas em meses, não previsões.
    months=np.repeat(np.arange(1,13),[31*24,28*24,31*24,30*24,31*24,30*24,31*24,31*24,30*24,31*24,30*24,31*24]);ti=np.where(np.isin(months,[12,1,2,3]),26,20)
    for face,temp in surfaces.items():ax.plot(range(1,13),[float(surface_rh(ti[months==m],65,temp[months==m]).mean()) for m in range(1,13)],label=face+' URin65%')
    ax.axhline(80,ls=':',color='black',label='Triagem80%');ax.set(xlabel='Mês',ylabel='UR superficial média (%)',title='Parede sem armário — TMY e Ti hipotética');ax.legend();fig.tight_layout();fig.savefig(external/'UR_superficial.png',dpi=150);plt.close(fig)


def main():
    import json
    import estudo_fotometrico as photo
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--dados',type=Path,default=EXTERNAL);parser.add_argument('--hipoteses',type=Path,default=CONFIG)
    parser.add_argument('--somente',choices=['solar','luz','umidade','termico','tudo'],default='tudo')
    args=parser.parse_args();external=args.dados.resolve()
    if external.is_relative_to(ROOT):parser.error('Dados e séries devem ficar fora do repositório')
    config=json.loads(args.hipoteses.read_text(encoding='utf-8'));OUT.mkdir(exist_ok=True);external.mkdir(parents=True,exist_ok=True)
    # Exigir ambos em qualquer execução evita gerar um relatório "completo"
    # sem a metade do clima ou tratar campo ausente como zero.
    era=load_era(external/config['clima']['era5_arquivo'],config);epw=load_epw(external/config['clima']['epw_arquivo'],config)
    g=photo.load_geometry();dump(OUT/'Orientacao.json',north_vector(ROOT/'09_Referencias/Plantas_e_manuais/Planta_oficial.pdf'))
    summary=climate_tables(era,epw,OUT);measure_proposals(OUT)
    print('Climas e exportação R54 conferidos; iniciando '+args.somente,flush=True)
    if args.somente in ('solar','tudo'):
        monthly,pts=solar_tables(g,config,OUT,external);solar_gains((era,epw),config,OUT,external);print('Sol e ganhos concluídos',flush=True)
    if args.somente in ('luz','tudo'):
        light,grid=light_tables(g,config,epw,OUT,external);print('Luz natural e integração concluídas',flush=True)
    if args.somente in ('umidade','tudo'):
        risk,station,surfaces=surface_tables(epw,config,OUT,external);moisture_tables(epw,g,config,OUT,external);glaser_tables(epw,config,OUT);print('Umidade e Glaser concluídos',flush=True)
    if args.somente in ('termico','tudo'):
        volume=sum(sum(c['area'] for c in photo.cells(rects,0,1))*g['heights'][r] for r,rects in g['floors'].items())
        ventilation_table(era,config,volume,OUT)
        for climate in (epw,era):
            print('RC: '+climate['name']+' '+str(len(climate['te']))+' horas',flush=True)
            result=simulate(climate,g,config,OUT,external)
            if climate['name']=='ERA5':heating_options(result,config,OUT)
    if args.somente=='tudo':
        plots(config,g,pts,grid,surfaces,external)
        from conforto_relatorio import supplemental
        supplemental(config,OUT,external,ROOT)
    sources=[CONFIG,ROOT/'09_Referencias/Plantas_e_manuais/Planta_oficial.pdf',ROOT/'06_Entregas/Caderno_pranchas/Geometria.json',
             ROOT/'03_Ambientes/Iluminacao/Grades_lux.csv',ROOT/'03_Ambientes/Equipamentos/Climatizacao_parcelas.csv']
    sources += sorted((ROOT/'ferramentas/estudos').glob('conforto_*.py'))+[Path(__file__)]
    import hashlib
    write_csv(OUT/'Rastreio.csv',[dict(fonte=str(p.relative_to(ROOT)).replace('\\','/'),
       sha256_LF_ou_binario=hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n') if p.suffix in ('.py','.json','.csv') else p.read_bytes()).hexdigest(),
       natureza='entrada ou código; textos normalizados LF, não medida real') for p in sources])
    print('Concluído. CSVs em '+str(OUT)+'; séries/gráficos em '+str(external),flush=True)


if __name__=='__main__':main()
