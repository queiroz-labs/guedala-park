"""Balanço RC sazonal e ventilação, sem selecionar potência de equipamento."""
import gzip
import csv
import math
import numpy as np
from conforto_fisica import Wall,local_sun,incidence,plane_irradiance,cross_flow,adaptive_limit
from conforto_geometria import obstruction
from conforto_clima import read_csv,write_csv,dump


def thermostat_response(matrix,den,ham,air,mass,target,active,heating=True,cap=None):
    """Controle ideal unilateral por conjunto ativo; não resfria para aquecer.

    Interzonas podem tornar uma demanda inicial redundante: remover a zona
    que precisaria de sinal contrário evita aquecimento+resfriamento fictício.
    """
    indices=np.flatnonzero(active);response=np.linalg.inv(matrix)
    operative=(air+mass)/2
    op_response=.5*(1+ham/den)[:,None]*response
    q=np.empty(0)
    for _ in range(len(air)+1):
        if not len(indices):break
        q=np.linalg.solve(op_response[np.ix_(indices,indices)],target-operative[indices])
        keep=q>=-1e-8 if heating else q<=1e-8
        if keep.all():break
        indices=indices[keep]
    if not len(indices):return air,mass,np.zeros(len(air))
    if cap is not None:q=np.clip(q,0,cap)
    delta=response[:,indices]@q;end_air=air+delta;end_mass=mass+ham/den*delta
    demand=np.zeros(len(air));demand[indices]=q
    return end_air,end_mass,demand


def window_radiation(climate,config,top=245,scenario='livre'):
    result=[];sun=local_sun(climate['alt'],climate['az'],top)
    for w in config['janelas']:
        cosi=incidence(climate['alt'],climate['az'],top+w['normal_relativa'])
        normal=np.maximum(-sun[:,w['eixo']],1e-8);thick=config['parede']['espessura_vano_m']
        reveal=np.maximum(0,1-abs(thick*sun[:,1-w['eixo']]/normal)/w['largura_m'])*np.maximum(0,1-abs(thick*sun[:,2]/normal)/w['altura_m'])
        visible=climate['alt']>obstruction(w,climate['az'],config,scenario)
        beam=climate['dni']*cosi*reveal*visible
        diffuse=.5*climate['dhi']+.1*climate['ghi']
        result.append((beam+diffuse)*w['largura_m']*w['altura_m']*config['vidro']['fracao_vidro'])
    return np.array(result).T  # W antes de SHGC


def ventilation_table(era,config,volume,out):
    vc=config['vento'];rows=[]
    areas=[sum(w['largura_m']*w['altura_m'] for w in config['janelas'] if w['eixo']==axis) for axis in (0,1)]
    for percentile in (10,50,90):
        speed=float(np.percentile(era['valtura'],percentile))
        for urban in vc['fatores_urbanos']:
            for direction in (135,315):
                for kind,fraction in [('correr',vc['abertura_correr']),('maximar_hipotese',vc['abertura_maximar'])]:
                    for opening in (1.,.5):
                        for path,area in [('portas_abertas',vc['passagem_aberta_m2']),('roupa_moveis',vc['passagem_obstaculos_m2']),('portas_fechadas',vc['passagem_fechada_m2'])]:
                            q,sign=cross_flow(speed*urban,direction,[a*fraction*opening for a in areas],config['azimute_topo_graus'],vc['cd'],area)
                            rows.append(dict(percentil=percentile,vento_altura_livre_m_s=round(speed,2),fator_urbano=urban,direcao_graus=direction,
                                             incidencia_SSE_graus=abs((direction-155+180)%360-180),tipo=kind,fracao_comando=opening,caminho=path,
                                             vazao_L_s=round(float(q)*1000,1),ACH_apartamento=round(float(q)*3600/volume,2),
                                             sentido='SSE_para_SW' if sign>0 else 'SW_para_SSE'))
    write_csv(out/'Ventilacao_cenarios.csv',rows)


