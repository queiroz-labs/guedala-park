"""Raios e janelas nominais R54; usa exportações validadas, não abre FreeCAD."""
import math
import numpy as np
from conforto_fisica import local_sun


def windows(config):
    return config['janelas']


def aperture(w,nu=10,nv=8):
    axis=w['eixo'];tangent=1-axis
    points=np.zeros((nu*nv,3));points[:,axis]=w['plano_m']
    points[:,tangent]=np.repeat(w['inicio_m']+(np.arange(nu)+.5)*w['largura_m']/nu,nv)
    points[:,2]=np.tile(w['peitoril_m']+(np.arange(nv)+.5)*w['altura_m']/nv,nu)
    return points


def reveal(points,direction,w,thickness):
    direction=np.broadcast_to(direction,np.shape(points))
    component=-direction[:,w['eixo']]
    outward=component>1e-8
    t=thickness/np.maximum(component,1e-8)
    outer=points+direction*t[:,None]
    other=1-w['eixo']
    return (outward&(outer[:,other]>=w['inicio_m'])&(outer[:,other]<=w['inicio_m']+w['largura_m'])
            &(outer[:,2]>=w['peitoril_m'])&(outer[:,2]<=w['peitoril_m']+w['altura_m']))


def trace_boxes(origins,directions,solids,max_distance=np.inf):
    """Primeiro AABB opaco; tangências não são volumes. Array de raios."""
    origins=np.broadcast_to(origins,directions.shape)
    count=len(directions);distance=np.broadcast_to(max_distance,(count,)).copy()
    hit=np.full(count,-1,int);face=np.full(count,-1,int)
    for i,(box,*_) in enumerate(solids):
        b=np.array(box);safe=np.where(abs(directions)>1e-12,directions,1e-30)
        near=(b[:3]-origins)/safe;far=(b[3:]-origins)/safe
        lower=np.minimum(near,far);upper=np.maximum(near,far)
        parallel=abs(directions)<1e-12
        inside=(origins>b[:3]+1e-9)&(origins<b[3:]-1e-9)
        lower=np.where(parallel,np.where(inside,-np.inf,np.inf),lower)
        upper=np.where(parallel,np.where(inside,np.inf,-np.inf),upper)
        lo=lower.max(axis=1);hi=upper.min(axis=1)
        valid=(hi>np.maximum(lo,1e-6))&(lo>1e-6)&(lo<distance-1e-6)
        distance[valid]=lo[valid];hit[valid]=i;face[valid]=np.argmax(lower[valid],axis=1)
    return distance,hit,face


def directions_az(directions,top):
    dx,dy= directions[:,0],directions[:,1]
    east=dx*np.sin(np.radians(top+90))+dy*np.sin(np.radians(top+180))
    north=dx*np.cos(np.radians(top+90))+dy*np.cos(np.radians(top+180))
    return np.degrees(np.arctan2(east,north))%360


def tower_horizon(w,az,config,scale_factor=1.):
    """Interseção de raio horizontal com polígonos digitalizados da situação.

    SEM ESCALA: largura gráfica de uma unidade / 7,4 m nominais; ±30%.
    A origem de cada janela se desloca dentro da unidade 06.
    """
    layout=config['situacao'];scale=layout['m_por_pixel']*scale_factor
    origin=np.array(layout['origem_unidade_pixel'])*scale
    # Dimensões CAD correspondem à projeção horizontal da unidade ampliada.
    center=aperture(w,1,1)[0,:2];origin+=center
    d=local_sun(np.zeros_like(az),az,config['azimute_topo_graus'])[...,:2]
    scalar=np.ndim(az)==0;d=np.atleast_2d(d);result=np.zeros(len(d))
    for tower in layout['torres']:
        points=np.array(tower['poligono_pixel'])*scale
        nearest=np.full(len(d),np.inf)
        for p,q in zip(points,np.roll(points,-1,axis=0)):
            edge=q-p;delta=p-origin
            cross=d[:,0]*edge[1]-d[:,1]*edge[0]
            valid=abs(cross)>1e-8;safe=np.where(valid,cross,1.)
            t=(delta[0]*edge[1]-delta[1]*edge[0])/safe
            u=(delta[0]*d[:,1]-delta[1]*d[:,0])/safe
            ix=valid&(t>0)&(u>=0)&(u<=1)
            nearest[ix]=np.minimum(nearest[ix],t[ix])
        delta_h=tower['altura_m']-config['altura_piso_m']-w['peitoril_m']-w['altura_m']/2
        angle=np.degrees(np.arctan2(max(0,delta_h),nearest))
        result=np.maximum(result,angle)
    return float(result[0]) if scalar else result


