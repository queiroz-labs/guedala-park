"""Extrai casos simultaneos do P14 e prepara registros vazios de montagem."""
from pathlib import Path
import csv, gzip, json, math
from fontes import sha, HASH_RULE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'04_Moveis/P14/Reacoes_e_operacao'
REF = ROOT/'04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia'

def read(p): return json.loads(p.read_text(encoding='utf-8'))

def main():
    src = read(OUT/'Resultados.json'); geom = read(OUT/'Geometria_R51.json')
    basepath = ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base = json.loads(gzip.decompress(basepath.read_bytes()))
    release = read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath']) == base['sha256']
    for part in geom['parts']:
        actual = base['objetos'][part['name']]['caixa_global']
        assert all(abs(a-b)<1e-6 for a,b in zip(actual,part['box_mm']))
    cases = src['cases']
    selectors = {
        'maior_resultante_pivo': lambda c:max(c['hinge_left_resultant_N'],c['hinge_right_resultant_N']),
        'maior_retencao_reversa': lambda c:-c['min_hinge_vertical_N'],
        'maior_tracao_articulador': lambda c:max(c['stay_left_N'],c['stay_right_N']),
        'maior_momento_interface_pivo': lambda c:max(math.hypot(*v) for v in c['hinge_wall_interface_MYZ_Nm']),
    }
    controls=[]
    for label,key in selectors.items():
        i=max(range(len(cases)),key=lambda j:key(cases[j]))
        controls.append({'control':label,'source_case_1based':i+1,'value':key(cases[i]),'case':cases[i]})
    sc=next(x for x in read(REF/'Resultados.json')['articuladores'] if x['id']=='cesto_direito')
    def distance(deg):
        # Rotacao positiva em YZ; sign da fonte escolhe o cotovelo das barras.
        t=math.radians(deg); y,z=[a-b for a,b in zip(sc['mobile'],sc['axis'])]
        moved=[sc['axis'][0]+y*math.cos(t)-z*math.sin(t),sc['axis'][1]+y*math.sin(t)+z*math.cos(t)]
        return math.dist(moved,sc['fixed'])
    assert abs(distance(55)-291)<1e-6
    lock=[]
    for d in [280,285,288,290,291]:
        lo,hi=0.,55.
        for _ in range(60):
            mid=(lo+hi)/2
            if distance(mid)<d:lo=mid
            else:hi=mid
        angle=(lo+hi)/2
        assert abs(distance(angle)-d)<1e-6
        lock.append({'assumed_terminal_distance_mm':d,'angle_deg':angle})
    inputs=[OUT/'Resultados.json',OUT/'Geometria_R51.json',REF/'Resultados.json',REF/'Fontes/Omega_7379.pdf',basepath,Path(__file__)]
    result={'scope':'Montagem nominal; sem ensaio e sem capacidade demonstrada','hash_rule':HASH_RULE,
            'inputs':{p.relative_to(ROOT).as_posix():sha(p) for p in inputs},'cad_sha256':base['sha256'],
            'controls':controls,'lock_sensitivity':lock,
            'pivot_candidate':{'code':'OMPCR1020','shoulder_diameter_mm':10,'shoulder_length_mm':20,
            'thread':'M8x1.25','thread_length_mm':13.25,'head_height_mm':7,'head_diameter_mm':16,
            'hex_SW_mm':5,'hex_depth_mm':4.3,'total_axial_mm':40.25,'lateral_gap_mm':52,
            'remaining_nominal_mm':11.75,'bushing':None,'retention':None,'tool_corridor':None},
            'physical_tests_executed':0,'capacity_demonstrated':False}
    (OUT/'Montagem_nominal.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['id','medicao_requerida','unidade','valor','evidencia','estado']
    measurements=[('C01A','Ombro util, bucha, arruelas, folga axial e alivio de raiz','mm'),
                  ('C01B','Engajamento de rosca e espessura resistente do apoio fixo','mm'),
                  ('C01C','Corredor de inserir, girar e retirar Allen SW5','mm/foto'),
                  ('C01D','Retencao axial e caminho contra levantamento do suporte','desenho'),
                  ('C02A','Distancia entre eixos ao engatar e ao liberar trava','mm'),
                  ('C02B','Angulo real e folgas de terminais durante percurso','grau/mm'),
                  ('C03A','Retirada do saco e desmontagem da armacao','foto/sequencia'),
                  ('C04A','Massas e centros de saco, pega e ferragens moveis','kg/mm')]
    # Regeneracao nao pode apagar medicoes preenchidas pela oficina.
    form=OUT/'Registro_montagem.csv'
    if form.exists():
        with form.open(encoding='utf-8-sig',newline='') as f:
            old=list(csv.DictReader(f,delimiter=';'))
        assert all(not r['valor'] and not r['evidencia'] and r['estado']=='NAO_EXECUTADO' for r in old), 'Preservar registros reais'
    with form.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';');w.writeheader()
        for id,label,unit in measurements:w.writerow(dict(id=id,medicao_requerida=label,unidade=unit,valor='',evidencia='',estado='NAO_EXECUTADO'))
    print('P14: geometria R52 conferida; 4 casos simultaneos; 5 sensibilidades; 8 registros vazios.')

if __name__=='__main__':main()
