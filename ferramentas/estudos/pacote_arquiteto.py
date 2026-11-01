"""Caderno e ZIP de revisão para o arquiteto; não abre nem modifica o CAD."""
import argparse
import csv
import hashlib
from html import escape
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
import zipfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, Image,
)
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "06_Entregas/Arquiteto"
PDF = OUT / "Caderno_arquiteto.pdf"
CAD_REVIEW = "02_Modelo_3D/Revisao_base_arquitetonica.csv"
INTERFACES = "03_Ambientes/Planta_pontos/Interfaces_prioritarias.csv"
PLANCHES = "06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R02.pdf"
SPEC = "01_Programa_e_decisoes/Caderno_de_especificacoes.md"
FIELD = "07_Imovel/Roteiro_dia_das_chaves_R01.md"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def rows(path):
    return list(csv.DictReader(StringIO(read(path)), delimiter=";"))


def plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("**", "").replace(chr(96), "").replace("→", " > ").replace("—", "-").replace("–", "-")


def make_pdf(destination, release):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("BodyGP", fontName="Helvetica", fontSize=9,
                              leading=12, spaceAfter=7, textColor=colors.HexColor("#24343b")))
    styles.add(ParagraphStyle("SmallGP", parent=styles["BodyGP"], fontSize=7.5, leading=10))
    styles["Title"].textColor = colors.HexColor("#173f46")
    body, small = styles["BodyGP"], styles["SmallGP"]
    story = []

    def p(text, style=body):
        return Paragraph(escape(plain(text)), style)

    def title(text):
        story.append(p(text, styles["Heading1"]))

    def table(data, widths):
        t = Table([[p(str(c), small) for c in row] for row in data],
                  colWidths=widths, repeatRows=1, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e7eeee")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, -1), .3, colors.HexColor("#cbd5d7")),
        ]))
        story.append(t)

    title("Guedala Park")
    story += [p("Caderno para revisão do arquiteto", styles["Title"]),
              p("Anteprojeto | emissão 01/11/2026 | não enviado"),
              p("Estudo nominal. Não executar. Medidas acabadas, compatibilização profissional e detalhamento executivo pendentes.")]
    table([
        ["Componente", "Referência e limite"],
        ["Modelo FreeCAD", release["cadRevision"] + " vigente, arquivo incluído sem alteração."],
        ["Pranchas no anexo", "R02, referência dos desenhos R54; 20 folhas A3 preservadas em tamanho original. Não são nova extração arquitetônica do R55."],
        ["Pontos", "R01: 53 funções, E06 adiada; posições e circuitos por compatibilizar."],
        ["Materiais", "Caderno R01: intenções de projeto; amostras, SKUs e produtos pendentes."],
        ["Revisão", "13 questões da base arquitetônica + 10 interfaces prioritárias."],
        ["Levantamento", "532 registros de preparação, nenhum valor medido preenchido."],
    ], [40 * mm, 132 * mm])
    story += [Spacer(1, 7 * mm),
              p("Solicitação ao arquiteto", styles["Heading2"]),
              p("Confirmar o escopo de levantamento e revisão; conciliar níveis, paredes/vãos e áreas; definir as interfaces de instalações e manutenção; indicar o formato editável necessário e as disciplinas/RT responsáveis."),
              p("Intercâmbio: FCStd nativo disponível. IFC/DWG/DXF/STEP não exportados; escolher formato e finalidade com o destinatário antes da conversão."),
              p("SHA256 do CAD: " + release["cadSHA256"], small),
              PageBreak()]

    title("Layout de referência")
    story.append(p("Planta mobiliada R03, cena R54; representação visual anterior ao R55. A vista inclui apresentações de acabamento do site, inclusive verde na janela do box, que segue candidato separado no CAD. Sem escala."))
    img = Image(str(ROOT / "03_Ambientes/Planta_mobiliada/Planta_mobiliada_R03.png"))
    img.drawWidth = 172 * mm
    img.drawHeight = img.imageHeight / img.imageWidth * img.drawWidth
    story += [img, Spacer(1, 8 * mm)]
    title("Comparação de níveis")
    table([
        ["Referência", "Demais ambientes", "Banheiro"],
        ["Piso no CAD", "Z = 0 mm", "Z = 0 mm"],
        ["Topo da envoltória R55", "2570 mm", "2570 mm"],
        ["Teto acabado de projeto", "2600 mm nominal", "2500 mm nominal"],
        ["Envoltória menos projeto", "-30 mm", "+70 mm"],
        ["Composição de piso no CAD", "Z -50 a 0 mm, representação nominal", "Z -50 a 0 mm, representação nominal"],
    ], [62 * mm, 55 * mm, 55 * mm])
    story.append(p("Quadro comparativo sem escala, não é corte construtivo. Forro não modelado; espessura gráfica de piso não comprova composição. Medir piso/teto acabados e desníveis antes de ajustar a envoltória ou os fechamentos dos armários. ARQ-01/11/12.", small))
    story.append(PageBreak())

    title("Materiais e acabamentos")
    story.append(p("Extrato da seção 1 do Caderno de especificações R01. A fonte completa acompanha o pacote. Mesma chapa física: mesmo acabamento nas duas faces; peças distintas exigem identificação e compatibilização. Amostras e códigos comerciais ainda condicionados."))
    section = read(SPEC).split("## 1. Materiais e acabamentos", 1)[1].split("## 2.", 1)[0]
    material_rows = []
    for line in section.splitlines():
        if line.startswith("|") and not re.match(r"^\|[- :|]+\|$", line):
            cells = [plain(c.strip()) for c in line.strip("|").split("|")]
            material_rows.append(cells)
    table(material_rows, [49 * mm, 38 * mm, 30 * mm, 55 * mm])
    story.append(PageBreak())

    for filename, heading, finding, action, owner, acceptance in [
        (CAD_REVIEW, "Base arquitetônica: 13 questões", "constatacao",
         "pergunta_exata", "quem_resolve", "criterio_de_encerramento"),
        (INTERFACES, "Instalações e manutenção: 10 interfaces", "conflito_ou_lacuna",
         "encaminhamento", "quem_resolve", "criterio_de_encerramento"),
    ]:
        title(heading)
        story.append(p("Revisão documental concluída em 01/11/2026; fechamento físico/técnico pendente. IDs correspondem aos CSV incluídos, com fontes e critérios completos."))
        for row in rows(filename):
            theme = row.get("tema", row.get("ambientes", ""))
            block = [p(row["id"] + " | " + theme, styles["Heading3"]),
                     p(row[finding]), p("Encaminhamento: " + row[action]),
                     p("Responsável: " + row[owner] + ". Critério completo no CSV, ID " + row["id"] + ".", small)]
            story.append(KeepTogether(block))
        story.append(PageBreak())

    title("Levantamento: datum e prioridades")
    story += [p("O roteiro completo e o índice CSV de medidas acompanham o pacote. Esta folha resume a preparação; não substitui as descrições físicas pendentes."),
              p("1. Identificar M0 junto à entrada, M1 e direção da fachada em croqui/fotos; demonstrar vínculo com o referencial da planta antes de converter PR-X/Y."),
              p("2. Medir faces acabadas na linha a 1000 mm do piso, alturas e desníveis; identificar faces, instrumento e evidências. Janela: largura/altura livre e peitoril em três posições."),
              p("3. PR-EIXO-X = 7400 mm é referência nominal de espelhamento, não dimensão de campo comprovada. Registrar transformação, reflexão quando aplicável e ponto de conferência."),
              p("4. Campos sem medida permanecem vazios. Não usar zero, médias ou aparência do vídeo como medição da unidade."),
              p("15 prioridades do roteiro vigente", styles["Heading2"])]
    priorities = []
    for line in read(FIELD).splitlines():
        if re.match(r"^\| \d+ \|", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            priorities.append([cells[0], cells[1], "Leitura/foto: ____________________"])
    table([["Ordem", "Face ou pendência de identificação", "Registro"]] + priorities,
          [13 * mm, 109 * mm, 50 * mm])
    story.append(PageBreak())
    title("Pranchas de referência: R02 / desenhos R54")
    story.append(p("As 20 folhas seguintes foram anexadas sem redimensionar. Plantas 1:50; elevações/detalhe 1:25. Imprimir A3 a 100%, sem ajustar ao papel; conferir a barra de 50 mm."))
    story.append(p("Incluem PL1-PL3 (paredes, layout e pontos), PT1-PT2 (pontos), E01-E12 (elevações), NC1 (triagem nominal de vãos) e DT1 (fechamento ao teto)."))
    story.append(p("A atualização de caminho/SHA dos envelopes para R55 não reexportou a arquitetura. Paredes, vãos, pisos e esquadrias precisam ser reconciliados antes de uma emissão executiva. Não trocar o rótulo das folhas para sugerir atualização geométrica."))
    story.append(p("As 23 questões anteriores e as fontes no ZIP são o complemento da revisão. O pacote está preparado para consulta ao arquiteto; não foi enviado e não comprova compatibilização física."))

    def footer(c, doc):
        c.setStrokeColor(colors.HexColor("#b9cacc"))
        c.line(19 * mm, 17 * mm, 191 * mm, 17 * mm)
        c.setFont("Helvetica", 7)
        c.drawString(19 * mm, 12 * mm, "Guedala Park | revisão do arquiteto | 01/11/2026 | ESTUDO - NÃO EXECUTAR")
        c.drawRightString(191 * mm, 12 * mm, str(doc.page))

    prefix = BytesIO()
    SimpleDocTemplate(prefix, pagesize=A4, rightMargin=19*mm, leftMargin=19*mm,
                      topMargin=18*mm, bottomMargin=23*mm,
                      title="Guedala Park - Revisão do arquiteto", author="Guedala Park").build(
                          story, onFirstPage=footer, onLaterPages=footer)
    writer = PdfWriter()
    lead = PdfReader(prefix)
    for page in lead.pages:
        writer.add_page(page)
    writer.add_outline_item("Revisão, materiais e levantamento", 0)
    writer.add_outline_item("Pranchas R02 / referência R54", len(lead.pages))
    for page in PdfReader(ROOT / PLANCHES).pages:
        writer.add_page(page)
    writer.add_metadata({"/Title": "Guedala Park - Caderno para revisão do arquiteto",
                         "/Subject": "Anteprojeto nominal; CAD R55 e pranchas R02/R54"})
    with destination.open("wb") as f:
        writer.write(f)
    return len(lead.pages)


def build(zip_path):
    release = json.loads(read("ferramentas/site/current_release.json"))
    cad = ROOT / release["cadPath"]
    if sha(cad.read_bytes()) != release["cadSHA256"]:
        raise ValueError("SHA do modelo não corresponde ao release")
    measured = list(csv.DictReader(StringIO(read("07_Imovel/Medidas_e_impactos.csv"))))
    if len(measured) != 532 or any(r["valor_medido"].strip() for r in measured):
        raise ValueError("Índice de campo mudou; revisar os textos antes de emitir")
    if len(rows(CAD_REVIEW)) != 13 or len(rows(INTERFACES)) != 10:
        raise ValueError("Revisões mudaram; revisar o caderno antes de emitir")
    if release["cadRevision"] != "R55":
        raise ValueError("Revisão CAD mudou; rever pacote")
    zip_path = zip_path.resolve()
    if zip_path.is_relative_to(ROOT):
        raise ValueError("ZIP deve ficar fora do repositório")
    if zip_path.exists():
        raise FileExistsError("Não sobrescrever ZIP já preparado: " + str(zip_path))
    OUT.mkdir(parents=True, exist_ok=True)
    pages = make_pdf(PDF, release)
    files = [
        ("06_Entregas/Arquiteto/Caderno_arquiteto.pdf", "Caderno novo A4 + 20 pranchas A3 R02/R54"),
        (release["cadPath"], "Modelo nativo R55; sem conversão ou modificação"),
        ("02_Modelo_3D/README.md", "Referência do modelo e limites"),
        ("02_Modelo_3D/Relatorio_mudanca.md", "Verificação completa e aceite históricos"),
        (CAD_REVIEW, "13 pendências de arquitetura"),
        (INTERFACES, "10 interfaces prioritárias"),
        (PLANCHES, "Pranchas originais R02/R54, sem redimensionar"),
        ("06_Entregas/Caderno_pranchas/README.md", "Origem e limites das pranchas"),
        ("03_Ambientes/Planta_pontos/Planta_pontos_R00.svg", "Desenho de pontos R01; nome legado R00"),
        ("03_Ambientes/Planta_pontos/README.md", "Funções de pontos e limites"),
        ("03_Ambientes/Planta_pontos/Quadro_cargas.md", "Referência parcial para RT"),
        (SPEC, "Especificações R01 completas"),
        ("01_Programa_e_decisoes/Programa_de_necessidades.md", "Programa R01"),
        (FIELD, "Roteiro completo de datum e prioridades"),
        ("07_Imovel/Medidas_e_impactos.csv", "Índice de campo vazio; não é levantamento"),
        ("04_Moveis/Dependencias/Folgas_ate_15.csv", "Folgas nominais da base anterior"),
        ("03_Ambientes/Planta_mobiliada/Planta_mobiliada_R03.png", "Layout visual R03/cena R54"),
    ]
    manifest = StringIO(newline="")
    w = csv.writer(manifest, delimiter=";")
    w.writerow(["caminho_no_zip", "origem_no_repositorio", "bytes", "sha256", "uso_e_limite"])
    payload = {}
    for path, purpose in files:
        data = (ROOT / path).read_bytes()
        payload[path] = data
        w.writerow([path, path, len(data), sha(data), purpose])
    manifest_bytes = manifest.getvalue().encode("utf-8-sig")
    (OUT / "Manifesto.csv").write_bytes(manifest_bytes)
    start = """GUEDALA PARK - PACOTE PARA REVISAO DO ARQUITETO
Emissão 01/11/2026. Preparado; não enviado. ESTUDO - NÃO EXECUTAR.

1. Abra 06_Entregas/Arquiteto/Caderno_arquiteto.pdf.
2. Consulte o FCStd R55 em 02_Modelo_3D, no FreeCAD.
3. Responda por ARQ-01...13 e INT-01...10 nos CSV correspondentes.
4. Use o roteiro de campo em 07_Imovel; valores reais estão vazios.
5. Confirme o formato editável necessário: IFC/DWG/DXF/STEP não incluídos.

O caderno reúne revisão, quadro de materiais, layout e levantamento, seguidos
das 20 pranchas A3 originais R02/referência R54. Não constitui reexportação
arquitetônica do R55. Imprima os anexos A3 a 100%, sem ajustar ao papel.
O nome Planta_pontos_R00.svg é legado; conteúdo documental R01.
Os fontes Markdown preservam referências ao repositório completo; nem todos
os estudos citados nesses documentos integram este recorte. Comece pelo PDF
e pelos caminhos do Manifesto.csv, que estão presentes no ZIP.

Manifesto.csv registra os hashes dos 17 arquivos de conteúdo.
"""
    payload["LEIA_PRIMEIRO.txt"] = start.encode("utf-8-sig")
    payload["Manifesto.csv"] = manifest_bytes
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in payload.items():
            z.writestr(path, data)
    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(payload)
        for path, data in payload.items():
            assert sha(z.read(path)) == sha(data), path
    assert sha(cad.read_bytes()) == release["cadSHA256"]
    print(json.dumps({"pdf": str(PDF), "paginas_revisao": pages, "paginas_total": pages + 20,
                      "arquivos_zip": len(payload), "zip": str(zip_path),
                      "zip_sha256": sha(zip_path.read_bytes()), "cad_sha256": release["cadSHA256"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, required=True, help="Destino novo fora do repositório")
    args = parser.parse_args()
    build(args.zip)
