"""Importa JSON, prepara campo.csv e executa a cadeia em pasta externa nova.

O índice real só recebe a importação; derivados são estudos externos. Para uma
fixture, --csv deve apontar para uma cópia externa do índice de medidas.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
for stream in (sys.stdout,sys.stderr):stream.reconfigure(encoding='utf-8')  # saída igual em terminal e em pipe no Windows
from importar_medidas_site import ROOT,DEFAULT_CSV,external,import_file


def run(input_path,output,csv_path=DEFAULT_CSV):
    output=external(output)
    if output.exists() and any(output.iterdir()):raise ValueError('Escolha pasta de saída nova/vazia')
    # Validar caminhos antes de importar; a cadeia exige uma subpasta vazia.
    if output in Path(csv_path).resolve().parents or output in Path(input_path).resolve().parents:
        raise ValueError('Guardar entradas fora da pasta de saída nova')
    result=import_file(input_path,csv_path,output/'Importacao.md',output/'campo.csv')
    spec=importlib.util.spec_from_file_location('cadeia_celular',ROOT/'04_Moveis/Dependencias/orquestrar.py')
    chain=importlib.util.module_from_spec(spec);spec.loader.exec_module(chain)
    summary,folder=chain.run(output/'campo.csv',output/'Cadeia')
    return result,summary,folder


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada',type=Path,required=True)
    parser.add_argument('--saida',type=Path,required=True)
    parser.add_argument('--csv',type=Path,default=DEFAULT_CSV,help='Índice a importar; fixture exige cópia externa')
    args=parser.parse_args()
    try:
        result,summary,folder=run(args.entrada,args.saida,args.csv)
    except (ValueError,KeyError,OSError,RuntimeError) as exc:
        parser.exit(1,'Cadeia não concluída: '+str(exc)+'\n')
    print(f"Peças alteradas: {summary['pecas_alteradas']}")
    print(f"Folgas negativas novas: {summary['novas_folgas_negativas']}")
    print(f"Pendências de propagação: {summary['pendencias_propagacao']}")
    print(f"Importação: {result['preenchidos']} linhas; {result['incompletos']} incompletas; {result['sem_datum']} sem datum; {result['entradas_cadeia']} entradas na cadeia")
    print('Limites: caixas fixas; referências sem vínculo por peça continuam pendentes; sem medida omitida convertida em zero.')
    for name in ('Cadeia.md','Impacto.md','Pecas_diferencas.csv','Pendencias_propagacao.csv'):
        print(str(folder/name))
    print(str(args.saida.resolve()/'Importacao.md'))


if __name__=='__main__':main()