def simulate(climate,g,config,out,external):
    """Sete zonas, dois nós por zona, integração implícita horária.

    Interzonas simétricas conservam calor. Ventilação cruzada distribuída por
    volume é aproximação de mistura com portas abertas, não rede CFD.
    """
    import estudo_fotometrico as photo
    rooms=list(g['floors']);nr=len(rooms);nc=len(climate['te']);tc=config['termico'];vc=config['vento']
    area=np.array([sum(c['area'] for c in photo.cells(g['floors'][r],0,1)) for r in rooms])
    volume=area*np.array([g['heights'][r] for r in rooms]);total_volume=volume.sum()
    # Fachadas expostas identificáveis; demais faces adiabáticas/vizinhos.
    sw_width={'quarto':2.45,'escritorio':2.30,'sala':2.45}
    sse_width={'quarto':2.95,'escritorio':1.00,'lavanderia':1.54,'banho':1.24}
    gross=np.array([[sw_width.get(r,0)*g['heights'][r],sse_width.get(r,0)*g['heights'][r]] for r in rooms])
    glass=np.zeros((nr,2));assignment=np.zeros((5,nr))
    for j,w in enumerate(config['janelas']):
        i=rooms.index(w['ambiente']);side=0 if w['eixo']==1 else 1
        glass[i,side]+=w['largura_m']*w['altura_m'];assignment[j,i]=1
    opaque=np.maximum(gross-glass,0);glazing=glass.sum(axis=1)*config['vidro']['fracao_vidro']
    # O caixilho opaco restante é agregado ao U equivalente da janela.
    glass_total=glass.sum(axis=1)
    write_csv(out/'Zonas_termicas.csv',[dict(ambiente=r,area_m2=round(float(area[i]),4),volume_m3=round(float(volume[i]),4),
              parede_SW_m2=round(float(opaque[i,0]),3),parede_SSE_m2=round(float(opaque[i,1]),3),janela_bruta_m2=round(float(glass_total[i]),3),
              comprimento_fachada_m=round(float(gross[i].sum()/g['heights'][r]),3),
              limite='envoltória nominal parcial; recessos/partes comuns a medir; vidro80% hipotético') for i,r in enumerate(rooms)])
    installed={r:0. for r in rooms}
    for row in read_csv(out.parent/'Iluminacao/Correntes_luz.csv'):
        if row['ambiente'] in installed:installed[row['ambiente']]+=float(row['W_entrada_cenario'])
    known={r:0. for r in rooms}
    for row in read_csv(out.parent/'Equipamentos/Climatizacao_parcelas.csv',','):
        if row['cenario']=='central_parcial':known[row['ambiente']]=float(row['equipamentos_referencia_H06_W'])
    sources=[]
    for i,r in enumerate(rooms):
        sources.append(dict(ambiente=r,luz_instalada_W=round(installed[r],2),pessoa_W=tc['ganho_pessoa_sensivel_W'],
                            aparelhos_referencia_H06_W=known[r],outros_aparelhos_hipotese_W=tc['ganhos_equipamentos_nao_conhecidos_W'][r],
                            fonte='climatizacao.py H02/H03/H06 + hipótese de uso; ausentes não viram zero medido'))
    write_csv(out/'Ganhos_internos.csv',sources)
    cases=['base','persiana_13_18','persiana_vent_noite','ventilador','sazonal_vedada','isolamento','ideal18','ideal20','AC_ideal26',
           'baixa_carga','alta_carga','az240','az250','torres','inverno_sombra','portatil1500_quarto',
           'blackout_claro','tecido_compacto','pelicula_refletiva','pelicula_tecido','persiana_blackout','vizinho22']
    ns=len(cases);p=config['parede'];wall=Wall(p['camadas'],p['rsi'],p['rse'])
    u=np.full(ns,wall.u);capacity=np.full(ns,tc['capacidade_massa_J_m2K']);shgc=np.full(ns,config['vidro']['shgc'])
    absorp=np.full(ns,p['absorcao_solar']);equipment_factor=np.ones(ns);urban=np.full(ns,vc['fator_urbano_central'])
    ach=np.full(ns,vc['infiltracao_ach'])
    for name,idx in [('baixa_carga',0),('alta_carga',1)]:
        k=cases.index(name);layers=[v[:] for v in p['camadas']];layers[1][1]=p['lambda_bloco_faixa'][idx]
        u[k]=Wall(layers,p['rsi'],p['rse']).u;shgc[k]=config['vidro']['shgc_faixa'][idx]
        absorp[k]=p['absorcao_faixa'][idx];equipment_factor[k]=tc['ganhos_equipamentos_faixa_fator'][idx]
        capacity[k]=tc['capacidade_massa_faixa'][1-idx];urban[k]=vc['fatores_urbanos'][0 if idx==0 else -1]
        ach[k]=vc['infiltracao_faixa_ach'][idx]
    ins=p['isolamento'];u[cases.index('isolamento')]=1/(1/wall.u+ins['espessura_m']/ins['lambda']+ins['gesso_m']/ins['gesso_lambda'])
    seasonal=('sazonal_vedada','isolamento','ideal18','ideal20','inverno_sombra','portatil1500_quarto')
    for name in seasonal:ach[cases.index(name)]=vc['infiltracao_vedada_ach']
    cm=capacity[:,None]*area;ca=np.broadcast_to(1200*volume,(ns,nr));ham=tc['h_ar_massa_W_m2K']*area
    hw=u[:,None]*opaque.sum(axis=1);base_hg=config['vidro']['u_W_m2K']*glass_total
    hpart=np.zeros(nr);hpart[rooms.index('circulacao')]=tc['hall_W_K']
    coupling=np.zeros((nr,nr))
    for a,b,h in [('quarto','circulacao',15),('escritorio','circulacao',15),('circulacao','sala',25),('sala','cozinha',40),('cozinha','lavanderia',20),('banho','circulacao',5)]:
        i,j=rooms.index(a),rooms.index(b);coupling[i,j]=coupling[j,i]=h
    # Coeficientes de transferência são hipóteses de porta aberta, não vazões.
    solar_windows=window_radiation(climate,config)
    angular={angle:window_radiation(climate,config,angle) for angle in (240,250)}
    tower_windows=window_radiation(climate,config,scenario='torres')
    plane=np.array([plane_irradiance(climate['alt'],climate['az'],normal,climate['ghi'],climate['dni'],climate['dhi']) for normal in (245,155)]).T
    openings=[sum(w['largura_m']*w['altura_m'] for w in config['janelas'] if w['eixo']==axis)*vc['abertura_correr'] for axis in (0,1)]
    qwind,flow_sign=cross_flow(climate['valtura'],climate['dir'],openings,245,vc['cd'],vc['passagem_aberta_m2'])
    top=np.empty((nc,ns,nr),np.float32);air=np.empty_like(top);mass=np.empty_like(top)
    heat=np.zeros_like(top);cool=np.zeros_like(top);removed=np.zeros((nc,ns),np.float32)
    solar_total=np.zeros((nc,ns),np.float32);solar_sw=np.zeros_like(solar_total)
    # Parcelas de calor no cenário base (sinal de ventilação/condução conservado).
    parts=np.zeros((nc,nr,6),np.float32)
    ta=np.full((ns,nr),float(climate['te'][0]));tm=ta.copy();max_energy_residual=0.
    for n in range(-336,nc):
        j=n%nc;te=float(climate['te'][j]);hour=float(climate['hour'][j]%24);month=int(climate['month'][j]);warm=month in (9,10,11,12,1,2,3)
        night=hour>=22 or hour<6
        occupancy=np.zeros(nr)
        if night:occupancy[rooms.index('quarto')]=tc['ocupacao_quarto_noite']
        elif 9<=hour<18:occupancy[rooms.index('escritorio')]=tc['ocupacao_escritorio_dia']
        elif 18<=hour<22:occupancy[rooms.index('sala')]=tc['ocupacao_sala_noite']
        lighting=np.array([installed[r]*(.5 if occupancy[i] else .1) if hour>=18 or hour<6 else 0 for i,r in enumerate(rooms)])
        eq=np.array([(tc['ganhos_equipamentos_nao_conhecidos_W'][r]+known[r])*(1 if occupancy[i] or r in ('cozinha','lavanderia') else .10) for i,r in enumerate(rooms)])
        internal=(lighting+tc['ganho_pessoa_sensivel_W']*occupancy)[None,:]+eq[None,:]*equipment_factor[:,None]
        factor=np.ones(ns);hg=np.tile(base_hg,(ns,1))
        if 13<=hour<18:
            for name in ('persiana_13_18','persiana_vent_noite','ventilador','AC_ideal26'):factor[cases.index(name)]=config['protecao']['persiana_fechada']['solar']
            if warm:
                for name in seasonal:factor[cases.index(name)]=config['protecao']['persiana_fechada']['solar']
            for name in ('blackout_claro','tecido_compacto','pelicula_refletiva','pelicula_tecido','persiana_blackout'):
                factor[cases.index(name)]=config['protecao'][name]['solar']
        if not warm and (hour>=18 or hour<7):
            for name in seasonal:
                k=cases.index(name);factor[k]=config['protecao']['persiana_fechada']['solar']
                hg[k]=glass_total/(1/config['vidro']['u_W_m2K']+config['vidro']['r_persiana_noturna_m2K_W'])
        qsolar=np.tile(solar_windows[j],(ns,1))
        qsolar[cases.index('az240')]=angular[240][j];qsolar[cases.index('az250')]=angular[250][j]
        qsolar[cases.index('torres')]=tower_windows[j]
        # Proteção altera só as três SW; banho/AS mantidos abertos no modelo óptico.
        qsolar[:,:3]*=factor[:,None];qsolar*=shgc[:,None]
        if not warm:qsolar[cases.index('inverno_sombra'),:3]=0
        qzone=qsolar@assignment
        extra_flow=np.zeros(ns)
        for name in ('persiana_vent_noite','ventilador')+seasonal:
            k=cases.index(name)
            if (hour>=20 or hour<7) and te<float(np.average(ta[k],weights=volume))-.5 and te>18:
                if name in ('persiana_vent_noite','ventilador') or warm:extra_flow[k]=qwind[j]*urban[k]
        hv=1200*(ach[:,None]*volume/3600+extra_flow[:,None]*volume/total_volume)
        if occupancy.any():
            k=cases.index('ventilador');internal[k]+=tc['ventilador_W']*(occupancy>0)
        # Sol-ar de cada face ponderada pela área opaca. Sem parede externa:
        # hw=0 e tsa=te é apenas valor neutro multiplicado por zero geométrico.
        irradiance=plane[j]@opaque.T/np.maximum(opaque.sum(axis=1),1e-8)
        tsa=te+absorp[:,None]*irradiance[None,:]*p['rse']
        den=cm/3600+ham+hw
        bm=cm/3600*tm+hw*tsa+.6*qzone+.4*internal
        neighbour_h=np.zeros((ns,nr));neighbour_h[cases.index('vizinho22')]=2*area*tc['vizinho_alternativo_W_m2K']
        diag=ca/3600+ham+hg+hv+hpart+neighbour_h+coupling.sum(axis=1)-ham**2/den
        matrix=np.tile(-coupling,(ns,1,1));ind=np.arange(nr);matrix[:,ind,ind]=diag
        b=ca/3600*ta+(hg+hv)*te+hpart*tc['hall_C']+neighbour_h*tc['vizinho_alternativo_C']+.4*qzone+.6*internal+ham*bm/den
        end_air=np.linalg.solve(matrix,b[...,None])[...,0]
        end_mass=(bm+ham*end_air)/den
        # Termostatos ideais por zona: solve linear response, repetido para
        # acoplamentos; demanda registrada não é potência de catálogo.
        heating=np.zeros((ns,nr));cooling=np.zeros((ns,nr))
        for name,target in [('ideal18',18.),('ideal20',20.),('AC_ideal26',26.),('portatil1500_quarto',20.)]:
            k=cases.index(name);op=(end_air[k]+end_mass[k])/2
            active=op>target if name=='AC_ideal26' else op<target
            if name=='portatil1500_quarto':
                bedroom=rooms.index('quarto');active&=np.arange(nr)==bedroom
                active&=night or hour<8
            if active.any():
                end_air[k],end_mass[k],q=thermostat_response(matrix[k],den[k],ham,end_air[k],end_mass[k],target,active,
                    heating=name!='AC_ideal26',cap=1500 if name=='portatil1500_quarto' else None)
                heating[k]=np.maximum(q,0);cooling[k]=np.maximum(-q,0)
        storage=(ca*(end_air-ta)+cm*(end_mass-tm))/3600
        flux=(hg+hv)*(te-end_air)+hw*(tsa-end_mass)+qzone+internal+hpart*(tc['hall_C']-end_air)
        flux+=neighbour_h*(tc['vizinho_alternativo_C']-end_air)+heating-cooling
        residual=float(np.max(abs(np.sum(storage-flux,axis=1))))
        max_energy_residual=max(max_energy_residual,residual)
        if residual>1e-6:raise ValueError('RC não conserva energia: '+str(residual)+' W')
        if n>=0:
            top[n]=(end_air+end_mass)/2;air[n]=end_air;mass[n]=end_mass;heat[n]=heating;cool[n]=cooling
            removed[n]=1200*extra_flow*np.maximum(0,np.average(end_air,axis=1,weights=volume)-te)
            solar_total[n]=qsolar.sum(axis=1);solar_sw[n]=qsolar[:,:3].sum(axis=1)
            parts[n,:,0]=qzone[0];parts[n,:,1]=hw[0]*(tsa[0]-end_mass[0]);parts[n,:,2]=hg[0]*(te-end_air[0])
            parts[n,:,3]=hv[0]*(te-end_air[0]);parts[n,:,4]=tc['ganho_pessoa_sensivel_W']*occupancy+lighting
            parts[n,:,5]=eq
        ta,tm=end_air,end_mass
    # Média externa móvel de sete dias ANTERIORES; primeiros sete dias sem
    # histórico ficam fora da contagem adaptativa, não preenchidos com zero.
    daily=climate['te'].reshape(-1,24).mean(axis=1);prev=np.full(len(daily),np.nan)
    for d in range(7,len(daily)):prev[d]=daily[d-7:d].mean()
    limit=adaptive_limit(np.repeat(prev,24));rows=[];ventrows=[]
    for m in range(1,13):
        mask=climate['month']==m;years=climate['years'];night=(climate['hour']%24>=22)|(climate['hour']%24<6)
        for k,name in enumerate(cases):
            for i,r in enumerate(rooms):
                values=top[mask,k,i];row=dict(clima=climate['name'],cenario=name,mes=m,ambiente=r,
                  Top_media_C=round(float(values.mean()),2),Top_min_C=round(float(values.min()),2),Top_max_C=round(float(values.max()),2),
                  Top_noite_media_C=round(float(top[mask&night,k,i].mean()),2),
                  h_ano_abaixo18=round(float((values<18).sum()/years),1),h_ano_abaixo20=round(float((values<20).sum()/years),1),
                  h_ano_acima26=round(float((values>26).sum()/years),1),h_ano_acima28=round(float((values>28).sum()/years),1),
                  h_ano_acima30=round(float((values>30).sum()/years),1),h_ano_acima32=round(float((values>32).sum()/years),1),
                  h_ano_acima_adapt_hipotese=round(float((values>limit[mask]).sum()/years),1),
                  h_validas_adapt_ano=round(float(np.isfinite(limit[mask]).sum()/years),1),
                  aquecimento_util_kWh_ano=round(float(heat[mask,k,i].sum()/1000/years),2),
                  resfriamento_sensivel_kWh_ano=round(float(cool[mask,k,i].sum()/1000/years),2))
                room_occupied=((climate['hour']%24>=22)|(climate['hour']%24<6)) if r=='quarto' else ((climate['hour']%24>=9)&(climate['hour']%24<18)) if r=='escritorio' else ((climate['hour']%24>=18)&(climate['hour']%24<22)) if r=='sala' else np.zeros(nc,bool)
                perceived=top[mask,k,i]-np.where(room_occupied[mask]&(top[mask,k,i]>=25),tc['ventilador_efeito_C'] if name=='ventilador' else 0,0)
                row['h_adapt_com_alivio_hipotese']=round(float((perceived>limit[mask]).sum()/years),1)
                row['h_ocupadas_acima_adapt']=round(float(((values>limit[mask])&room_occupied[mask]).sum()/years),1)
                row['h_ocupadas_acima_adapt_com_alivio']=round(float(((perceived>limit[mask])&room_occupied[mask]).sum()/years),1)
                rows.append(row)
            ix=mask&(extra_mask(climate['hour']))
            # kWh são calor extraído, não consumo elétrico de abrir a janela.
            ventrows.append(dict(clima=climate['name'],mes=m,cenario=name,
                h_noite_remocao_ano=round(float((removed[mask,k]>1).sum()/years),1),
                calor_removido_noite_kWh_ano=round(float(removed[mask,k].sum()/1000/years),2),
                massa_inicio_noite_C=round(float(np.average(mass[mask&(climate['hour']%24==20),k],axis=1,weights=area).mean()),2),
                massa_fim_noite_C=round(float(np.average(mass[mask&(climate['hour']%24==6),k],axis=1,weights=area).mean()),2)))
    write_csv(out/('Conforto_'+climate['name']+'.csv'),rows)
    write_csv(out/('Remocao_noite_'+climate['name']+'.csv'),ventrows)
    potential=[]
    indoor=np.average(top[:,cases.index('base')],axis=1,weights=volume)
    for m in range(1,13):
        mask=climate['month']==m
        for urban_factor in vc['fatores_urbanos']:
            q=qwind*urban_factor
            cooling=q*1200*(indoor-climate['te'])
            potential.append(dict(clima=climate['name'],mes=m,fator_urbano=urban_factor,
                ACH_p10=round(float(np.percentile(q[mask]*3600/total_volume,10)),2),
                ACH_p50=round(float(np.percentile(q[mask]*3600/total_volume,50)),2),
                ACH_p90=round(float(np.percentile(q[mask]*3600/total_volume,90)),2),
                h_ano_potencial_remove_calor=round(float((cooling[mask]>10).sum()/climate['years']),1),
                h_ano_potencial_adiciona_calor=round(float((cooling[mask]<-10).sum()/climate['years']),1),
                h_ano_SSE_entrada=round(float((flow_sign[mask]>0).sum()/climate['years']),1),
                limite='Vento e Tar de base fechado; potencial inicial, não hora de conforto garantida depois de abrir'))
    write_csv(out/('Ventilacao_potencial_'+climate['name']+'.csv'),potential)
    partrows=[]
    for m in range(1,13):
        mask=climate['month']==m
        for i,r in enumerate(rooms):
            vals=parts[mask,i];partrows.append(dict(clima=climate['name'],mes=m,ambiente=r,solar_media_W=round(float(vals[:,0].mean()),1),
               parede_sol_ar_media_W=round(float(vals[:,1].mean()),1),vidro_conducao_media_W=round(float(vals[:,2].mean()),1),
               infiltracao_media_W=round(float(vals[:,3].mean()),1),pessoas_luz_media_W=round(float(vals[:,4].mean()),1),
               aparelhos_hipotese_media_W=round(float(vals[:,5].mean()),1),solar_pico_W=round(float(vals[:,0].max()),1)))
    write_csv(out/('Parcelas_'+climate['name']+'.csv'),partrows)
    dump(out/('Conservacao_'+climate['name']+'.json'),dict(residuo_maximo_W=max_energy_residual,
           limite_W=1e-6,horas=nc,cenarios=len(cases),natureza='balanço numérico; não valida calibração física'))
    np.savez_compressed(external/('Termico_'+climate['name']+'.npz'),Top=top,Tar=air,Tmassa=mass,
                        aquecimento_W=heat,resfriamento_W=cool,ambientes=rooms,cenarios=cases,
                        tempo=[t.isoformat() for t in climate['time']],solar_total_W=solar_total,solar_SW_W=solar_sw)
    # CSV largo: todas as temperaturas operativas, um cenário por linha.
    with gzip.open(external/('Temperaturas_'+climate['name']+'.csv.gz'),'wt',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,delimiter=';');writer.writerow(['data_UTC_menos3','cenario']+['Top_'+r+'_C' for r in rooms])
        for j,t in enumerate(climate['time']):
            for k,name in enumerate(cases):writer.writerow([t.isoformat(),name]+np.round(top[j,k],2).tolist())
    return dict(rooms=rooms,cases=cases,area=area,volume=volume,opaque=opaque,glass=glass_total,wall=wall,monthly=rows,
                exterior_length=gross.sum(axis=1)/np.array([g['heights'][r] for r in rooms]),
                solar_total=solar_total,solar_sw=solar_sw,top=top,heat=heat,cool=cool)


