/* Fontes explícitas. Medidas nominais; não constitui liberação para fabricação. */
const WORKSHOP_DOCS = [
  {
    "id": "dossie",
    "title": "Guia do montador",
    "category": "Começar",
    "rooms": [
      "all"
    ],
    "status": "Consolidado",
    "summary": "Medidas, ferragens, acabamentos e pendências por módulo.",
    "path": "05_Entregas/Dossie_marcenaria_R45.html"
  },
  {
    "id": "matriz",
    "title": "Medidas dos 20 módulos",
    "category": "Medidas",
    "rooms": [
      "all"
    ],
    "status": "Nominal",
    "summary": "Vãos internos em milímetros e o que falta fechar.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md"
  },
  {
    "id": "interfaces",
    "title": "Uniões entre chapas",
    "category": "Montagem",
    "rooms": [
      "all"
    ],
    "status": "Em estudo",
    "summary": "171 contatos nominais; ligação e caminho da carga a definir.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md"
  },
  {
    "id": "fixas",
    "title": "Ferragens fixas e suspensão",
    "category": "Ferragens",
    "rooms": [
      "all"
    ],
    "status": "Candidatas",
    "summary": "Pinos, conectores, suportes e restrições de montagem.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md"
  },
  {
    "id": "varoes",
    "title": "Varões do roupeiro",
    "category": "Ferragens",
    "rooms": [
      "quarto"
    ],
    "status": "Em estudo",
    "summary": "Quatro varões; oito terminais. Corte depende do suporte.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Varoes.md"
  },
  {
    "id": "bancada",
    "title": "Estrutura da bancada",
    "category": "Montagem",
    "rooms": [
      "escritorio"
    ],
    "status": "Alternativa",
    "summary": "Bancada de 2000 × 700 × 30 mm; reforço separado em estudo.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Bancada.md"
  },
  {
    "id": "minifix",
    "title": "Minifix do aéreo C",
    "category": "Ferragens",
    "rooms": [
      "cozinha"
    ],
    "status": "Alternativa",
    "summary": "20 conjuntos propostos para montagem fixa em chapa de 18 mm.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Minifix_C.md"
  },
  {
    "id": "espelheiro",
    "title": "Pinos e prateleiras do espelheiro",
    "category": "Ferragens",
    "rooms": [
      "banho"
    ],
    "status": "Em estudo",
    "summary": "Oito apoios candidatos; carga da chapa e parede não liberadas.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Espelheiro.md"
  },
  {
    "id": "gavetas",
    "title": "Gavetas, guias e rodízios",
    "category": "Ferragens",
    "rooms": [
      "cozinha",
      "quarto",
      "escritorio"
    ],
    "status": "Em estudo",
    "summary": "Compatibilidade, carga, engates e retirada das gavetas.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html"
  },
  {
    "id": "movento",
    "title": "Alternativa MOVENTO 400",
    "category": "Ferragens",
    "rooms": [
      "escritorio"
    ],
    "status": "Alternativa",
    "summary": "Preserva o útil; conflitos locais e retirada ainda pendentes.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Alternativas_escritorio/Resultado.html"
  },
  {
    "id": "portas",
    "title": "Portas e articulações",
    "category": "Ferragens",
    "rooms": [
      "all"
    ],
    "status": "Em estudo",
    "summary": "Ensaios de portas, banco e mecanismos; não é liberação executiva.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html"
  },
  {
    "id": "cesto",
    "title": "Cesto basculante",
    "category": "Ferragens",
    "rooms": [
      "lavanderia"
    ],
    "status": "Em estudo",
    "summary": "Frente 550 × 521 × 18; saco removível e curso até 55° preservados.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md"
  },
  {
    "id": "mesa-varal",
    "title": "Mesa Berlin e varal",
    "category": "Compatibilização",
    "rooms": [
      "sala",
      "lavanderia"
    ],
    "status": "Em estudo",
    "summary": "Mesa pronta; quadro do varal de 1000 × 500, sem placa de ocultação.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Mesa_e_varal.md"
  },
  {
    "id": "banco",
    "title": "Apoios e estrutura do banco",
    "category": "Montagem",
    "rooms": [
      "sala"
    ],
    "status": "Em estudo",
    "summary": "Duas tampas e armazenamento preservados; apoios e ligações pendentes.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Banco_estrutura/Resultado.html"
  },
  {
    "id": "southco",
    "title": "Southco: fixação e almofadas",
    "category": "Ferragens",
    "rooms": [
      "sala"
    ],
    "status": "Em estudo",
    "summary": "R47 separada da R45; eixo, fixações e batente ainda não fechados.",
    "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html"
  },
  {
    "id": "batente",
    "title": "Batente mecânico do banco",
    "category": "Montagem",
    "rooms": [
      "sala"
    ],
    "status": "Alternativa",
    "summary": "Geometria nominal de parada a 90°; não fabricar pelo eixo hipotético.",
    "path": "01_Projeto/Southco_banco_R47_2026-10-23/Batente_estudo.md"
  },
  {
    "id": "torneiras",
    "title": "Conferência de cubas e torneiras",
    "category": "Compatibilização",
    "rooms": [
      "cozinha",
      "banho"
    ],
    "status": "Em estudo",
    "summary": "Envelopes e medidas disponíveis; instalação depende dos produtos.",
    "path": "01_Projeto/Conferencia_torneiras_2026-10-23/Conferencia.html"
  },
  {
    "id": "purangi",
    "title": "Purangi: vedação e abertura",
    "category": "Compatibilização",
    "rooms": [
      "banho"
    ],
    "status": "Não liberado",
    "summary": "Compatibilidade integral não comprovada; troca não liberada.",
    "path": "01_Projeto/Conferencia_torneiras_2026-10-23/Resultado_vedacao_abertura.md"
  },
  {
    "id": "forno",
    "title": "Forno: grelhas e manutenção",
    "category": "Compatibilização",
    "rooms": [
      "cozinha"
    ],
    "status": "Em estudo",
    "summary": "R02 dos apoios e grelhas removíveis; montagem e ventilação condicionadas.",
    "path": "01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md"
  },
  {
    "id": "cad",
    "title": "Modelo FreeCAD R45",
    "category": "FreeCAD",
    "rooms": [
      "all"
    ],
    "status": "Modelo nominal",
    "summary": "Consolidação dimensional; grupos de estudo não são fabricação aprovada.",
    "path": "01_Projeto/Consolidacao_R45_2026-10-23/Guedala_Park_R45_Consolidado.FCStd"
  },
  {
    "id": "cad-southco",
    "title": "FreeCAD: fixação Southco",
    "category": "FreeCAD",
    "rooms": [
      "sala"
    ],
    "status": "Estudo separado",
    "summary": "Proposta R47 para inspeção; não substitui o modelo principal.",
    "path": "01_Projeto/Southco_banco_R47_2026-10-23/Southco_Fixacao_ESTUDO.FCStd"
  },
  {
    "id": "cad-purangi",
    "title": "FreeCAD: sensibilidade Purangi",
    "category": "FreeCAD",
    "rooms": [
      "banho"
    ],
    "status": "Estudo separado",
    "summary": "Envelopes hipotéticos para conferir abertura; não é CAD certificado.",
    "path": "01_Projeto/Conferencia_torneiras_2026-10-23/Purangi_R45_SENSIBILIDADE.FCStd"
  },
  {
    "id": "executivo",
    "title": "Pranchas executivas e plano de corte",
    "category": "Executivo",
    "rooms": [
      "all"
    ],
    "status": "Pendente",
    "summary": "Faltam cotas de campo, furação, fitas de borda, folgas, ligações e liberação por peça.",
    "path": null
  },
  {
    "id": "planta",
    "title": "Planta oficial do apartamento",
    "category": "Arquitetura",
    "rooms": [
      "all"
    ],
    "status": "Documento de origem",
    "summary": "Referência de planta; não substitui levantamento acabado.",
    "path": "02_Plantas_e_manuais/Planta_oficial.pdf"
  },
  {
    "id": "pisos",
    "title": "Pisos e rodapés",
    "category": "Arquitetura",
    "rooms": [
      "all"
    ],
    "status": "Escolhas e estudos",
    "summary": "Acabamentos, interfaces e condições de instalação. Conferir revisão e quantitativos nas fontes.",
    "path": "01_Projeto/Pisos_e_rodapes.md"
  },
  {
    "id": "luz-quarto",
    "title": "Iluminação do quarto",
    "category": "Iluminação",
    "rooms": [
      "quarto"
    ],
    "status": "Em desenvolvimento",
    "summary": "Comandos, temperaturas e relação com a cabeceira e os armários.",
    "path": "01_Projeto/Portas_e_quarto/Iluminacao_R00.md"
  },
  {
    "id": "instalacoes",
    "title": "Instalações: compatibilização executiva",
    "category": "Instalações",
    "rooms": [
      "all"
    ],
    "status": "Pendente",
    "summary": "Conferir em campo os pontos elétricos, hidráulicos, gás e ventilação; plantas executivas compatibilizadas ainda não reunidas.",
    "path": null
  },
  {
    "id": "levantamento",
    "title": "Levantamento para fabricação",
    "category": "Executivo",
    "rooms": [
      "all"
    ],
    "status": "Pendente",
    "summary": "Cotas acabadas, diagonais, prumo, esquadro, níveis, revestimentos e substratos de fixação precisam de levantamento.",
    "path": null
  }
];
const MODULE_GUIDANCE = {
  "P01": {
    "hardware": [
      "Quatro varões Ø20 nominais; oito terminais. Ø25 é alternativa, não substituição.",
      "Trilhos e gavetas: conferir estudo de mecanismos."
    ],
    "pending": [
      "Resistência dos varões e suportes, carga das prateleiras, montagem das divisórias; mecanismo correr em estudo próprio.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "varoes",
      "gavetas",
      "portas"
    ]
  },
  "P02": {
    "hardware": [
      "Dobradiças de referência em revisão; quatro formas inválidas registradas."
    ],
    "pending": [
      "Corte real em L e união de canto; não calcular carga nem volume útil pelo retângulo envolvente. Apoio LateralApoioPrincipal é proposta.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas"
    ]
  },
  "P03": {
    "hardware": [
      "Mecanismo de correr: conferir estudo de portas."
    ],
    "pending": [
      "Contato é nominal: ligação e transferência de carga não demonstradas. Acoplamento de montagem e capacidade da base sob malas.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas"
    ]
  },
  "P04": {
    "hardware": [
      "Suspensão e ligações dos divisores ainda a dimensionar."
    ],
    "pending": [
      "Vão 851,5 merece reforço ou limite de conteúdo. Fundo contínuo pode ajudar somente se sua união for dimensionada; não presumir três vãos iguais.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas"
    ]
  },
  "P05": {
    "hardware": [
      "Duas portas; dobradiças reguláveis com amortecimento escolhidas."
    ],
    "pending": [
      "Prateleira explicitamente marcada hidráulica a recortar; não liberar corte/armazenamento sem sifão e cuba. Apoio inferior não decorre só de encostar na lateral.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "torneiras",
      "portas"
    ]
  },
  "P06": {
    "hardware": [
      "FGVTN 500 candidata; capacidade publicada corrigida para 35 kg.",
      "Engates, folgas e fixações ainda a fechar."
    ],
    "pending": [
      "Gavetas e ferragens por estudo específico. Fixação e carga da caixa/base ainda condicionais.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "gavetas"
    ]
  },
  "P07": {
    "hardware": [
      "Inserto M4 curto nas grelhas: candidato, retenção no MDF não comprovada."
    ],
    "pending": [
      "Respeitar estudo Fischer R31/R02 de ventilação; a travessa e base não autorizam fechar canais. Ligações, apoios e instalação real pendentes.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "forno"
    ]
  },
  "P08": {
    "hardware": [
      "Seis rodízios, roda 30 e altura total 39 mm; produto exato pendente.",
      "Guias 3 mm com corrida 2 mm são proposta; batente removível a definir."
    ],
    "pending": [
      "Rodízios/seis rodas e mecanismo em estudo de gavetas. Não tratar guias como suporte de peso.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "gavetas"
    ]
  },
  "P09": {
    "hardware": [
      "Dobradiças com amortecimento; suspensão e ligações a detalhar."
    ],
    "pending": [
      "Não apresentar dois nichos íntegros de 298×312: canal técnico corta profundidade. Manter acesso ao duto e definir conexão dos divisores curtos.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Guararapes Azul Petróleo escolhido. Conferir amostra, lote, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas"
    ]
  },
  "P10": {
    "hardware": [
      "20 conjuntos Minifix 262.26.034 + 262.28.920 como alternativa fixa."
    ],
    "pending": [
      "Alternativa Minifix modelada para peças fixas. Se removíveis, criar folga de montagem e apoiar conforme ferragem; não comprar pinos presumindo encaixe sem ajuste.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Guararapes Azul Petróleo escolhido. Conferir amostra, lote, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "minifix",
      "portas"
    ]
  },
  "P11": {
    "hardware": [
      "Suspensão, ligação da prateleira e carga a dimensionar."
    ],
    "pending": [
      "Flexão da prateleira sob 20 kg estimada 2,64 mm imediata; não é carga aprovada. Ligações e suspensão pendentes.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Guararapes Azul Petróleo escolhido. Conferir amostra, lote, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas"
    ]
  },
  "P12": {
    "hardware": [
      "Fixação do divisor e suspensão pendentes."
    ],
    "pending": [
      "Fixação do divisor e suspensão; reserva 100 sobre geladeira tem margem nominal zero além do mínimo considerado.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Guararapes Azul Petróleo escolhido. Conferir amostra, lote, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas"
    ]
  },
  "P13": {
    "hardware": [
      "Apoio e fixação da chapa precisam ser demonstrados."
    ],
    "pending": [
      "100 acima mantém escolha F104, divergente de 300 no manual. Pés reais e suporte da chapa não demonstrados. Não chamar espaço ventilado de nicho fechado.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas"
    ]
  },
  "P14": {
    "hardware": [
      "Pivôs, retenção, amortecimento e limitador a 55° não selecionados.",
      "FGVTN excluiu fornecimento de mecanismo para esta aplicação."
    ],
    "pending": [
      "Seleção do tanque/cuba e hidráulica. Não converter reserva de volume útil 380×350×200 em capacidade garantida. Pivôs/cesto em estudo articulado.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "cesto",
      "mesa-varal"
    ]
  },
  "P15": {
    "hardware": [
      "Suspensão e ligação com fundo ou reforço ainda a definir."
    ],
    "pending": [
      "Cenário de base somente nas laterais dá 4,78 mm imediata para 20 kg. Reforço ou suspensão/ligação com fundo dimensionada, antes de limitar carga.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.",
    "documentIds": [
      "matriz",
      "fixas",
      "mesa-varal"
    ]
  },
  "P16": {
    "hardware": [
      "FGVTN 400 e MOVENTO 400 são alternativas em estudo.",
      "Engates, datum, retirada e interferências ainda pendentes."
    ],
    "pending": [
      "Variante de traseira 20 e folgas da corrediça no estudo de gavetas; preservar compatibilidade com estrutura da bancada.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "gavetas",
      "movento",
      "bancada"
    ]
  },
  "P17": {
    "hardware": [
      "Dobradiças amortecidas; suspensão e ligações ainda a dimensionar."
    ],
    "pending": [
      "Divisórias 18 não equivalem a montantes até piso: carga depende das ligações e da suspensão. Não somar capacidade das ferragens sem distribuição.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "bancada",
      "portas"
    ]
  },
  "P18": {
    "hardware": [
      "Referência vigente BC43 de correr; frente removível M6 em estudo."
    ],
    "pending": [
      "Abertura frontal 507 não é altura útil 509 de versões anteriores. Hidráulica e frente removível M6 dependem de estudo BC43. Não usar Modulo017 histórico oculto.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: bege fosco liso nas frentes e madeira clara nas laterais. Código de chapa pendente; espelheiro com frente espelhada.",
    "documentIds": [
      "matriz",
      "fixas",
      "portas",
      "torneiras",
      "purangi"
    ]
  },
  "P19": {
    "hardware": [
      "Oito pinos Häfele 282.04.711 candidatos para duas prateleiras."
    ],
    "pending": [
      "Oito apoios .711 cabem no estudo separado. Resistência da chapa estreita limita carga; ancoragem da caixa na parede desconhecida.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: bege fosco liso nas frentes e madeira clara nas laterais. Código de chapa pendente; espelheiro com frente espelhada.",
    "documentIds": [
      "matriz",
      "fixas",
      "espelheiro",
      "torneiras",
      "purangi"
    ]
  },
  "P20": {
    "hardware": [
      "Southco candidata com fixação R47 em estudo separado.",
      "Rockler traseira e abertura frontal foram rejeitadas. Batente independente pendente."
    ],
    "pending": [
      "Fechar eixo real, ligações, apoios, almofadas e batente independente conforme R47. Southco permanece candidata; Rockler traseira e abertura frontal rejeitadas.",
      "Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte."
    ],
    "finish": "Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.",
    "documentIds": [
      "matriz",
      "fixas",
      "banco",
      "southco",
      "batente",
      "mesa-varal"
    ]
  }
};
function WORKSHOP_DOC_URL(doc){return doc.path ? "docs/"+doc.path+(doc.path.endsWith(".md") ? ".html" : "") : null;}
