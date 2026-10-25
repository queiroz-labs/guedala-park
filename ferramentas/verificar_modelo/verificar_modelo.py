"""Verifica o modelo FreeCAD vigente e acusa erro se algo foi alterado sem querer.

Uso (python comum, na raiz do repo):
  python ferramentas/verificar_modelo/verificar_modelo.py            # rapido, sem abrir o FreeCAD (segundos)
  python ferramentas/verificar_modelo/verificar_modelo.py --completo # abre no FreeCADCmd e compara com a base (minutos)
  python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base
      grava a base nova. So depois que Elias aprovar a mudanca do modelo.

Saida: 0 = ok, 1 = erro. Avisos nao reprovam.
A base fica em 02_Modelo_3D/Base_verificacao.json.
"""
import hashlib, json, os, subprocess, sys, tempfile, zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RELEASE = RAIZ / 'ferramentas/site/current_release.json'
BASE = RAIZ / '02_Modelo_3D/Base_verificacao.json'
INSPETOR = Path(__file__).with_name('inspecionar_freecad.py')
FREECADCMD = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'

erros, avisos = [], []


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def rapido():
    rel = json.loads(RELEASE.read_text(encoding='utf-8'))
    cad = RAIZ / rel['cadPath']
    if not cad.exists():
        erros.append('Modelo vigente nao encontrado: %s (current_release.json -> cadPath)' % rel['cadPath'])
        return rel, cad
    # um so modelo vigente na pasta do modelo
    extras = [p.name for p in (RAIZ / '02_Modelo_3D').glob('*.FCStd') if p != cad]
    if extras:
        erros.append('Mais de um .FCStd em 02_Modelo_3D (so o vigente pode ficar): %s' % ', '.join(extras))
    lixo = [str(p.relative_to(RAIZ)) for pat in ('*.FCBak', '*.FCStd1', '*.FCStd.*') for p in RAIZ.rglob(pat)
            if '.git' not in p.parts and 'node_modules' not in p.parts]
    if lixo:
        erros.append('Backups/temporarios do FreeCAD na pasta do projeto: %s' % ', '.join(lixo[:10]))
    try:
        with zipfile.ZipFile(cad) as z:
            nomes = set(z.namelist())
            if z.testzip() is not None:
                erros.append('Arquivo .FCStd corrompido (CRC do ZIP falhou)')
            if 'Document.xml' not in nomes:
                erros.append('Document.xml ausente no .FCStd')
            if 'GuiDocument.xml' not in nomes:
                erros.append('GuiDocument.xml ausente: cores e visibilidade foram perdidas (salvo pelo FreeCADCmd?)')
    except zipfile.BadZipFile:
        erros.append('Modelo vigente nao e um .FCStd valido')
        return rel, cad
    atual = sha(cad)
    if atual != rel['cadSHA256']:
        erros.append('O modelo mudou e o current_release.json nao foi atualizado (SHA %s... esperado %s...). '
                     'Se a mudanca foi aprovada, rode --completo --atualizar-base e atualize o release.' % (atual[:12], rel['cadSHA256'][:12]))
    if BASE.exists():
        base = json.loads(BASE.read_text(encoding='utf-8'))
        if base.get('sha256') != rel['cadSHA256']:
            avisos.append('A base de verificacao e de outro arquivo (%s...); rode --completo --atualizar-base' % base.get('sha256', '')[:12])
    else:
        avisos.append('Sem base de verificacao; rode --completo --atualizar-base')
    return rel, cad


def inspecionar(cad, refinar=None):
    if not FREECADCMD.exists():
        erros.append('FreeCADCmd nao encontrado em %s' % FREECADCMD)
        return None
    saida = Path(tempfile.gettempdir()) / 'gp_retrato_modelo.json'
    env = dict(os.environ, GP_MODELO=str(cad), GP_SAIDA=str(saida))
    arq_ref = Path(tempfile.gettempdir()) / 'gp_refinar.json'
    if refinar:
        arq_ref.write_text(json.dumps(refinar), encoding='utf-8')
        env['GP_REFINAR'] = str(arq_ref)
    else:
        env.pop('GP_REFINAR', None)
    antes = sha(cad)
    proc = subprocess.run([str(FREECADCMD), str(INSPETOR)], env=env, capture_output=True, text=True, errors='replace')
    if sha(cad) != antes:
        erros.append('A inspecao alterou o arquivo do modelo; isso nunca deveria acontecer')
    if not saida.exists():
        erros.append('FreeCADCmd nao gerou o retrato: %s' % (proc.stdout + proc.stderr)[-800:])
        return None
    retrato = json.loads(saida.read_text(encoding='utf-8'))
    saida.unlink()
    return retrato