def extra_mask(hours):return (hours%24>=20)|(hours%24<7)


def heating_options(result,config,out):
    tc=config['termico'];rows=[];design=[];ins=config['parede']['isolamento'];wall=result['wall']
    for i,r in enumerate(result['rooms']):
        for te in (5.,10.):
            for ti in (18.,20.):
                for ach in config['vento']['infiltracao_faixa_ach']:
                    ua_wall=wall.u*result['opaque'][i].sum();ua_glass=config['vidro']['u_W_m2K']*result['glass'][i]
                    ua_air=1200*result['volume'][i]*ach/3600
                    loss=(ua_wall+ua_glass+ua_air)*(ti-te)
                    insulated_u=1/(1/wall.u+ins['espessura_m']/ins['lambda']+ins['gesso_m']/ins['gesso_lambda'])
                    design.append(dict(ambiente=r,Te_C=te,Ti_C=ti,ACH=ach,UA_parede_W_K=round(float(ua_wall),2),UA_janela_W_K=round(float(ua_glass),2),UA_ar_W_K=round(float(ua_air),2),
                        aquecimento_sem_ganhos_W=round(float(loss),1),economia_isolamento_W=round(float((wall.u-insulated_u)*result['opaque'][i].sum()*(ti-te)),1),
                        perda_area_isolamento_m2=round(float(result['exterior_length'][i]*(ins['espessura_m']+ins['gesso_m'])),3),
                        hall_vizinhos='adiabáticos no cálculo de perda; hall/ganhos excluídos deste ensaio de madrugada'))
        for target in (18,20):
            k=result['cases'].index('ideal'+str(target));energy=float(result['heat'][:,k,i].sum()/1000/10);hours=float((result['heat'][:,k,i]>.1).sum()/10)
            for name,power,cop,cost in [('portatil_resistivo',1500.,1.,'R$200–800 hipótese sem cotação'),('split_quente_frio_condicional',780.,tc['cop_aquecimento'],'R$3000–7000 por zona instalado, hipótese'),('piso_radiante_condicional',70*result['area'][i],1.,'R$250–600/m² hipótese; base/controle adicionais')]:
                if name=='piso_radiante_condicional' and r in ('banho','lavanderia'):continue
                electric=energy/cop
                rows.append(dict(ambiente=r,opcao=name,setpoint_C=target,potencia_eletrica_referencia_W=round(float(power),1),
                     corrente_equivalente_127V_A='' if name.startswith('split') else round(float(power/127),2),h_demanda_ano=round(hours,1),h_equivalentes_plena_potencia_ano=round(electric*1000/power,1),
                     energia_util_kWh_ano=round(energy,1),energia_eletrica_kWh_ano=round(electric,1),
                     custo_energia_base_R_ano=round(electric*tc['tarifa_base_R_kWh'],2),custo_cenario_total_R_ano=round(electric*tc['tarifa_total_hipotese_R_kWh'],2),
                     investimento_hipotese=cost,
                     limite='Termostato ideal; capacidade real não verificada. COP3 hipótese; 780W referência anterior de split frio não confirma modelo quente/frio. Piso100W/m² em70% da área hipotético, <=27°C no sistema/base, SKU/RT pendentes; referência127V não define tensão de split.'))
    write_csv(out/'Aquecimento_madrugada.csv',design);write_csv(out/'Aquecimento_opcoes.csv',rows)
