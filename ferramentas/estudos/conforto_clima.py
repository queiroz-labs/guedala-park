"""Leitura estrita dos dois climas e resumos; séries brutas ficam fora do Git."""
import csv
import hashlib
import json
from datetime import datetime,timedelta
from pathlib import Path
import numpy as np
from conforto_fisica import solar,required


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(path,delimiter=';'):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=delimiter))


def write_csv(path,rows):
    rows=list(rows)
    if not rows:raise ValueError('Saída vazia: '+str(path))
    with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)


def dump(path,data):Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def erbs(ghi,alt,doy):
    """Erbs1982, partição horária GHI; incerteza extra do ERA5 sem DNI/DHI.

    A fonte fornece GHI médio da hora anterior. Avaliar a geometria no meio
    desse intervalo evita deslocar sol para a hora seguinte.
    """
    cosz=np.maximum(np.sin(np.radians(alt)),.065)
    extra=1367*(1+.033*np.cos(2*np.pi*np.asarray(doy)/365))
    kt=np.clip(np.asarray(ghi)/(extra*cosz),0,1)
    frac=np.where(kt<=.22,1-.09*kt,np.where(kt<=.8,.9511-.1604*kt+4.388*kt**2-16.638*kt**3+12.336*kt**4,.165))
    dhi=np.asarray(ghi)*frac
    dni=np.maximum(0,(np.asarray(ghi)-dhi)/cosz)
    # Energia GHI residual perto do horizonte permanece toda difusa.
    dhi=np.where(np.asarray(alt)<=0,ghi,dhi);dni=np.where(np.asarray(alt)<=0,0,dni)
    return dni,dhi


def load_era(path,config):
    if sha(path)!=required(config['clima'],'era5_sha256'):raise ValueError('SHA do ERA5 divergente')
    obj=json.loads(Path(path).read_text(encoding='utf-8'));h=required(obj,'hourly')
    units=required(obj,'hourly_units')
    if units['wind_speed_10m']!='m/s' or obj['utc_offset_seconds']!=-10800:raise ValueError('Unidade/fuso ERA5 inesperados')
    names={'te':'temperature_2m','rh':'relative_humidity_2m','td':'dew_point_2m','v10':'wind_speed_10m',
           'v100':'wind_speed_100m','dir':'wind_direction_10m','dir100':'wind_direction_100m','ghi':'shortwave_radiation'}
    data={k:np.array(required(h,v),float) for k,v in names.items()}
    times=[datetime.fromisoformat(t) for t in h['time']]
    if len(times)!=87672 or times[0]!=datetime(2015,1,1) or times[-1]!=datetime(2024,12,31,23):raise ValueError('Período ERA5 incompleto')
    if any(b-a!=timedelta(hours=1) for a,b in zip(times,times[1:])):raise ValueError('Lacuna ou hora duplicada')
    data.update(time=times,month=np.array([d.month for d in times]),hour=np.array([d.hour for d in times],float),
                doy=np.array([d.timetuple().tm_yday for d in times]),years=10,name='ERA5')
    for key,value in data.items():
        if isinstance(value,np.ndarray) and (len(value)!=len(times) or not np.isfinite(value).all()):raise ValueError('Ausência em '+key)
    return complete(data,config)


def load_epw(path,config):
    if sha(path)!=required(config['clima'],'epw_sha256'):raise ValueError('SHA do EPW divergente')
    lines=Path(path).read_text(encoding='utf-8-sig').splitlines()
    header=next(csv.reader([lines[0]]))
    if header[0]!='LOCATION' or header[5]!='837800':raise ValueError('Estação EPW inesperada')
    rows=[r for r in csv.reader(lines[8:]) if r]
    if len(rows)!=8760:raise ValueError('EPW incompleto')
    data={k:np.array([float(r[i]) for r in rows]) for k,i in [('te',6),('td',7),('rh',8),('ghi',13),('dni',14),('dhi',15),('dir',20),('v10',21)]}
    if (any(not np.isfinite(v).all() for v in data.values()) or max(data['te'])>=99 or max(data['td'])>=99
        or max(data['rh'])>100 or max(data['ghi'])>=9999 or max(data['dni'])>=9999 or max(data['dhi'])>=9999
        or max(data['v10'])>=999 or max(data['dir'])>360):raise ValueError('Dado EPW ausente')
    times=[datetime(2026,int(r[1]),int(r[2]))+timedelta(hours=int(r[3])) for r in rows]
    mid=[t-timedelta(minutes=30) for t in times]
    data.update(time=times,month=np.array([int(r[1]) for r in rows]),hour=np.array([int(r[3]) for r in rows],float),
                doy=np.array([t.timetuple().tm_yday for t in mid]),years=1,name='TMYx')
    data['v100']=data['v10']*10**.2;data['dir100']=data['dir'].copy()  # EPW não tem 100m; hipótese separada.
    return complete(data,config)


