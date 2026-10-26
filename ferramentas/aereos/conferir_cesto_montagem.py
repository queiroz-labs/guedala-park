"""Confere preservacao de casos e distancia via lei dos cossenos."""
from pathlib import Path
import csv, json, math
from fontes import sha
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/P14/Reacoes_e_operacao'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    d=read(OUT/'Montagem_nominal.json');src=read(OUT/'Resultados.json')
    for path,h in d['inputs'].items():assert sha(ROOT/path)==h,path
    for row in d['controls']:
        assert row['case']==src['cases'][row['source_case_1based']-1]
    sc=next(x for x in read(ROOT/'04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia/Resultados.json')['articuladores'] if x['id']=='cesto_direito')
    fy,fz=[a-b for a,b in zip(sc['fixed'],sc['axis'])]
    my,mz=[a-b for a,b in zip(sc['mobile'],sc['axis'])]
    r1=math.hypot(fy,fz);r2=math.hypot(my,mz)
    phi=math.atan2(mz,my)-math.atan2(fz,fy)
    error=0.
    for row in d['lock_sensitivity']:
        length=math.sqrt(r1*r1+r2*r2-2*r1*r2*math.cos(phi+math.radians(row['angle_deg'])))
        error=max(error,abs(length-row['assumed_terminal_distance_mm']))
    assert error<1e-6
    p=d['pivot_candidate']
    assert p['total_axial_mm']==p['shoulder_length_mm']+p['thread_length_mm']+p['head_height_mm']
    assert p['remaining_nominal_mm']==p['lateral_gap_mm']-p['total_axial_mm']
    with (OUT/'Registro_montagem.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    assert len(rows)==8 and all(not r['valor'] and not r['evidencia'] and r['estado']=='NAO_EXECUTADO' for r in rows)
    assert d['physical_tests_executed']==0 and not d['capacity_demonstrated']
    result={'status':'OK_MONTAGEM_NOMINAL_P14','preserved_simultaneous_cases':4,'lock_sensitivities':5,
            'max_distance_error_mm':error,'empty_measurement_records':8,'physical_tests_executed':0,
            'result_sha256':sha(OUT/'Montagem_nominal.json')}
    (OUT/'Verificacao_montagem.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result)
if __name__=='__main__':main()
