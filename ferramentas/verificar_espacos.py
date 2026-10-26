"""Detecta espaços possivelmente apagados em Markdown; nunca corrige texto.

Padrão: aviso. --bloquear reprova todos os achados; --bloquear-corrigidos
reprova apenas os arquivos revisados no JSON. Aceita caminhos para conferir
um subconjunto e --excecoes para usar outro arquivo de configuração.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CONFIG = RAIZ / 'ferramentas/espacos_excecoes.json'
EXCLUIDOS = ('/Fontes/', '/fontes/', '/Historico/',
             '/Componentes/Estudos/', '/Contratos_e_atraso/Pesquisa/')
PALAVRAS = (
    'acessos', 'apoios', 'caixas', 'calços', 'cantos', 'casos', 'chapas',
    'cortes', 'configurações', 'conjuntos', 'dobradiças', 'entradas',
    'equilíbrios', 'excluídos', 'ferragens', 'folhas', 'gavetas', 'grupos',
    'incluídos', 'limitadores', 'linhas', 'móveis', 'painéis', 'pares',
    'parafusos', 'peças', 'pontos', 'portas', 'poses', 'posições', 'páginas',
    'reações', 'registros', 'retalhos', 'trajetórias', 'verificações', 'vetores',
)
PADROES = (
    re.compile(r'[a-zà-ú](?:P\d{2}|R\d{2}|T\d{2}|C\d{2})(?!\d)'),
    re.compile(r'\d+(?:[.,]\d+)*(?:' + '|'.join(PALAVRAS) + r')(?![a-zà-ú])'),
)
# Preservar exemplos de código, destinos de links e transcrições literais.
PROTEGIDO = re.compile(
    r'```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`|\]\([^)]*\)'
    r'|https?://[^\s<>]+|“[^”]*”|"[^"\n]*"|<!--[^>]*-->'
)


def ocorrencias(texto, arquivo='', excecoes=()):
    """Retorna (linha, coluna, trecho), preservando posições no texto original."""
    visivel = PROTEGIDO.sub(lambda m: re.sub(r'[^\r\n]', ' ', m.group()), texto)
    resultado = []
    for numero, linha in enumerate(visivel.splitlines(), 1):
        for padrao in PADROES:
            for match in padrao.finditer(linha):
                # Exceções exatas e locais: não escondem outras ocorrências da linha.
                ignorado = False
                for exc in excecoes:
                    if exc['arquivo'] != arquivo:
                        continue
                    for literal in re.finditer(re.escape(exc['trecho']), linha):
                        if literal.start() <= match.start() and match.end() <= literal.end():
                            ignorado = True
                if not ignorado:
                    resultado.append((numero, match.start() + 1, match.group()))
    return sorted(set(resultado))


def arquivos_vigentes():
    proc = subprocess.run(
        ['git', '-c', 'core.quotepath=off', 'ls-files', '-co',
         '--exclude-standard', '--', '*.md'], cwd=RAIZ,
        check=True, capture_output=True, text=True, encoding='utf-8')
    return sorted({f for f in proc.stdout.splitlines()
                   if not any(x in '/' + f for x in EXCLUIDOS)
                   and Path(f).name != 'Registro_de_decisoes.md'})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arquivos', nargs='*')
    parser.add_argument('--excecoes', type=Path, default=CONFIG)
    parser.add_argument('--bloquear', action='store_true')
    parser.add_argument('--bloquear-corrigidos', action='store_true')
    args = parser.parse_args(argv)
    config = json.loads(args.excecoes.read_text(encoding='utf-8'))
    excecoes = config.get('excecoes', [])
    for exc in excecoes:
        if not all(isinstance(exc.get(k), str) and exc[k].strip()
                   for k in ('arquivo', 'trecho', 'motivo')):
            parser.error('Cada exceção precisa de arquivo, trecho literal e motivo.')
    corrigidos = set(config.get('corrigidos', []))
    arquivos = args.arquivos or arquivos_vigentes()
    erros = avisos = 0
    for nome in sorted(set(arquivos)):
        path = (RAIZ / nome).resolve()
        nome = path.relative_to(RAIZ).as_posix()
        if not path.is_file():
            print(f'ERRO: arquivo ausente: {nome}')
            erros += 1
            continue
        for linha, coluna, trecho in ocorrencias(path.read_text(encoding='utf-8'), nome, excecoes):
            bloqueia = args.bloquear or (args.bloquear_corrigidos and nome in corrigidos)
            rotulo = 'ERRO' if bloqueia else 'AVISO'
            erros += int(bloqueia)
            avisos += int(not bloqueia)
            print(f'{rotulo}: {nome}:{linha}:{coluna}: possível espaço apagado: {trecho}')
    print(f'Espaços: {erros} erro(s), {avisos} aviso(s), {len(set(arquivos))} arquivo(s)')
    return int(erros > 0)


if __name__ == '__main__':
    raise SystemExit(main())