def obstruction(w,az,config,scenario):
    az=np.asarray(az);h=np.zeros_like(az,dtype=float)
    if scenario=='livre':return h
    if scenario in ('hospital10','hospital20'):
        height=10 if scenario=='hospital10' else 20
        delta=abs((az-249+180)%360-180)
        return np.where(delta<=10,height,0.)
    if scenario=='torres':return tower_horizon(w,az,config)
    if scenario=='torre155':
        return np.where(abs((az-155+180)%360-180)<=20,40.,0.)
    if scenario=='combinado':return np.maximum(obstruction(w,az,config,'hospital20'),tower_horizon(w,az,config))
    raise ValueError('Obstrução desconhecida: '+scenario)


def patch(w,alt,az,solids,floors,config,top=None,nu=16,nv=12):
    """Quadratura da abertura, primeiro impacto 3D; áreas estimadas por feixe.

    Cada raio carrega Ajanela/N × cos(i). Área na face = fluxo/cos(face).
    Não confundir profundidade não recortada com área real no piso.
    """
    top=config['azimute_topo_graus'] if top is None else top
    sun=local_sun(alt,az,top);cosine=-sun[w['eixo']]
    empty=dict(piso_m2=0.,parede_m2=0.,moveis_m2=0.,profundidade_m=0.,
               profundidade_sem_recorte_m=0.,atingidos='',pontos_piso=[])
    if alt<=0 or cosine<=1e-6:return empty
    pts=aperture(w,nu,nv);allowed=reveal(pts,sun,w,config['parede']['espessura_vano_m'])
    pts=pts[allowed]
    if not len(pts):return empty
    dr=np.broadcast_to(-sun,pts.shape);start=pts+dr*1e-5
    dist,hit,face=trace_boxes(start,dr,solids)
    floor_dist=-start[:,2]/dr[:,2]
    floor_points=start+dr*floor_dist[:,None]
    on_floor=np.zeros(len(pts),bool)
    for rects in floors.values():
        for r in rects:on_floor|=((floor_points[:,0]>=r[0])&(floor_points[:,0]<=r[2])&(floor_points[:,1]>=r[1])&(floor_points[:,1]<=r[3]))
    floor_hit=on_floor&(floor_dist<dist)
    dist[floor_hit]=floor_dist[floor_hit];face[floor_hit]=2;hit[floor_hit]=-2
    flux=w['largura_m']*w['altura_m']/nu/nv*cosine
    area=np.zeros(len(pts));valid=np.isfinite(dist)&(face>=0)
    area[valid]=flux/np.maximum(abs(sun[face[valid]]),1e-9)
    walls=np.array([False if i<0 else solids[i][1].startswith('parede') for i in hit])
    furniture=(hit>=0)&~walls
    end=start+dr*np.where(np.isfinite(dist),dist,0)[:,None]
    names=sorted({solids[i][1] for i in hit[furniture]})
    return dict(piso_m2=float(area[floor_hit].sum()),parede_m2=float(area[walls].sum()),
                moveis_m2=float(area[furniture].sum()),
                profundidade_m=float(np.max(abs(end[valid,w['eixo']]-w['plano_m']))) if valid.any() else 0.,
                profundidade_sem_recorte_m=float(w['peitoril_m']+w['altura_m'])*cosine/sun[2],
                atingidos='|'.join(names),pontos_piso=floor_points[floor_hit].tolist())


def sky_component(points,ws,solids,config,external_lux=10000,scenario='livre',nu=8,nv=8):
    """Componente do céu: quadratura de luminância CIE encoberto pela janela.

    L(altura)=Lz(1+2sin altura)/3, Ehorizontal=7πLz/9.
    Oclusão por AABBs, peitoril, vãos/revelos e horizonte angular.
    """
    points=np.asarray(points);out=np.zeros(len(points));top=config['azimute_topo_graus']
    lz=external_lux*9/(7*np.pi)
    for w in ws:
        aps=aperture(w,nu,nv);n=len(aps)
        origin=np.repeat(points,n,axis=0);target=np.tile(aps,(len(points),1))
        vec=target-origin;distance=np.linalg.norm(vec,axis=1)
        direction=vec/np.maximum(distance[:,None],1e-9)
        cosw=-direction[:,w['eixo']];up=direction[:,2]
        valid=(cosw>0)&(up>0)&reveal(target,direction,w,config['parede']['espessura_vano_m'])
        az=directions_az(direction,top);alt=np.degrees(np.arcsin(np.clip(up,-1,1)))
        valid&=alt>obstruction(w,az,config,scenario)
        _,hit,_=trace_boxes(origin,direction,solids,distance-1e-5)
        valid&=hit<0
        lumi=lz*(1+2*np.maximum(up,0))/3
        e=np.where(valid,lumi*up*cosw/(distance**2+1e-20)*w['largura_m']*w['altura_m']/n,0)
        out+=e.reshape(len(points),n).sum(axis=1)*w.get('tau_vis',config['vidro']['tau_vis'])*config['vidro']['fracao_vidro']
    return out


