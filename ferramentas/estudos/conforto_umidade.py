"""Superfícies, balanços de vapor, cavidades e Glaser condicionais."""
import math
import numpy as np
from conforto_fisica import (Wall,saturation,dewpoint,mixing_ratio,rh_from_w,surface_rh,
    moisture_step,critical_frsi,cavity_surface,plane_irradiance)
from conforto_clima import write_csv


def surface_tables(climate,config,out,external):
    p=config['parede'];wall=Wall(p['camadas'],p['rsi'],p['rse']);months=climate['month']
    ti=np.where(np.isin(months,[12,1,2,3]),26.,20.)
    rows=[];station=[];surfaces={}
    for normal,label in [(245,'SW'),(155,'SSE')]:
        rad=plane_irradiance(climate['alt'],climate['az'],normal,climate['ghi'],climate['dni'],climate['dhi'])
        tsa=climate['te']+p['absorcao_solar']*rad*p['rse']
        ts=wall.series(tsa,ti);surfaces[label]=ts
        components={'bloco':ts,'vidro':ti-config['vidro']['u_W_m2K']*p['rsi']*(ti-climate['te']),
                    'aluminio_frsi03':climate['te']+.3*(ti-climate['te']),
                    'aluminio_frsi07':climate['te']+.7*(ti-climate['te'])}
        for m in range(1,13):
            ix=months==m;te=float(np.percentile(climate['te'][ix],5));indoor=float(ti[ix][0]);tstat=indoor-wall.u*p['rsi']*(indoor-te)
            station.append(dict(mes=m,face=label,Te_p05_C=round(te,2),Ti_hipotese_C=indoor,U_W_m2K=round(wall.u,3),
                                capacidade_J_m2K=wall.capacity,Ts_estacionaria_sem_sol_C=round(tstat,2),Ts_transiente_media_C=round(float(ts[ix].mean()),2),
                                Ts_transiente_min_C=round(float(ts[ix].min()),2),Ts_transiente_max_C=round(float(ts[ix].max()),2)))
            for rh in config['umidade']['ur_interna_cenarios']:
                for component,temperature in components.items():
                    srh=surface_rh(ti[ix],rh,temperature[ix]);fcrit=critical_frsi(indoor,rh,te)
                    rows.append(dict(mes=m,face=label,componente=component,UR_interna_pct=rh,Ti_C=indoor,
                          Ts_media_C=round(float(temperature[ix].mean()),2),Ts_min_C=round(float(temperature[ix].min()),2),
                          UR_superficial_media_pct=round(float(srh.mean()),1),h_ge75=int((srh>=75).sum()),h_ge80=int((srh>=80).sum()),
                          h_ge90=int((srh>=90).sum()),h_condensacao=int((srh>=100).sum()),fRsi_crit80=round(fcrit,3) if math.isfinite(fcrit) else '',
                          natureza='potencial higrotérmico, sem sorção/chuva/biologia; não diagnóstico'))
    write_csv(out/'Superficies_mensais.csv',station);write_csv(out/'Umidade_superficial.csv',rows)
    np.savez_compressed(external/'Superficies_TMYx.npz',Ti=ti,Ts_SW=surfaces['SW'],Ts_SSE=surfaces['SSE'])
    cabinet_rows=[]
    for face,ts in surfaces.items():
        # Temperatura exterior equivalente que reproduz a superfície do 1D.
        equivalent=ti-(ti-ts)/(wall.u*p['rsi'])
        for back in (.006,.015):
            for gap in (0.,.01,.02,.03):
                for opening_cm2 in (0,20,50,100):
                    if gap==0 and opening_cm2>0:continue  # sem caminho físico no modelo.
                    for pressure in ((.2,) if opening_cm2==0 else (.05,.2,.5)):
                        # Duas grelhas iguais em série; cada área livre nominal.
                        q=.6*(opening_cm2/10000/math.sqrt(2))*math.sqrt(2*pressure/1.2)
                        conv=1200*q/(.6*2.6)
                        fraction=conv/(2+conv)
                        temperature=cavity_surface(ti,equivalent,1/wall.u-p['rsi'],back,gap,fraction,p['rsi'])
                        for rh in (50,65,80):
                            potential=surface_rh(ti,rh,temperature)
                            for m in range(1,13):
                                ix=months==m
                                cabinet_rows.append(dict(face=face,fundo_mm=int(back*1000),vao_mm=int(gap*1000),
                                      cada_grelha_livre_cm2=opening_cm2,delta_p_hipotese_Pa=pressure,vazao_hipotese_L_s=round(q*1000,3),
                                      UR_ambiente_pct=rh,mes=m,Ts_min_C=round(float(temperature[ix].min()),2),h_ge80=int((potential[ix]>=80).sum()),
                                      h_condensacao=int((potential[ix]>=100).sum()),fracao_mistura_termica=round(fraction,3),
                                      UR_ambiente_teto_para_superficie80_pct=round(float(np.min(80*saturation(temperature[ix])/saturation(ti[ix]))),1)))
    write_csv(out/'Fundos_armarios.csv',cabinet_rows)
    return rows,station,surfaces