def comparar(base, atual):
    bo, ao = base['objetos'], atual['objetos']
    removidos = sorted(set(bo) - set(ao))
    novos = sorted(set(ao) - set(bo))
    if removidos:
        erros.append('%d objetos removidos: %s' % (len(removidos), ', '.join(removidos[:15])))
    if novos:
        avisos.append('%d objetos novos: %s' % (len(novos), ', '.join(novos[:15])))
    geo, pos, vis, expr = [], [], [], []
    for n in sorted(set(bo) & set(ao)):
        b, a = bo[n], ao[n]
        if b.get('forma') != a.get('forma'):
            geo.append(n)
        if b.get('posicao') != a.get('posicao'):
            pos.append(n)
        if b.get('visivel') != a.get('visivel'):
            vis.append(n)
        if b.get('expressoes') != a.get('expressoes'):
            expr.append(n)
    for rotulo, lista in (('geometria alterada', geo), ('posicao alterada', pos), ('visibilidade alterada', vis), ('expressoes alteradas', expr)):
        if lista:
            avisos.append('%d com %s: %s' % (len(lista), rotulo, ', '.join(lista[:15])))
    if atual['total_expressoes'] < base['total_expressoes']:
        erros.append('Expressoes perdidas: %d -> %d' % (base['total_expressoes'], atual['total_expressoes']))
    inval_base = {i['nome'] for i in base['invalidos']}
    inval_novos = [i for i in atual['invalidos'] if i['nome'] not in inval_base]
    if inval_novos:
        erros.append('%d objetos invalidos novos: %s' % (len(inval_novos), ', '.join('%s %s' % (i['nome'], i['estado']) for i in inval_novos[:15])))
    suspeitos = []
    if 'caixas_sobrepostas' in atual and 'caixas_sobrepostas' in base:
        cb = {(p[0], p[1]): p[2] for p in base['caixas_sobrepostas']}
        ca = {(p[0], p[1]): p[2] for p in atual['caixas_sobrepostas']}
        suspeitos = sorted(k for k in ca if k not in cb or ca[k] > cb[k] * 1.05 + 1)
    return suspeitos


def main():
    completo = '--completo' in sys.argv
    atualizar = '--atualizar-base' in sys.argv
    rel, cad = rapido()
    if completo and cad.exists():
        retrato = inspecionar(cad)
        if retrato:
            retrato['sha256'] = sha(cad)
            retrato['revisao'] = rel['cadRevision']
            if atualizar:
                if retrato['invalidos']:
                    avisos.append('Base gravada com %d objetos invalidos registrados' % len(retrato['invalidos']))
                BASE.write_text(json.dumps(retrato, ensure_ascii=False, indent=0), encoding='utf-8')
                print('Base gravada: %s (%d objetos, %d pares de caixas sobrepostas registrados como esperados)' % (
                    BASE.relative_to(RAIZ), retrato['total_objetos'], len(retrato.get('caixas_sobrepostas', []))))
                erros[:] = [e for e in erros if 'current_release.json nao foi atualizado' not in e]
            elif BASE.exists():
                suspeitos = comparar(json.loads(BASE.read_text(encoding='utf-8')), retrato)
                if suspeitos:
                    print('Triagem: %d pares de pecas com caixas novas/maiores; conferindo a intersecao exata...' % len(suspeitos))
                    exato = inspecionar(cad, [list(k) for k in suspeitos])
                    batidas = [e for e in (exato or {}).get('colisoes_exatas', []) if e[2] > 0.01]
                    if batidas:
                        erros.append('%d colisoes novas (pecas se sobrepondo): %s' % (len(batidas), '; '.join('%s x %s (%.1f mm3)' % tuple(e) for e in batidas[:15])))
                    else:
                        avisos.append('%d pares tiveram caixa maior, mas sem sobreposicao real' % len(suspeitos))
            print('Inspecao em %.0f s: %d objetos, %d formas ativas, %d pares de caixas sobrepostas' % (
                retrato['segundos'], retrato['total_objetos'], retrato.get('formas_ativas', 0), len(retrato.get('caixas_sobrepostas', []))))
    for a in avisos:
        print('AVISO:', a)
    for e in erros:
        print('ERRO:', e)
    print('Modelo: %s' % ('OK' if not erros else '%d erro(s)' % len(erros)))
    sys.exit(1 if erros else 0)


main()
