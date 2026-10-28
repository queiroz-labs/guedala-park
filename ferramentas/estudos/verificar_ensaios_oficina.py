"""Confere completude documental, nunca capacidade; não escreve nos registros."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "04_Moveis/Ensaios_oficina/Registro.csv"
COLUNAS = (
    "ensaio_id", "medicao_id", "descricao", "unidade", "tipo", "fonte",
    "replica", "instante", "ponto", "data", "operador_codigo", "peca_lote",
    "configuracao", "instrumento_resolucao", "protocolo", "criterio",
    "registros_previstos", "carga_aplicada", "posicao_carga", "duracao_s",
    "ciclo", "condicoes", "valor", "evidencia", "observacoes", "estado",
)


def requisitos():
    """Mínimos independentes do arquivo recebido; ampliar conforme plano real."""
    itens = []

    def add(ensaio, mid, descricao, unidade="texto", fonte="Caderno.md"):
        itens.append(dict(ensaio_id=ensaio, medicao_id=mid, descricao=descricao,
                          unidade=unidade, tipo="texto" if unidade == "texto" else "numero",
                          fonte=fonte))

    for mid, desc, unit in [
        ("material", "Material, código e composição de cada peça", "texto"),
        ("espessura", "Espessura por peça e ponto", "mm"),
        ("massa", "Massa individual de cada componente", "kg"),
        ("umidade", "Umidade do painel", "%"),
    ]:
        add("E01", mid, desc, unit)
    for acesso in ("base90", "base158", "tampo90", "tampo158"):
        for op in ("insercao", "giro", "retirada", "folga"):
            add("E02", f"{acesso}_{op}", f"T0 {acesso}: {op}",
                "mm" if op == "folga" else "texto",
                "../Aereos_suspensao/P04_registro_laboratorio.csv")
    for grupo in ("P04_base_divisor", "P04_topo_divisor", "P04_lateral",
                  "P04_traseiro", "P15_base_lateral", "P15_base_fundo", "P15_fundo_laterais"):
        for grandeza, unidade in (("forca", "N"), ("junta", "mm"), ("aparelho", "mm"),
                                  ("recuperacao", "mm"), ("dano", "texto")):
            add("E03", f"{grupo}_{grandeza}", f"{grupo}: {grandeza} por patamar", unidade)
    for ensaio, movel in (("E04", "P04"), ("E05", "P12"), ("E06", "P17")):
        for caso in range(1, 7):
            for grandeza, unidade in (("vertical", "N"), ("para_fora", "N"), ("deslocamento", "mm")):
                add(ensaio, f"caso{caso}_{grandeza}", f"{movel} caso {caso}: {grandeza}", unidade)
        for grandeza, unidade in (("acesso", "texto"), ("retencao", "texto"),
                                  ("contato_inferior", "texto"), ("juntas", "mm"),
                                  ("base", "mm"), ("fundo", "mm"), ("topo", "mm"),
                                  ("aparelho", "mm"), ("recuperacao", "mm"), ("dano", "texto")):
            add(ensaio, f"caixa_{grandeza}", f"{movel} caixa completa: {grandeza}", unidade)
    for composicao in ("simples", "dupla_solta", "composta"):
        for grandeza, unidade in (("processo", "texto"), ("frente", "mm"), ("centro", "mm"),
                                  ("apoio", "mm"), ("camadas", "mm"), ("retorno", "mm"),
                                  ("dano", "texto")):
            if composicao == "simples" and grandeza == "camadas":
                unidade = "texto"  # Registrar ausência de segunda camada, não um zero medido.
            add("E07", f"{composicao}_{grandeza}",
                f"{composicao}: {grandeza}; expandir para 3 corpos e instantes do plano", unidade)
    add("E07", "caixa", "Comparação na caixa completa, após corpos", "texto")
    for n in range(1, 11):
        add("E08", f"apoio{n}", f"Contato da face principal {n}")
    for n in range(1, 8):
        add("E08", f"inferior{n}", f"Contato da região inferior {n}")
    for tampa in ("maior", "menor"):
        for grandeza, unidade in (("eixo", "mm"), ("engate", "mm"), ("liberacao", "mm"),
                                  ("angulo", "graus"), ("forca", "N"), ("flecha", "mm"),
                                  ("corpo", "mm"), ("retorno", "mm"), ("manutencao", "texto")):
            add("E08", f"{tampa}_{grandeza}", f"Tampa {tampa}: {grandeza}", unidade)
    for mid, unidade in (("ombro", "mm"), ("bucha", "mm"), ("arruelas", "mm"),
                         ("folga_axial", "mm"), ("alivio", "mm"), ("rosca", "mm"),
                         ("apoio_resistente", "mm"), ("SW5", "mm"), ("retencao", "texto"),
                         ("engate", "mm"), ("liberacao", "mm"), ("angulo", "graus"),
                         ("folga_terminal", "mm"), ("retirada_saco", "texto"),
                         ("retirada_armacao", "texto"), ("massa", "kg"), ("centro", "mm"),
                         ("forca", "N"), ("repeticao_protecao", "texto")):
        add("E09", mid, f"P14: {mid}; identificar lado/peça/ponto", unidade,
            "../P14/Reacoes_e_operacao/Registro_montagem.csv")
    for roda in range(1, 7):
        for grandeza, unidade in (("altura", "mm"), ("folga", "mm"), ("contato", "texto")):
            add("E10", f"roda{roda}_{grandeza}", f"Roda {roda}: {grandeza}", unidade)
    for mid, unidade in (("massa", "kg"), ("curso", "mm"), ("forca", "N"),
                         ("fundo", "mm"), ("batente", "texto"), ("retirada", "texto")):
        add("E10", mid, f"P08: {mid}", unidade)
    for mid, unidade in (("massa_tampo", "kg"), ("composicao_tampo", "texto"),
                         ("unioes", "texto"), ("estabilidade", "texto")):
        add("E11", mid, f"P16: {mid}", unidade)
    for gaveta in ("inferior", "superior"):
        for mid, unidade in (("massa", "kg"), ("curso", "mm"), ("folga", "mm"),
                             ("forca", "N"), ("deslocamento", "mm"),
                             ("retorno", "mm"), ("engate_retirada", "texto")):
            add("E11", f"{gaveta}_{mid}", f"P16 {gaveta}: {mid}", unidade)
    for movel, quantidade in (("P01", 4), ("P06", 3)):
        for gaveta in range(1, quantidade + 1):
            for mid, unidade in (("largura", "mm"), ("profundidade", "mm"),
                                 ("recuo_fundo", "mm"), ("curso", "mm"), ("ajuste", "mm"),
                                 ("folga", "mm"), ("forca", "N"), ("retirada", "texto")):
                add("E12", f"{movel}_{gaveta}_{mid}", f"{movel} gaveta {gaveta}: {mid}", unidade)
    for movel in ("P01", "P09", "P11", "P15"):
        for mid, unidade in (("montagem", "texto"), ("forca", "N"), ("deslocamento", "mm"),
                             ("aparelho", "mm"), ("retorno", "mm"), ("contato", "texto")):
            add("E13", f"{movel}_{mid}", f"{movel}: {mid}; expandir grupos/casos do plano", unidade)
    for mid in ("piso", "parede", "ancoragem", "instalacoes", "folgas"):
        add("A01", mid, f"Após as chaves: {mid}; fora da rodada de oficina")
    return itens


def normalizar(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold().strip())
                   if not unicodedata.combining(c))


def preenchido(value):
    texto = normalizar(value)
    return bool(texto) and texto not in {"-", "—", "n/a", "na", "pendente", "a definir", "ok"} \
        and "a definir" not in texto and "pendente" not in texto


def numero(value):
    try:
        valor = Decimal(value.replace(",", "."))
        return valor if valor.is_finite() else None
    except InvalidOperation:
        return None


def arquivo_local(base, value):
    # Referência de arquivo relativa à cópia privada, não URL ou caminho absoluto.
    path = Path(value)
    return bool(value) and not path.is_absolute() and ":" not in value and (base / path).is_file()


def verificar(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        if reader.fieldnames != list(COLUNAS):
            raise ValueError("Cabeçalho diferente do modelo Registro.csv (ordem e nomes obrigatórios)")
        rows = list(reader)
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("Linha com número de colunas incorreto")
    rows = [{k: v.strip() for k, v in row.items()} for row in rows]
    specs = requisitos()
    esperados = {(r["ensaio_id"], r["medicao_id"]): r for r in specs}
    ensaios = list(dict.fromkeys(r["ensaio_id"] for r in specs))
    if any(r["ensaio_id"] not in ensaios for r in rows):
        raise ValueError("Ensaio desconhecido; conferir ID antes de processar")
    saidas = []
    for ensaio in ensaios:
        grupo = [r for r in rows if r["ensaio_id"] == ensaio]
        minimos = {mid for (eid, mid) in esperados if eid == ensaio}
        faltantes = minimos - {r["medicao_id"] for r in grupo}
        erros = [f"IDs mínimos ausentes: {', '.join(sorted(faltantes))}"] if faltantes else []
        # Campos de planejamento presentes no modelo não contam como resultado.
        entrada = COLUNAS[6:-1]
        iniciado = any(any(r[k] for k in entrada) or r["estado"] != "pendente de execução"
                       for r in grupo)
        if iniciado and ensaio == "E07":
            for mid in sorted(minimos - {"caixa"}):
                replicas = {r["replica"] for r in grupo
                            if r["medicao_id"] == mid and preenchido(r["replica"])}
                if len(replicas) < 3:
                    erros.append(f"{mid}: faltam as três réplicas do roteiro P15")
        chaves = set()
        for i, r in enumerate(grupo, 1):
            chave = (r["medicao_id"], r["replica"], r["instante"], r["ponto"])
            if chave in chaves:
                erros.append(f"linha do ensaio {i}: medição duplicada")
            chaves.add(chave)
            spec = esperados.get((ensaio, r["medicao_id"]))
            if not r["medicao_id"] or r["tipo"] not in {"numero", "texto"} or not r["unidade"]:
                erros.append(f"linha {i}: identificação/tipo/unidade inválidos")
            if spec and any(r[k] != spec[k] for k in ("unidade", "tipo")):
                erros.append(f"linha {i}: unidade/tipo divergem do requisito")
            if not iniciado:
                continue
            obrigatorios = [k for k in COLUNAS[6:] if k not in {"observacoes"}]
            if any(not preenchido(r[k]) for k in obrigatorios):
                erros.append(f"linha {i}: campos obrigatórios vazios ou pendentes")
            if r["estado"] not in {"executado", "interrompido"}:
                erros.append(f"linha {i}: estado não registra execução")
            if r["estado"] == "interrompido" and not preenchido(r["observacoes"]):
                erros.append(f"linha {i}: falta causa da interrupção")
            if r["tipo"] == "numero" and numero(r["valor"]) is None:
                erros.append(f"linha {i}: valor numérico não finito ou inválido")
            for k in ("duracao_s", "ciclo", "registros_previstos"):
                valor = numero(r[k])
                if valor is None or valor < 0 or (k != "duracao_s" and valor != valor.to_integral_value()):
                    erros.append(f"linha {i}: {k} inválido")
            previstos = numero(r["registros_previstos"])
            if previstos != len(grupo):
                erros.append(f"linha {i}: total previsto difere das {len(grupo)} linhas do ensaio")
            try:
                if date.fromisoformat(r["data"]).isoformat() != r["data"]:
                    raise ValueError
            except ValueError:
                erros.append(f"linha {i}: data deve ser AAAA-MM-DD válida")
            for k in ("evidencia", "protocolo"):
                if not arquivo_local(path.parent, r[k]):
                    erros.append(f"linha {i}: arquivo {k} ausente ou referência não relativa")
        status = ("dados incompletos" if erros else
                  "dados completos — revisar com RT" if iniciado else "sem dados")
        saidas.append((ensaio, status, erros))
    return saidas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        resultados = verificar(args.csv)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print(f"Arquivo inválido: {error}", file=sys.stderr)
        return 2
    for ensaio, status, erros in resultados:
        print(f"{ensaio}: {status}")
        for erro in erros[:5]:
            print(f"  - {erro}")
        if len(erros) > 5:
            print(f"  - mais {len(erros) - 5} pendências")
    return 1 if any(status == "dados incompletos" for _, status, _ in resultados) else 0


if __name__ == "__main__":
    raise SystemExit(main())