def typical_day(climate,month,warm):
    starts=np.flatnonzero((climate['month']==month)&(climate['hour']==1))
    # EPW hour=1 é início do primeiro intervalo. Dias representativos, não extremos.
    means=np.array([climate['td' if warm else 'te'][s:s+24].mean() for s in starts])
    target=np.percentile(means,75 if warm else 25)
    return int(starts[np.argmin(abs(means-target))])


def moisture_tables(climate,g,config,out,external):
    import estudo_fotometrico as photo
    cfg=config['umidade'];pressure=cfg['pressao_Pa'];density=cfg['densidade_ar_seco_kg_m3'];summary=[];detail=[]
    for season,month,warm in [('verao',1,True),('inverno',7,False)]:
        start=typical_day(climate,month,warm);ti=cfg['temperatura_verao_C'] if warm else cfg['temperatura_inverno_C']
        for room in g['floors']:
            volume=sum(c['area'] for c in photo.cells(g['floors'][room],0,1))*g['heights'][room]
            cases=[('fechada',cfg['ach_fechado']*volume/3600),('aberta',cfg['ach_aberto']*volume/3600)]
            if room=='banho':cases += [('exaustor_'+str(q),q/1000) for q in cfg['banho_exaustores_L_s']]
            for case,flow in cases:
                w=float(mixing_ratio(ti,60,pressure));initial=density*volume*w
                generated=exported=condensed=0.;remaining=cfg['roupa_agua_inicial_kg'] if room=='lavanderia' else 0.
                recovery='nao_alcancou_em48h';dry='nao_secou_em48h';rhvalues=[];srhvalues=[];after=[]
                for step in range(576):
                    hour=step/12;clock=hour%24;j=(start+int(hour))%len(climate['te'])
                    te=float(climate['te'][j]);rh_out=float(climate['rh'][j]);ws=float(mixing_ratio(te,rh_out,pressure))
                    rh_before=float(rh_from_w(ti,w,pressure));source_h=0.
                    if room=='banho' and 6.5<=clock<6.75:source_h=cfg['banho_kg']/(cfg['banho_duracao_min']/60)
                    if room=='quarto' and (clock>=22 or clock<6):source_h=2*cfg['pessoa_kg_h']
                    if room=='escritorio' and 9<=clock<18:source_h=cfg['pessoa_kg_h']
                    if room=='sala' and 18<=clock<22:source_h=2*cfg['pessoa_kg_h']
                    if room=='cozinha' and 18<=clock<19:source_h=cfg['coccao_kg_h']
                    evaporated=0.
                    if room=='lavanderia':
                        evaporated=min(remaining,cfg['roupa_evaporacao_kg_h']*max(0,1-rh_before/100)/12)
                        remaining-=evaporated;source_h=evaporated*12
                        if 17<=clock<18:source_h+=cfg['lavadora_lavaloucas_kg_ciclo']
                        if remaining<=.05 and dry=='nao_secou_em48h':dry=round(hour+1/12,2)
                    supply=ws
                    if case.startswith('exaustor'):
                        # Reposição hipotética metade exterior/metade apartamento60%.
                        supply=.5*ws+.5*float(mixing_ratio(ti,60,pressure))
                    w,ventmass=moisture_step(w,source_h/3600,flow,supply,volume,300,density)
                    generated+=source_h/12;exported+=ventmass
                    saturated=float(mixing_ratio(ti,100,pressure))
                    drain=max(0,(w-saturated)*density*volume);condensed+=drain;w=min(w,saturated)
                    rh=float(rh_from_w(ti,w,pressure));ts=ti-(ti-te)*.35  # ponte/frio local hipotético fRsi0,65.
                    srh=float(surface_rh(ti,rh,ts));rhvalues.append(rh);srhvalues.append(srh)
                    if 6.75<=hour<24:after.append((hour,rh))
                    detail.append(dict(estacao=season,dia_TMY=climate['time'][start].strftime('%m-%d'),ambiente=room,cenario=case,
                         hora=round(hour+1/12,3),Te_C=te,UR_externa_pct=rh_out,Ti_C=ti,UR_pct=round(rh,2),Ts_ponte_hipotese_C=round(ts,2),
                         UR_superficie_pct=round(srh,2),gerado_acumulado_kg=round(generated,5),condensado_kg=round(condensed,5),roupa_agua_restante_kg=round(remaining,4)))
                if room=='banho':
                    for (h,rh),(h2,rh2) in zip(after,after[1:]):
                        if rh<70 and rh2<70:recovery=round((h+1/12-6.75)*60,1);break
                residual=initial+generated-exported-condensed-density*volume*w
                if abs(residual)>1e-9:raise ValueError('Falha de conservação da massa de vapor')
                summary.append(dict(estacao=season,dia_TMY=climate['time'][start].strftime('%m-%d'),ambiente=room,cenario=case,Ti_C=ti,
                       vazao_L_s=round(flow*1000,2),ACH=round(flow*3600/volume,2),UR_media_pct=round(float(np.mean(rhvalues)),1),
                       UR_max_pct=round(max(rhvalues),1),UR_superficie_max_pct=round(max(srhvalues),1),
                       retorno_banho_70_min=recovery if room=='banho' else '',secagem_roupa_h=dry if room=='lavanderia' else '',
                       agua_roupa_restante48h_kg=round(remaining,3) if room=='lavanderia' else '',vapor_gerado48h_kg=round(generated,3),
                       condensado_ar48h_kg=round(condensed,3),residuo_massa_kg=round(residual,12)))
    write_csv(out/'Balanco_umidade.csv',summary);write_csv(external/'Umidade_5min.csv',detail)
    return summary


