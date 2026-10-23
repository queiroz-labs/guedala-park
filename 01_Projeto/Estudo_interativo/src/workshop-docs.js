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
  },
  {
    "id": "acabamentos-r13",
    "title": "Branco TX nos interiores",
    "category": "Acabamentos",
    "rooms": [
      "all"
    ],
    "status": "Escolhido",
    "summary": "Diretriz vigente por face: interiores Branco TX e padrões escolhidos nas faces aparentes.",
    "path": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
  },
  {
    "id": "planta-cotada",
    "title": "Planta cotada · distâncias entre paredes",
    "category": "Arquitetura",
    "rooms": [
      "all"
    ],
    "status": "R13",
    "summary": "Cotas oficiais por ambiente e diferenças da reconstrução identificadas.",
    "path": "05_Entregas/Planta_cotada_R13/index.html"
  },
  {
    "id": "fichas",
    "title": "Fichas completas dos 20 móveis",
    "category": "Começar",
    "rooms": [
      "all"
    ],
    "status": "R13",
    "summary": "Medidas, vistas, peças, acabamentos, ferragens e montagem.",
    "path": "05_Entregas/Fichas_fabricacao_R13/index.html"
  },
  {
    "id": "campo",
    "title": "O que medir no apartamento",
    "category": "Levantamento",
    "rooms": [
      "all"
    ],
    "status": "Preencher em campo",
    "summary": "Folha por móvel: dimensões físicas, instalações, níveis e paredes.",
    "path": "05_Entregas/Fichas_fabricacao_R13/Levantamento.html"
  },
  {
    "id": "ficha-P01",
    "title": "P01 · Roupeiro",
    "category": "Ficha de montagem",
    "rooms": [
      "quarto"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P01.html"
  },
  {
    "id": "ficha-P02",
    "title": "P02 · Canto em L",
    "category": "Ficha de montagem",
    "rooms": [
      "quarto"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P02.html"
  },
  {
    "id": "ficha-P03",
    "title": "P03 · Maleiro",
    "category": "Ficha de montagem",
    "rooms": [
      "quarto"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P03.html"
  },
  {
    "id": "ficha-P04",
    "title": "P04 · Aéreo da cabeceira",
    "category": "Ficha de montagem",
    "rooms": [
      "quarto"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P04.html"
  },
  {
    "id": "ficha-P05",
    "title": "P05 · Gabinete da pia",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P05.html"
  },
  {
    "id": "ficha-P06",
    "title": "P06 · Gaveteiro da cozinha",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P06.html"
  },
  {
    "id": "ficha-P07",
    "title": "P07 · Módulo de cocção",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P07.html"
  },
  {
    "id": "ficha-P08",
    "title": "P08 · Gaveta de limpeza",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P08.html"
  },
  {
    "id": "ficha-P09",
    "title": "P09 · Aéreo D · depurador",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P09.html"
  },
  {
    "id": "ficha-P10",
    "title": "P10 · Aéreo C · uso diário",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P10.html"
  },
  {
    "id": "ficha-P11",
    "title": "P11 · Aéreo B · micro",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P11.html"
  },
  {
    "id": "ficha-P12",
    "title": "P12 · Aéreo A · geladeira",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P12.html"
  },
  {
    "id": "ficha-P13",
    "title": "P13 · Apoio do micro",
    "category": "Ficha de montagem",
    "rooms": [
      "cozinha"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P13.html"
  },
  {
    "id": "ficha-P14",
    "title": "P14 · Gabinete tanque e cesto",
    "category": "Ficha de montagem",
    "rooms": [
      "lavanderia"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P14.html"
  },
  {
    "id": "ficha-P15",
    "title": "P15 · Aéreo da lavanderia",
    "category": "Ficha de montagem",
    "rooms": [
      "lavanderia"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P15.html"
  },
  {
    "id": "ficha-P16",
    "title": "P16 · Gaveteiro do escritório",
    "category": "Ficha de montagem",
    "rooms": [
      "escritorio"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P16.html"
  },
  {
    "id": "ficha-P17",
    "title": "P17 · Aéreo do escritório",
    "category": "Ficha de montagem",
    "rooms": [
      "escritorio"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P17.html"
  },
  {
    "id": "ficha-P18",
    "title": "P18 · Gabinete do banheiro",
    "category": "Ficha de montagem",
    "rooms": [
      "banho"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P18.html"
  },
  {
    "id": "ficha-P19",
    "title": "P19 · Espelheiro",
    "category": "Ficha de montagem",
    "rooms": [
      "banho"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P19.html"
  },
  {
    "id": "ficha-P20",
    "title": "P20 · Banco baú",
    "category": "Ficha de montagem",
    "rooms": [
      "sala"
    ],
    "status": "R13",
    "summary": "Ficha imprimível, peças CSV e fechamentos técnicos.",
    "path": "05_Entregas/Fichas_fabricacao_R13/P20.html"
  }
];
const MODULE_GUIDANCE = {
  "P01": {
    "hardware": [
      "Quatro varões Ø20 nominais; oito terminais. Ø25 é alternativa, não substituição.",
      "Trilhos e gavetas: conferir estudo de mecanismos."
    ],
    "pending": [
      "Confirmar envelope real, retenção antidescarrilamento, padrão de furação, seções completas dos trilhos e posição dos freios.",
      "Dimensionar suporte dos trilhos e ligações da base/topo; capacidade de60 kg por porta não dimensiona a marcenaria.",
      "Determinar datum vertical, recortes traseiros e desenho dos engates da FGVTN; o STEP400 não deve ser escalado para500.",
      "Fechar carga útil incluindo massa da caixa, frente, acessórios e conteúdo; 35kg não significa35kg de conteúdo.",
      "Compatibilizar suportes centrais: eixo superior82mm abaixo da base do maleiro e inferior52mm abaixo da prateleira; altura externa63 do suporte não é a cota eixo–face.",
      "Definir carga dos varões e das prateleiras; rigidez de tubo e fixação no MDF são verificações separadas.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Portas externas do roupeiro: amadeirado/Arenza; interiores e gavetas internas Branco TX. offwhite no CAD é referência anterior; não recolorido nesta auditoria.",
      "Resistência dos varões e suportes, carga das prateleiras, montagem das divisórias; mecanismo correr em estudo próprio.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P01",
      "matriz",
      "fixas",
      "varoes",
      "gavetas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P01",
      "name": "Roupeiro",
      "room": "quarto",
      "dimensions": [
        2000.0,
        644.0,
        2132.0
      ],
      "internalMeasures": "Dois setores superiores com 973 de largura; profundidade 550. Base topo 80; varões superiores eixo 2050. Nichos inferiores de sapatos 355×400; alturas livres 242 /242 /182 entre base e níveis 340/600/800. Varões baixos 332 entre divisórias.",
      "panels": [
        {
          "id": "Peca206",
          "name": "Lateral direita",
          "dimensions": [
            2132.0,
            568.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca206 (Lateral direita016); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca207",
          "name": "Lateral esquerda",
          "dimensions": [
            2132.0,
            568.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca207 (Lateral esquerda); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca208",
          "name": "Fundo",
          "dimensions": [
            2096.0,
            1964.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca208 (Fundo)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca209",
          "name": "Base · topo 80 mm",
          "dimensions": [
            1964.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca209 (Base · topo 80 mm)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca210",
          "name": "Divisória",
          "dimensions": [
            2052.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca210 (Divisória)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca211",
          "name": "Sapateira · três níveis",
          "dimensions": [
            400.0,
            355.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca211 (Sapateira · três níveis)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca212",
          "name": "Sapateira · três níveis",
          "dimensions": [
            400.0,
            355.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca212 (Sapateira · três níveis001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca213",
          "name": "Sapateira · três níveis",
          "dimensions": [
            400.0,
            355.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca213 (Sapateira · três níveis002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR08",
          "name": "Lateral comum esquerda · Gaveta de roupa - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR08 (Lateral comum esquerda · Gaveta de roupa - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR001",
          "name": "Lateral comum direita · Gaveta de roupa - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR001 (Lateral comum direita · Gaveta de roupa - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR002",
          "name": "Fundo comum · Gaveta de roupa - proposta R08",
          "dimensions": [
            490.0,
            323.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR002 (Fundo comum · Gaveta de roupa - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR003",
          "name": "Traseira comum · Gaveta de roupa - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR003 (Traseira comum · Gaveta de roupa - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR004",
          "name": "Dianteira comum16 · Gaveta de roupa - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR004 (Dianteira comum16 · Gaveta de roupa - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR005",
          "name": "Frente preservada · Gaveta de roupa - proposta R08",
          "dimensions": [
            353.0,
            142.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR005 (Frente preservada · Gaveta de roupa - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR012",
          "name": "Lateral comum esquerda · Gaveta de roupa001 - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR012 (Lateral comum esquerda · Gaveta de roupa001 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR013",
          "name": "Lateral comum direita · Gaveta de roupa001 - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR013 (Lateral comum direita · Gaveta de roupa001 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR014",
          "name": "Fundo comum · Gaveta de roupa001 - proposta R08",
          "dimensions": [
            490.0,
            323.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR014 (Fundo comum · Gaveta de roupa001 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR015",
          "name": "Traseira comum · Gaveta de roupa001 - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR015 (Traseira comum · Gaveta de roupa001 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR016",
          "name": "Dianteira comum16 · Gaveta de roupa001 - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR016 (Dianteira comum16 · Gaveta de roupa001 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR017",
          "name": "Frente 130 (R29, era 142) · Gaveta de roupa001 - proposta R08",
          "dimensions": [
            353.0,
            130.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR017 (Frente 130 (R29, era 142) · Gaveta de roupa001 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca226",
          "name": "Sapateira · três níveis",
          "dimensions": [
            400.0,
            355.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca226 (Sapateira · três níveis003)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca227",
          "name": "Sapateira · três níveis",
          "dimensions": [
            400.0,
            355.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca227 (Sapateira · três níveis004)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca228",
          "name": "Sapateira · três níveis",
          "dimensions": [
            400.0,
            355.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca228 (Sapateira · três níveis005)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR024",
          "name": "Lateral comum esquerda · Gaveta de roupa002 - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR024 (Lateral comum esquerda · Gaveta de roupa002 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR025",
          "name": "Lateral comum direita · Gaveta de roupa002 - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR025 (Lateral comum direita · Gaveta de roupa002 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR026",
          "name": "Fundo comum · Gaveta de roupa002 - proposta R08",
          "dimensions": [
            490.0,
            323.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR026 (Fundo comum · Gaveta de roupa002 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR027",
          "name": "Traseira comum · Gaveta de roupa002 - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR027 (Traseira comum · Gaveta de roupa002 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR028",
          "name": "Dianteira comum16 · Gaveta de roupa002 - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR028 (Dianteira comum16 · Gaveta de roupa002 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR029",
          "name": "Frente preservada · Gaveta de roupa002 - proposta R08",
          "dimensions": [
            353.0,
            142.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR029 (Frente preservada · Gaveta de roupa002 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR036",
          "name": "Lateral comum esquerda · Gaveta de roupa003 - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR036 (Lateral comum esquerda · Gaveta de roupa003 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR037",
          "name": "Lateral comum direita · Gaveta de roupa003 - proposta R08",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR037 (Lateral comum direita · Gaveta de roupa003 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR038",
          "name": "Fundo comum · Gaveta de roupa003 - proposta R08",
          "dimensions": [
            490.0,
            323.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR038 (Fundo comum · Gaveta de roupa003 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR039",
          "name": "Traseira comum · Gaveta de roupa003 - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR039 (Traseira comum · Gaveta de roupa003 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR040",
          "name": "Dianteira comum16 · Gaveta de roupa003 - proposta R08",
          "dimensions": [
            313.0,
            73.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR040 (Dianteira comum16 · Gaveta de roupa003 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR041",
          "name": "Frente 130 (R29, era 142) · Gaveta de roupa003 - proposta R08",
          "dimensions": [
            353.0,
            130.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR041 (Frente 130 (R29, era 142) · Gaveta de roupa003 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca241",
          "name": "Divisória",
          "dimensions": [
            1002.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca241 (Divisória001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca242",
          "name": "Divisória",
          "dimensions": [
            1002.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca242 (Divisória002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca243",
          "name": "Divisória",
          "dimensions": [
            1002.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca243 (Divisória003)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca244",
          "name": "Divisória",
          "dimensions": [
            1002.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca244 (Divisória004)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca245",
          "name": "Prateleira curta · topo 1100",
          "dimensions": [
            705.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca245 (Prateleira curta · topo 1100)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca246",
          "name": "Prateleira curta · topo 1101",
          "dimensions": [
            705.0,
            550.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca246 (Prateleira curta · topo 1101)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca247",
          "name": "Roupeiro — porta direita — deslizar para esquerda — frente proposta",
          "dimensions": [
            1999.0,
            995.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca247 (Roupeiro — porta direita — deslizar para esquerda — frente proposta); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca248",
          "name": "Roupeiro — porta esquerda — deslizar para direita — frente proposta",
          "dimensions": [
            1999.0,
            995.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca248 (Roupeiro — porta esquerda — deslizar para direita — frente proposta); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Kit de correr para duas folhas",
          "reference": "Rometal RO-62 + Guia Flex 4032",
          "quantity": 2,
          "unit": "kit de 1 porta",
          "status": "candidato",
          "assembly": "Cada kit contém 2 carros, 2 guias e 2 freios; conferir retenções e conteúdo comercial.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "derivation": "2 folhas × 1 kit por folha"
        },
        {
          "item": "Carros integrantes dos kits RO-62",
          "reference": "Componentes do RO-62 / Guia Flex 4032",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos 2 kits; linha de conferência, não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "includedIn": "Kit de correr para duas folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Guias integrantes dos kits RO-62",
          "reference": "Componentes do RO-62 / Guia Flex 4032",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos 2 kits; linha de conferência, não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "includedIn": "Kit de correr para duas folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Freios integrantes dos kits RO-62",
          "reference": "Componentes do RO-62 / Guia Flex 4032",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos 2 kits; linha de conferência, não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "includedIn": "Kit de correr para duas folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Trilhos inferiores",
          "reference": "Rometal RM-023",
          "quantity": null,
          "unit": "trecho / barra a detalhar",
          "status": "pendente",
          "assembly": "Quantidade comercial e comprimento de corte dependem do plano das vias; não converter quatro kits em quatro barras. RM-025 largura28 e RM-023 largura34 conforme manual citado.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Para18–20, o manual aponta RM-025 superior/largura28 e RM-023 inferior/largura34. Guia Flex centrado na espessura e recuo de30 indicado; freios com posição a regular. Fontes PDF/TXT e páginas renderizadas emFontes. RO-47 e guia da linha Origem também arquivados como comparação. Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/frei"
            }
          ]
        },
        {
          "item": "Trilhos superiores",
          "reference": "Rometal RM-025",
          "quantity": null,
          "unit": "trecho / barra a detalhar",
          "status": "pendente",
          "assembly": "Quantidade comercial e comprimento de corte dependem do plano das vias; não converter quatro kits em quatro barras. RM-025 largura28 e RM-023 largura34 conforme manual citado.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Para18–20, o manual aponta RM-025 superior/largura28 e RM-023 inferior/largura34. Guia Flex centrado na espessura e recuo de30 indicado; freios com posição a regular. Fontes PDF/TXT e páginas renderizadas emFontes. RO-47 e guia da linha Origem também arquivados como comparação. Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/frei"
            }
          ]
        },
        {
          "item": "Parafusos carros RO-62",
          "reference": "3,5 × 14 CC",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Dimensões documentais; falta contar furos efetivos da configuração e verificar piloto/penetração.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/freios,3,5×12 CF para retenção. Isso não define pilotos, resistência, comprimento efetivo de penetração, encaixe nem a fixação de cada suporte. Eixos do padrão MDF22/86 a partir da borda e8,5/32,5 acima da base estão desenhados como linhas, sem furos ou diâmetro de piloto. Espelhamento do lado direito é proposta a confirmar. **Não há STEP oficial nas fontes consultadas.** As peças CAD de carro, guia, retenção, freio e perfis são reservas transparentes, com dimensões hipotéticas explícitas"
            }
          ]
        },
        {
          "item": "Parafusos guias/freios RO-62",
          "reference": "3,5 × 22 CC",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Dimensões documentais; falta contar furos efetivos da configuração e verificar piloto/penetração.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/freios,3,5×12 CF para retenção. Isso não define pilotos, resistência, comprimento efetivo de penetração, encaixe nem a fixação de cada suporte. Eixos do padrão MDF22/86 a partir da borda e8,5/32,5 acima da base estão desenhados como linhas, sem furos ou diâmetro de piloto. Espelhamento do lado direito é proposta a confirmar. **Não há STEP oficial nas fontes consultadas.** As peças CAD de carro, guia, retenção, freio e perfis são reservas transparentes, com dimensões hipotéticas explícitas"
            }
          ]
        },
        {
          "item": "Parafusos retenção RO-62",
          "reference": "3,5 × 12 CF",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Dimensões documentais; falta contar furos efetivos da configuração e verificar piloto/penetração.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/freios,3,5×12 CF para retenção. Isso não define pilotos, resistência, comprimento efetivo de penetração, encaixe nem a fixação de cada suporte. Eixos do padrão MDF22/86 a partir da borda e8,5/32,5 acima da base estão desenhados como linhas, sem furos ou diâmetro de piloto. Espelhamento do lado direito é proposta a confirmar. **Não há STEP oficial nas fontes consultadas.** As peças CAD de carro, guia, retenção, freio e perfis são reservas transparentes, com dimensões hipotéticas explícitas"
            }
          ]
        },
        {
          "item": "Corrediças ocultas, 500 mm",
          "reference": "FGVTN 54FGOC12500TSX0",
          "quantity": 4,
          "unit": "par",
          "status": "candidato",
          "assembly": "Capacidade publicada35kg; curso475 ±3mm, não500. Modelo de caixa legado exige compatibilização.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
              "trecho": "Roupeiro — Gaveta, 001, 002, 003 | 54FGOC12500TSX0 | 4 pares | 355 × 550 | 344 externos / 314 internos × 500 | +30 sobre mínimo 520 | Cozinha — Gaveta004, 005, 006 | 54FGOC12500TSX0 | 3 pares | 583 × 572 | 572 externos / 542 internos × 500 | +52 sobre mínimo 520 | Escritório — Gaveta008, 009 | 54FGOC12400TSX0 | 2 pares | 364 × 412 na R44; 432 na variante R04 | 353 externos / 323 internos × 400 | −8 R44; +12 R04 | São 7 pares de 500 + 2 pares de 400, total 18 guias e 9 conjuntos de engates esquerdo/direito compatíveis. Conferir se os engates vêm nos kits para evitar compra duplicada. Não misturar engate convencional com opcional 3D sem o desenho da combinação exata. Parafusos de fixação e seus comprimentos aguardam desenho definitivo, espessura real e substrato. As caixas atuais vieram de outra família: +1 mm na largura interna/externa e +"
            }
          ],
          "derivation": "1 par por gaveta: 4 gavetas"
        },
        {
          "item": "Engates das corrediças 500",
          "reference": "Par esquerdo/direito correspondente ao kit FGVTN 500; SKU não confirmado",
          "quantity": 4,
          "unit": "par E/D",
          "status": "pendente",
          "assembly": "Não duplicar se os engates vierem incluídos. Não misturar convencional e opcional3D.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
              "trecho": "São 7 pares de 500 + 2 pares de 400, total 18 guias e 9 conjuntos de engates esquerdo/direito compatíveis. Conferir se os engates vêm nos kits para evitar compra duplicada. Não misturar engate convencional com opcional 3D sem o desenho da combinação exata. Parafusos de fixação e seus comprimentos aguardam desenho definitivo, espessura real e substrato. As caixas atuais vieram de outra família: +1 mm na largura interna/externa e +10 mm n"
            }
          ],
          "includedWhenBundled": true
        },
        {
          "item": "Parafusos das guias e engates",
          "reference": null,
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Definir pelo desenho e material reais; não quantificar pela geometria de outra família.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Parafusos guias;Conforme furo e substrato;A definir;peca;NAO QUANTIFICADO;Gabarito de cada comprimento e resistencia do substrato Fixacao frentes escritorio;Parafuso4x30 arruela1.2 conforme estudoR04;8;conjunto;HIPOTESE GEOMETRICA;Resistenc"
            }
          ]
        },
        {
          "item": "Varões, cortes nominais",
          "reference": "Candidato Ø20 Häfele 801.01.702; alternativa Ø25 Bigfer 0907266400",
          "quantity": 4,
          "unit": "corte",
          "status": "candidato",
          "assembly": "2 vãos973 +2 vãos332 =2610mm nominais. O corte final desconta encaixe dos suportes; não cortar pelos vãos.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Varoes.md",
              "trecho": "O modelo possui quatro cilindros Ø20: dois vãos nominais 973 e dois 332. Eixos superiores emZ2050, inferioresZ1030; todosY3655. A soma nominal é 2610 mm, antes de descontos dos suportes e perdas de corte. Oito suportes terminais são necessários. Cilindro CAD maciço não demonstra que o produto real seja maciço nem define sua resistência. ## Candidatos documentados Para manter Ø20, o catálogo Häfele apresenta tubo de aço niquelado 801.01.702, barra 2500 mm, parede 0,7 mm; suporte terminal 803.51.702, latão niquelado, dimensão 28×12,5 mm, placa e luva roscada. Suporte central 802.02.220 é aparafu"
            }
          ],
          "derivation": "2 × 973 + 2 × 332 = 2610 mm antes dos descontos"
        },
        {
          "item": "Suportes terminais dos varões",
          "reference": "Ø20 Häfele 803.51.702; alternativa Ø25 Bigfer 9168010111",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 terminais por varão; Ø20 e Ø25 pertencem a alternativas incompatíveis entre si.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Varoes.md",
              "trecho": "Para manter Ø20, o catálogo Häfele apresenta tubo de aço niquelado 801.01.702, barra 2500 mm, parede 0,7 mm; suporte terminal 803.51.702, latão niquelado, dimensão 28×12,5 mm, placa e luva roscada. Suporte central 802.02.220 é aparafusado sob prateleira, dimensão 63×38×19 mm. [Häfele Hotel Assortment, página 69](https://www.hafeleindia.co.in/Catalogues/PDF/HotelAssortment2020.pdf). Para alternativa nacional de Ø25, o catálogo Bigfer informa tubo 0907266400, aço cromado 25×3000 mm, parede 0,75 mm e suporte terminal redondo 9168010111. Não traz carga admissível do conjunto no trecho consultado. [Bigfer, catálogo do marceneiro, página 68](https://www.bigfer.com.br/catalogo-marceneiro-3-edicao_revisado/). A alterna"
            }
          ],
          "derivation": "4 varões × 2 terminais"
        },
        {
          "item": "Suportes centrais dos dois varões longos",
          "reference": "Häfele 802.02.220 para a alternativa Ø20",
          "quantity": 2,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Somente se adotados e compatibilizados; não somar como compra liberada.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Varoes.md",
              "trecho": "Dois apoios centrais são uma alternativa para os varões longos, não item liberado para compra. A carga admissível de cada conjunto e da fixação no MDF continua pendente do fabricante/marceneiro."
            }
          ],
          "optional": true
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "33contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Amadeirado; referência Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:414"
        }
      ],
      "fieldChecks": [
        {
          "id": "P01-CAMPO-1",
          "measure": "Medir largura acabada em três alturas, profundidade disponível, pé-direito, diagonais, prumo e encontro com rodapé.",
          "method": "Trena/laser, nível e diagonais; registrar mínimo e máximo.",
          "affects": "Ajuste das laterais, arremate ao teto, acesso pela cama e trilhos.",
          "value": null
        },
        {
          "id": "PAREDE-QUARTO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Confirmar envelope real, retenção antidescarrilamento, padrão de furação, seções completas dos trilhos e posição dos freios.",
        "Dimensionar suporte dos trilhos e ligações da base/topo; capacidade de60 kg por porta não dimensiona a marcenaria.",
        "Determinar datum vertical, recortes traseiros e desenho dos engates da FGVTN; o STEP400 não deve ser escalado para500.",
        "Fechar carga útil incluindo massa da caixa, frente, acessórios e conteúdo; 35kg não significa35kg de conteúdo.",
        "Compatibilizar suportes centrais: eixo superior82mm abaixo da base do maleiro e inferior52mm abaixo da prateleira; altura externa63 do suporte não é a cota eixo–face.",
        "Definir carga dos varões e das prateleiras; rigidez de tubo e fixação no MDF são verificações separadas.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Portas externas do roupeiro: amadeirado/Arenza; interiores e gavetas internas Branco TX. offwhite no CAD é referência anterior; não recolorido nesta auditoria.",
        "Resistência dos varões e suportes, carga das prateleiras, montagem das divisórias; mecanismo correr em estudo próprio.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Preservar quatro gavetas internas e dois setores superiores; regular o sistema real de correr antes de conferir acesso às gavetas.",
        "Montar divisórias e apoios com ligação dimensionada; contato nominal não comprova suporte.",
        "AP = vão vertical −35 mm e transpasse30 mm são compatíveis nominalmente. Passo38 e distribuição10/25 da folga vertical são hipóteses, não cotas executivas.",
        "Caixas FGVTN em laterais15: largura interna A−41 e externa A−11; folga centrada nominal5,5mm/lado. Compatibilizar caixa/recortes/engates antes do corte.",
        "Furos de terminais opostos na divisória18 devem ser desencontrados ou ter profundidades compatíveis."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Varoes.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P01.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P01.svg"
    }
  },
  "P02": {
    "hardware": [
      "Dobradiças de referência em revisão; quatro formas inválidas registradas."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Detalhar união das placas em L e apoio lateral proposto; o retângulo envolvente650 ×1050 não é área útil da placa.",
      "Revisar as quatro formas de dobradiças do canto apontadas como inválidas no inventário.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Corte real em L e união de canto; não calcular carga nem volume útil pelo retângulo envolvente. Apoio LateralApoioPrincipal é proposta.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P02",
      "matriz",
      "fixas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P02",
      "name": "Canto em L",
      "room": "quarto",
      "dimensions": [
        650.0,
        1050.0,
        308.0
      ],
      "internalMeasures": "Base topo 2150, tampo começa 2422: altura 272. Fundos 18. Caixa envolvente 650×1050 não representa área útil da placa em L.",
      "panels": [
        {
          "id": "PlacaL",
          "name": "Base em L",
          "dimensions": [
            1050.0,
            650.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PlacaL (Base em L); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PlacaL001",
          "name": "Tampo em L",
          "dimensions": [
            1050.0,
            650.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PlacaL001 (Tampo em L); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca255",
          "name": "Fundo do braço principal",
          "dimensions": [
            632.0,
            272.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca255 (Fundo do braço principal)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca256",
          "name": "Fundo do retorno",
          "dimensions": [
            1032.0,
            272.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca256 (Fundo do retorno)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "LateralApoioPrincipal",
          "name": "Lateral 18 mm de apoio da principal - proposta R03",
          "dimensions": [
            612.0,
            272.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD LateralApoioPrincipal (Lateral 18 mm de apoio da principal - proposta R03)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteSimplesR04",
          "name": "Porta A - canecos comuns",
          "dimensions": [
            306.0,
            271.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteSimplesR04 (Porta A - canecos comuns); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteSimplesR001",
          "name": "Porta B - canecos comuns",
          "dimensions": [
            306.0,
            271.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteSimplesR001 (Porta B - canecos comuns); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioPortaBR04",
          "name": "Lateral 18 mm de apoio da porta B - proposta",
          "dimensions": [
            272.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioPortaBR04 (Lateral 18 mm de apoio da porta B - proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FaixaQuinaAR04",
          "name": "Faixa fixa A 142 mm - proposta",
          "dimensions": [
            306.0,
            142.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FaixaQuinaAR04 (Faixa fixa A 142 mm - proposta); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FaixaQuinaBR04",
          "name": "Faixa fixa B 124 mm - proposta",
          "dimensions": [
            306.0,
            124.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FaixaQuinaBR04 (Faixa fixa B 124 mm - proposta); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD)",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 2 dobradiças = 4 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Canto A/B | 271 × 306 × 18 | 2 | 2 | 0.97 / 1.12 / 1.34 | alta/estreita | Banheiro correr R43 | 292 × 500 × 18 | 2 | correr | 1.71 / 1.97 / 2.37 | alta/estreita | As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A ta"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "0contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Amadeirado; referência Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:414"
        }
      ],
      "fieldChecks": [
        {
          "id": "P02-CAMPO-1",
          "measure": "Medir os dois braços acabados, ângulo real, pé-direito e desvios das paredes no canto.",
          "method": "Duas diagonais e nível; croqui com referências fixas.",
          "affects": "Contorno real em L, faixas de compensação e posição das portas.",
          "value": null
        },
        {
          "id": "PAREDE-QUARTO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Detalhar união das placas em L e apoio lateral proposto; o retângulo envolvente650 ×1050 não é área útil da placa.",
        "Revisar as quatro formas de dobradiças do canto apontadas como inválidas no inventário.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Corte real em L e união de canto; não calcular carga nem volume útil pelo retângulo envolvente. Apoio LateralApoioPrincipal é proposta.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Usar o contorno real em L; o retângulo 650 × 1050 não é plano de corte.",
        "Conferir portas A/B e porta vizinha em conjunto; faixas e apoios continuam propostas.",
        "Manter duas portas independentes e quatro dobradiças comuns; canto articulado com71T7550/79T8500 é histórico superado."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P02.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P02.svg"
    }
  },
  "P03": {
    "hardware": [
      "Mecanismo de correr: conferir estudo de portas."
    ],
    "pending": [
      "Confirmar envelope real, retenção antidescarrilamento, padrão de furação, seções completas dos trilhos e posição dos freios.",
      "Dimensionar suporte dos trilhos e ligações da base/topo; capacidade de60 kg por porta não dimensiona a marcenaria.",
      "Maleiro: folhas670 ×237 ×18 são baixas/largas. Não adotar Comfort240: massa estimada2,14–2,57kg abaixo da faixa mínima15kg do acessório.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Contato é nominal: ligação e transferência de carga não demonstradas. Acoplamento de montagem e capacidade da base sob malas.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P03",
      "matriz",
      "fixas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P03",
      "name": "Maleiro",
      "room": "quarto",
      "dimensions": [
        1350.0,
        650.0,
        308.0
      ],
      "internalMeasures": "Vão 1314×632×272 entre faces. BaseZ2132–2150; topo 2422–2440. Divisória do roupeiroX6381–6399 chega à base e separa faixas 973 e 323 ao longo da largura.",
      "panels": [
        {
          "id": "Peca259",
          "name": "Lateral direita",
          "dimensions": [
            650.0,
            308.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca259 (Lateral direita017); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca260",
          "name": "Lateral esquerda",
          "dimensions": [
            650.0,
            308.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca260 (Lateral esquerda001); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca261",
          "name": "Fundo",
          "dimensions": [
            1314.0,
            272.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca261 (Fundo001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca262",
          "name": "Base",
          "dimensions": [
            1314.0,
            632.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca262 (Base); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca263",
          "name": "Tampo",
          "dimensions": [
            1314.0,
            632.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca263 (Tampo)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca264",
          "name": "Maleiro — porta direita — deslizar para esquerda — frente proposta",
          "dimensions": [
            670.0,
            237.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca264 (Maleiro — porta direita — deslizar para esquerda — frente proposta); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca265",
          "name": "Maleiro — porta esquerda — deslizar para direita — frente proposta",
          "dimensions": [
            670.0,
            237.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca265 (Maleiro — porta esquerda — deslizar para direita — frente proposta); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Kit de correr para duas folhas",
          "reference": "Rometal RO-62 + Guia Flex 4032",
          "quantity": 2,
          "unit": "kit de 1 porta",
          "status": "candidato",
          "assembly": "Cada kit contém 2 carros, 2 guias e 2 freios; conferir retenções e conteúdo comercial.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "derivation": "2 folhas × 1 kit por folha"
        },
        {
          "item": "Carros integrantes dos kits RO-62",
          "reference": "Componentes do RO-62 / Guia Flex 4032",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos 2 kits; linha de conferência, não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "includedIn": "Kit de correr para duas folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Guias integrantes dos kits RO-62",
          "reference": "Componentes do RO-62 / Guia Flex 4032",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos 2 kits; linha de conferência, não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "includedIn": "Kit de correr para duas folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Freios integrantes dos kits RO-62",
          "reference": "Componentes do RO-62 / Guia Flex 4032",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos 2 kits; linha de conferência, não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada; não transformar estes em kitsRO-62. Não contar subcomponentes como novos kits. 2. Portas de abrir: decisões que já podem ser tomadas A orientação oficial Blum relaciona quantidade a peso acabado, altura, largura e material; dá2dobradiças como referência para4–6kg e3para6–12kg, com aplicação até600mm de largura. Recomenda maior afastamento possível entre dobradi"
            }
          ],
          "includedIn": "Kit de correr para duas folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Trilhos inferiores",
          "reference": "Rometal RM-023",
          "quantity": null,
          "unit": "trecho / barra a detalhar",
          "status": "pendente",
          "assembly": "Quantidade comercial e comprimento de corte dependem do plano das vias; não converter quatro kits em quatro barras. RM-025 largura28 e RM-023 largura34 conforme manual citado.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Para18–20, o manual aponta RM-025 superior/largura28 e RM-023 inferior/largura34. Guia Flex centrado na espessura e recuo de30 indicado; freios com posição a regular. Fontes PDF/TXT e páginas renderizadas emFontes. RO-47 e guia da linha Origem também arquivados como comparação. Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/frei"
            }
          ]
        },
        {
          "item": "Trilhos superiores",
          "reference": "Rometal RM-025",
          "quantity": null,
          "unit": "trecho / barra a detalhar",
          "status": "pendente",
          "assembly": "Quantidade comercial e comprimento de corte dependem do plano das vias; não converter quatro kits em quatro barras. RM-025 largura28 e RM-023 largura34 conforme manual citado.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Para18–20, o manual aponta RM-025 superior/largura28 e RM-023 inferior/largura34. Guia Flex centrado na espessura e recuo de30 indicado; freios com posição a regular. Fontes PDF/TXT e páginas renderizadas emFontes. RO-47 e guia da linha Origem também arquivados como comparação. Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/frei"
            }
          ]
        },
        {
          "item": "Parafusos carros RO-62",
          "reference": "3,5 × 14 CC",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Dimensões documentais; falta contar furos efetivos da configuração e verificar piloto/penetração.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/freios,3,5×12 CF para retenção. Isso não define pilotos, resistência, comprimento efetivo de penetração, encaixe nem a fixação de cada suporte. Eixos do padrão MDF22/86 a partir da borda e8,5/32,5 acima da base estão desenhados como linhas, sem furos ou diâmetro de piloto. Espelhamento do lado direito é proposta a confirmar. **Não há STEP oficial nas fontes consultadas.** As peças CAD de carro, guia, retenção, freio e perfis são reservas transparentes, com dimensões hipotéticas explícitas"
            }
          ]
        },
        {
          "item": "Parafusos guias/freios RO-62",
          "reference": "3,5 × 22 CC",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Dimensões documentais; falta contar furos efetivos da configuração e verificar piloto/penetração.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/freios,3,5×12 CF para retenção. Isso não define pilotos, resistência, comprimento efetivo de penetração, encaixe nem a fixação de cada suporte. Eixos do padrão MDF22/86 a partir da borda e8,5/32,5 acima da base estão desenhados como linhas, sem furos ou diâmetro de piloto. Espelhamento do lado direito é proposta a confirmar. **Não há STEP oficial nas fontes consultadas.** As peças CAD de carro, guia, retenção, freio e perfis são reservas transparentes, com dimensões hipotéticas explícitas"
            }
          ]
        },
        {
          "item": "Parafusos retenção RO-62",
          "reference": "3,5 × 12 CF",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Dimensões documentais; falta contar furos efetivos da configuração e verificar piloto/penetração.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
              "trecho": "Manual propõe parafusos3,5×14 CC para carros e3,5×22 CC para guias/freios,3,5×12 CF para retenção. Isso não define pilotos, resistência, comprimento efetivo de penetração, encaixe nem a fixação de cada suporte. Eixos do padrão MDF22/86 a partir da borda e8,5/32,5 acima da base estão desenhados como linhas, sem furos ou diâmetro de piloto. Espelhamento do lado direito é proposta a confirmar. **Não há STEP oficial nas fontes consultadas.** As peças CAD de carro, guia, retenção, freio e perfis são reservas transparentes, com dimensões hipotéticas explícitas"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "6contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Amadeirado; referência Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:414"
        }
      ],
      "fieldChecks": [
        {
          "id": "P03-CAMPO-1",
          "measure": "Medir altura acabada até o teto nos extremos e no encontro com o canto.",
          "method": "Laser/nível a partir do mesmo datum do roupeiro.",
          "affects": "Altura final do maleiro, arremate e passagem de montagem.",
          "value": null
        },
        {
          "id": "PAREDE-QUARTO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Confirmar envelope real, retenção antidescarrilamento, padrão de furação, seções completas dos trilhos e posição dos freios.",
        "Dimensionar suporte dos trilhos e ligações da base/topo; capacidade de60 kg por porta não dimensiona a marcenaria.",
        "Maleiro: folhas670 ×237 ×18 são baixas/largas. Não adotar Comfort240: massa estimada2,14–2,57kg abaixo da faixa mínima15kg do acessório.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Contato é nominal: ligação e transferência de carga não demonstradas. Acoplamento de montagem e capacidade da base sob malas.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Compatibilizar montagem do maleiro com as divisórias do roupeiro e com o canto.",
        "Fechar transferência de carga da base e acesso aos trilhos antes da montagem definitiva.",
        "AP = vão vertical −35 mm e transpasse30 mm são compatíveis nominalmente. Passo38 e distribuição10/25 da folga vertical são hipóteses, não cotas executivas."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Correr_R14_2026-10-14/README.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P03.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P03.svg"
    }
  },
  "P04": {
    "hardware": [
      "Suspensão e ligações dos divisores ainda a dimensionar."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Validar folhas439,75/440,25 ×306, mais largas que altas, com fabricante: não extrapolar a orientação de carga de portas altas.",
      "Verificar a ligação/rigidez no vão851,5 e dimensionar contribuição do fundo, sem presumir três vãos iguais.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Vão 851,5 merece reforço ou limite de conteúdo. Fundo contínuo pode ajudar somente se sua união for dimensionada; não presumir três vãos iguais.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P04",
      "matriz",
      "fixas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P04",
      "name": "Aéreo da cabeceira",
      "room": "quarto",
      "dimensions": [
        1800.0,
        250.0,
        308.0
      ],
      "internalMeasures": "Profundidade 212 e altura 272. Vãos longitudinais 425,75 /407,75 /851,5. Divisor central 36; apoio terminal 18 e faixa 7 proposta.",
      "panels": [
        {
          "id": "Peca266",
          "name": "Lateral direita",
          "dimensions": [
            308.0,
            230.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca266 (Lateral direita018); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca267",
          "name": "Lateral esquerda",
          "dimensions": [
            308.0,
            230.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca267 (Lateral esquerda002); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca268",
          "name": "Fundo",
          "dimensions": [
            1764.0,
            272.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca268 (Fundo002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca269",
          "name": "Base",
          "dimensions": [
            1764.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca269 (Base001); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca270",
          "name": "Tampo",
          "dimensions": [
            1764.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca270 (Tampo001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR015",
          "name": "Cabeceira porta 4 - abrir para direita — frente com canecos",
          "dimensions": [
            439.75,
            306.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR015 (Cabeceira porta 4 - abrir para direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR016",
          "name": "Cabeceira porta 3 - abrir para esquerda — frente com canecos",
          "dimensions": [
            439.75,
            306.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR016 (Cabeceira porta 3 - abrir para esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR017",
          "name": "Cabeceira porta 2 - abrir para direita — frente com canecos",
          "dimensions": [
            440.25,
            306.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR017 (Cabeceira porta 2 - abrir para direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FaixaFixaEstudo",
          "name": "Faixa fixa · proposta, não aprovada",
          "dimensions": [
            272.0,
            18.0,
            7.0
          ],
          "thickness": 7.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FaixaFixaEstudo (Faixa fixa · proposta, não aprovada); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioComumR003",
          "name": "Apoio interno cabeceira 1 - proposta18",
          "dimensions": [
            272.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioComumR003 (Apoio interno cabeceira 1 - proposta18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioComumR004",
          "name": "Apoio interno cabeceira 2 - proposta18",
          "dimensions": [
            272.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioComumR004 (Apoio interno cabeceira 2 - proposta18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioOpostoR001",
          "name": "Cabeceira - segundo18 no divisor das portas2/3; conjunto36",
          "dimensions": [
            272.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioOpostoR001 (Cabeceira - segundo18 no divisor das portas2/3; conjunto36)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioOpostoR002",
          "name": "Cabeceira - apoio18 da vizinha à direita; proposta",
          "dimensions": [
            272.0,
            212.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioOpostoR002 (Cabeceira - apoio18 da vizinha à direita; proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteVizinhaR18",
          "name": "Cabeceira porta 1 - abrir para esquerda — frente com canecos",
          "dimensions": [
            440.25,
            306.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Amadeirado, referência Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteVizinhaR18 (Cabeceira porta 1 - abrir para esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:414",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "4 folhas × 2 dobradiças = 8 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Cabeceira A | 439.75 × 306 × 18 | 2 | 2 | 1.57 / 1.82 / 2.18 | baixa/larga | Cabeceira B | 440.25 × 306 × 18 | 2 | 2 | 1.58 / 1.82 / 2.18 | baixa/larga | Espelheiro | 297 × 748 × 18 | 2 | 3 | 4.82 / 5.22 / 5.82 | alta/estreita | Roupeiro correr | 995 × 1999 × 18 | 2 | correr | 23.27 / 26.85 / 32.22 | alta/estreita | Maleiro correr | 670 × 237 × 18 | 2 | correr | 1.86 / 2.14 / 2.57 | baixa/larga | "
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "4 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "19contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Amadeirado; referência Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Amadeirado; referência Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:414"
        }
      ],
      "fieldChecks": [
        {
          "id": "P04-CAMPO-1",
          "measure": "Conferir comprimento livre, prumo, posição da cabeceira e pontos elétricos/iluminação na faixa do aéreo.",
          "method": "Trena/laser, fotos com escala e localização das instalações.",
          "affects": "Alinhamento com canto, abertura das portas e rota da iluminação.",
          "value": null
        },
        {
          "id": "PAREDE-QUARTO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Validar folhas439,75/440,25 ×306, mais largas que altas, com fabricante: não extrapolar a orientação de carga de portas altas.",
        "Verificar a ligação/rigidez no vão851,5 e dimensionar contribuição do fundo, sem presumir três vãos iguais.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Vão 851,5 merece reforço ou limite de conteúdo. Fundo contínuo pode ajudar somente se sua união for dimensionada; não presumir três vãos iguais.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Preservar vãos desiguais; não dividir o conjunto automaticamente em três nichos iguais.",
        "Vão maior de 851,5 mm exige fechamento técnico da ligação/rigidez antes de definir carga.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17.",
        "Quatro folhas;6dobradiças em K5/R16 e2na vizinha em K6/R17 no estudo FGVTN. Apoios18 e divisor centralduplo36 preservados."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P04.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P04.svg"
    }
  },
  "P05": {
    "hardware": [
      "Duas portas; dobradiças reguláveis com amortecimento escolhidas."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Compatibilizar recorte hidráulico e acesso às conexões do cooktop/forno com armazenamento; não atribuir apoio à prateleira só pelo contato com laterais.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Prateleira explicitamente marcada hidráulica a recortar; não liberar corte/armazenamento sem sifão e cuba. Apoio inferior não decorre só de encostar na lateral.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P05",
      "matriz",
      "fixas",
      "torneiras",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P05",
      "name": "Gabinete da pia",
      "room": "cozinha",
      "dimensions": [
        650.0,
        610.0,
        720.0
      ],
      "internalMeasures": "Largura 614, profundidade 572. Base topo 198; prateleira 482–500: altura inferior 284 e superior até corpo 900 de 400.",
      "panels": [
        {
          "id": "Peca276",
          "name": "Lateral direita",
          "dimensions": [
            720.0,
            590.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca276 (Lateral direita019); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca277",
          "name": "Lateral esquerda",
          "dimensions": [
            720.0,
            590.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca277 (Lateral esquerda003); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca278",
          "name": "Fundo",
          "dimensions": [
            684.0,
            614.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca278 (Fundo003)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca279",
          "name": "Base",
          "dimensions": [
            614.0,
            572.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca279 (Base002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca280",
          "name": "Prateleira de estudo · hidráulica a recortar",
          "dimensions": [
            614.0,
            572.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca280 (Prateleira de estudo · hidráulica a recortar)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR10",
          "name": "Gabinete da pia - porta direita — frente com canecos",
          "dimensions": [
            718.0,
            322.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR10 (Gabinete da pia - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR001",
          "name": "Gabinete da pia - porta esquerda — frente com canecos",
          "dimensions": [
            718.0,
            322.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR001 (Gabinete da pia - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 2 dobradiças = 4 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Pia | 322 × 718 × 18 | 2 | 2 | 2.70 / 3.12 / 3.75 | alta/estreita | Depurador | 322 × 590 × 18 | 2 | 2 | 2.22 / 2.56 / 3.08 | alta/estreita | Uso diário | 270.5 × 1016 × 18 | 2 | 3 | 3.22 / 3.71 / 4.45 | alta/estreita | Micro-ondas | 345.5 × 608 × 18 | 2 | 2 | 2.46 / 2.84 / 3.40 | alta/estreita | Geladeira | 397.5 × 582 × 18 | 2 | 2 | 2.71 / 3.12 / 3.75 | alta/estreita | Lavanderia | 414.5 × 578 ×"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "7contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:1050"
        }
      ],
      "fieldChecks": [
        {
          "id": "P05-CAMPO-1",
          "measure": "Localizar água, esgoto, sifão, cuba instalada e conexões; medir protrusões e espaço de manutenção.",
          "method": "Croqui cotado a partir de piso/parede acabados e gabarito do conjunto real.",
          "affects": "Recorte da prateleira hidráulica, base, lixeira e acesso às conexões.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Compatibilizar recorte hidráulico e acesso às conexões do cooktop/forno com armazenamento; não atribuir apoio à prateleira só pelo contato com laterais.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Prateleira explicitamente marcada hidráulica a recortar; não liberar corte/armazenamento sem sifão e cuba. Apoio inferior não decorre só de encostar na lateral.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "A prateleira hidráulica precisa de recorte e bordas protegidas conforme conjunto real.",
        "Garantir desmontagem/acesso a sifão e engates sem depender de quebrar a marcenaria.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17.",
        "Prateleira614 ×572 ×18 deve manter acesso ao sifão e ser recortada somente após fechar cuba/válvula/sifão."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P05.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P05.svg"
    }
  },
  "P06": {
    "hardware": [
      "FGVTN 500 candidata; capacidade publicada corrigida para 35 kg.",
      "Engates, folgas e fixações ainda a fechar."
    ],
    "pending": [
      "Determinar datum vertical, recortes traseiros e desenho dos engates da FGVTN; o STEP400 não deve ser escalado para500.",
      "Fechar carga útil incluindo massa da caixa, frente, acessórios e conteúdo; 35kg não significa35kg de conteúdo.",
      "G3: cenário de madeira900kg/m³ consome15,626kg e deixa19,374kg até35kg, antes de acessórios. Recalcular com materiais e caixa definitivos.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Gavetas e ferragens por estudo específico. Fixação e carga da caixa/base ainda condicionais.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P06",
      "matriz",
      "fixas",
      "gavetas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P06",
      "name": "Gaveteiro da cozinha",
      "room": "cozinha",
      "dimensions": [
        619.0,
        610.0,
        720.0
      ],
      "internalMeasures": "Caixa entre faces 583×572; base topo 198. Fundos/laterais 18.",
      "panels": [
        {
          "id": "Peca283",
          "name": "Lateral direita",
          "dimensions": [
            720.0,
            590.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca283 (Lateral direita020); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca284",
          "name": "Lateral esquerda",
          "dimensions": [
            720.0,
            590.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca284 (Lateral esquerda004); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca285",
          "name": "Fundo",
          "dimensions": [
            684.0,
            583.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca285 (Fundo004)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca286",
          "name": "Base",
          "dimensions": [
            583.0,
            572.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca286 (Base003)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR048",
          "name": "Lateral comum esquerda · G3 · mantimentos - proposta R08",
          "dimensions": [
            490.0,
            300.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR048 (Lateral comum esquerda · G3 · mantimentos - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR049",
          "name": "Lateral comum direita · G3 · mantimentos - proposta R08",
          "dimensions": [
            490.0,
            300.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR049 (Lateral comum direita · G3 · mantimentos - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR050",
          "name": "Fundo comum · G3 · mantimentos - proposta R08",
          "dimensions": [
            551.0,
            490.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR050 (Fundo comum · G3 · mantimentos - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR051",
          "name": "Traseira comum · G3 · mantimentos - proposta R08",
          "dimensions": [
            541.0,
            273.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR051 (Traseira comum · G3 · mantimentos - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR052",
          "name": "Dianteira comum16 · G3 · mantimentos - proposta R08",
          "dimensions": [
            541.0,
            273.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR052 (Dianteira comum16 · G3 · mantimentos - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR053",
          "name": "Frente preservada · G3 · mantimentos - proposta R08",
          "dimensions": [
            617.0,
            396.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR053 (Frente preservada · G3 · mantimentos - proposta R08); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "MontagemG2R016",
          "name": "Parte_traseira_da_gaveta[3B0R-000X] - proposta R07",
          "dimensions": [
            541.0,
            73.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD MontagemG2R016 (Parte_traseira_da_gaveta[3B0R-000X] - proposta R07)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "MontagemG2R017",
          "name": "Lateral_da_gaveta_à_esquerda[3B0R-0010] - proposta R07",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD MontagemG2R017 (Lateral_da_gaveta_à_esquerda[3B0R-0010] - proposta R07)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "MontagemG2R018",
          "name": "Lateral_da_gaveta_à_direita[3B0R-0015] - proposta R07",
          "dimensions": [
            490.0,
            100.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD MontagemG2R018 (Lateral_da_gaveta_à_direita[3B0R-0015] - proposta R07)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "MontagemG2R019",
          "name": "Fundo_da_gaveta[3B0R-001A] - proposta R07",
          "dimensions": [
            551.0,
            490.0,
            16.2
          ],
          "thickness": 16.2,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD MontagemG2R019 (Fundo_da_gaveta[3B0R-001A] - proposta R07)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "MontagemG2R020",
          "name": "Frente_da_gaveta[3B0R-001H] - proposta R07",
          "dimensions": [
            617.0,
            156.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD MontagemG2R020 (Frente_da_gaveta[3B0R-001H] - proposta R07); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR060",
          "name": "Lateral comum esquerda · G1 · talheres - proposta R08",
          "dimensions": [
            490.0,
            80.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR060 (Lateral comum esquerda · G1 · talheres - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR061",
          "name": "Lateral comum direita · G1 · talheres - proposta R08",
          "dimensions": [
            490.0,
            80.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR061 (Lateral comum direita · G1 · talheres - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR062",
          "name": "Fundo comum · G1 · talheres - proposta R08",
          "dimensions": [
            551.0,
            490.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR062 (Fundo comum · G1 · talheres - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR063",
          "name": "Traseira comum · G1 · talheres - proposta R08",
          "dimensions": [
            541.0,
            53.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR063 (Traseira comum · G1 · talheres - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR064",
          "name": "Dianteira comum16 · G1 · talheres - proposta R08",
          "dimensions": [
            541.0,
            53.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR064 (Dianteira comum16 · G1 · talheres - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR065",
          "name": "Frente preservada · G1 · talheres - proposta R08",
          "dimensions": [
            617.0,
            156.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR065 (Frente preservada · G1 · talheres - proposta R08); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Corrediças ocultas, 500 mm",
          "reference": "FGVTN 54FGOC12500TSX0",
          "quantity": 3,
          "unit": "par",
          "status": "candidato",
          "assembly": "Capacidade publicada35kg; curso475 ±3mm, não500. Modelo de caixa legado exige compatibilização.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
              "trecho": "Roupeiro — Gaveta, 001, 002, 003 | 54FGOC12500TSX0 | 4 pares | 355 × 550 | 344 externos / 314 internos × 500 | +30 sobre mínimo 520 | Cozinha — Gaveta004, 005, 006 | 54FGOC12500TSX0 | 3 pares | 583 × 572 | 572 externos / 542 internos × 500 | +52 sobre mínimo 520 | Escritório — Gaveta008, 009 | 54FGOC12400TSX0 | 2 pares | 364 × 412 na R44; 432 na variante R04 | 353 externos / 323 internos × 400 | −8 R44; +12 R04 | São 7 pares de 500 + 2 pares de 400, total 18 guias e 9 conjuntos de engates esquerdo/direito compatíveis. Conferir se os engates vêm nos kits para evitar compra duplicada. Não misturar engate convencional com opcional 3D sem o desenho da combinação exata. Parafusos de fixação e seus comprimentos aguardam desenho definitivo, espessura real e substrato. As caixas atuais vieram de outra família: +1 mm na largura interna/externa e +"
            }
          ],
          "derivation": "1 par por gaveta: 3 gavetas"
        },
        {
          "item": "Engates das corrediças 500",
          "reference": "Par esquerdo/direito correspondente ao kit FGVTN 500; SKU não confirmado",
          "quantity": 3,
          "unit": "par E/D",
          "status": "pendente",
          "assembly": "Não duplicar se os engates vierem incluídos. Não misturar convencional e opcional3D.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
              "trecho": "São 7 pares de 500 + 2 pares de 400, total 18 guias e 9 conjuntos de engates esquerdo/direito compatíveis. Conferir se os engates vêm nos kits para evitar compra duplicada. Não misturar engate convencional com opcional 3D sem o desenho da combinação exata. Parafusos de fixação e seus comprimentos aguardam desenho definitivo, espessura real e substrato. As caixas atuais vieram de outra família: +1 mm na largura interna/externa e +10 mm n"
            }
          ],
          "includedWhenBundled": true
        },
        {
          "item": "Parafusos das guias e engates",
          "reference": null,
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Definir pelo desenho e material reais; não quantificar pela geometria de outra família.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Parafusos guias;Conforme furo e substrato;A definir;peca;NAO QUANTIFICADO;Gabarito de cada comprimento e resistencia do substrato Fixacao frentes escritorio;Parafuso4x30 arruela1.2 conforme estudoR04;8;conjunto;HIPOTESE GEOMETRICA;Resistenc"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "4contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:1050"
        }
      ],
      "fieldChecks": [
        {
          "id": "P06-CAMPO-1",
          "measure": "Medir vão acabado sob a pedra, esquadro, altura útil e interferência com pia/cocção vizinhas.",
          "method": "Trena/nível e abertura com gabarito de profundidade da gaveta.",
          "affects": "Largura da caixa, folgas laterais e montagem das corrediças.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Determinar datum vertical, recortes traseiros e desenho dos engates da FGVTN; o STEP400 não deve ser escalado para500.",
        "Fechar carga útil incluindo massa da caixa, frente, acessórios e conteúdo; 35kg não significa35kg de conteúdo.",
        "G3: cenário de madeira900kg/m³ consome15,626kg e deixa19,374kg até35kg, antes de acessórios. Recalcular com materiais e caixa definitivos.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Gavetas e ferragens por estudo específico. Fixação e carga da caixa/base ainda condicionais.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Conferir gavetas e guias como conjuntos compatíveis; preservar G1/G2/G3 e seus usos.",
        "Abertura total e amortecimento das três gavetas constam das escolhas; SKU, regulagem e fixação ainda precisam de projeto.",
        "Caixas FGVTN em laterais15: largura interna A−41 e externa A−11; folga centrada nominal5,5mm/lado. Compatibilizar caixa/recortes/engates antes do corte."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P06.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P06.svg"
    }
  },
  "P07": {
    "hardware": [
      "Inserto M4 curto nas grelhas: candidato, retenção no MDF não comprovada."
    ],
    "pending": [
      "Dimensionar ligações da base/nervuras e das réguas; capacidade térmica e estrutural não é comprovada apenas pela área das grelhas.",
      "Fechar tipo/comprimento de M4, retenção de rosca, torque, piloto e acesso; conferir resistência no material efetivo.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Respeitar estudo Fischer R31/R02 de ventilação; a travessa e base não autorizam fechar canais. Ligações, apoios e instalação real pendentes.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P07",
      "matriz",
      "fixas",
      "forno",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P07",
      "name": "Módulo de cocção",
      "room": "cozinha",
      "dimensions": [
        613.0,
        597.5,
        900.0
      ],
      "internalMeasures": "Vão lateral 577; base plana 577×535×18, topo 138. Travessa 577×212×30 emZ660–690; trás terminaY6955, reservando 45 até parede nominal 7000.",
      "panels": [
        {
          "id": "Peca305",
          "name": "Lateral direita do forno - R30 deslocada 13 mm (vão 577)",
          "dimensions": [
            900.0,
            590.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca305 (Lateral direita do forno - R30 deslocada 13 mm (vão 577)); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca306",
          "name": "Lateral esquerda do forno",
          "dimensions": [
            900.0,
            590.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca306 (Lateral esquerda do forno); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca307",
          "name": "Travessa cocção · avançada27 para liberar ar traseiro45 · proposta",
          "dimensions": [
            577.0,
            212.0,
            30.0
          ],
          "thickness": 30.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca307 (Travessa cocção · avançada27 para liberar ar traseiro45 · proposta); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BasePlanaR31",
          "name": "BasePlana · proposta R31",
          "dimensions": [
            577.0,
            535.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BasePlanaR31 (BasePlana · proposta R31)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioEsquerdoR31",
          "name": "ApoioEsquerdo · proposta R31",
          "dimensions": [
            505.0,
            120.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioEsquerdoR31 (ApoioEsquerdo · proposta R31)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioCentralR31",
          "name": "ApoioCentral · proposta R31",
          "dimensions": [
            505.0,
            120.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioCentralR31 (ApoioCentral · proposta R31)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioDireitoR31",
          "name": "ApoioDireito · proposta R31",
          "dimensions": [
            505.0,
            120.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioDireitoR31 (ApoioDireito · proposta R31)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ReguaInferiorBaixaR31",
          "name": "ReguaInferiorBaixa · proposta R31",
          "dimensions": [
            577.0,
            18.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ReguaInferiorBaixaR31 (ReguaInferiorBaixa · proposta R31); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ReguaInferiorAltaR31",
          "name": "ReguaInferiorAlta · proposta R31",
          "dimensions": [
            577.0,
            18.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ReguaInferiorAltaR31 (ReguaInferiorAlta · proposta R31); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ReguaSuperiorBaixaR31",
          "name": "ReguaSuperiorBaixa · proposta R31",
          "dimensions": [
            577.0,
            18.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ReguaSuperiorBaixaR31 (ReguaSuperiorBaixa · proposta R31); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ReguaSuperiorAltaR31",
          "name": "ReguaSuperiorAlta · proposta R31",
          "dimensions": [
            577.0,
            18.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ReguaSuperiorAltaR31 (ReguaSuperiorAlta · proposta R31); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Grelhas removíveis sob medida",
          "reference": "Inox304, chapa1,5;600 ×90mm,12 rasgos por grelha",
          "quantity": 2,
          "unit": "peça",
          "status": "candidato",
          "assembly": "Área geométrica aberta272,43cm² por peça; conferir acabamento e rigidez, sem cobrir ventilação própria do forno.",
          "evidence": [
            {
              "path": "01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md",
              "trecho": "Duas grelhas iguais, sob medida, removíveis por quatro parafusos cada.** Dimensão externa candidata600 ×90 mm, cobrindo a abertura de560 ×60 sem reduzir a largura do módulo613. Uma fica abaixo do forno, outra acima. Acabamento e cor devem acompanhar a marcenaria já escolhida; a representação escura da prancha não aprova uma nova cor. | Item | Especificação candidata para cotação | |---|---| | Quantidade | 2 peças iguais | | Material | Chapa inox304, espessura1,5 mm, como referência de fabricação; fornecedor confirmar planicidade, resistência dos filetes e acabamento compatível com uso junto ao forno | | Dimensões externas | 600 ×90; cantos externosR2, bordas rebarbadas e sem arestas cortantes | | Ventilação | 12 rasgos retangulares com cantosR3, cada um134 ×17; quatro colunas e três linhas | | Coordenadas dos rasgos | Origem no canto inferior esquerdo da grelha. X inicial23,163,303,443; "
            }
          ]
        },
        {
          "item": "Parafusos desmontáveis das grelhas",
          "reference": "M4; comprimento e cabeça a fechar",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "4 parafusos por grelha; não depender de retirada repetida de rosca diretamente no MDF.",
          "evidence": [
            {
              "path": "01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md",
              "trecho": "Fixação | Quatro furosØ4,5, centrosX100/500 e Z7,5/82,5; propostaM4 com porca retida ou sistema equivalente desmontável, sem depender de parafuso repetidamente retirado da madeira | | Suporte ao móvel | Duas réguas candidatas577 ×18 ×18 por grelha, ligadas às laterais, fora da abertura de ar; ligação e retenção da rosca a detalhar | | Guarnição/tela | Nenhuma tela fina ou guarnição invadindo os rasgos considerada no cálculo. Se acrescentada, recalcular área efetiva e perdas | O gabarito1:1 contém apenas contornos de corte e furos, emmilímetros."
            }
          ],
          "derivation": "2 grelhas × 4 pontos"
        },
        {
          "item": "Roscas retidas das grelhas",
          "reference": "InsertoM4 curto candidato RAMPA SKD30 439408001 ou porca retida validada",
          "quantity": 8,
          "unit": "posição de rosca",
          "status": "candidato",
          "assembly": "8 interfaces de M4 necessárias; a ficha RAMPA consultada é para madeira dura e não comprova retenção em MDF.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Grelhas removíveis do forno | InsertoM4 curto, exemploRAMPA SKD30 439408001 | Geometria 8×8 é candidata; ficha consultada é para madeira dura, não comprova retenção no MDF. Não liberar substituição nem torque. | | Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das later"
            }
          ],
          "derivation": "1 rosca correspondente a cada um dos 8 parafusos",
          "quantityBasis": "Interfaces necessárias, não SKU aprovado"
        },
        {
          "item": "Réguas de apoio das grelhas",
          "reference": "577 ×18 ×18mm; conectores a definir",
          "quantity": 4,
          "unit": "régua proposta",
          "status": "candidato",
          "assembly": "2 por grelha, fora da abertura de ar; definir ligação às laterais.",
          "evidence": [
            {
              "path": "01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md",
              "trecho": "Suporte ao móvel | Duas réguas candidatas577 ×18 ×18 por grelha, ligadas às laterais, fora da abertura de ar; ligação e retenção da rosca a detalhar | | Guarnição/tela | Nenhuma tela fina ou guarnição invadindo os rasgos considerada no cálculo. Se acrescentada, recalcular área efetiva e perdas | O g"
            }
          ],
          "derivation": "2 grelhas × 2 réguas"
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "4contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:1050"
        }
      ],
      "fieldChecks": [
        {
          "id": "P07-CAMPO-1",
          "measure": "Levantar posições dos pontos, profundidade até a parede e aberturas reais para ventilação e retirada do forno.",
          "method": "Croqui cotado e conferência do aparelho real com seu manual.",
          "affects": "Base, apoios, réguas removíveis e manutenção sem fechar canais.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Dimensionar ligações da base/nervuras e das réguas; capacidade térmica e estrutural não é comprovada apenas pela área das grelhas.",
        "Fechar tipo/comprimento de M4, retenção de rosca, torque, piloto e acesso; conferir resistência no material efetivo.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Respeitar estudo Fischer R31/R02 de ventilação; a travessa e base não autorizam fechar canais. Ligações, apoios e instalação real pendentes.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Preservar canais de ventilação Fischer e retirada das grelhas; não preencher reservas como se fossem volume de guarda.",
        "Base e apoios R31 são detalhe proposto; fixação dos insertos e sustentação precisam de validação.",
        "Manter base plana e três nervuras até o piso; faixa traseira45 ×560 e canais de entrada/saída não podem ser fechados pelas uniões."
      ],
      "sources": [
        "01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P07.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P07.svg"
    }
  },
  "P08": {
    "hardware": [
      "Seis rodízios, roda 30 e altura total 39 mm; produto exato pendente.",
      "Guias 3 mm com corrida 2 mm são proposta; batente removível a definir."
    ],
    "pending": [
      "Obter ficha primária do rodízio: silicone, capacidade dinâmica, altura39 e furação; BigferRB30/12.02.008 é polímero e38,5, não substituição automática.",
      "Dimensionar piso de apoio, distribuição entre rodas e batente de impacto com massa própria da gaveta e conteúdo.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Rodízios/seis rodas e mecanismo em estudo de gavetas. Não tratar guias como suporte de peso.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
      "Confirmar se a reserva vira peça efetiva e quais faces ficam aparentes; não há solução estrutural executiva."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P08",
      "matriz",
      "fixas",
      "gavetas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P08",
      "name": "Gaveta de limpeza",
      "room": "cozinha",
      "dimensions": [
        1269.0,
        530.0,
        180.0
      ],
      "internalMeasures": "Reserva entre apoios laterais 1233, altura 180; guias laterais 3 e corrida 2 são proposta sem apoio vertical.",
      "panels": [
        {
          "id": "PecaBaixaR13",
          "name": "Frente baixa preservada1223x106 - recuo80",
          "dimensions": [
            1223.0,
            106.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR13 (Frente baixa preservada1223x106 - recuo80); 01_Projeto/Registro_de_decisoes.md:1050",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBaixaR001",
          "name": "Fundo18 sobre rodas - proposta",
          "dimensions": [
            1223.0,
            442.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR001 (Fundo18 sobre rodas - proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBaixaR002",
          "name": "Lateral18 baixa - proposta",
          "dimensions": [
            406.0,
            88.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR002 (Lateral18 baixa - proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBaixaR003",
          "name": "Lateral18 baixa - proposta",
          "dimensions": [
            406.0,
            88.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR003 (Lateral18 baixa - proposta001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBaixaR004",
          "name": "Parede frente/trás18 baixa - proposta",
          "dimensions": [
            1223.0,
            88.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR004 (Parede frente/trás18 baixa - proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBaixaR005",
          "name": "Parede frente/trás18 baixa - proposta",
          "dimensions": [
            1223.0,
            88.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR005 (Parede frente/trás18 baixa - proposta001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBaixaR036",
          "name": "Reserva apoio lateral18 dos gabinetes - estrutura NÃO calculada",
          "dimensions": [
            530.0,
            180.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR036 (Reserva apoio lateral18 dos gabinetes - estrutura NÃO calculada)",
          "finishComplete": false,
          "remainingFinish": "Confirmar se a reserva vira peça efetiva e quais faces ficam aparentes; não há solução estrutural executiva.",
          "quantity": 1
        },
        {
          "id": "PecaBaixaR037",
          "name": "Reserva apoio lateral18 dos gabinetes - estrutura NÃO calculada",
          "dimensions": [
            530.0,
            180.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBaixaR037 (Reserva apoio lateral18 dos gabinetes - estrutura NÃO calculada001)",
          "finishComplete": false,
          "remainingFinish": "Confirmar se a reserva vira peça efetiva e quais faces ficam aparentes; não há solução estrutural executiva.",
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Rodízios fixos",
          "reference": "Candidato Quadrilátero roda30/altura39, silicone a confirmar",
          "quantity": 6,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Duas fileiras. Capacidade dinâmica, composição, furação e fixação pendentes; não somar6capacidades como carga garantida.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
              "trecho": "Preservar 1187 × 406 × 88 úteis, cabos fixos de 1125 e seis rodas fixas em duas fileiras. O gabarito usa Ø30 e altura39, fundo18, borda superior Z145 e gabinete Z180 (35 de reserva). A madeira calculada no estudo R13 pesa 12,918–15,502 kg para densidades 750–900; valor de referência anterior, não reextraído nesta rodada. Candidato | O que está comprovado | Decisão | Quadrilátero fixo30, anúncio Elmar/MadeiraMadeira | Anúncio declara silicone e altura39; sem capacidade dinâmica e sem desenho primário obtido | Manter candidato, não liberar compra por descrição comercial | Bigfer RB30 fixo 12.02.008 | Catálogo ofici"
            }
          ]
        },
        {
          "item": "Guias laterais de marcenaria",
          "reference": "Faixa3mm + corrida2mm de estudo",
          "quantity": 2,
          "unit": "faixa",
          "status": "candidato",
          "assembly": "Não são apoios verticais; definir material, desgaste e conexão.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Guia lateral gaveta baixa;Guia3 com corrida2 proposta;2;peca;PROPOSTA;Material desgaste e fixacao Batente gaveta baixa;Removivel para retirada de limpeza;A definir;conjunto;PENDENTE;Definir curso de parada acesso e carga de impacto"
            }
          ]
        },
        {
          "item": "Batente removível para limpeza",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "Definir curso, impacto e acesso de retirada sem perder altura útil.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Batente gaveta baixa;Removivel para retirada de limpeza;A definir;conjunto;PENDENTE;Definir curso de parada acesso e carga de impacto"
            }
          ]
        },
        {
          "item": "Fixadores dos seis rodízios",
          "reference": null,
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Contagem depende da chapa e furação do rodízio escolhido.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Rodizios gaveta baixa;Fixo roda30 altura39 silicone;6;peca;PRODUTO EXATO PENDENTE;Capacidade dinamica material primario fixacao e batente Guia lateral gaveta baixa;Guia3 com corrida2 proposta;2;peca;PROPOSTA;Material desgaste e fixacao Bate"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "0contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:1050"
        }
      ],
      "fieldChecks": [
        {
          "id": "P08-CAMPO-1",
          "measure": "Medir desnível/irregularidade ao longo do percurso e altura livre sob os gabinetes.",
          "method": "Régua e nível; gabarito da roda selecionada sobre o piso real.",
          "affects": "Altura do fundo, ajuste das seis rodas, guias e batente.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter ficha primária do rodízio: silicone, capacidade dinâmica, altura39 e furação; BigferRB30/12.02.008 é polímero e38,5, não substituição automática.",
        "Dimensionar piso de apoio, distribuição entre rodas e batente de impacto com massa própria da gaveta e conteúdo.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Rodízios/seis rodas e mecanismo em estudo de gavetas. Não tratar guias como suporte de peso.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
        "Confirmar se a reserva vira peça efetiva e quais faces ficam aparentes; não há solução estrutural executiva."
      ],
      "assembly": [
        "A gaveta baixa corre em seis rodas; guias laterais não são suporte vertical.",
        "Preservar manutenção, batente e estrutura independente dos gabinetes; não substituir por família MOVENTO."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P08.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P08.svg"
    }
  },
  "P09": {
    "hardware": [
      "Dobradiças com amortecimento; suspensão e ligações a detalhar."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Dimensionar ligações dos divisores curtos, suspensão e acesso ao duto; não tratar como dois nichos livres298 ×312.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Não apresentar dois nichos íntegros de 298×312: canal técnico corta profundidade. Manter acesso ao duto e definir conexão dos divisores curtos.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P09",
      "matriz",
      "fixas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P09",
      "name": "Aéreo D · depurador",
      "room": "cozinha",
      "dimensions": [
        650.0,
        350.0,
        592.0
      ],
      "internalMeasures": "Vão 614×312×556. Divisor 18 emX3211–3229 limita apenas os 118 mm dianteiros. Reserva central do duto 196×178×556 ocupa a região posterior.",
      "panels": [
        {
          "id": "Peca315",
          "name": "Lateral direita",
          "dimensions": [
            592.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca315 (Lateral direita021); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca316",
          "name": "Lateral esquerda",
          "dimensions": [
            592.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca316 (Lateral esquerda005); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca317",
          "name": "Fundo",
          "dimensions": [
            614.0,
            556.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca317 (Fundo005)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca318",
          "name": "Base",
          "dimensions": [
            614.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca318 (Base004); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca319",
          "name": "Tampo",
          "dimensions": [
            614.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca319 (Tampo002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca320",
          "name": "Divisória",
          "dimensions": [
            556.0,
            118.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca320 (Divisória005)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR002",
          "name": "D · acima do depurador - porta direita — frente com canecos",
          "dimensions": [
            590.0,
            322.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR002 (D · acima do depurador - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR003",
          "name": "D · acima do depurador - porta esquerda — frente com canecos",
          "dimensions": [
            590.0,
            322.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR003 (D · acima do depurador - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 2 dobradiças = 4 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Depurador | 322 × 590 × 18 | 2 | 2 | 2.22 / 2.56 / 3.08 | alta/estreita | Uso diário | 270.5 × 1016 × 18 | 2 | 3 | 3.22 / 3.71 / 4.45 | alta/estreita | Micro-ondas | 345.5 × 608 × 18 | 2 | 2 | 2.46 / 2.84 / 3.40 | alta/estreita | Geladeira | 397.5 × 582 × 18 | 2 | 2 | 2.71 / 3.12 / 3.75 | alta/estreita | Lavanderia | 414.5 × 578 × 18 | 2 | 2 | 2.80 / 3.23 / 3.88 | alta/estreita | Escritório | 496 "
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "8contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Guararapes Azul Petróleo",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2507"
        }
      ],
      "fieldChecks": [
        {
          "id": "P09-CAMPO-1",
          "measure": "Localizar saída real, diâmetro/seção, eixo e protrusões do duto atrás do armário.",
          "method": "Croqui cotado com aparelho e conexão reais.",
          "affects": "Canal posterior, divisores curtos e acesso de manutenção.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Dimensionar ligações dos divisores curtos, suspensão e acesso ao duto; não tratar como dois nichos livres298 ×312.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Não apresentar dois nichos íntegros de 298×312: canal técnico corta profundidade. Manter acesso ao duto e definir conexão dos divisores curtos.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Reservar canal técnico posterior e acesso ao duto; não apresentar dois nichos íntegros de profundidade total.",
        "Detalhar ligações dos divisores curtos e suspensão do armário.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17.",
        "Preservar canal técnico posterior196 ×178 ×556; o divisor corta apenas118mm dianteiros."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P09.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P09.svg"
    }
  },
  "P10": {
    "hardware": [
      "20 conjuntos Minifix 262.26.034 + 262.28.920 como alternativa fixa."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Confirmar opção de prateleiras fixas desmontáveis ou reguláveis; se reguláveis, projetar folga e suporte próprios.",
      "Validar ferramenta/acesso, material, tolerâncias, resistência das uniões e contribuição do fundo; teste sem colisão não dimensiona carga.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Alternativa Minifix modelada para peças fixas. Se removíveis, criar folga de montagem e apoiar conforme ferragem; não comprar pinos presumindo encaixe sem ajuste.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P10",
      "matriz",
      "fixas",
      "minifix",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P10",
      "name": "Aéreo C · uso diário",
      "room": "cozinha",
      "dimensions": [
        547.0,
        350.0,
        1018.0
      ],
      "internalMeasures": "511×312; alturas livres 180 /192 /258 /298. Prateleiras 18 encostam nas laterais sem folga.",
      "panels": [
        {
          "id": "Peca324",
          "name": "Lateral direita",
          "dimensions": [
            1018.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca324 (Lateral direita022); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca325",
          "name": "Lateral esquerda",
          "dimensions": [
            1018.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca325 (Lateral esquerda006); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca326",
          "name": "Fundo",
          "dimensions": [
            982.0,
            511.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca326 (Fundo006)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca327",
          "name": "Base",
          "dimensions": [
            511.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca327 (Base005); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca328",
          "name": "Tampo",
          "dimensions": [
            511.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca328 (Tampo003)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca329",
          "name": "Prateleira",
          "dimensions": [
            511.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca329 (Prateleira)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca330",
          "name": "Prateleira",
          "dimensions": [
            511.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca330 (Prateleira001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca331",
          "name": "Prateleira",
          "dimensions": [
            511.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca331 (Prateleira002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR004",
          "name": "C · uso diário - porta direita — frente com canecos",
          "dimensions": [
            1016.0,
            270.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR004 (C · uso diário - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR005",
          "name": "C · uso diário - porta esquerda — frente com canecos",
          "dimensions": [
            1016.0,
            270.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR005 (C · uso diário - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 6,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 3 dobradiças = 6 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Uso diário | 270.5 × 1016 × 18 | 2 | 3 | 3.22 / 3.71 / 4.45 | alta/estreita | Micro-ondas | 345.5 × 608 × 18 | 2 | 2 | 2.46 / 2.84 / 3.40 | alta/estreita | Geladeira | 397.5 × 582 × 18 | 2 | 2 | 2.71 / 3.12 / 3.75 | alta/estreita | Lavanderia | 414.5 × 578 × 18 | 2 | 2 | 2.80 / 3.23 / 3.88 | alta/estreita | Escritório | 496 × 548 × 18 | 4 | 2 | 3.18 / 3.67 / 4.40 | alta/estreita | Cabeceira A | 43"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 3",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 6,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Caixas Minifix da alternativa fixa desmontável",
          "reference": "Häfele Minifix15 262.26.034",
          "quantity": 20,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "4 por painel Peca327–331; base, topo e3prateleiras. A alternativa não serve para prateleira regulável.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Minifix_C.md",
              "trecho": "Cinco painéis horizontais Peca327–331, quatro conjuntos em cada: 20 caixas e 20 pinos. Dois pontos por extremidade, Y6730 e 6922, a 60 mm das bordas. Eixos das caixas X2400 e 2843, a 34 mm das extremidades. O eixo do pino fica 9 mm acima da face inferior do painel. Furação cega proposta dos pinos 8,5 mm; conferir ponta da ferramenta. Acesso às caixas pela face superior da base e inferior das demais peças. Coordenadas completas em `Minifix_C.json`. | Verificação | Resultado | |---|---| | Madeira atrás da caixa com furo máximo 14 e chapa 18 | 4 mm nominal; 3,7 mm se a chapa medir 17,7 | | Madeira atrás do piloto 8,5 em lateral 18 | 9,5 mm nominal, sem ponta de broca | | Distância da caixa Ø15 "
            }
          ],
          "derivation": "5 painéis × 4 caixas"
        },
        {
          "item": "Pinos Minifix correspondentes",
          "reference": "Häfele S100 262.28.920",
          "quantity": 20,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Rosca especial pré-furo5, comprimento8, B34. Não adicionar suportes soltos para a mesma união.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Minifix_C.md",
              "trecho": "Seleção dimensional: Minifix 15 para painel 18 sem aba, natural 262.26.034, com pino S100 262.28.920, rosca especial para pré-furo 5, comprimento de rosca 8 e B34. Alojamento Ø15, profundidade 13,5+0,5, eixo A9. Passagem para cabeça Ø7. [Catálogo oficial Häfele, páginas impressas FF2.10, FF2.14 e FF2.17](https://hafelethailand.com/wp-content/uploads/2025/12/02-connector-technology-shelf-supports.pdf). ## Arranjo verificável Cinco painéis horizontais Peca327–331, quatro conjuntos em cada: 20 caixas e 20 pinos. Dois pontos por extremidade, Y6730 e 6922, a 60 mm das bordas. Eixos das caixas X2400 e 2843, a 34 mm das extremidades. O eixo do pino "
            }
          ],
          "derivation": "1 pino × cada uma das 20 caixas"
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "15contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Guararapes Azul Petróleo",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2507"
        }
      ],
      "fieldChecks": [
        {
          "id": "P10-CAMPO-1",
          "measure": "Medir prumo, alinhamento com os aéreos vizinhos e posição de tomadas/obstáculos.",
          "method": "Laser/nível e croqui da faixa de instalação.",
          "affects": "Cota de montagem, fundos e pontos de suspensão.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Confirmar opção de prateleiras fixas desmontáveis ou reguláveis; se reguláveis, projetar folga e suporte próprios.",
        "Validar ferramenta/acesso, material, tolerâncias, resistência das uniões e contribuição do fundo; teste sem colisão não dimensiona carga.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Alternativa Minifix modelada para peças fixas. Se removíveis, criar folga de montagem e apoiar conforme ferragem; não comprar pinos presumindo encaixe sem ajuste.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Prateleiras atuais encostam nas laterais: a alternativa Minifix é para montagem fixa.",
        "Se optar por removíveis, revisar folgas e suportes; não comprar pinos presumindo encaixe do CAD sem alteração.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17.",
        "Minifix: alojamentoØ15 profundidade13,5+0,5, eixoA9 e passagemØ7; piloto cego proposto8,5mm. Pontos60mm das bordas dianteira/traseira,34mm das extremidades.",
        "Acesso às caixas pela face superior da base e inferior dos demais painéis. Não replicar pilotos8,5opostos em divisória18 sem verificar pontas e desencontro."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Minifix_C.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P10.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P10.svg"
    }
  },
  "P11": {
    "hardware": [
      "Suspensão, ligação da prateleira e carga a dimensionar."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Prateleira661 ×312 ×18: definir carga, ligação com fundo e rigidez;2,64mm sob20kg é cenário de flexão imediata, não carga aprovada.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Flexão da prateleira sob 20 kg estimada 2,64 mm imediata; não é carga aprovada. Ligações e suspensão pendentes.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P11",
      "matriz",
      "fixas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P11",
      "name": "Aéreo B · micro",
      "room": "cozinha",
      "dimensions": [
        697.0,
        350.0,
        610.0
      ],
      "internalMeasures": "661×312; alturas 258 e 298 separadas por prateleira 18.",
      "panels": [
        {
          "id": "Peca334",
          "name": "Lateral direita",
          "dimensions": [
            610.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca334 (Lateral direita023); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca335",
          "name": "Lateral esquerda",
          "dimensions": [
            610.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca335 (Lateral esquerda007); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca336",
          "name": "Fundo",
          "dimensions": [
            661.0,
            574.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca336 (Fundo007)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca337",
          "name": "Base",
          "dimensions": [
            661.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca337 (Base006); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca338",
          "name": "Tampo",
          "dimensions": [
            661.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca338 (Tampo004)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca339",
          "name": "Prateleira",
          "dimensions": [
            661.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca339 (Prateleira003)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR006",
          "name": "B · acima do micro - porta direita — frente com canecos",
          "dimensions": [
            608.0,
            345.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR006 (B · acima do micro - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR007",
          "name": "B · acima do micro - porta esquerda — frente com canecos",
          "dimensions": [
            608.0,
            345.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR007 (B · acima do micro - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 2 dobradiças = 4 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Micro-ondas | 345.5 × 608 × 18 | 2 | 2 | 2.46 / 2.84 / 3.40 | alta/estreita | Geladeira | 397.5 × 582 × 18 | 2 | 2 | 2.71 / 3.12 / 3.75 | alta/estreita | Lavanderia | 414.5 × 578 × 18 | 2 | 2 | 2.80 / 3.23 / 3.88 | alta/estreita | Escritório | 496 × 548 × 18 | 4 | 2 | 3.18 / 3.67 / 4.40 | alta/estreita | Cabeceira A | 439.75 × 306 × 18 | 2 | 2 | 1.57 / 1.82 / 2.18 | baixa/larga | Cabeceira B | 440"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "9contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Guararapes Azul Petróleo",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2507"
        }
      ],
      "fieldChecks": [
        {
          "id": "P11-CAMPO-1",
          "measure": "Medir nicho aberto, alturas dos vizinhos, tomadas e comprimento real do cabo do aparelho.",
          "method": "Gabarito/aparelho real e croqui cotado.",
          "affects": "Acesso, passagem do cabo e ventilação; não resolve divergência de manual.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Prateleira661 ×312 ×18: definir carga, ligação com fundo e rigidez;2,64mm sob20kg é cenário de flexão imediata, não carga aprovada.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Flexão da prateleira sob 20 kg estimada 2,64 mm imediata; não é carga aprovada. Ligações e suspensão pendentes.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Conferir ligação da prateleira e suspensão; a estimativa de flexão para 20 kg não aprova essa carga.",
        "Manter a interface de ventilação do micro separada da especificação da caixa.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P11.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P11.svg"
    }
  },
  "P12": {
    "hardware": [
      "Fixação do divisor e suspensão pendentes."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Detalhar ligação do divisor central18 e suspensão; reserva100mm sobre geladeira não tem tolerância adicional além do mínimo considerado.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Fixação do divisor e suspensão; reserva 100 sobre geladeira tem margem nominal zero além do mínimo considerado.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P12",
      "matriz",
      "fixas",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P12",
      "name": "Aéreo A · geladeira",
      "room": "cozinha",
      "dimensions": [
        801.0,
        350.0,
        584.0
      ],
      "internalMeasures": "Interior 765×312×548, divisor 18 central: dois vãos 373,5.",
      "panels": [
        {
          "id": "Peca342",
          "name": "Lateral direita",
          "dimensions": [
            584.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca342 (Lateral direita024); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca343",
          "name": "Lateral esquerda",
          "dimensions": [
            584.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca343 (Lateral esquerda008); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca344",
          "name": "Fundo",
          "dimensions": [
            765.0,
            548.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca344 (Fundo008)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca345",
          "name": "Base",
          "dimensions": [
            765.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca345 (Base007); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca346",
          "name": "Tampo",
          "dimensions": [
            765.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca346 (Tampo005)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca347",
          "name": "Divisória",
          "dimensions": [
            548.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca347 (Divisória006)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR008",
          "name": "A · acima da geladeira - porta direita — frente com canecos",
          "dimensions": [
            582.0,
            397.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR008 (A · acima da geladeira - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR009",
          "name": "A · acima da geladeira - porta esquerda — frente com canecos",
          "dimensions": [
            582.0,
            397.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Guararapes Azul Petróleo",
          "specifiedMaterial": "face interna Branco TX; face aparente Guararapes Azul Petróleo",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR009 (A · acima da geladeira - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 2 dobradiças = 4 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Geladeira | 397.5 × 582 × 18 | 2 | 2 | 2.71 / 3.12 / 3.75 | alta/estreita | Lavanderia | 414.5 × 578 × 18 | 2 | 2 | 2.80 / 3.23 / 3.88 | alta/estreita | Escritório | 496 × 548 × 18 | 4 | 2 | 3.18 / 3.67 / 4.40 | alta/estreita | Cabeceira A | 439.75 × 306 × 18 | 2 | 2 | 1.57 / 1.82 / 2.18 | baixa/larga | Cabeceira B | 440.25 × 306 × 18 | 2 | 2 | 1.58 / 1.82 / 2.18 | baixa/larga | Espelheiro | 297 ×"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "9contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Guararapes Azul Petróleo. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Guararapes Azul Petróleo",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2507"
        }
      ],
      "fieldChecks": [
        {
          "id": "P12-CAMPO-1",
          "measure": "Conferir altura/largura/profundidade do produto real e desníveis do piso sob os pés reguláveis.",
          "method": "Produto/manual específico e trena; foto da etiqueta do modelo.",
          "affects": "Cota do aéreo e reservas de ventilação sobre a geladeira.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Detalhar ligação do divisor central18 e suspensão; reserva100mm sobre geladeira não tem tolerância adicional além do mínimo considerado.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Fixação do divisor e suspensão; reserva 100 sobre geladeira tem margem nominal zero além do mínimo considerado.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Fixar divisor e suspensão conforme detalhamento; não somar capacidades de ferragens sem distribuição de carga.",
        "Reserva nominal de 100 mm sobre a geladeira não contém margem extra além da premissa adotada.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P12.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P12.svg"
    }
  },
  "P13": {
    "hardware": [
      "Apoio e fixação da chapa precisam ser demonstrados."
    ],
    "pending": [
      "Fechar suporte/fixação da chapa697 e posição dos pés do ME23P.",
      "Resolver documentalmente a divergência de ventilação: escolhaF104 mantém100mm acima enquanto manual pede300mm; não chamar a instalação de validada.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "100 acima mantém escolha F104, divergente de 300 no manual. Pés reais e suporte da chapa não demonstrados. Não chamar espaço ventilado de nicho fechado.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Apoio aberto: referência Arenza do CAD. A regra de interiores Branco TX não recolore automaticamente uma prateleira aberta.",
    "documentIds": [
      "ficha-P13",
      "matriz",
      "fixas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P13",
      "name": "Apoio do micro",
      "room": "cozinha",
      "dimensions": [
        697.0,
        470.0,
        18.0
      ],
      "internalMeasures": "Apoio 697×470×18; micro deixa 123 e 113 nas laterais do apoio aberto,100 atrás e 100 acima; projeção frontal do apoio excede aparelho 18.",
      "panels": [
        {
          "id": "Peca350",
          "name": "Prateleira de apoio · topo 1550",
          "dimensions": [
            697.0,
            470.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": null,
          "materialEvidence": "Peca350.MaterialReferencia",
          "finishComplete": false,
          "remainingFinish": "Aplicação por face ainda não individualizada",
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Fixações do apoio do micro-ondas",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "Apoio697 ×470 ×18; definir distribuição real dos pés do aparelho e caminho da carga.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
              "trecho": "| P13 | Micro-ondas | Apoio 697×470×18; micro deixa 123 e 113 nas laterais do apoio aberto,100 atrás e 100 acima; projeção frontal do apoio excede aparelho 18. |100 acima mantém escolha F104, divergente de 300 no manual. Pés reais e suporte da chapa não demonstrados. Não chamar espaço ventilado de nicho fechado. | | P14 | Tanque/cesto | Entre laterais 554; base 554×562×18. Tanque 420×390 é reserva, não produto. Região hidráulica posterior 450 de largura até 280 da parede, sobe até 630; superior avança 330 e chega 700. | Seleção do tanque/cuba e hidráulica. Não converter reserva de volume útil 380×350×200 em capacidade garantida. Pivôs/cesto em estudo articulado. | | P15 | Aéreo lavanderia | "
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "0contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Apoio aberto: referência Arenza do CAD. A regra de interiores Branco TX não recolore automaticamente uma prateleira aberta.",
      "finishSpecs": [
        {
          "area": "Faces aparentes",
          "material": "Arenza / wood: referência CAD do apoio aberto",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:1050"
        }
      ],
      "fieldChecks": [
        {
          "id": "P13-CAMPO-1",
          "measure": "Medir posição dos pés, cabo/tomada e espaço de retirada do aparelho real.",
          "method": "Gabarito dos quatro pés e croqui em vista superior.",
          "affects": "Distribuição de apoio e eventual passagem de cabos.",
          "value": null
        },
        {
          "id": "PAREDE-COZINHA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Fechar suporte/fixação da chapa697 e posição dos pés do ME23P.",
        "Resolver documentalmente a divergência de ventilação: escolhaF104 mantém100mm acima enquanto manual pede300mm; não chamar a instalação de validada.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "100 acima mantém escolha F104, divergente de 300 no manual. Pés reais e suporte da chapa não demonstrados. Não chamar espaço ventilado de nicho fechado.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "A chapa é apoio aberto, não nicho fechado.",
        "Não liberar pelo envelope: suporte, pés do aparelho e divergência de afastamento superior precisam ser resolvidos.",
        "O apoio aberto não deve ser tratado como nicho fechado."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P13.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P13.svg"
    }
  },
  "P14": {
    "hardware": [
      "Pivôs, retenção, amortecimento e limitador a 55° não selecionados.",
      "FGVTN excluiu fornecimento de mecanismo para esta aplicação."
    ],
    "pending": [
      "Escolher material e construção da armação;15,134kg móveis e38,73Nm são cenário com roupa8kg e densidade900, antes de saco/pivôs/pega.",
      "Obter mecanismo ensaiado para55°, carga variável e desenho aberto/fechado com fixações. FGVTN já excluiu fornecimento desta aplicação.",
      "Marathon04-LHF450-35-W é conjunto completo de comparação, não autorização para usar seus braços com saco/frente atuais. HDS-10H24,5–29,4Nm/90° não comprova esta aplicação.",
      "Compatibilizar produto real do tanque/cuba e hidráulica; reserva geométrica não autoriza recorte.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Seleção do tanque/cuba e hidráulica. Não converter reserva de volume útil 380×350×200 em capacidade garantida. Pivôs/cesto em estudo articulado.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P14",
      "matriz",
      "fixas",
      "cesto",
      "mesa-varal",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P14",
      "name": "Gabinete tanque e cesto",
      "room": "lavanderia",
      "dimensions": [
        590.0,
        630.0,
        920.0
      ],
      "internalMeasures": "Entre laterais 554; base 554×562×18. Tanque 420×390 é reserva, não produto. Região hidráulica posterior 450 de largura até 280 da parede, sobe até 630; superior avança 330 e chega 700.",
      "panels": [
        {
          "id": "Peca352",
          "name": "Lateral direita",
          "dimensions": [
            802.0,
            610.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca352 (Lateral direita025); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca353",
          "name": "Lateral esquerda",
          "dimensions": [
            802.0,
            610.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca353 (Lateral esquerda009); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaCestoR15",
          "name": "Base98 - frente até580 desde parede",
          "dimensions": [
            562.0,
            554.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaCestoR15 (Base98 - frente até580 desde parede)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaCestoR001",
          "name": "Rodapé80 sob a base, recuado50 da face - R29 (era110)",
          "dimensions": [
            554.0,
            80.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaCestoR001 (Rodapé80 sob a base, recuado50 da face - R29 (era110)); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaCestoR002",
          "name": "Painel superior removível675–897 - Arenza liso",
          "dimensions": [
            550.0,
            222.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaCestoR002 (Painel superior removível675–897 - Arenza liso); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaCestoR003",
          "name": "Frente inferior521 - face630, junta lateral2 proposta",
          "dimensions": [
            550.0,
            521.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaCestoR003 (Frente inferior521 - face630, junta lateral2 proposta); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FundoTanqueR29",
          "name": "Fundo009 com abertura hidráulica 450x602 - R29",
          "dimensions": [
            802.0,
            554.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FundoTanqueR29 (Fundo009 com abertura hidráulica 450x602 - R29)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioCestoC01R31",
          "name": "C01 · apoio inferior do cesto · proposto",
          "dimensions": [
            580.0,
            98.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioCestoC01R31 (C01 · apoio inferior do cesto · proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioCestoC02R31",
          "name": "C02 · apoio inferior do cesto · proposto",
          "dimensions": [
            580.0,
            98.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioCestoC02R31 (C02 · apoio inferior do cesto · proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioCestoC03R31",
          "name": "C03 · apoio inferior do cesto · proposto",
          "dimensions": [
            554.0,
            80.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioCestoC03R31 (C03 · apoio inferior do cesto · proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Pivôs do cesto",
          "reference": null,
          "quantity": 2,
          "unit": "posição de pivô",
          "status": "pendente",
          "assembly": "Duas posições ideais do estudo; não são duas ferragens comerciais especificadas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md",
              "trecho": "aproximadamente74,21 N por pivô somente em distribuição simétrica; esforços de retenção, mãos e impacto se somam. Fonte reproduzível: `Cesto_com_armacao.json`. Pequenas diferenças para R41 vêm do uso de g=9,80665 em vez de9,81. Centros usados são os centros dos paralelepípedos do gabarito, não de ferragens reais. ## Triagem de produtos reais | Ferragem/conjunto | Evidência | Compatibilidade com escopo atual"
            }
          ],
          "derivation": "Dois apoios do eixo ideal; força simétrica é hipótese"
        },
        {
          "item": "Mecanismo de retenção e controle de queda",
          "reference": null,
          "quantity": 1,
          "unit": "sistema",
          "status": "pendente",
          "assembly": "Dimensionar pivôs, parada55° e controle de transição vazio/cheio como funções distintas; quantidade de braços/fixadores não definida.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md",
              "trecho": "Separar três funções no dimensionamento: pivôs suportam o conjunto; batentes/limitadores recebem o esforço no55°; amortecimento ou retenção controla a transição entre cheio e vazio. Uma mola escolhida só para8 kg pode empurrar o conjunto vazio de modo indesejado. Um limitador que apenas para em55° não controla a queda até lá. Usar catálogo de “porta até6kg” ou somar duas capacidades não resolve essas funções. Consulta técnica preparada a partir destes dados deve exigir: mecanismo ensaiado com15,13 kg móveis de referência e momento variável até38,73 Nm; espessura18; frente550×521; curso55°; laterais52mmcom apoios existentes; saco retirável sem reduzir400×200×400; desenhos completo/aberto e carga das fixações. Nenhuma comunicação nova enviada neste est"
            }
          ]
        },
        {
          "item": "Limitadores e fixações do conjunto",
          "reference": null,
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Preservar frente550 ×521 ×18 e saco400 ×200 ×400 removível; não reduzir frente para tornar candidato aparentemente compatível.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md",
              "trecho": "Consulta técnica preparada a partir destes dados deve exigir: mecanismo ensaiado com15,13 kg móveis de referência e momento variável até38,73 Nm; espessura18; frente550×521; curso55°; laterais52mmcom apoios existentes; saco retirável sem reduzir400×200×400; desenhos completo/aberto e carga das fixações. Nenhuma comunicação nova enviada neste estudo."
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "1contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:273"
        }
      ],
      "fieldChecks": [
        {
          "id": "P14-CAMPO-1",
          "measure": "Localizar pontos e medir tanque/sifão/conexões reais, janela e interferências no percurso de manutenção.",
          "method": "Gabarito do conjunto selecionado e teste do saco/armação real no vão.",
          "affects": "Recortes, painel removível, envelope hidráulico e retirada do cesto.",
          "value": null
        },
        {
          "id": "PAREDE-LAVANDERIA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Escolher material e construção da armação;15,134kg móveis e38,73Nm são cenário com roupa8kg e densidade900, antes de saco/pivôs/pega.",
        "Obter mecanismo ensaiado para55°, carga variável e desenho aberto/fechado com fixações. FGVTN já excluiu fornecimento desta aplicação.",
        "Marathon04-LHF450-35-W é conjunto completo de comparação, não autorização para usar seus braços com saco/frente atuais. HDS-10H24,5–29,4Nm/90° não comprova esta aplicação.",
        "Compatibilizar produto real do tanque/cuba e hidráulica; reserva geométrica não autoriza recorte.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Seleção do tanque/cuba e hidráulica. Não converter reserva de volume útil 380×350×200 em capacidade garantida. Pivôs/cesto em estudo articulado.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Preservar frente lisa, saco removível/lavável e acesso de manutenção.",
        "Volume hidráulico é reserva; pivô, retenção e limitador de 55° não estão selecionados.",
        "Mecanismo deve permitir manutenção e retirada do saco, preservando52mm laterais do cenário. Não tratar corpo/armação do gabarito como produto real."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P14.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P14.svg"
    }
  },
  "P15": {
    "hardware": [
      "Suspensão e ligação com fundo ou reforço ainda a definir."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Base799 ×312 ×18:4,78mm sob20kg é cenário, não carga. Dimensionar reforço ou ligação estrutural com fundo/suspensão preservando o vão.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Cenário de base somente nas laterais dá 4,78 mm imediata para 20 kg. Reforço ou suspensão/ligação com fundo dimensionada, antes de limitar carga.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P15",
      "matriz",
      "fixas",
      "mesa-varal",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P15",
      "name": "Aéreo da lavanderia",
      "room": "lavanderia",
      "dimensions": [
        835.0,
        350.0,
        580.0
      ],
      "internalMeasures": "799×312×544 entre faces. Base e topo 18, nenhum divisor intermediário físico direto.",
      "panels": [
        {
          "id": "Peca359",
          "name": "Lateral direita",
          "dimensions": [
            580.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca359 (Lateral direita026); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca360",
          "name": "Lateral esquerda",
          "dimensions": [
            580.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca360 (Lateral esquerda010); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca361",
          "name": "Fundo",
          "dimensions": [
            799.0,
            544.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca361 (Fundo010)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca362",
          "name": "Base",
          "dimensions": [
            799.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca362 (Base008); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca363",
          "name": "Tampo",
          "dimensions": [
            799.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca363 (Tampo006)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR010",
          "name": "Aéreo da lavanderia - porta direita — frente com canecos",
          "dimensions": [
            578.0,
            414.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR010 (Aéreo da lavanderia - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR011",
          "name": "Aéreo da lavanderia - porta esquerda — frente com canecos",
          "dimensions": [
            578.0,
            414.5,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR011 (Aéreo da lavanderia - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2507",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 2 dobradiças = 4 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Lavanderia | 414.5 × 578 × 18 | 2 | 2 | 2.80 / 3.23 / 3.88 | alta/estreita | Escritório | 496 × 548 × 18 | 4 | 2 | 3.18 / 3.67 / 4.40 | alta/estreita | Cabeceira A | 439.75 × 306 × 18 | 2 | 2 | 1.57 / 1.82 / 2.18 | baixa/larga | Cabeceira B | 440.25 × 306 × 18 | 2 | 2 | 1.58 / 1.82 / 2.18 | baixa/larga | Espelheiro | 297 × 748 × 18 | 2 | 3 | 4.82 / 5.22 / 5.82 | alta/estreita | Roupeiro correr | 9"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "6contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2507"
        }
      ],
      "fieldChecks": [
        {
          "id": "P15-CAMPO-1",
          "measure": "Medir parede acabada, janela, registros/tubulação, aquecedor e percurso do varal.",
          "method": "Croqui cotado e teste de aberturas reais.",
          "affects": "Cota de montagem, acesso técnico e afastamentos dos conjuntos.",
          "value": null
        },
        {
          "id": "PAREDE-LAVANDERIA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Base799 ×312 ×18:4,78mm sob20kg é cenário, não carga. Dimensionar reforço ou ligação estrutural com fundo/suspensão preservando o vão.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Cenário de base somente nas laterais dá 4,78 mm imediata para 20 kg. Reforço ou suspensão/ligação com fundo dimensionada, antes de limitar carga.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Não presumir divisor intermediário inexistente no CAD.",
        "Vão de 799 mm exige ligação com fundo/reforço e suspensão dimensionadas.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P15.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P15.svg"
    }
  },
  "P16": {
    "hardware": [
      "FGVTN 400 e MOVENTO 400 são alternativas em estudo.",
      "Engates, datum, retirada e interferências ainda pendentes."
    ],
    "pending": [
      "Corrigir datum/recortes sem apagar interferências por tentativa: conflitos0,125–0,175mm no fundo e1,902mm³ no gancho direito registrados.",
      "Resolver reserva superior de retirada e coordenar as duas caixas com tampo/estrutura; diferença pequena não equivale a tolerância aprovada.",
      "Escolher MOVENTO400 ou varianteFGVTN400; quantitativos são alternativas e não somam4pares.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Variante de traseira 20 e folgas da corrediça no estudo de gavetas; preservar compatibilidade com estrutura da bancada.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
      "Arenza aprovado explicitamente nas frentes; padrão comercial da face lateral aparente da caixa não individualizado. wood é referência CAD."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Arenza nas frentes das gavetas. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P16",
      "matriz",
      "fixas",
      "gavetas",
      "movento",
      "bancada",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P16",
      "name": "Gaveteiro do escritório",
      "room": "escritorio",
      "dimensions": [
        400.0,
        450.0,
        240.0
      ],
      "internalMeasures": "Interior 364×412×204 na caixa original: base topo 498, topo começa 702. Corpo externo 400×430×240.",
      "panels": [
        {
          "id": "Peca367",
          "name": "Lateral direita",
          "dimensions": [
            430.0,
            240.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca367 (Lateral direita027)",
          "finishComplete": false,
          "remainingFinish": "Arenza aprovado explicitamente nas frentes; padrão comercial da face lateral aparente da caixa não individualizado. wood é referência CAD.",
          "quantity": 1
        },
        {
          "id": "Peca368",
          "name": "Lateral esquerda",
          "dimensions": [
            430.0,
            240.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca368 (Lateral esquerda011)",
          "finishComplete": false,
          "remainingFinish": "Arenza aprovado explicitamente nas frentes; padrão comercial da face lateral aparente da caixa não individualizado. wood é referência CAD.",
          "quantity": 1
        },
        {
          "id": "Peca369",
          "name": "Fundo",
          "dimensions": [
            364.0,
            204.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca369 (Fundo011)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca370",
          "name": "Base",
          "dimensions": [
            412.0,
            364.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca370 (Base009)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca371",
          "name": "Tampo",
          "dimensions": [
            412.0,
            364.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca371 (Tampo007)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR072",
          "name": "Lateral comum esquerda · Gaveta escritório 1 - proposta R08",
          "dimensions": [
            390.0,
            80.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR072 (Lateral comum esquerda · Gaveta escritório 1 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR073",
          "name": "Lateral comum direita · Gaveta escritório 1 - proposta R08",
          "dimensions": [
            390.0,
            80.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR073 (Lateral comum direita · Gaveta escritório 1 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR074",
          "name": "Fundo comum · Gaveta escritório 1 - proposta R08",
          "dimensions": [
            390.0,
            332.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR074 (Fundo comum · Gaveta escritório 1 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR075",
          "name": "Traseira comum · Gaveta escritório 1 - proposta R08",
          "dimensions": [
            322.0,
            53.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR075 (Traseira comum · Gaveta escritório 1 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR076",
          "name": "Dianteira comum16 · Gaveta escritório 1 - proposta R08",
          "dimensions": [
            322.0,
            53.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR076 (Dianteira comum16 · Gaveta escritório 1 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR077",
          "name": "Frente preservada · Gaveta escritório 1 - proposta R08",
          "dimensions": [
            398.0,
            118.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR077 (Frente preservada · Gaveta escritório 1 - proposta R08); 01_Projeto/Registro_de_decisoes.md:2184",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR084",
          "name": "Lateral comum esquerda · Gaveta escritório 2 - proposta R08",
          "dimensions": [
            390.0,
            80.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR084 (Lateral comum esquerda · Gaveta escritório 2 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR085",
          "name": "Lateral comum direita · Gaveta escritório 2 - proposta R08",
          "dimensions": [
            390.0,
            80.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR085 (Lateral comum direita · Gaveta escritório 2 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR086",
          "name": "Fundo comum · Gaveta escritório 2 - proposta R08",
          "dimensions": [
            390.0,
            332.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR086 (Fundo comum · Gaveta escritório 2 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR087",
          "name": "Traseira comum · Gaveta escritório 2 - proposta R08",
          "dimensions": [
            322.0,
            53.0,
            15.0
          ],
          "thickness": 15.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR087 (Traseira comum · Gaveta escritório 2 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR088",
          "name": "Dianteira comum16 · Gaveta escritório 2 - proposta R08",
          "dimensions": [
            322.0,
            53.0,
            16.0
          ],
          "thickness": 16.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR088 (Dianteira comum16 · Gaveta escritório 2 - proposta R08)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "GavetaComumR089",
          "name": "Frente preservada · Gaveta escritório 2 - proposta R08",
          "dimensions": [
            398.0,
            118.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD GavetaComumR089 (Frente preservada · Gaveta escritório 2 - proposta R08); 01_Projeto/Registro_de_decisoes.md:2184",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Corrediças recomendadas para continuidade",
          "reference": "Blum MOVENTO760H4000S, BLUMOTION S, classe40kg",
          "quantity": 2,
          "unit": "par",
          "status": "candidato",
          "assembly": "Alternativa posterior recomendada preserva caixa/útilR44; exclui TIP-ON e estabilizador não selecionados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Alternativas_escritorio/Resultado.html",
              "trecho": "Pacote identificado Dois pares de 760H4000S, MOVENTO com BLUMOTION S, classe40kg; dois engates esquerdos e dois direitos T51.7601; fixação por parafusos do sistema conforme desenho de cada guia; gabarito T65.1000.02 para engates/ganchos. Não inclui TIP-ON, estabilizador lateral nem ajuste de profundidade para frente embutida: as frentes aqui são aplicadas. O kit comercial deve discriminar ambos os engates por par. Códigos oficiais identificam as peças, não comprovam estoque/preço local. O manual apresenta para guias parafusos 609.1500 (Ø3,5×15) ou de sistema661.1450.HG (Ø6×14,5), em posições indicadas na folha26. Não são dois métodos para somar no mesmo furo. O desenho deve ser conferido na revisão do produto comprado, inclusive a opção de substituição indicada por asterisco. Na lateral18, um parafuso de comprimento15 deixa pelo menos3 de pele geométrica se toda a haste penetrasse madeir"
            }
          ],
          "exclusiveGroup": "P16.corredicas",
          "option": "MOVENTO400"
        },
        {
          "item": "Engates MOVENTO",
          "reference": "Blum T51.7601 esquerdo e direito",
          "quantity": 2,
          "unit": "par E/D",
          "status": "candidato",
          "assembly": "2esquerdos +2direitos; não duplicar quando incluídos no kit.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Alternativas_escritorio/Resultado.html",
              "trecho": "Dois pares de 760H4000S, MOVENTO com BLUMOTION S, classe40kg; dois engates esquerdos e dois direitos T51.7601; fixação por parafusos do sistema conforme desenho de cada guia; gabarito T65.1000.02 para engates/ganchos. Não inclui TIP-ON, estabilizador lateral nem ajuste de profundidade para frente embutida: as frentes aqui são aplicadas. O kit comercial deve discriminar ambos os engates por par. Códigos oficiais identificam as peças, não comprovam estoque/preço local. O manual apresenta para guias parafusos 609.1500 (Ø3,5×15) ou de sistema661.1450.HG (Ø6×14,5), em posições indicadas na folha26. Não são d"
            }
          ],
          "exclusiveGroup": "P16.engates",
          "option": "MOVENTO400",
          "includedWhenBundled": true,
          "derivation": "2 gavetas × 1 par E/D"
        },
        {
          "item": "Parafusos de guias MOVENTO",
          "reference": "Blum609.1500 Ø3,5×15 OU661.1450.HG Ø6×14,5",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Métodos alternativos, não dois parafusos no mesmo furo. Contar posições na revisão do produto adquirido.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Alternativas_escritorio/Resultado.html",
              "trecho": "O manual apresenta para guias parafusos 609.1500 (Ø3,5×15) ou de sistema661.1450.HG (Ø6×14,5), em posições indicadas na folha26. Não são dois métodos para somar no mesmo furo. O desenho deve ser conferido na revisão do produto comprado, inclusive a opção de substituição indicada por asterisco. Na lateral18, um parafuso de comprimento15 deixa pelo menos3 de pele geométrica se toda a haste penetrasse madeira; a espessura do perfil aumenta a sobra. Isso não avalia arrancamento ou piloto. Comparação sem redução do armazenamento Opção | Gabinete mínimo / existente | Caixa e útil longitudinal | Decisão | MOVENTO400 | 4"
            }
          ],
          "option": "MOVENTO400"
        },
        {
          "item": "Gabarito de engates e ganchos",
          "reference": "Blum T65.1000.02",
          "quantity": null,
          "unit": "ferramenta de montagem",
          "status": "candidato",
          "assembly": "Ferramenta reutilizável; confirmar disponibilidade com a marcenaria, não presumir compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Alternativas_escritorio/Resultado.html",
              "trecho": "gabarito T65.1000.02 para engates/ganchos. Não inclui TIP-ON, estabilizador lateral nem ajuste de profundidade para frente embutida: as frentes aqui são aplicadas. O kit comercial deve discriminar ambos os engates por par. Códigos oficiais identificam as peças, não comprovam estoque/preço local. O m"
            }
          ]
        },
        {
          "item": "Corrediças alternativas que exigem variante da caixa",
          "reference": "FGVTN54FGOC12400TSX0,35kg",
          "quantity": 2,
          "unit": "par",
          "status": "candidato",
          "assembly": "Alternativa exclusiva à MOVENTO: exige mínimo420mm livres;R44 tem412 eR04propõe432.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
              "trecho": "Escritório — Gaveta008, 009 | 54FGOC12400TSX0 | 2 pares | 364 × 412 na R44; 432 na variante R04 | 353 externos / 323 internos × 400 | −8 R44; +12 R04 | São 7 pares de 500 + 2 pares de 400, total 18 guias e 9 conjuntos de engates esquerdo/direito compatíveis. Conferir se os engates vêm nos kits para evitar compra duplicada. Não misturar engate convencional com opcional 3D sem o desenho da combinação exata. Parafusos de fixação e seus comprimentos aguardam desenho definitivo, espessura real e subs"
            }
          ],
          "exclusiveGroup": "P16.corredicas",
          "option": "FGVTN400"
        },
        {
          "item": "Engates da alternativa FGVTN400",
          "reference": "Código do par correspondente não confirmado",
          "quantity": 2,
          "unit": "par E/D",
          "status": "pendente",
          "assembly": "Não combinar com T51.7601Blum.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Engates400;Par esquerdo direito correspondente ao kit400;2;conjunto;NAO DUPLICAR SE INCLUSO;Confirmar codigo embalagem e desenho Parafusos guias;Conforme furo e substrato;A definir;peca;NAO QUANTIFICADO;Gabarito de cada comprimento e resist"
            }
          ],
          "exclusiveGroup": "P16.engates",
          "option": "FGVTN400",
          "includedWhenBundled": true
        },
        {
          "item": "Fixação das frentes na variante FGVTN R04",
          "reference": "Parafuso4×30 + arruela1,2mm",
          "quantity": 8,
          "unit": "conjunto",
          "status": "candidato",
          "assembly": "Hipótese geométricaR04; não transferir automaticamente ao pacoteMOVENTO. Piloto/arrancamento pendentes.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
              "trecho": "Fixacao frentes escritorio;Parafuso4x30 arruela1.2 conforme estudoR04;8;conjunto;HIPOTESE GEOMETRICA;Resistencia piloto e engates pendentes Rodizios gaveta baixa;Fixo roda30 altura39 silicone;6;peca;PRODUTO EXATO PENDENTE;Capacidade dinamica material primario "
            }
          ],
          "option": "FGVTN400 R04"
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "6contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Arenza nas frentes das gavetas. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Arenza nas frentes das gavetas",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2184"
        }
      ],
      "fieldChecks": [
        {
          "id": "P16-CAMPO-1",
          "measure": "Conferir altura real sob bancada, curso frontal disponível e envelopes da cadeira/sofá usados.",
          "method": "Trena e gabarito da gaveta aberta, cadeira e sofá na posição de uso.",
          "affects": "Retirada de gaveta, curso e interferência com reforços da bancada.",
          "value": null
        },
        {
          "id": "PAREDE-ESCRITORIO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Corrigir datum/recortes sem apagar interferências por tentativa: conflitos0,125–0,175mm no fundo e1,902mm³ no gancho direito registrados.",
        "Resolver reserva superior de retirada e coordenar as duas caixas com tampo/estrutura; diferença pequena não equivale a tolerância aprovada.",
        "Escolher MOVENTO400 ou varianteFGVTN400; quantitativos são alternativas e não somam4pares.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Variante de traseira 20 e folgas da corrediça no estudo de gavetas; preservar compatibilidade com estrutura da bancada.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
        "Arenza aprovado explicitamente nas frentes; padrão comercial da face lateral aparente da caixa não individualizado. wood é referência CAD."
      ],
      "assembly": [
        "Preservar duas gavetas à esquerda e centro livre da bancada.",
        "Abertura total foi escolhida; amortecimento das gavetas do escritório não foi confirmado.",
        "MOVENTO400: caixa390, útil359; largura interna364−42=322, externa352 com laterais15. Gabarito oficial rege furos traseiros/engates.",
        "Não reduzir comprimento a350: perderia50mm úteis com MOVENTO ou40mm com FGVTN em paredes equivalentes."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Alternativas_escritorio/Resultado.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Resultado.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Gavetas/Ferragens_quantitativo.csv",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P16.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P16.svg"
    }
  },
  "P17": {
    "hardware": [
      "Dobradiças amortecidas; suspensão e ligações ainda a dimensionar."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Dimensionar distribuição de carga, suspensão e ligações dos quatro vãos482/464/482/464; não somar capacidades de suspensores sem distribuição.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Divisórias 18 não equivalem a montantes até piso: carga depende das ligações e da suspensão. Não somar capacidade das ferragens sem distribuição.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Off-white fosco. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P17",
      "matriz",
      "fixas",
      "bancada",
      "portas",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P17",
      "name": "Aéreo do escritório",
      "room": "escritorio",
      "dimensions": [
        2000.0,
        350.0,
        550.0
      ],
      "internalMeasures": "Quatro vãos longitudinais 482 /464 /482 /464; profundidade 312 e altura 514. Centro duplo 36.",
      "panels": [
        {
          "id": "Peca384",
          "name": "Lateral direita",
          "dimensions": [
            550.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca384 (Lateral direita028); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca385",
          "name": "Lateral esquerda",
          "dimensions": [
            550.0,
            330.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca385 (Lateral esquerda012); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca386",
          "name": "Fundo",
          "dimensions": [
            1964.0,
            514.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca386 (Fundo012)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca387",
          "name": "Base",
          "dimensions": [
            1964.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca387 (Base010); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca388",
          "name": "Tampo",
          "dimensions": [
            1964.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca388 (Tampo008)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioComumR11",
          "name": "Apoio interno escritório 1 - proposta18",
          "dimensions": [
            514.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioComumR11 (Apoio interno escritório 1 - proposta18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioComumR001",
          "name": "Apoio interno escritório 2 - proposta18",
          "dimensions": [
            514.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioComumR001 (Apoio interno escritório 2 - proposta18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioComumR002",
          "name": "Apoio interno escritório 3 - proposta18",
          "dimensions": [
            514.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioComumR002 (Apoio interno escritório 3 - proposta18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR11",
          "name": "Escritório porta 4 - abrir para direita — frente com canecos",
          "dimensions": [
            548.0,
            496.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR11 (Escritório porta 4 - abrir para direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR012",
          "name": "Escritório porta 3 - abrir para esquerda — frente com canecos",
          "dimensions": [
            548.0,
            496.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR012 (Escritório porta 3 - abrir para esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR013",
          "name": "Escritório porta 2 - abrir para direita — frente com canecos",
          "dimensions": [
            548.0,
            496.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR013 (Escritório porta 2 - abrir para direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR014",
          "name": "Escritório porta 1 - abrir para esquerda — frente com canecos",
          "dimensions": [
            548.0,
            496.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Off-white fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Off-white fosco",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR014 (Escritório porta 1 - abrir para esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2012",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "ApoioOpostoR18",
          "name": "Escritório - segundo18 no divisor das portas2/3; conjunto36",
          "dimensions": [
            514.0,
            312.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD ApoioOpostoR18 (Escritório - segundo18 no divisor das portas2/3; conjunto36)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD); alternativa FGVTN TN MS Slow H0 51MS15XTN2200BF, não cumulativa",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "4 folhas × 2 dobradiças = 8 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Escritório | 496 × 548 × 18 | 4 | 2 | 3.18 / 3.67 / 4.40 | alta/estreita | Cabeceira A | 439.75 × 306 × 18 | 2 | 2 | 1.57 / 1.82 / 2.18 | baixa/larga | Cabeceira B | 440.25 × 306 × 18 | 2 | 2 | 1.58 / 1.82 / 2.18 | baixa/larga | Espelheiro | 297 × 748 × 18 | 2 | 3 | 4.82 / 5.22 / 5.82 | alta/estreita | Roupeiro correr | 995 × 1999 × 18 | 2 | correr | 23.27 / 26.85 / 32.22 | alta/estreita | Maleiro"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "4 × 2",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "19contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Off-white fosco. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Off-white fosco",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2012"
        }
      ],
      "fieldChecks": [
        {
          "id": "P17-CAMPO-1",
          "measure": "Medir faixa livre, prumo, tomadas e alturas dos equipamentos/monitores sob o armário.",
          "method": "Laser/nível, croqui e posicionamento do equipamento real.",
          "affects": "Cota de instalação, aberturas e suspensão.",
          "value": null
        },
        {
          "id": "PAREDE-ESCRITORIO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Dimensionar distribuição de carga, suspensão e ligações dos quatro vãos482/464/482/464; não somar capacidades de suspensores sem distribuição.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Divisórias 18 não equivalem a montantes até piso: carga depende das ligações e da suspensão. Não somar capacidade das ferragens sem distribuição.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos."
      ],
      "assembly": [
        "Portas convencionais de abrir, perfil na borda e amortecimento foram escolhidos.",
        "Apoios de 18 mm e centro duplo de 36 mm dependem das uniões e da suspensão, não são montantes até o piso.",
        "Alternativa FGVTN H0: caneco Ø35 × 11,3 mm, chapa 18 nominal; a furação Blum de 13 mm não é autorização para reutilização. K5/recobrimento16, exceto duas dobradiças da folha vizinha da cabeceira com K6/17.",
        "Divisor centralduplo36 preservado; divisórias18 não são montantes até piso."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Avanco_pendencias_2026-10-21/Ferragens/Dobradicas_46_compatibilidade.html",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P17.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P17.svg"
    }
  },
  "P18": {
    "hardware": [
      "Referência vigente BC43 de correr; frente removível M6 em estudo."
    ],
    "pending": [
      "Validar resistência do conjunto removível, porcas/cavilhas e suspensão no material escolhido;30kgRO25não é capacidade do gabinete.",
      "Conferir variante sobreposta/embutida RO25 e desenho real antes de usinar cavidadeØ32×10 e pilotos ilustrativos.",
      "Fechar comprimento útilM6, retenção dos batentes, acabamento de bordas/cavas/furos e ferramenta compacta nos acessos.",
      "Definir produto hidráulico e acesso; recorteØ100 do sifão de referência é cenário e não ordem de corte.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Abertura frontal 507 não é altura útil 509 de versões anteriores. Hidráulica e frente removível M6 dependem de estudo BC43. Não usar Modulo017 histórico oculto.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
      "Distribuição do acabamento aparente do quadro (bege da frente versus madeira lateral) não individualizada; escolher tecnicamente sem presumir."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Bege fosco nas frentes; madeira clara nas laterais. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P18",
      "matriz",
      "fixas",
      "portas",
      "torneiras",
      "purangi",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P18",
      "name": "Gabinete do banheiro",
      "room": "banho",
      "dimensions": [
        600.0,
        470.0,
        545.0
      ],
      "internalMeasures": "Caixa 564×382; base topo 218. Quadro frontal: vão 564×507 entre base 218 e travessa 725, profundidade 70. Laterais traseiras até 745.",
      "panels": [
        {
          "id": "Peca396",
          "name": "Fundo",
          "dimensions": [
            564.0,
            509.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Madeira clara (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca396 (Fundo013)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BC43_LateralE",
          "name": "Montante frontal esquerdo18×70×543",
          "dimensions": [
            543.0,
            70.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_LateralE (Montante frontal esquerdo18×70×543)",
          "finishComplete": false,
          "remainingFinish": "Distribuição do acabamento aparente do quadro (bege da frente versus madeira lateral) não individualizada; escolher tecnicamente sem presumir.",
          "quantity": 1
        },
        {
          "id": "BC43_LateralD",
          "name": "Montante frontal direito18×70×543",
          "dimensions": [
            543.0,
            70.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_LateralD (Montante frontal direito18×70×543)",
          "finishComplete": false,
          "remainingFinish": "Distribuição do acabamento aparente do quadro (bege da frente versus madeira lateral) não individualizada; escolher tecnicamente sem presumir.",
          "quantity": 1
        },
        {
          "id": "BC43_Base",
          "name": "Base do quadro564×70×18",
          "dimensions": [
            564.0,
            70.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_Base (Base do quadro564×70×18)",
          "finishComplete": false,
          "remainingFinish": "Distribuição do acabamento aparente do quadro (bege da frente versus madeira lateral) não individualizada; escolher tecnicamente sem presumir.",
          "quantity": 1
        },
        {
          "id": "BC43_Travessa",
          "name": "Topo do quadro564×70×18",
          "dimensions": [
            564.0,
            70.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_Travessa (Topo do quadro564×70×18)",
          "finishComplete": false,
          "remainingFinish": "Distribuição do acabamento aparente do quadro (bege da frente versus madeira lateral) não individualizada; escolher tecnicamente sem presumir.",
          "quantity": 1
        },
        {
          "id": "BC43_CaixaE",
          "name": "Lateral original esquerda com furos de união",
          "dimensions": [
            545.0,
            400.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Madeira clara, padrão exato a escolher",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_CaixaE (Lateral original esquerda com furos de união); 01_Projeto/Registro_de_decisoes.md:2939",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BC43_CaixaD",
          "name": "Lateral original direita com furos de união",
          "dimensions": [
            545.0,
            400.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Madeira clara, padrão exato a escolher",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_CaixaD (Lateral original direita com furos de união); 01_Projeto/Registro_de_decisoes.md:2939",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BC43_CaixaBase",
          "name": "Base original preservada",
          "dimensions": [
            564.0,
            382.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_CaixaBase (Base original preservada)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BC43_PainelEsquerda",
          "name": "Folha 292×500×18 — cava18×80×6",
          "dimensions": [
            500.0,
            292.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Bege fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Bege fosco liso",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_PainelEsquerda (Folha 292×500×18 — cava18×80×6); 01_Projeto/Registro_de_decisoes.md:2939",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BC43_PainelDireita",
          "name": "Folha 292×500×18 — cava18×80×001",
          "dimensions": [
            500.0,
            292.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Bege fosco (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Bege fosco liso",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BC43_PainelDireita (Folha 292×500×18 — cava18×80×001); 01_Projeto/Registro_de_decisoes.md:2939",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Confirmat de união do quadro",
          "reference": "7 ×50; referência de tipo GTV WK-CF0750-01",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "1por extremidade da base/topo; pré-furo escalonado conforme chapa/parafuso.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Cavilhas da união permanente do quadro",
          "reference": "Ø8 ×30",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Alinham os encontros fixos do quadro; distintas das cavilhas de desmontagem.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Parafusos de retirada do quadro",
          "reference": "M6 ×100, cabeça nominalØ10 ×6",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Acessos frontais; rebaixoØ11 ×6 é de estudo; conferir rosca útil.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Porcas transversais",
          "reference": "Häfele264.82.014 como referência dimensional M6 Ø10 ×14",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Alojadas nas laterais;4mm nominais de madeira remanescente não comprovam resistência.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Cavilhas da interface desmontável",
          "reference": "Ø8 ×30",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "15mm por peça; colar somente no quadro, preservando retirada.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Kits de correr das folhas",
          "reference": "Rometal RO25",
          "quantity": 2,
          "unit": "kit de 1 porta",
          "status": "candidato",
          "assembly": "Cada kit2carros+2guias; RO25real ainda não representado por CAD oficial.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Trilhos do conjunto",
          "reference": "Rometal RM026,564mm por trecho",
          "quantity": 4,
          "unit": "trecho",
          "status": "candidato",
          "assembly": "2 inferiores + 2 superiores; 4 × 564 = 2256 mm totais antes da otimização de barras.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Parafusos das ferragens RO25",
          "reference": "3,5 ×12 CF",
          "quantity": 24,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "4por carro e2por guia:4carros×4 +4guias×2 =24.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Batentes de curso",
          "reference": "Propostas dimensionais próprias, não acessórios homologados RO25",
          "quantity": 4,
          "unit": "contato de parada",
          "status": "candidato",
          "assembly": "3pads2mm;1calço35+pad2 para preservar cava traseira.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Parafusos do calço traseiro",
          "reference": "4 ×50",
          "quantity": 2,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Penetração nominal15na lateral,3mm restantes; cabeças sob pad removível.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ]
        },
        {
          "item": "Carros RO25 incluídos nos kits",
          "reference": "Rometal RO25",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos2kits; não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ],
          "includedIn": "Kits de correr das folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Guias RO25 incluídos nos kits",
          "reference": "Rometal RO25",
          "quantity": 4,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Já incluídos nos2kits; não compra adicional.",
          "evidence": [
            {
              "path": "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
              "trecho": "Peças e uniões propostas — mm | Item | Quantidade | Dimensão / observação | |---|---:|---| | Montantes do quadro | 2 | 18 × 70 × 543 | | Base e topo do quadro | 2 | 564 × 70 × 18; entre os montantes | | Folhas | 2 | 292 × 500 × 18; transpasse24 | | Confirmat de união do quadro | 4 | 7 × 50; um por extremidade da base/topo | | Cavilhas de união permanente do quadro | 4 | Ø8 × 30; completam a orientação dos encontros | | Parafusos de retirada do conjunto | 4 | M6 × 100; cabeça cilíndrica nominalØ10 ×6; rebaixoØ11 ×6 no estudo | | Porcas transversais | 4 | M6, Ø10 ×14; referência dimensional Häfele264.82.014 | | Cavilhas na interface desmontável | 4 | Ø8 ×30;15 em cada peça; colar apenas no quadro | | Kits RO25 | 2 | Cada um:2 carros e2 guias, conforme manual Rev11 | | Trilhos RM026 | 4 | 564; dois inferiores e dois superiores | | Parafusos das ferragens RO25 | 24 | 3,5 ×12 CF:4 por carro e2 por guia no detalhamento | | Batentes | 4 | Contatos de fim de curso, um com prolongamento de35 para manter a cava traseira visível; três pads2 colados; o calço traseiro35 + pad2 recebe2 parafusos4×50 | O calço traseiro recebe dois parafusos4×50, eixosY4860/Z465/475, pela faceX2813 em direção à lateral esquerda;15 de penetração nominal na lateral, deixando3 até o exterior. As cabeças ficam sob o pad removível. Pré-furar conforme chapa, sem colar o conjunto frontal à caixa. Os batentes são propostas dimensionais, não acessórios homologados RO25. Não substituir a retenção própria do sistema por um simples batente. Montar e regular conforme o kit real. Não foi localizado STEP oficial; carros e guias continuam identificados como envelopes. ## Cotas das fixações Sistema global da R42: X transversal; Y cresce para o fundo; Z é altura sobre piso. Face frontal do quadro Y4820, junta quadro/caixa Y4890. - Quatro M6: X2771/3349, Z260/680. Relativo à face externa esquerda do quadro: X11/589; alturas60/480 a partir de sua base. Cabeças rebaixadas pela frente. Furo passante ilustrativoØ6,5. Verificar comprimento de rosca útil no parafuso escolhido. - Porcas: eixo Y4915,25 atrás da junta; furo"
            }
          ],
          "includedIn": "Kits de correr das folhas",
          "derivation": "2 kits × 2 componentes"
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "0contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Bege fosco nas frentes; madeira clara nas laterais. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Bege fosco nas frentes; madeira clara nas laterais",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2939"
        }
      ],
      "fieldChecks": [
        {
          "id": "P18-CAMPO-1",
          "measure": "Medir parede, altura/posição da pedra, sifão, engates e percurso frontal de retirada junto ao vaso/porta.",
          "method": "Croqui com datum no piso acabado e gabarito do quadro removível inteiro.",
          "affects": "Recortes e manutenção frontal, sem colar a junta desmontável.",
          "value": null
        },
        {
          "id": "PAREDE-BANHO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Validar resistência do conjunto removível, porcas/cavilhas e suspensão no material escolhido;30kgRO25não é capacidade do gabinete.",
        "Conferir variante sobreposta/embutida RO25 e desenho real antes de usinar cavidadeØ32×10 e pilotos ilustrativos.",
        "Fechar comprimento útilM6, retenção dos batentes, acabamento de bordas/cavas/furos e ferramenta compacta nos acessos.",
        "Definir produto hidráulico e acesso; recorteØ100 do sifão de referência é cenário e não ordem de corte.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Abertura frontal 507 não é altura útil 509 de versões anteriores. Hidráulica e frente removível M6 dependem de estudo BC43. Não usar Modulo017 histórico oculto.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
        "Distribuição do acabamento aparente do quadro (bege da frente versus madeira lateral) não individualizada; escolher tecnicamente sem presumir."
      ],
      "assembly": [
        "No estudo BC43, retirar o quadro frontal inteiro pelas quatro uniões M6; não colar/selar permanentemente a junta desmontável.",
        "Proteger bordas, cavas e furos da umidade com acabamento compatível a especificar; ferragens continuam condicionais.",
        "Usar vão frontal 507 mm; não propagar 509 mm de referências históricas como abertura livre atual.",
        "Montar cantos do quadro em bancada; manutenção habitual retira apenas4M6frontais. Não colar ou selar permanentemente a junta desmontável.",
        "Prever tampas de acabamento removíveis sobre os4acessosM6; não estão modeladas e não devem impedir a ferramenta.",
        "Vão frontal507 e folhas500 seguem regra−7. O interior histórico509 não substitui o vão frontal; manter essa distinção.",
        "Guias e carros para a face interna. Cavas18 ×80 ×6 evitam pega saliente; fechar retenção pelo kit real, não apenas pelos batentes."
      ],
      "sources": [
        "01_Projeto/Avanco_pendencias_2026-10-21/Banheiro_solucao/Detalhamento_R02/Detalhamento.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P18.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P18.svg"
    }
  },
  "P19": {
    "hardware": [
      "Oito pinos Häfele 282.04.711 candidatos para duas prateleiras."
    ],
    "pending": [
      "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
      "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
      "Definir carga das prateleiras rasas e validar retenção/adesivo do vidro4mm independentemente da dobradiça.",
      "Não transferir80kg publicados para4pinos à capacidade da chapa; confirmar furação, eixo da cabeça e acabamento do SKU.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
      "Não usar material mirror como acabamento integral das chapas FrenteComumR019/R020: vidro frontal e substrato de madeira são camadas distintas.",
      "Oito apoios .711 cabem no estudo separado. Resistência da chapa estreita limita carga; ancoragem da caixa na parede desconhecida.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
      "Acabamento da face inferior aparente não individualizado; madeira clara aprovada apenas nas laterais."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Espelho na frente; madeira clara nas laterais. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P19",
      "matriz",
      "fixas",
      "espelheiro",
      "torneiras",
      "purangi",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P19",
      "name": "Espelheiro",
      "room": "banho",
      "dimensions": [
        600.0,
        150.0,
        750.0
      ],
      "internalMeasures": "Prateleiras 560×104×18; folgas 2 nas laterais e fundo. Vãos verticais 226 /226 /226 entre base 1168, níveis 1394–1412/1638–1656 e topo 1882.",
      "panels": [
        {
          "id": "Peca400",
          "name": "Lateral direita",
          "dimensions": [
            750.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Madeira clara (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Madeira clara, padrão exato a escolher",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca400 (Lateral direita030); 01_Projeto/Registro_de_decisoes.md:2953",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca401",
          "name": "Lateral esquerda",
          "dimensions": [
            750.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Madeira clara (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Madeira clara, padrão exato a escolher",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca401 (Lateral esquerda014); 01_Projeto/Registro_de_decisoes.md:2953",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca402",
          "name": "Fundo",
          "dimensions": [
            714.0,
            564.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Madeira clara (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca402 (Fundo014)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca403",
          "name": "Base",
          "dimensions": [
            564.0,
            108.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Madeira clara (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca403 (Base012)",
          "finishComplete": false,
          "remainingFinish": "Acabamento da face inferior aparente não individualizado; madeira clara aprovada apenas nas laterais.",
          "quantity": 1
        },
        {
          "id": "Peca404",
          "name": "Tampo",
          "dimensions": [
            564.0,
            108.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Madeira clara (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca404 (Tampo009)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR019",
          "name": "Armário espelhado raso - porta direita — frente com canecos",
          "dimensions": [
            748.0,
            297.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Espelho (camada distinta do substrato)",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR019 (Armário espelhado raso - porta direita — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2953",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "FrenteComumR020",
          "name": "Armário espelhado raso - porta esquerda — frente com canecos",
          "dimensions": [
            748.0,
            297.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Espelho (camada distinta do substrato)",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD FrenteComumR020 (Armário espelhado raso - porta esquerda — frente com canecos); 01_Projeto/Registro_de_decisoes.md:2953",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PrateleiraEspelhadoR12",
          "name": "Prateleira removível espelhado 1 - proposta",
          "dimensions": [
            560.0,
            104.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PrateleiraEspelhadoR12 (Prateleira removível espelhado 1 - proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PrateleiraEspelhadoR001",
          "name": "Prateleira removível espelhado 2 - proposta",
          "dimensions": [
            560.0,
            104.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PrateleiraEspelhadoR001 (Prateleira removível espelhado 2 - proposta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de caneco das portas de abrir",
          "reference": "Blum 71B3550 (base CAD)",
          "quantity": 6,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "2 folhas × 3 dobradiças = 6 no estudo vigente. Quantidade identificada; resistência e produto final não aprovados.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "Espelheiro | 297 × 748 × 18 | 2 | 3 | 4.82 / 5.22 / 5.82 | alta/estreita | Roupeiro correr | 995 × 1999 × 18 | 2 | correr | 23.27 / 26.85 / 32.22 | alta/estreita | Maleiro correr | 670 × 237 × 18 | 2 | correr | 1.86 / 2.14 / 2.57 | baixa/larga | Canto A/B | 271 × 306 × 18 | 2 | 2 | 0.97 / 1.12 / 1.34 | alta/estreita | Banheiro correr R43 | 292 × 500 × 18 | 2 | correr | 1.71 / 1.97 / 2.37 | alta/es"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            },
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Blum71B3550 | 56 dobradiças | Oferta identificada; acabamento pendente | Varotti: par08888383, acabamento Onyx | Código-base igual ao estudo; oferta encontrada é Onyx. Não alterar acabamento/modelo automaticamente; conta"
            }
          ],
          "derivation": "2 × 3",
          "quantityBasis": "Contagem vigente R45, não dimensionamento final por massa"
        },
        {
          "item": "Calços correspondentes às dobradiças",
          "reference": "Blum 173H7100; H0 próprio do conjunto FGVTN somente se essa alternativa for escolhida",
          "quantity": 6,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Um calço por dobradiça; não misturar fabricante/furação e não duplicar se já incluído. A quantidade histórica56 da fonteR38 é superada pela contagemR45.",
          "evidence": [
            {
              "path": "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
              "trecho": "Calços | Blum173H7100; alternativa175H3100 não aplicada | 56 calços | Não fechado: código/estoque exato | Marceneiro: calço cruz0; Floresta: calço reto05891994 | Calço cruz: distância37mm, excêntrico, mas anúncio não identifica173H7100. Calço reto05891994 usa20mm e é outra implan"
            },
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "As famílias de abrir totalizam24folhas e52dobradiças no estudo vigente:42 comuns/20folhas,4 no canto e6 no espelheiro. As4dobradiças e2folhas antigas do gabinete do banheiro foram excluídas: a R43 as substituiu por portas de correr. A tabela históricaR41/R42 com56não é quantitativo vigente de compra. A contagem não é aprovação de resistência. Roupeiro/maleiro têm4folhas e4kitsRO-62 de uma porta; cada kit tem2carros,2guias e2freios. O banheiroR43 acrescenta2folhas comRO25/RM026, em lista separada"
            }
          ],
          "includedWhenBundled": true,
          "derivation": "1 calço × cada dobradiça"
        },
        {
          "item": "Limitadores de abertura, somente nas folhas que necessitarem",
          "reference": "Blum 70T3553 somente com a dobradiça Blum compatível",
          "quantity": null,
          "unit": "unidade",
          "status": "pendente",
          "assembly": "Nas folhas efetivamente limitadas, equipar todas as dobradiças daquela folha; não multiplicar automaticamente por 52.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
              "trecho": "O curso86° no CAD utiliza cinemáticaBlum. A TN MS abre110° e não possui trajetória/componente limitador86° confirmado nesta pesquisa. Nas portas onde há obstáculo, uma simulaçãoBlum não validaFGVTN. Se mantidaBlum, o limitador70T3553 é referência comercial compatível com a família e deve equipar todas as dobradiças da folha limitada; seu encaixeCAD ainda tem diagnóstico pendente. Não estender automaticamente a compra a52limitadores. 3. Portas de correr Rometal RO-62: limite60kg por porta, espessura15–25mm, AP=AV−35 e transpasse20–30. O modelo usa18mm, transpasse30; roupeiro995×1999 e maleiro670×237. A massa bruta é menor que60kg nos três cenários, mas esse limite não dimensiona painel, fixação, trilhos, retenção ou empenamento. Compatibilidade nominal resolvida: 2034−35=1999 e272−35=237. O"
            }
          ]
        },
        {
          "item": "Apoios das duas prateleiras",
          "reference": "Häfele282.04.711",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "4por prateleira; já incluídos na necessidade anterior, não8adicionais.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Espelheiro.md",
              "trecho": "Duas prateleiras 560 × 104 × 18 mm, cada uma com quatro apoios Häfele 282.04.711. As folgas nominais de 2 mm em cada lateral e no fundo permanecem. Nenhuma mudança de tampa, porta ou volume interno. O catálogo do fabricante mostra haste Ø5 × 8 mm, projeção da cabeça 10 mm, largura 7,5 mm e espessura 2,7 mm. A referência vizinha 282.04.712 tem outras cotas: não misturar sua descrição com a .711. [Catálogo Häfele, página 7.154](https://assets.daro.com/HafeleLiterature/18T7-154.pdf). ## Coordenadas de montagem Coordenadas globais do modelo, em mm. Em ambas as laterais, quatro furos Ø5 cegos com profundidade proposta 8,5 mm. O datum vertical abaixo é o eixo da haste na aproximação usada; conferir a peça física antes de furar. | Superfície interna | X | Y"
            }
          ],
          "derivation": "2 prateleiras × 4 apoios"
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "6contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        },
        {
          "item": "Suspensão do móvel e interface com a parede",
          "reference": null,
          "quantity": null,
          "unit": "conjunto",
          "status": "pendente",
          "assembly": "SAH215/9189903pesquisado exige rebaixo16mm ausente nas caixas atuais; não lançar como compatível. Conector–móvel, trilho e ancoragem são interfaces distintas.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
              "trecho": "Suspensão de aéreos | HettichSAH215, referência 9189903, pesquisada | Requer rebaixo posterior mínimo 16 além da face traseira do fundo. Os fundos atuais terminam na mesma face das laterais: zero reserva. Não cabe automaticamente sem mudar caixa/afastamento. | | Fixação na parede | Buchas/parafusos compatíveis com substrato real | Pendência legítima de campo. Não selecionar bucha universal como prova de carga. Conector móvel, trilho e parede são elos distintos. | ## Suspensão e caminho da carga O SAH215 pesquisado tem ajuste e capacidade publicada 45 kg por peça nas condições de ensaio, fixação obrigatória na lateral e necessidade de rebaixo 16. Essa capacidade "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Espelho na frente; madeira clara nas laterais. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Espelho na frente; madeira clara nas laterais",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:2953"
        }
      ],
      "fieldChecks": [
        {
          "id": "P19-CAMPO-1",
          "measure": "Medir posição da cuba/torneira, saída elétrica, prumo e faixa livre acima e abaixo do espelheiro.",
          "method": "Trena/laser e fotos com escala; gabarito da abertura das portas.",
          "affects": "Altura de instalação, abertura e iluminação sem colisão com torneira.",
          "value": null
        },
        {
          "id": "PAREDE-BANHO",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter massa da folha acabada (chapa, fita, adesivo, puxador e vidro se houver) e validar quantidade/fixação pela tabela do fabricante da ferragem escolhida.",
        "Fechar padrão de parafusos, piloto, profundidade de caneco e trajetória da ferragem real; a cinemática Blum não valida automaticamente FGVTN.",
        "Definir carga das prateleiras rasas e validar retenção/adesivo do vidro4mm independentemente da dobradiça.",
        "Não transferir80kg publicados para4pinos à capacidade da chapa; confirmar furação, eixo da cabeça e acabamento do SKU.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Definir sistema de suspensão e ligação à caixa antes de quantificar; a alternativaHettichSAH215exige16mmtraseiros e não cabe automaticamente no fundo alinhado atual.",
        "Não usar material mirror como acabamento integral das chapas FrenteComumR019/R020: vidro frontal e substrato de madeira são camadas distintas.",
        "Oito apoios .711 cabem no estudo separado. Resistência da chapa estreita limita carga; ancoragem da caixa na parede desconhecida.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
        "Acabamento da face inferior aparente não individualizado; madeira clara aprovada apenas nas laterais."
      ],
      "assembly": [
        "Porta em madeira e espelho são camadas diferentes; a espessura geométrica da chapa não inclui automaticamente o vidro.",
        "Prateleiras removíveis preservam folgas nominais de 2 mm; oito apoios são candidatos e ancoragem permanece a definir.",
        "HasteØ5×8; cabeça10×7,5×2,7. Furos cegos propostosØ5×8,5; folgas2mm laterais/fundo preservadas.",
        "Prateleiras560 ×104 ×18; lateraisY5184/5250, níveisZ1394/1638no estudo. Conferir datum real da haste antes de furar."
      ],
      "sources": [
        "01_Projeto/Consolidacao_R45_2026-10-23/Portas_e_articulacoes/Relatorio.html",
        "01_Projeto/Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/README.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Espelheiro.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P19.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P19.svg"
    }
  },
  "P20": {
    "hardware": [
      "Southco candidata com fixação R47 em estudo separado.",
      "Rockler traseira e abertura frontal foram rejeitadas. Batente independente pendente."
    ],
    "pending": [
      "Obter CAD/medida oficial da distância eixo–face, envelope montado e identificação inequívoca do sentidoF0/R0. Não usar20,3/2nem escala de imagem como cota de eixo.",
      "Recalcular torque com massa e centro de gravidade móveis: NBK publica181g/180g por conjunto;2dobradiças6110+contraplacas somam688,56g antes de parafusos/batente, invalidando a suposição anterior de0,5kgcomo valor fechado.",
      "Dimensionar dobramento/solda, receptores, roscas, classe/torqueM6, madeira e apoio local; verificar batente por impacto e ligações completas.",
      "Ajustar bolsões provisórios e batente ao CAD real sem reduzir armazenamento; verificar revestimento e conforto, sem inferir comportamento da espuma.",
      "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
      "Estrutura, ligações, eixos e retenção das duas tampas devem seguir revisão R47; a menção Rockler da matriz é histórica e foi superada.",
      "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
      "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
      "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
      "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
      "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
      "Detalhar face superior sob almofada, recessos e composição com receptor R47; não inferir uma chapa comercial de duas faces."
    ],
    "finish": "Interiores Branco TX. Faces aparentes: Greenplac Arenza na base aparente; estofado separado. Faces registradas separadamente; não implica chapa dupla pronta.",
    "documentIds": [
      "ficha-P20",
      "matriz",
      "fixas",
      "banco",
      "southco",
      "batente",
      "mesa-varal",
      "acabamentos-r13"
    ],
    "fabrication": {
      "code": "P20",
      "name": "Banco baú",
      "room": "sala",
      "dimensions": [
        1800.0,
        450.0,
        470.0
      ],
      "internalMeasures": "Duas tampas preservadas 971×448×20 e 825×448×20.",
      "panels": [
        {
          "id": "Peca407",
          "name": "Lateral esquerda",
          "dimensions": [
            450.0,
            400.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca407 (Lateral esquerda015); 01_Projeto/Registro_de_decisoes.md:612",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca408",
          "name": "Fundo",
          "dimensions": [
            1764.0,
            382.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Greenplac Arenza (referência CAD)",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca408 (Fundo015)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR16",
          "name": "Frente18 estrutural - apoio não calculado",
          "dimensions": [
            1764.0,
            400.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR16 (Frente18 estrutural - apoio não calculado); 01_Projeto/Registro_de_decisoes.md:612",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR001",
          "name": "Fundo potes/travessas a80 - hipótese18",
          "dimensions": [
            390.0,
            362.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR001 (Fundo potes/travessas a80 - hipótese18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR002",
          "name": "Fundo demais setores a100 - hipótese18",
          "dimensions": [
            1384.0,
            390.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR002 (Fundo demais setores a100 - hipótese18)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR003",
          "name": "Divisória18 contínua - centro da junta",
          "dimensions": [
            390.0,
            320.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR003 (Divisória18 contínua - centro da junta)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR004",
          "name": "Divisória18 contínua - centro da junta",
          "dimensions": [
            390.0,
            300.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR004 (Divisória18 contínua - centro da junta001)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR005",
          "name": "Divisória18 contínua - centro da junta",
          "dimensions": [
            390.0,
            300.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR005 (Divisória18 contínua - centro da junta002)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR029",
          "name": "Painel posterior de estudo18 removível - folgas3",
          "dimensions": [
            356.0,
            202.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR029 (Painel posterior de estudo18 removível - folgas3)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR030",
          "name": "Painel frontal de estudo18 removível - folgas3",
          "dimensions": [
            356.0,
            177.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR030 (Painel frontal de estudo18 removível - folgas3)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Peca406AtualR31",
          "name": "Lateral fechada18 - banco com acesso superior",
          "dimensions": [
            450.0,
            400.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "face interna Branco TX; face aparente Greenplac Arenza",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Peca406AtualR31 (Lateral fechada18 - banco com acesso superior); 01_Projeto/Registro_de_decisoes.md:612",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR007AtualR31",
          "name": "Prateleira contínua da extensão - acesso por cima",
          "dimensions": [
            800.0,
            372.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR007AtualR31 (Prateleira contínua da extensão - acesso por cima)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "PecaBancoR006AtualR31",
          "name": "PecaBancoR006 · recorte híbrido R02 integrado",
          "dimensions": [
            390.0,
            192.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD PecaBancoR006AtualR31 (PecaBancoR006 · recorte híbrido R02 integrado)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Apoio_B01R31",
          "name": "Apoio_B01 · híbridoR02 proposto",
          "dimensions": [
            390.0,
            80.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Apoio_B01R31 (Apoio_B01 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Apoio_B02R31",
          "name": "Apoio_B02 · híbridoR02 proposto",
          "dimensions": [
            390.0,
            82.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Apoio_B02R31 (Apoio_B02 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Apoio_B03R31",
          "name": "Apoio_B03 · híbridoR02 proposto",
          "dimensions": [
            390.0,
            82.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Apoio_B03R31 (Apoio_B03 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Apoio_B04R31",
          "name": "Apoio_B04 · híbridoR02 proposto",
          "dimensions": [
            1764.0,
            18.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Apoio_B04R31 (Apoio_B04 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_frente0R31",
          "name": "Sarrafo_frente0 · híbridoR02 proposto",
          "dimensions": [
            800.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": false,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_frente0R31 (Sarrafo_frente0 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_tras0R31",
          "name": "Sarrafo_tras0 · híbridoR02 proposto",
          "dimensions": [
            800.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_tras0R31 (Sarrafo_tras0 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_frente1R31",
          "name": "Sarrafo_frente1 · híbridoR02 proposto",
          "dimensions": [
            198.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_frente1R31 (Sarrafo_frente1 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_tras1R31",
          "name": "Sarrafo_tras1 · híbridoR02 proposto",
          "dimensions": [
            198.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_tras1R31 (Sarrafo_tras1 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_frente2R31",
          "name": "Sarrafo_frente2 · híbridoR02 proposto",
          "dimensions": [
            350.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_frente2R31 (Sarrafo_frente2 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_tras2R31",
          "name": "Sarrafo_tras2 · híbridoR02 proposto",
          "dimensions": [
            350.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_tras2R31 (Sarrafo_tras2 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_frente3R31",
          "name": "Sarrafo_frente3 · híbridoR02 proposto",
          "dimensions": [
            362.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_frente3R31 (Sarrafo_frente3 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "Ref_Sarrafo_tras3R31",
          "name": "Sarrafo_tras3 · híbridoR02 proposto",
          "dimensions": [
            362.0,
            126.0,
            18.0
          ],
          "thickness": 18.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD Ref_Sarrafo_tras3R31 (Sarrafo_tras3 · híbridoR02 proposto)",
          "finishComplete": true,
          "remainingFinish": null,
          "quantity": 1
        },
        {
          "id": "BancoR43_Painel1",
          "name": "BancoR43_Painel1",
          "dimensions": [
            971.0,
            448.0,
            20.0
          ],
          "thickness": 20.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BancoR43_Painel1 (BancoR43_Painel1)",
          "finishComplete": false,
          "remainingFinish": "Detalhar face superior sob almofada, recessos e composição com receptor R47; não inferir uma chapa comercial de duas faces.",
          "quantity": 1
        },
        {
          "id": "BancoR43_Painel2",
          "name": "BancoR43_Painel2",
          "dimensions": [
            825.0,
            448.0,
            20.0
          ],
          "thickness": 20.0,
          "rectangular": true,
          "cadMaterial": "Não individualizado",
          "specifiedMaterial": "Branco TX · faces internas",
          "materialEvidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5; função CAD BancoR43_Painel2 (BancoR43_Painel2)",
          "finishComplete": false,
          "remainingFinish": "Detalhar face superior sob almofada, recessos e composição com receptor R47; não inferir uma chapa comercial de duas faces.",
          "quantity": 1
        }
      ],
      "hardwareRows": [
        {
          "item": "Dobradiças de atrito da tampa971",
          "reference": "Southco E6-10-6110F0-50 ou R0-50, sentido a confirmar",
          "quantity": 2,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "F0é pré-seleção de orientação, não mão aprovada. O sufixo0é essencial; não substituir pela varianteFsem0.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "A maior tampa usa, como pré-seleção, duas unidades12,4±2,5N·m; a menor, duas10,7±2,1N·m. São famíliasE6-10-6110F0/R0 eE6-10-695F0/R0, acabamento50. O sentido F0 é inferência da montagem estudada e deve ser confirmado na peça/CAD antes da compra; não substituir por códigos sem o zero, que têm torque diferente no outro sentido. Cenário | Tampa971 | Tampa825 | Painel a900kg/m³, sem afirmar material real | 7,830kg | 6,653kg | Momento máximo de peso na faixa de eixos | 17,51N·m | 14,88N·m | Torque mínimo do par | 19,8N·m | 17,2N·m | Reserva após orçamento hipotético de0,5kg metálicos móveis aaté60mm do eixo | 2,00N·m | 2,03N·m | As duas contraplatinas somam0,327kg po"
            }
          ]
        },
        {
          "item": "Dobradiças de atrito da tampa825",
          "reference": "Southco E6-10-695F0-50 ou R0-50, sentido a confirmar",
          "quantity": 2,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Retenção por atrito; não é assistência de elevação nem amortecimento hidráulico.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "A maior tampa usa, como pré-seleção, duas unidades12,4±2,5N·m; a menor, duas10,7±2,1N·m. São famíliasE6-10-6110F0/R0 eE6-10-695F0/R0, acabamento50. O sentido F0 é inferência da montagem estudada e deve ser confirmado na peça/CAD antes da compra; não substituir por códigos sem o zero, que têm torque diferente no outro sentido. Cenário | Tampa971 | Tampa825 | Painel a900kg/m³, sem afirmar material real | 7,830kg | 6,653kg | Momento máximo de peso na faixa de eixos | 17,51N·m | 14,88N·m | Torque mínimo do par | 19,8N·m | 17,2N·m | Reserva após orçamento hipotético de0,5kg metálicos móveis aaté60mm do eixo | 2,00N·m | 2,03N·m | As duas contraplatinas somam0,327kg po"
            }
          ]
        },
        {
          "item": "Contraplatinas móveis",
          "reference": "Aço26 ×80 ×10,2roscasM6por peça",
          "quantity": 4,
          "unit": "peça",
          "status": "candidato",
          "assembly": "Furos normais nas tampas preservam formato/espessura; não promete fixação sem furação.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "Contraplatina móvel | 4 peças de aço26×80×10, X110–136 eZ390–400. Duas roscasM6 por peça, linhaX125, centrosY±23. | Fica na faixa já ocupada pelo apoio traseiro; não reduz os compartimentos. Exige quatro furos normais por tampa, sem afinar, recortar bordas ou mudar suas dimensões. | Alojamento no corpo | 27×81×10,5, apenas no fundo/sarrafo traseiro. Calço nominal0,5 no fundo do alojamento, sob a contraplatina fechada. | Rebaixo é no corpo, não na tampa. Calço restitui o apoio vertical fechado; tolerâncias, acabamento e apoio efetivo precisam ser acertados em fabricação. | Suporte fixo | Faixa de aço80×6, ligada à traseira do corpo; vista nominal recuada10 na parte superior, alojada dentro da"
            }
          ]
        },
        {
          "item": "Suportes fixos das dobradiças",
          "reference": "Faixa de aço80 ×6; dobra e recuo a detalhar",
          "quantity": 4,
          "unit": "peça",
          "status": "candidato",
          "assembly": "Quantidade derivada das4posições de dobradiça; recuo10é hipótese até obter eixo real.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "Suporte fixo | Faixa de aço80×6, ligada à traseira do corpo; vista nominal recuada10 na parte superior, alojada dentro da reserva do encosto. | Não usa espuma como estrutura e não depende de ancoragem na parede. Exige detalhar dobra/união e compatibilizar encosto. Recuo10 é hipótese ajustável ao eixo real, não cota Southco confirmada. | Placa receptora fixa | 4 peças80×100×6, alojadas emX112–118 na traseira; quatro pontosM6 por suporte, linhasZ280/360 eY±23. | Porcas/roscas ficam contidas na madeira existente. A montagem deve anteceder o fechamento dos sarrafos. Não há porca saliente dentro do baú. | Parafusos móveis | 8M6×35 + arruelas1,6, como combinação dimensional proposta: aba4,5 + tamp"
            }
          ]
        },
        {
          "item": "Placas receptoras fixas",
          "reference": "Aço80 ×100 ×6",
          "quantity": 4,
          "unit": "peça",
          "status": "candidato",
          "assembly": "4pontosM6por suporte; montar antes do fechamento dos sarrafos.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "Placa receptora fixa | 4 peças80×100×6, alojadas emX112–118 na traseira; quatro pontosM6 por suporte, linhasZ280/360 eY±23. | Porcas/roscas ficam contidas na madeira existente. A montagem deve anteceder o fechamento dos sarrafos. Não há porca saliente dentro do baú. | Parafusos móveis | 8M6×35 + arruelas1,6, como combinação dimensional proposta: aba4,5 + tampa20 + arruela1,6 deixam8,9 de engajamento na contraplatina10. | Restam1,1mm nominais antes da face inferior; conferir rosca útil, tolerância e ponta reais. Não constitui seleção comercial definitiva. | Parafusos do suporte ao corpo | 16M6 de montagem, receptores embutidos e folga cega para eventual ponta dentro do sarrafo. | Comprimento "
            }
          ]
        },
        {
          "item": "Parafusos móveis",
          "reference": "M6 ×35",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Combinação dimensional candidata;8,9mmnominais de rosca com aba4,5+tampa20+arruela1,6.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "Parafusos móveis | 8M6×35 + arruelas1,6, como combinação dimensional proposta: aba4,5 + tampa20 + arruela1,6 deixam8,9 de engajamento na contraplatina10. | Restam1,1mm nominais antes da face inferior; conferir rosca útil, tolerância e ponta reais. Não constitui seleção comercial definitiva. | Parafusos do suporte ao corpo | 16M6 de montagem, receptores embutidos e folga cega para eventual ponta dentro do sarrafo. | Comprimento final, classe, acesso e torque de aperto pendentes. Não furar o interior por comprimento escolhido por aproximação. | Se “não mexer nas tampas” significar também não fazer qualquer furo de fixação, esta proposta não atende: os parafusos passantes precisam de furos. O e"
            }
          ]
        },
        {
          "item": "Arruelas dos parafusos móveis",
          "reference": "Espessura1,6mm; diâmetros/classe a definir",
          "quantity": 8,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "1por cada um dos8M6móveis; confirmar SKU e tolerâncias.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "Parafusos móveis | 8M6×35 + arruelas1,6, como combinação dimensional proposta: aba4,5 + tampa20 + arruela1,6 deixam8,9 de engajamento na contraplatina10. | Restam1,1mm nominais antes da face inferior; conferir rosca útil, tolerância e ponta reais. Não constitui seleção comercial definitiva. | Parafusos do suporte ao corpo | 16M6 de montagem, receptores embutidos e folga cega para eventual ponta dentro do sarrafo. | Comprimento final, classe, acesso e torque de aperto pendentes. Não furar o interior por comprimento escolhido por aproximação. | Se “não mexer nas tampas” significar também não fazer qualquer furo de fixação, esta proposta não atende: os parafusos passantes precisam de furos. O e"
            }
          ]
        },
        {
          "item": "Parafusos suporte–corpo",
          "reference": "M6; comprimento e classe a definir",
          "quantity": 16,
          "unit": "unidade",
          "status": "candidato",
          "assembly": "Não perfurar interior escolhendo comprimento por aproximação; acesso/torque pendentes.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
              "trecho": "Parafusos do suporte ao corpo | 16M6 de montagem, receptores embutidos e folga cega para eventual ponta dentro do sarrafo. | Comprimento final, classe, acesso e torque de aperto pendentes. Não furar o interior por comprimento escolhido por aproximação. | Se “não mexer nas tampas” significar também não fazer qualquer furo de fixação, esta proposta não atende: os parafusos passantes precisam de furos. O estudo preserva integralmente formato, espessura, posição e quantidade das duas tampas, mas não promete fixação sem furação. O que o CAD demonstrouSem invasão dos gabaritos armazenados nos testes: quatro conjuntos fechados e910poses de tampas+contraplatinas contra conteúdo/prateleira. Mais546po"
            }
          ]
        },
        {
          "item": "Fixadores da folha fixa de cada Southco ao suporte",
          "reference": "M6; comprimento, rosca e travamento a detalhar",
          "quantity": 8,
          "unit": "posição de fixação",
          "status": "pendente",
          "assembly": "Derivação de2furos na folha fixa×4dobradiças. São interfaces da dobradiça, distintas dos16suporte–corpo; lista executiva deve reconciliar os conjuntos.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Geometria_fabricante.md",
              "trecho": "quatro furos de passagem para M6: dois em cada folha. O espaçamento longitudinal entre os dois furos de uma folha é 46 ± 0,2 mm; cada linha está a 25 mm da referência da articulação na posição plana. A preparação do painel no desenho é Ø6,7 +0,1 mm. Os 50 mm entre linhas são da posição plana, não são uma distância que se possa aplicar diretamente a duas faces perpendiculares. As folhas têm 4,5 mm, a largura máxima do conjunto é 91,6 mm e sua projeção total a partir "
            }
          ],
          "derivation": "4 dobradiças × 2 furos na folha fixa",
          "quantityBasis": "Necessidade geométrica deduzida, não parafuso comprado"
        },
        {
          "item": "Batentes independentes das tampas",
          "reference": null,
          "quantity": 2,
          "unit": "conjunto",
          "status": "candidato",
          "assembly": "2conjuntos adicionais aos4suportesSouthco; não usar encosto estofado ou limite de software como parada.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Batente_estudo.md",
              "trecho": "Um batente independente por tampa, central longitudinalmente emY4236,5 eY5136,5, com suporte metálico próprio ancorado à traseira do corpo. Não usar o encosto estofado como estrutura nem atribuir capacidade de parada à dobradiça Southco. Chapa de contato móvel de aço30×80×10mm: X118–148, Ycentro±40, Z420–430, sobre a tampa existente. Bolsa na face inferior da almofada aproximadamente34×84×12mm, sujeita a tolerâncias e revestimento, deixando38mm nominais de espessura externa. Essa bolsa não muda a altura nem o perímetro da almofada. A chapa se apoia integralmente na face superior da tampa; fixadores de localização"
            }
          ],
          "derivation": "1 conjunto por tampa × 2 tampas"
        },
        {
          "item": "Chapas móveis de contato do batente",
          "reference": "Aço30 ×80 ×10mm no eixo hipotéticoX100/Z430",
          "quantity": 2,
          "unit": "peça",
          "status": "candidato",
          "assembly": "Dimensão depende diretamente do eixo real; não fabricar pela hipótese. União à tampa não definida.",
          "evidence": [
            {
              "path": "01_Projeto/Southco_banco_R47_2026-10-23/Batente_estudo.md",
              "trecho": "Chapa de contato móvel de aço30×80×10mm: X118–148, Ycentro±40, Z420–430, sobre a tampa existente. Bolsa na face inferior da almofada aproximadamente34×84×12mm, sujeita a tolerâncias e revestimento, deixando38mm nominais de espessura externa. Essa bolsa não muda a altura nem o perímetro da almofada. A chapa se apoia integralmente na face superior da tampa; fixadores de localização devem ficar dentro da espessura da tampa, sem peças inferiores invadindo armazenamento. Não está especificada a união definitiva da chapa à tampa. Batente fixo com face frontal emX100, largura80, contato emZ454–466 e corpo dentro deX84–100. O suporte inferior e a placa receptora podem seguir o princípio R47, com dimensionamento próprio: aço de8mm, largura"
            }
          ],
          "derivation": "1 chapa por conjunto de batente"
        },
        {
          "item": "Ligações dos painéis da carcaça",
          "reference": null,
          "quantity": null,
          "unit": "conector / fixador",
          "status": "pendente",
          "assembly": "19contatos diretos retangulares identificados nesta amostra. Escolher ligação por interface/carga/acesso; zero na amostra não significa ausência de uniões.",
          "evidence": [
            {
              "path": "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
              "trecho": "Contato não significa ligação dimensionada. Este levantamento identifica onde é necessário detalhar conectores. Somente peças diretas ativas, físicas e retangulares (volume ≥99,5% da caixa envolvente). Excluídos planos, peças virtuais, frentes móveis e peças não retangulares. Espessuras e cotas nominais; não substitui tolerância de fabricação. | Módulo | Peças | Plano do contato | Dimensões mm | Leitura | |---|---|---|---|---| | Modulo | Peca206 / Peca208 "
            }
          ]
        }
      ],
      "finishSummary": "Interiores Branco TX. Faces aparentes: Greenplac Arenza na base aparente; estofado separado. Faces registradas separadamente; não implica chapa dupla pronta.",
      "finishSpecs": [
        {
          "area": "Interiores identificados",
          "material": "Branco TX",
          "status": "Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos",
          "evidence": "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md:5"
        },
        {
          "area": "Faces aparentes",
          "material": "Greenplac Arenza na base aparente; estofado separado",
          "status": "Escolha documental preservada; distinguir cada face da mesma peça",
          "evidence": "01_Projeto/Registro_de_decisoes.md:612"
        }
      ],
      "fieldChecks": [
        {
          "id": "P20-CAMPO-1",
          "measure": "Medir parede/piso, encontro com sofá, encosto/espumas reais e percurso de abertura e manutenção.",
          "method": "Nível, trena e gabaritos das tampas/almofadas em posição de uso.",
          "affects": "Assentamento da base, folgas da tampa e acesso ao armazenamento; eixo Southco depende da ferragem escolhida.",
          "value": null
        },
        {
          "id": "PAREDE-SALA",
          "measure": "Identificar substrato real, espessura acessível e instalações ocultas na faixa de fixação.",
          "method": "Inspeção do local e documentação da construção; localizar instalações antes de definir perfurações.",
          "affects": "Escolha técnica de ancoragem, comprimento e posição das fixações deste ambiente.",
          "value": null
        }
      ],
      "technicalChecks": [
        "Obter CAD/medida oficial da distância eixo–face, envelope montado e identificação inequívoca do sentidoF0/R0. Não usar20,3/2nem escala de imagem como cota de eixo.",
        "Recalcular torque com massa e centro de gravidade móveis: NBK publica181g/180g por conjunto;2dobradiças6110+contraplacas somam688,56g antes de parafusos/batente, invalidando a suposição anterior de0,5kgcomo valor fechado.",
        "Dimensionar dobramento/solda, receptores, roscas, classe/torqueM6, madeira e apoio local; verificar batente por impacto e ligações completas.",
        "Ajustar bolsões provisórios e batente ao CAD real sem reduzir armazenamento; verificar revestimento e conforto, sem inferir comportamento da espuma.",
        "Fechar mapa de uniões por interface: material real, conector, quantidade por encontro, distâncias de borda, piloto/profundidade e acesso da ferramenta; contato de borda não é ligação dimensionada.",
        "Estrutura, ligações, eixos e retenção das duas tampas devem seguir revisão R47; a menção Rockler da matriz é histórica e foi superada.",
        "Definir produto construtivo da chapa, classe/adequação ao uso e espessura de compra; menor dimensão do CAD não é automaticamente espessura executiva.",
        "Definir união, sequência, folgas e mapa de usinagem com a ferragem selecionada; não substituir essa decisão por medição de campo.",
        "Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.",
        "Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.",
        "Fechar fita/selagem por aresta, sentido do veio nas faces decorativas e usinagens com os produtos definidos.",
        "Detalhar face superior sob almofada, recessos e composição com receptor R47; não inferir uma chapa comercial de duas faces."
      ],
      "assembly": [
        "Preservar duas tampas e armazenamento; três painéis do encosto não significam três tampas.",
        "Southco e batente R47 estão em estudo separado; não usar Rockler traseira rejeitada como especificação vigente.",
        "Não fabricar o batente pela hipótese do eixo: ferragem real, ligação e receptor precisam ser fechados.",
        "Preservar duas tampas971 ×448 ×20e825 ×448 ×20. Rebaixos das contraplatinas são no corpo/sarrafo, não redução da espessura das tampas.",
        "Bolsões sob almofadas já autorizados:4provisórios40 ×96 ×25com25mmnominais de espuma acima. Envelopes não validam cilindro real ou batente.",
        "Assento fechado deve apoiar no corpo/apoios. Dobradicas de atrito não recebem automaticamente a carga de assento."
      ],
      "sources": [
        "01_Projeto/Southco_banco_R47_2026-10-23/Relatorio.html",
        "01_Projeto/Southco_banco_R47_2026-10-23/Geometria_fabricante.md",
        "01_Projeto/Southco_banco_R47_2026-10-23/Batente_estudo.md",
        "01_Projeto/Southco_banco_R47_2026-10-23/CAD_busca_2026-10-23.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md",
        "01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Interfaces_retangulares.md",
        "01_Projeto/Registro_de_decisoes.md",
        "01_Projeto/Estudo_interativo/src/cad-data.js",
        "01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md"
      ],
      "sheetPath": "05_Entregas/Fichas_fabricacao_R13/P20.html",
      "drawingPath": "05_Entregas/Fichas_fabricacao_R13/P20.svg"
    }
  }
};
function WORKSHOP_DOC_URL(doc){return doc.path ? "docs/"+doc.path+(doc.path.endsWith(".md") ? ".html" : "") : null;}
