"""Resumo pequeno e hashes dos dados externos da conferencia de movimentos."""
from pathlib import Path
import argparse,csv,hashlib,json


def native_pairs(native, source_sha):
    if native['sha256'] != source_sha:
        raise ValueError('Retrato nativo de outra fonte')
    return {tuple(sorted(p[:2])) for case in native['movimentos'].values() for p in case['novas_intersecoes']}


def run(source,out):
    broad=json.loads((source/'Articulacoes_resumo.json').read_text())
    brep=json.loads((source/'BREP_articulacoes.json').read_text())
    native=json.loads((source/'Validacao_nativa_articulacoes.json').read_text())
    clearances=json.loads((source/'Folgas_resumo.json').read_text(encoding='utf-8'))
    candidates=json.loads((source/'Candidatos_articulados.json').read_text())
    assert broad['source_sha256']==brep['source_sha256']==native['source_sha256']==clearances['source_sha256']
    rows=[]
    for p in brep['pairs']:
        if not p['first_positive']:continue
        a,b=candidates['bodies'][p['a']],candidates['bodies'][p['b']]
        rows.append(dict(objeto_a=p['a'],objeto_b=p['b'],controle_a=a['group'],controle_b=b['group'],
            estado_a=p['first_positive']['state_a'],unidade_a=a['unit'],estado_b=p['first_positive']['state_b'],unidade_b=b['unit'],
            volume_amostrado_mm3=round(p['first_positive']['intersection_mm3'],3),ausente_nos_106_cenarios=p['new_pair']))
    with (out/'Interferencias_R54.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['objeto_a','objeto_b','controle_a','controle_b','estado_a','unidade_a','estado_b','unidade_b','volume_amostrado_mm3','ausente_nos_106_cenarios']
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';');w.writeheader();w.writerows(rows)
    summary={k:v for k,v in broad.items() if k not in ('control_members','table_sha256')}
    summary.update(native_validation_complete=native['complete'],native_poses=len(native['poses']),
        native_matrices=sum(p['matrices'] for p in native['poses']),native_maximum_matrix_error=native['maximum_error'],
        brep_pairs=len(brep['pairs']),internal_hinge_pairs_excluded=brep['internal_hinge_pairs_excluded'],
        initial_positive_pairs=sum(p['initial_intersection_mm3']>0.01 for p in brep['pairs']),
        new_positive_pairs=sum(p['new_pair'] for p in brep['pairs']),positive_during_motion=len(rows),
        brep_candidate_states_checked=sum(p['checked_candidate_states'] for p in brep['pairs']),
        source_unchanged=brep['source_unchanged'],
        minimum_sampled_distances=clearances,
        external_sha256={n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in [
            'Snapshot.json','Pares_articulacoes.csv','Candidatos_articulados.json','Validacao_poses.json',
            'Validacao_nativa_articulacoes.json','BREP_articulacoes.json','Retrato_nativo_R54.json',
            'Folgas_BREP.csv','Folgas_resumo.json']})
    (out/'Resultado_R54.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.source,a.out)