def glaser_tables(climate,config,out):
    p=config['parede'];ins=p['isolamento'];rows=[]
    for face,az in [('SW',245),('SSE',155)]:
        rad=plane_irradiance(climate['alt'],climate['az'],az,climate['ghi'],climate['dni'],climate['dhi'])
        for month in range(1,13):
            mask=climate['month']==month
            for condition in ('media_mensal','noite_fria_p05'):
                te=float(climate['te'][mask].mean() if condition=='media_mensal' else np.percentile(climate['te'][mask],5))
                rh_ext=float(climate['rh'][mask].mean())
                radiation=float(rad[mask].mean()) if condition=='media_mensal' else 0.
                tse=te+p['absorcao_solar']*radiation*p['rse'];ti=26 if month in (12,1,2,3) else 20
                for rh in (50,65,80):
                    for material,mu in [('sem_isolamento',None),('la_hipotese',1),('EPS_hipotese',40)]:
                        layers=p['camadas']+([[ins['espessura_m'],ins['lambda'],10000],[ins['gesso_m'],ins['gesso_lambda'],10000]] if mu is not None else [])
                        mus=[15,ins['mu_bloco'],15]+([mu,ins['mu_gesso']] if mu is not None else [])
                        resist=np.array([v[0]/v[1] for v in layers]);sd=np.array([v[0]*m for v,m in zip(layers,mus)])
                        cum_r=np.cumsum(resist)+p['rse'];rt=resist.sum()+p['rse']+p['rsi']
                        temperatures=tse+(ti-tse)*cum_r/rt
                        vapor=saturation(te)*rh_ext/100+(saturation(ti)*rh/100-saturation(te)*rh_ext/100)*np.cumsum(sd)/sd.sum()
                        potential=vapor/saturation(temperatures)*100
                        j=int(np.argmax(potential))
                        rows.append(dict(face=face,mes=month,condicao=condition,material=material,UR_interna_pct=rh,Te_C=round(te,2),Ti_C=ti,
                                 interface_critica_apos_camada=j+1,T_interface_C=round(float(temperatures[j]),2),UR_interface_max_pct=round(float(potential[j]),1),
                                 condensacao_potencial=bool(potential[j]>=100),
                                 limite='Glaser instantâneo estacionário hipotético; não calcula água anual acumulada; SD real/barreira/chuva/2D pendentes'))
    write_csv(out/'Isolamento_Glaser.csv',rows)
    ac=[]
    for td in (20.,21.,22.):
        for ts in (16.,18.,20.,22.,24.,26.):
            ac.append(dict(orvalho_externo_C=td,superficie_C=ts,condensacao_exterior_possivel=ts<td,
                           local='tubulação/ponte exposta ao ar exterior úmido; não rodapé aquecido automaticamente'))
    write_csv(out/'AC_ponto_orvalho.csv',ac)