def complete(data,config):
    # ERA5 etiqueta é fim da hora de radiação; EPW hour=1..24 igualmente.
    alt,az=solar(data['doy'],data['hour']-.5,config['latitude'],config['longitude'],config['fuso_h'])
    data.update(alt=alt,az=az)
    if 'dni' not in data:data['dni'],data['dhi']=erbs(data['ghi'],alt,data['doy'])
    v10,v100=data['v10'],data['v100'];valid=(v10>.1)&(v100>.1)
    alpha=np.full(len(v10),.2);alpha[valid]=np.log(v100[valid]/v10[valid])/np.log(10)
    data['alpha']=alpha
    data['valtura']=v10*(config['altura_piso_m']/10)**alpha
    if np.any((data['rh']<0)|(data['rh']>100)) or np.any(data['ghi']<0):raise ValueError('Clima fora do domínio')
    return data


def climate_tables(era,epw,out):
    rows=[]
    for climate in (era,epw):
        for m in range(1,13):
            ix=climate['month']==m;t=climate['te'][ix];ys=climate['years']
            days=t.reshape(-1,24)
            row=dict(clima=climate['name'],mes=m,horas=int(ix.sum()),Tmedia_C=round(float(t.mean()),2),
                     minima_media_diaria_C=round(float(days.min(axis=1).mean()),2),maxima_media_diaria_C=round(float(days.max(axis=1).mean()),2),
                     Tmin_C=round(float(t.min()),2),Tmax_C=round(float(t.max()),2),orvalho_medio_C=round(float(climate['td'][ix].mean()),2),
                     vento10_medio_m_s=round(float(climate['v10'][ix].mean()),2),vento100_medio_m_s=round(float(climate['v100'][ix].mean()),2),
                     alfa_mediano=round(float(np.median(climate['alpha'][ix])),3))
            for limit in (16,18,20):row['h_ano_abaixo_'+str(limit)]=round(float((t<limit).sum()/ys),1)
            for limit in (26,28,30,32):row['h_ano_acima_'+str(limit)]=round(float((t>limit).sum()/ys),1)
            row['dias_ano_Tmax_ge30']=round(float((days.max(axis=1)>=30).sum()/ys),1)
            rows.append(row)
    write_csv(out/'Clima_mensal.csv',rows)
    rows=[]
    for name,mask in [('ano',np.ones(len(era['te']),bool)),('verao_13_19',np.isin(era['month'],[12,1,2,3])&(era['hour']>=13)&(era['hour']<=19))]:
        sectors=((era['dir'][mask]+22.5)//45).astype(int)%8
        for i,label in enumerate(('N','NE','L','SE','S','SO','O','NO')):
            hit=sectors==i
            rows.append(dict(periodo=name,setor=label,azimute_central=i*45,frequencia_pct=round(float(hit.mean()*100),2),
                             velocidade10_media_m_s=round(float(era['v10'][mask][hit].mean()),2)))
    write_csv(out/'Vento_setores.csv',rows)
    rows=[]
    for m in range(1,13):
        for h in range(24):
            ix=(era['month']==m)&(era['hour']==h)
            rows.append(dict(mes=m,hora_UTC_menos3=h,Tmedia_C=round(float(era['te'][ix].mean()),2),T_p90_C=round(float(np.percentile(era['te'][ix],90)),2),
                             UR_media_pct=round(float(era['rh'][ix].mean()),1),vento10_m_s=round(float(era['v10'][ix].mean()),2)))
    write_csv(out/'Clima_diurno.csv',rows)
    t=era['te'];days=t.reshape(-1,24);cold=t<16
    summary=dict(horas=len(t),anos=10,min_C=float(t.min()),min_em=era['time'][int(t.argmin())].isoformat(),
                 max_C=float(t.max()),max_em=era['time'][int(t.argmax())].isoformat(),
                 horas_ano_menor16=float((t<16).sum()/10),horas_ano_menor18=float((t<18).sum()/10),
                 horas_ano_18a26=float(((t>=18)&(t<=26)).sum()/10),
                 pct_frio16_entre0e12=float((cold&(era['hour']<12)).sum()/cold.sum()*100),
                 dias30_por_ano=[int((days[np.array([dt.year for dt in era['time'][::24]])==year].max(axis=1)>=30).sum()) for year in range(2015,2025)],
                 vento10_percentis=[float(v) for v in np.percentile(era['v10'],[10,50,90])],
                 vento_altura_percentis=[float(v) for v in np.percentile(era['valtura'],[10,50,90])],
                 alfa_mediano=float(np.median(era['alpha'])),
                 limite='ERA5 reanálise regional; TMYx estação/ano sintético; não temperatura dentro do apartamento')
    dump(out/'Clima_resumo.json',summary)
    return summary
