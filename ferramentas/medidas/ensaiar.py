"""Ensaio cronometrado; gera em temporário, confere resultados e preserva fontes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from time import perf_counter

sys.dont_write_bytecode = True
from recalcular import ROOT, saida_segura


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensaiar(output):
    scenario = ROOT/'ferramentas/medidas/cenarios/ensaio_chaves.csv'
    sources = [ROOT/'07_Imovel/Medidas_e_impactos.csv', ROOT/'ferramentas/fatos.json',
               ROOT/'02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd',
               ROOT/'04_Moveis/Dependencias/Impacto.json', ROOT/'04_Moveis/Dependencias/Impacto.md']
    sources += [p for p in (ROOT/'06_Entregas/Caderno_pranchas').iterdir() if p.is_file()]
    before = {str(p):sha(p) for p in sources}
    times = {}
    def run(label, cmd):
        start = perf_counter()
        subprocess.run([sys.executable,'-B',*map(str,cmd)],cwd=ROOT,check=True)
        times[label] = round(perf_counter()-start, 4)
    start = perf_counter()
    run('recalculo_s', ['ferramentas/medidas/recalcular.py','--cenario',scenario,'--saida',output/'impacto'])
    run('pranchas_s', ['ferramentas/pranchas/gerar.py','--cenario',scenario,'--saida',output/'pranchas'])
    check_start = perf_counter()
    report = json.loads((output/'impacto/Impacto.json').read_text(encoding='utf-8'))
    drawn = json.loads((output/'pranchas/Impacto_moveis.json').read_text(encoding='utf-8'))
    if report['resultados'] != drawn['resultados'] or report['envelopes'] != drawn['envelopes']:
        raise AssertionError('Pranchas e recálculo divergentes')
    rows = {(r['movel'],r['cota']):r for r in report['resultados']}
    expected = {('P03','fechamento_teto'):30, ('P17','fechamento_teto'):20,
                ('P05','ponto_C05_x'):300, ('P01','janela-1_peitoril'):990}
    for key, value in expected.items():
        if rows[key]['depois_mm'] != value:
            raise AssertionError((key,rows[key]['depois_mm'],value))
    if rows['P05','extensao_y']['folgas_mm']['fim'] != -12:
        raise AssertionError('Prumo não foi descontado')
    if rows['P01','extensao_x']['folgas_mm']['fim'] != 458:
        raise AssertionError('Quarto não ganhou 18 mm de folga')
    if rows['P20','altura']['folgas_mm']['topo'] != 2180:
        raise AssertionError('Teto da sala não atualizado')
    if rows['P14','extensao_x']['folgas_mm']['fim'] != 670:
        raise AssertionError('Lavanderia não perdeu 30 mm de folga')
    if rows['P12','extensao_x']['folgas_mm']['fim'] != 825:
        raise AssertionError('Cozinha não perdeu 25 mm de folga')
    if any(r['delta_mm'] for r in report['resultados'] if r['tipo']=='envelope'):
        raise AssertionError('Caixa fixa foi redimensionada')
    svgs = list((output/'pranchas').glob('*.svg'))
    if len(svgs) != 20 or any('recalculado, não modelado' not in p.read_text(encoding='utf-8') for p in svgs):
        raise AssertionError('Faltam folhas/marcação de cenário')
    times['conferencia_relatorios_s'] = round(perf_counter()-check_start, 4)
    times['fluxo_total_s'] = round(perf_counter()-start, 4)
    pdf = output/'pranchas/Guedala_Park_Pranchas_R02.pdf'
    first_pdf = sha(pdf)
    run('repeticao_pranchas_s',['ferramentas/pranchas/gerar.py','--cenario',scenario,'--saida',output/'pranchas'])
    repeated = json.loads((output/'pranchas/Impacto.json').read_text(encoding='utf-8'))
    if repeated['alteracoes'] or sha(pdf) != first_pdf:
        raise AssertionError('Geração não determinística')
    if before != {str(p):sha(p) for p in sources}:
        raise AssertionError('Fonte/entrega vigente alterada pelo ensaio')
    summary = dict(cenario='FICTÍCIO; não é medição real',tempos=times,
                   regras=len(rows),referencias_alteradas=sum(r['delta_mm']!=0 for r in report['resultados']),
                   status={s:sum(r['status']==s for r in report['resultados']) for s in sorted({r['status'] for r in report['resultados']})},
                   folhas=20,originais_preservados=True,pdf_deterministico=True,
                   fixture_sha256=sha(scenario),pdf_sha256=first_pdf,
                   manual=['Distribuir folgas e decidir alterações de caixa com oficina',
                           'Compatibilizar PR-WALLS/vãos com DIM; dimensões não resolvem topologia',
                           'Conferir recortes, montagem, calços e acesso a pontos',
                           'Editar FreeCAD e reexportar fichas somente depois de decisão'])
    (output/'Resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida',type=Path,help='Pasta externa nova para inspeção; omitir para apagar saídas ao terminar')
    args=parser.parse_args()
    if args.saida:
        output=saida_segura(args.saida)
        output.mkdir(parents=True,exist_ok=False)
        ensaiar(output)
    else:
        with tempfile.TemporaryDirectory(prefix='guedala-ensaio-') as tmp:
            ensaiar(Path(tmp))
