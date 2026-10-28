"""Auditoria nominal R44/R54, sem abrir/salvar CAD ou recalcular resistência.

Compara envelopes por ID; não usa internalMeasures (texto derivado da matriz).
CSV completo deve ser gravado fora do repositório.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / '04_Moveis/Inventario_dimensional'


def load_js(path, name):
    return json.JSONDecoder().raw_decode(re.split(r'\b' + name + r'\s*=\s*', path.read_text(encoding='utf-8'), maxsplit=1)[1])[0]


def world_bbox(part):
    return [7400 - 10*(part['x']+part['w']), 10*part['z'], 10*part['y'],
            7400-10*part['x'], 10*(part['z']+part['d']), 10*(part['y']+part['h'])]


def compare(old, parts):
    rows = []
    for part in parts:
        key = part['source']
        if key not in old:
            continue
        a, b = old[key]['bbox'], world_bbox(part)
        for axis, label in enumerate(('X', 'Y', 'Z')):
            for kind, av, bv in [('mínimo', a[axis], b[axis]), ('máximo', a[axis+3], b[axis+3]),
                                  ('dimensão', a[axis+3]-a[axis], b[axis+3]-b[axis])]:
                rows.append([part['module'], key, label, kind, round(av, 6), round(bv, 6), round(bv-av, 6)])
    return rows


# Dimensões de painéis citadas nos três documentos. Os três eixos são auditados.
PANELS = {
 'P01': ['Peca209','Peca210','Peca211','Peca212','Peca213'],
 'P02': ['PlacaL','PlacaL001','Peca255'], 'P03': ['Peca262','Peca263'],
 'P04': ['Peca269','ApoioComumR003','ApoioOpostoR001','FaixaFixaEstudo'],
 'P05': ['Peca279','Peca280'], 'P06': ['Peca286','MontagemG2R019'],
 'P07': ['BasePlanaR31','Peca307'], 'P08': ['PecaBaixaR001','PecaBaixaR002'],
 'P09': ['Peca318','Peca320'], 'P10': ['Peca327','Peca329','Peca330','Peca331'],
 'P11': ['Peca337','Peca339'], 'P12': ['Peca345','Peca347'], 'P13': ['Peca350'],
 'P14': ['PecaCestoR15'], 'P15': ['Peca362'], 'P16': ['Peca370','GavetaComumR084','GavetaComumR087'],
 'P17': ['Peca387'], 'P18': ['BC43_CaixaBase','BC43_Travessa'],
 'P19': ['PrateleiraEspelhadoR12'], 'P20': ['BancoR43_Painel1','BancoR43_Painel2','Ref_Sarrafo_frente0R31','Ref_Sarrafo_tras0R31']}

# (módulo, descrição, face superior, índice, face inferior, índice).
GAPS = [
 ('P01','setor superior', 'Peca206',0,'Peca210',3),
 ('P01','nicho inferior 1','Peca211',2,'Peca209',5),
 ('P01','nicho inferior 2','Peca212',2,'Peca211',5),
 ('P01','nicho inferior 3','Peca213',2,'Peca212',5),
 ('P02','altura interna','PlacaL001',2,'PlacaL',5),
 ('P03','altura interna','Peca263',2,'Peca262',5),
 ('P04','vão 1','ApoioComumR003',1,'Peca266',4),
 ('P04','vão 2','ApoioOpostoR001',1,'ApoioComumR003',4),
 ('P04','vão 3','ApoioOpostoR002',1,'ApoioComumR004',4),
 ('P05','altura inferior','Peca280',2,'Peca279',5),
 ('P05','altura superior até corpo','Peca276',5,'Peca280',5),
 ('P06','largura interna','Peca283',0,'Peca284',3),
 ('P07','largura interna','Peca305',0,'Peca306',3),
 ('P08','reserva entre apoios','PecaBaixaR036',0,'PecaBaixaR037',3),
 ('P09','altura interna','Peca319',2,'Peca318',5),
 ('P09','nicho esquerdo','Peca320',0,'Peca316',3),
 ('P09','nicho direito','Peca315',0,'Peca320',3),
 ('P10','altura 1','Peca329',2,'Peca327',5),
 ('P10','altura 2','Peca330',2,'Peca329',5),
 ('P10','altura 3','Peca331',2,'Peca330',5),
 ('P10','altura 4','Peca328',2,'Peca331',5),
 ('P11','altura 1','Peca339',2,'Peca337',5),
 ('P11','altura 2','Peca338',2,'Peca339',5),
 ('P12','altura interna','Peca346',2,'Peca345',5),
 ('P12','nicho esquerdo','Peca347',0,'Peca343',3),
 ('P12','nicho direito','Peca342',0,'Peca347',3),
 ('P14','largura interna','Peca352',0,'Peca353',3),
 ('P15','altura interna','Peca363',2,'Peca362',5),
 ('P16','largura interna','Peca368',0,'Peca367',3),
 ('P16','altura interna','Peca371',2,'Peca370',5),
 ('P17','altura interna','Peca388',2,'Peca387',5),
 ('P18','abertura frontal','BC43_Travessa',2,'BC43_Base',5),
 ('P19','altura 1','PrateleiraEspelhadoR12',2,'Peca403',5),
 ('P19','altura 2','PrateleiraEspelhadoR001',2,'PrateleiraEspelhadoR12',5),
 ('P19','altura 3','Peca404',2,'PrateleiraEspelhadoR001',5),
 ('P20','vão transversal','Ref_Sarrafo_frente0R31',0,'Ref_Sarrafo_tras0R31',3),
 ('P20','junta tampas','BancoR43_Painel2',1,'BancoR43_Painel1',4),
]


def run(output):
    output = output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('CSV completo deve ficar fora do git/repositório')
    source = AREA / 'Inventario/Solidos_finitos_ativos_R44.json'
    cad_path = ROOT / 'ferramentas/site/src/cad-data.js'
    cad = load_js(cad_path, 'CAD_DATA')
    if cad['current_revision'] != 'R54':
        raise ValueError('Esperada R54; revisão mudou, revisar o estudo')
    old = {p['name']:p for p in json.loads(source.read_text(encoding='utf-8'))}
    rows = compare(old, cad['parts'])
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['modulo','id','eixo','metrica','R44_mm','R54_mm','delta_mm']); w.writerows(rows)
    byid = {p['source']:p for p in cad['parts']}
    lines = ['# Reconciliação dimensional R44 → R54', '',
       '28/10/2026. Cotas nominais de projeto, não medição presencial. Envelopes do exportador R54 comparados por ID com os sólidos R44. Não representa validação de montagem, contato BRep, massa ou resistência.', '',
       '| Módulo | Peça | R44 X × Y × Z (mm) | R54 X × Y × Z (mm) | Δ X / Y / Z (mm) |', '|---|---|---|---|---|']
    fmt = lambda v: f'{v:.6f}'.rstrip('0').rstrip('.') if v else '0'
    for module, keys in PANELS.items():
        for key in keys:
            if key not in old or key not in byid:
                lines.append(f'| {module} | {key} | — | — | ID ausente: não recalculado |'); continue
            a, b = old[key]['bbox'], world_bbox(byid[key])
            da = [a[i+3]-a[i] for i in range(3)]; db = [b[i+3]-b[i] for i in range(3)]
            lines.append(f'| {module} | {key} | '+ ' × '.join(map(fmt,da))+' | '+' × '.join(map(fmt,db))+' | '+' / '.join(fmt(round(db[i]-da[i],6)) for i in range(3))+' |')
    lines += ['', '## Vãos entre faces recalculados', '', '| Módulo / medida | R44 mm | R54 mm | Δ mm |', '|---|---|---|---|']
    for module, description, hi, hi_i, lo, lo_i in GAPS:
        if hi not in old or lo not in old or hi not in byid or lo not in byid:
            lines.append(f'| {module} / {description} | — | — | ID ausente: {hi} / {lo} |'); continue
        av = old[hi]['bbox'][hi_i] - old[lo]['bbox'][lo_i]
        bv = world_bbox(byid[hi])[hi_i] - world_bbox(byid[lo])[lo_i]
        lines.append(f'| {module} / {description} | {fmt(av)} | {fmt(bv)} | {fmt(round(bv-av,6))} |')
    lines += ['', '## Limites e números que não são dimensões atuais', '',
      '- A matriz já continha a profundidade 312 do divisor P09: a geometria R44 tinha 118; Δ +194 mm. O texto atualizado antes deste estudo é preservado.',
      '- Escritório: quatro painéis da gaveta superior diminuíram 6 mm em Z. Laterais 80 → 74; frente interna/traseira 53 → 47. Inferior permanece 80/53. A caixa externa permanece 400 × 430 × 240 e o vão 364 × 412 × 204. Não transferir a proposta FGVTN histórica para a MOVENTO vigente.',
      '- G2: envelope superior 629,196152 → 628; diferença de envelope histórico, não comprovação de remoção física de material nem alteração da espessura comercial.',
      '- Banco: painéis e sarrafos exportados mantêm dimensões e posições. Contatos, áreas de apoio por interseção, interferências com ferragens e resistência da simulação R44 continuam históricos: igualdade de envelope não revalida BRep ou ferragens atuais.',
      '- Catálogos (cursos, mínimos de instalação, parafusos), variantes R04 e massas/cargas/flexões não são cotas extraídas da R54. Permanecem identificados como históricos nos relatórios, sem extrapolação.',
      '- Reservas de tanque/hidráulica, eletrodomésticos, varões e folgas contra parede não são recalculados a partir de painéis. Mantêm a fonte anterior e pendência; não substituem medidas reais nem refinam itens condicionados.',
      '- Pergunta técnica pendente: os resultados históricos de fixações/contatos do banco permanecem aplicáveis às ferragens atuais? Exige geometria BRep/ferragem específica; não decorre desta comparação.',
      '', '## Rastreabilidade', '',
      f'- CSV completo: {len(rows)} medidas; {len({r[1] for r in rows})} IDs comuns. Eixos e posições incluídos, com tolerância de leitura de 0,02 mm para envelopes de malhas curvas.',
      f'- SHA256 CSV: `{hashlib.sha256(output.read_bytes()).hexdigest()}`.',
      f'- SHA256 sólidos R44: `{hashlib.sha256(source.read_bytes()).hexdigest()}`.',
      f'- Modelo declarado pelo exportador R54: `{cad["current_source_sha256"]}`.',
      '- Entrega externa: `../outputs/Comparacao_R44_R54/dimensoes_R44_R54.csv`.',
      '- Comando: `python -B ferramentas/estudos/reconciliar_documentos_dimensionais.py --csv ../outputs/Comparacao_R44_R54/dimensoes_R44_R54.csv`.',
      '- O comando escreve apenas este resumo e o CSV solicitado; não abre nem salva o FreeCAD e não regenera o site.', '']
    (AREA/'Inventario/Comparacao_R44_R54.md').write_text('\n'.join(lines), encoding='utf-8')
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--csv', type=Path, required=True)
    args = parser.parse_args(); print(f'{len(run(args.csv))} medidas comparadas')