def internal_reflection(flux,rho,total_surface):
    """Cavidade difusa uniforme: fluxo refletido / área / (1−ρ)."""
    if not 0<=rho<1 or total_surface<=0:raise ValueError('Reflexão inválida')
    return flux*rho/(total_surface*(1-rho))


def daylight_grid(g,config,furniture=True,ceiling=False,curtain=1.,rho_wall=None,step=.5,receiver_solids=None):
    import estudo_fotometrico as photo
    solids=photo.room_solids(g) if furniture else [(b,'parede',(.5,.6,.7)) for b in g['walls']]
    if ceiling:
        for name in ('P02','P03','P04','P09','P10','P11','P12','P15','P19'):
            b=g['modules'][name]
            if b[5]<2.6:solids.append(([b[0],b[1],b[5],b[3],b[4],2.6],name+'_fechamento_hipotese',(.5,.6,.7)))
    rho_wall=config['luz']['rho_parede'] if rho_wall is None else rho_wall
    rows=[];data={}
    for room,rects in g['floors'].items():
        # Mesmos receptores em todos os cenários: remover móveis não pode
        # aparentar piora apenas por incluir novas células antes ocupadas.
        receiver_solids=photo.room_solids(g) if receiver_solids is None else receiver_solids
        grid=photo.clean_grid(rects,.75,step,[b for b,*_ in receiver_solids])
        if not grid:raise ValueError('Grade vazia: '+room)
        points=np.array([c['point'] for c in grid]);area=np.array([c['area'] for c in grid])
        sc=sky_component(points,windows(config),solids,config,config['luz']['externa_lux'])
        floor_area=sum(c['area'] for c in photo.cells(rects,0,1))
        perimeter=4*math.sqrt(floor_area)  # aproximação declarada; geometria irregular.
        surface=2*floor_area+perimeter*g['heights'][room]
        rho=(rho_wall*perimeter*g['heights'][room]+(config['luz']['rho_piso']+config['luz']['rho_teto'])*floor_area)/surface
        # Fechamento de energia split-flux: fluxo disponível estimado pela média
        # SC no plano, não por uma janela inventada na cozinha sem abertura.
        incident_flux=float(np.average(sc,weights=area))*floor_area
        irc=internal_reflection(incident_flux,rho,surface)
        natural=(sc+irc)*curtain
        data[room]=dict(points=points,areas=area,sc=sc*curtain,irc=irc*curtain,lux=natural,solids=solids)
        rows.append(dict(ambiente=room,pontos=len(grid),area_livre_m2=round(float(area.sum()),3),
                         DF_media_pct=round(float(np.average(natural,weights=area))/config['luz']['externa_lux']*100,3),
                         DF_min_pct=round(float(natural.min())/config['luz']['externa_lux']*100,3),
                         lux_medio=round(float(np.average(natural,weights=area)),1),lux_min=round(float(natural.min()),1),
                         IRC_lux=round(float(irc*curtain),1)))
    return rows,data


def sun_at_points(points,ws,solids,config,alt,az,dni_lux):
    """Lux direto horizontal; sem modelo de BRDF, DGP ou UGR solar."""
    points=np.asarray(points);sun=local_sun(alt,az,config['azimute_topo_graus'])
    result=np.zeros(len(points))
    if alt<=0:return result
    direction=np.broadcast_to(sun,points.shape)
    for w in ws:
        axis=w['eixo'];other=1-axis
        if sun[axis]>=-1e-8:continue
        dist=(w['plano_m']-points[:,axis])/sun[axis]
        target=points+dist[:,None]*sun
        valid=(dist>0)&(target[:,other]>=w['inicio_m'])&(target[:,other]<=w['inicio_m']+w['largura_m'])&(target[:,2]>=w['peitoril_m'])&(target[:,2]<=w['peitoril_m']+w['altura_m'])
        valid&=reveal(target,direction,w,config['parede']['espessura_vano_m'])
        _,hit,_=trace_boxes(points,direction,solids,np.maximum(0,dist)-1e-5)
        valid&=hit<0
        result+=valid*dni_lux*sun[2]*w.get('tau_vis',config['vidro']['tau_vis'])*config['vidro']['fracao_vidro']
    return result
