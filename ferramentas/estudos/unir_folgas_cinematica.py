"""Une particoes somente apos conferir hashes, cobertura e unicidade dos pares."""
from pathlib import Path
import argparse,csv,hashlib,json,math


def run(out, resume, parts):
    data=json.loads((out/'Candidatos_articulados.json').read_text())
    excluded={tuple(sorted(p)) for p in data['internal_hinge_pairs']}
    with (out/'Pares_articulacoes.csv').open(newline='') as f:
        expected={(r['objeto_a'],r['objeto_b']) for r in csv.DictReader(f,delimiter=';') if tuple(sorted((r['objeto_a'],r['objeto_b']))) not in excluded}
    records={};fields=None
    sources=[resume] if resume else []
    meta=[]
    for i in range(parts):
        m=json.loads((out/('Folgas_parte_%s.json'%i)).read_text(encoding='utf-8'))
        assert m['source_sha256']==data['sha256'] and m['source_unchanged']
        assert m['partition']==i and m['partitions']==parts
        assert m['resume_sha256']==(hashlib.sha256(resume.read_bytes()).hexdigest() if resume else None)
        source=out/('Folgas_parte_%s.csv'%i)
        assert hashlib.sha256(source.read_bytes()).hexdigest()==m['table_sha256']
        sources.append(source);meta.append(m)
    for source in sources:
        with source.open(encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f,delimiter=';')
            if fields is None:fields=reader.fieldnames
            assert reader.fieldnames==fields
            for r in reader:
                key=r['objeto_a'],r['objeto_b']
                assert key not in records and key in expected and None not in r and None not in r.values()
                if r['distancia_minima_amostrada_mm']:
                    value=float(r['distancia_minima_amostrada_mm']);assert math.isfinite(value) and value>=0
                if r['limite_superior_amostrado_mm']:
                    lower,upper=float(r['limite_inferior_certificado_mm']),float(r['limite_superior_amostrado_mm'])
                    assert math.isfinite(lower) and math.isfinite(upper) and 0<=lower<=upper+1e-7
                records[key]=r
    assert set(records)==expected, 'Particao incompleta'
    table=out/'Folgas_BREP.csv'
    with table.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter=';');writer.writeheader()
        writer.writerows(records[k] for k in sorted(records))
    exact=[r for r in records.values() if r['distancia_minima_amostrada_mm']]
    summary=dict(source_sha256=data['sha256'],source_unchanged=True,pairs=len(records),
        pairs_with_exact_minimum=len(exact),near_pair_threshold_mm=meta[0]['near_pair_threshold_mm'],
        pairs_with_interval=sum('intervalo:' in r['cobertura'] for r in records.values()),
        native_call_timeouts=sum('chamada nativa' in r['cobertura'] for r in records.values()),
        exact_distance_calls=sum(int(r['avaliacoes_BREP']) for r in records.values()),
        zero_distance_pairs=sum(float(r['distancia_minima_amostrada_mm'])<=1e-7 for r in exact),
        internal_hinge_pairs_excluded=len(excluded),tolerance_mm=1e-7,parallel_parts=parts,
        table_sha256=hashlib.sha256(table.read_bytes()).hexdigest(),
        limit=meta[0]['limit'])
    (out/'Folgas_resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--resume',type=Path);p.add_argument('--parts',type=int,required=True)
    a=p.parse_args();run(a.out,a.resume,a.parts)
