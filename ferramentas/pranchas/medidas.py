"""Resolução estrita de medidas: campo vence nominal; nunca transforma vazio em zero."""
import csv
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Medida:
    mm: float | None
    origem: str
    fontes: tuple

    def menos(self, other):
        value = None if self.mm is None or other.mm is None else self.mm - other.mm
        origin = 'medido' if self.origem == other.origem == 'medido' else 'nominal'
        return Medida(value, origin, self.fontes + other.fontes)


def numero(text, *, nominal=False):
    text = text.strip()
    if not text:
        return None
    # Os registros PD históricos incluem comentário após o primeiro valor em mm.
    pattern = r'^(-?\d+(?:[.,]\d+)?)\s*(mm|cm|m)(?=\s|$)'
    match = re.match(pattern, text)
    if not match or (not nominal and match.end() != len(text)):
        raise ValueError(f'Medida inválida: {text!r}. Use número e unidade, por exemplo 2470 mm.')
    return float(match[1].replace(',', '.')) * {'mm': 1, 'cm': 10, 'm': 1000}[match[2]]


def carregar(root):
    with (root / '07_Imovel/Medidas_e_impactos.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    by_id = {r['codigo_medida']: r for r in rows}
    if len(by_id) != len(rows):
        raise ValueError('Código de medida duplicado')
    return by_id


def resolver(rows, code):
    parent, _, component = code.partition('/')
    row = rows[parent]
    measured = bool(row['valor_medido'].strip())
    raw = row['valor_medido'] if measured else row['valor_nominal_atual']
    try:
        if component:
            # DIM-* já reúne cotas oficiais. Lê um eixo sem duplicá-lo em outra linha.
            tokens=re.findall(r'(-?\d+(?:[.,]\d+)?)\s*(mm|cm|m)?',raw)
            tokens=[(n,u) for n,u in tokens if n]
            if measured and not re.fullmatch(r'\s*-?\d+(?:[.,]\d+)?\s*(?:mm|cm|m)?(?:\s*[×x;]\s*-?\d+(?:[.,]\d+)?\s*(?:mm|cm|m)?)*\s*',raw):
                raise ValueError('Use cotas separadas por ×, com unidade: 2450 × 2950 mm')
            index=int(component)
            if index>=len(tokens):
                raise ValueError('Falta um eixo na medida composta')
            unit=tokens[index][1] or (tokens[-1][1] if tokens else '')
            value=numero(tokens[index][0]+' '+unit)
        else:
            value = numero(raw, nominal=not measured)
    except ValueError as exc:
        raise ValueError(f'{code}: {exc}') from exc
    return Medida(value, 'medido' if measured else 'nominal', (code,))
