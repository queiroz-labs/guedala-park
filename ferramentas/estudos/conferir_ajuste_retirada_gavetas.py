"""Triagem continua de envelopes para ajuste/retirada, sem abrir CAD."""
from pathlib import Path
import gzip,hashlib,json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Inventario_dimensional/Gavetas'
def overlap(a,b): return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
def move(b,axis,d):
    c=b[:];c[axis]+=d;c[axis+3]+=d;return c
def swept(b,travel,zmax):
    c=b[:];c[1]-=travel;c[5]+=zmax;return c

def main():
    bp=ROOT/'02_Modelo_3D/Base_verificacao.json.gz';base=json.loads(gzip.decompress(bp.read_bytes()));objects=base['objetos']
    rel=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    proposal=json.loads((OUT/'Proposta_FGVTN_500.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/rel['cadPath']).read_bytes()).hexdigest()==base['sha256']==proposal['cad_sha256']
    audit=json.loads((OUT/'Conferencia_P01_P06.json').read_text(encoding='utf-8'))
    def ancestors(n):
        result=[]
        while n in objects and n not in result:
            result.append(n);n=objects[n].get('pai')
        return result
    parts={n:o for n,o in objects.items() if o.get('forma',{}).get('solidos',0)>0 and o.get('tipo','').startswith(('Part::','PartDesign::')) and all(objects[a].get('visivel',True) for a in ancestors(n))}
    excluded=[n for n,o in parts.items() if any(a.startswith(('GuiasComuns','GuiasG2')) for a in ancestors(n)) or 'T51.7601' in o.get('rotulo','')]
    parts={n:o for n,o in parts.items() if n not in excluded}
    changes={p['object']:p['proposed_box_mm'] for p in proposal['parts']}
    fronts={p['drawer']:p['object'] for p in proposal['parts'] if p['role']=='frente_decorativa'}
    assert overlap(swept([0,0,0,1,1,1],10,3),[0,-5,2,1,-4,3])
    movements=json.loads((ROOT/'ferramentas/verificar_modelo/movimentos.json').read_text(encoding='utf-8'))
    def has_pose(x,control):
        if isinstance(x,dict): return any(has_pose(v,control) for v in x.values())
        if isinstance(x,list): return x==[control,'Deslocamento',600] or any(has_pose(v,control) for v in x)
        return False
    assert has_pose(movements,'ControleCorrerR14') and has_pose(movements,'ControleCorrerR001')
    assert any('LocalX=20 mm + Deslocamento'==e for e in objects['PortaCorrer']['expressoes'])
    assert any('LocalX=985 mm - Deslocamento'==e for e in objects['PortaCorrer001']['expressoes'])
    rows=[]; summaries=[]
    for src in audit['rows']:
        drawer=src['drawer'];moving=[n for n in parts if drawer in ancestors(n)]
        assert len([n for n in moving if n in changes])==6
        assert any('Extensao' in x for x in objects[drawer]['expressoes'])
        door='PortaCorrer' if drawer in ['Gaveta','Gaveta001'] else 'PortaCorrer001' if src['module']=='P01' else None
        for variant in ['R52','proposta']:
            boxes={n:(changes[n] if variant=='proposta' and n in changes else o['caixa_global']) for n,o in parts.items()}
            rear=max(boxes[n][4] for n in moving)
            clear=rear-src['carcass_front_y_mm']
            summaries.append(dict(drawer=drawer,variant=variant,rear_y_mm=rear,carcass_front_y_mm=src['carcass_front_y_mm'],
                travel_to_clear_carcass_plane_mm=clear,
                remaining_inside_at_C472_475_478_mm=[rear-c-src['carcass_front_y_mm'] for c in [472,475,478]],
                hypothetical_straight_removal_travel_mm=clear+1,additional_after_C472_475_478_mm=[clear+1-c for c in [472,475,478]]))
            for door_open in ([False,True] if door else [True]):
                fixed={n:b for n,b in boxes.items() if n not in moving}
                if door and door_open:
                    fixed={n:move(b,0,-600 if door=='PortaCorrer' else 600) if door in ancestors(n) else b for n,b in fixed.items()}
                for mode in ['frente_acompanha','frente_realinhada']:
                    for travel in [0,478,clear+1]:
                        candidates=[];baseline=[];checks=0
                        for n in moving:
                            env=swept(boxes[n],travel,0 if mode=='frente_realinhada' and n==fronts[drawer] else 3)
                            for k,b in fixed.items():
                                checks+=1
                                if overlap(boxes[n],b):baseline.append([n,k])
                                if overlap(env,b):candidates.append([n,k])
                        rows.append(dict(drawer=drawer,variant=variant,door=door,door_displacement_mm=600 if door and door_open else 0,
                            front_mode=mode,travel_mm=travel,adjustment_interval_mm=[0,3],pair_checks=checks,
                            closed_baseline_candidates=baseline,swept_candidates=candidates,
                            new_candidates=[p for p in candidates if p not in baseline]))
    gaps=[]
    # Independent adjustment a_lower,a_upper in [0,3]: gap = g+a_upper-a_lower.
    for lower,upper in [('Gaveta','Gaveta001'),('Gaveta002','Gaveta003'),('Gaveta004','Gaveta005'),('Gaveta005','Gaveta006')]:
        g=objects[fronts[upper]]['caixa_global'][2]-objects[fronts[lower]]['caixa_global'][5]
        gaps.append(dict(lower=lower,upper=upper,nominal_gap_mm=g,min_gap_independent_adjustments_mm=g-3))
    for d,obs in [('Gaveta001','Peca245'),('Gaveta003','Peca246'),('Gaveta006','Peca308')]:
        f=objects[fronts[d]]['caixa_global'];o=objects[obs]['caixa_global']
        assert all(min(f[i+3],o[i+3])-max(f[i],o[i])>0 for i in [0,1])
        g=o[2]-f[5];gaps.append(dict(lower=d,upper=obs,nominal_gap_mm=g,min_gap_independent_adjustments_mm=g-3))
    result=dict(cad_sha256=base['sha256'],base_sha256=hashlib.sha256(bp.read_bytes()).hexdigest(),cad_opened=False,cad_changed=False,
        physical_tests_executed=0,total_pair_checks=sum(r['pair_checks'] for r in rows),front_gaps=gaps,depth_summary=summaries,cases=rows,excluded_hardware_objects=excluded,
        obstacle_policy='Visible Part/PartDesign solid leaves; saved ancestor visibility. Excludes GuiasComuns/GuiasG2 and T51 references, not actual FGVTN products.',
        limits=['AABB continuous translational sweep, not BRep collision proof. Candidate includes pre-existing contacts.',
                'Single drawer, other drawers closed at zero adjustment. Independent upper adjustment can only increase vertical front gap.',
                'Front realignment is hypothetical: mounting/fasteners and adjustment range not demonstrated.',
                'Straight removal assumes released clips and external support; no lift/tilt/hands or real release geometry.',
                '600 mm door pose from saved movement scenarios; no simultaneous access to both P01 columns.',
                '1 mm beyond carcass plane is bookkeeping margin, not ergonomic allowance or product withdrawal stroke.'])
    (OUT/'Ajuste_vertical_retirada.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),front_gaps=gaps,open_door_new_candidates=[{k:r[k] for k in ['drawer','variant','front_mode','travel_mm','new_candidates']} for r in rows if (not r['door'] or r['door_displacement_mm']) and r['new_candidates']]),ensure_ascii=True))
if __name__=='__main__':main()
