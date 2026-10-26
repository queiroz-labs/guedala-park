/* Dados atuais do projeto. Medidas em centímetros, salvo indicação. */
const PROJECT={
  "revision": "Consulta de marcenaria · FreeCAD R52 · iluminação CB02",
  "date": "26 outubro 2026",
  "mirrored": false,
  "name": "Guedala Park",
  "area": "40,18 m²",
  "unit": "Torre 2 · final 06",
  "ceiling": 260,
  "officeCeilingStudy": 247,
  "heightStudy": "2,60 m = 260 cm = 2600 mm — medida a confirmar; hipótese para testes, não fabricação. Elias, 26/10/2026. Não é medição do Guedala nem média do Vila das Belezas 3. Escritório: cenário separado de 2,47 m com forro, a confirmar. Forros, sancas e rebaixos não têm alturas verificadas.",
  "note": "Projeto inteiro pronto antes da mudança. Escolhas de programa preservadas. Medidas, produtos candidatos, estudos de construção e fabricação continuam condicionados.",
  "rooms": [
    {
      "id": "all",
      "name": "Apartamento",
      "sub": "Visão completa",
      "bounds": [
        -10,
        -10,
        750,
        710
      ],
      "color": "#e8e0d3"
    },
    {
      "id": "sala",
      "name": "Sala + jantar",
      "sub": "Bonnie, mesa e painel",
      "bounds": [
        485,
        175,
        750,
        565
      ],
      "color": "#dcc5a2"
    },
    {
      "id": "quarto",
      "name": "Quarto",
      "sub": "Queen e armazenamento",
      "bounds": [
        -10,
        90,
        375,
        405
      ],
      "color": "#c4b9a8"
    },
    {
      "id": "escritorio",
      "name": "Escritório",
      "sub": "Trabalho e hóspedes",
      "bounds": [
        245,
        -10,
        495,
        305
      ],
      "color": "#748a8f"
    },
    {
      "id": "cozinha",
      "name": "Cozinha",
      "sub": "Arenza + Azul Petróleo",
      "bounds": [
        380,
        530,
        750,
        710
      ],
      "color": "#2d4a50"
    },
    {
      "id": "lavanderia",
      "name": "Lavanderia",
      "sub": "Varal e área de serviço",
      "bounds": [
        245,
        530,
        390,
        710
      ],
      "color": "#cfcbc0"
    },
    {
      "id": "banho",
      "name": "Banheiro",
      "sub": "Sauge e greige",
      "bounds": [
        245,
        395,
        475,
        540
      ],
      "color": "#89957a"
    }
  ],
  "materials": [
    {
      "id": "chairFabric",
      "name": "Estofado claro · cadeiras Lina",
      "color": "#d8d0c2",
      "type": "fabric",
      "rooms": [
        "sala"
      ],
      "status": "Referência aprovada",
      "note": "Composição clara com estrutura amadeirada, recuperada da representação R43/R45. Conferir tecido e acabamento do produto real."
    },
    {
      "id": "whiteTX",
      "name": "Branco TX · interiores",
      "color": "#f3f2ed",
      "type": "solid",
      "rooms": [
        "sala",
        "quarto",
        "escritorio",
        "cozinha",
        "lavanderia",
        "banho"
      ],
      "status": "Escolhido",
      "note": "Faces internas identificadas nas fichas. As partes visíveis mantêm seus padrões. Fabricante, código e composição da chapa a definir. Tom digital aproximado."
    },
    {
      "id": "mirror",
      "name": "Espelho · frente do espelheiro",
      "color": "#b9d0d3",
      "type": "solid",
      "rooms": [
        "banho"
      ],
      "status": "Escolhido",
      "note": "Representação clara do espelho, sem simulação de reflexos. Camada frontal distinta da madeira e do interior Branco TX."
    },
    {
      "id": "finishPending",
      "name": "Acabamento ainda não definido",
      "color": "#bbbdb7",
      "type": "solid",
      "rooms": [],
      "status": "Pendente",
      "note": "Cinza neutro identifica superfícies sem acabamento registrado e volumes de estudo. Não é uma escolha de chapa."
    },
    {
      "id": "wood",
      "name": "Greenplac Arenza",
      "color": "#c4a27b",
      "type": "wood",
      "rooms": [
        "cozinha",
        "escritorio",
        "lavanderia",
        "sala",
        "quarto"
      ],
      "status": "Escolhido / referência",
      "note": "Escolhido na cozinha/escritório e testeira. Referência de composição na sala/quarto. Amostras a conferir."
    },
    {
      "id": "petrol",
      "name": "Guararapes Azul Petróleo",
      "color": "#294b51",
      "type": "solid",
      "rooms": [
        "cozinha"
      ],
      "status": "Escolhido",
      "note": "Superiores contínuos da geladeira ao cooktop. Lavanderia em Arenza. Duratex Azul Profundo é alternativa, não substituição aprovada."
    },
    {
      "id": "altblue",
      "name": "Duratex Azul Profundo",
      "color": "#263b45",
      "type": "solid",
      "rooms": [
        "cozinha"
      ],
      "status": "Alternativa",
      "note": "Alternativa de chapa à cor principal, ainda não escolhida."
    },
    {
      "id": "stone",
      "name": "Granito Branco Itaúnas",
      "color": "#ded7c7",
      "type": "stone",
      "rooms": [
        "cozinha",
        "lavanderia",
        "banho"
      ],
      "status": "Escolhido",
      "note": "Pedra natural. Padrão e cor variam por lote."
    },
    {
      "id": "paint",
      "name": "Algodão Egípcio",
      "color": "#e6dfd1",
      "type": "solid",
      "rooms": [
        "sala",
        "quarto",
        "escritorio",
        "cozinha",
        "lavanderia",
        "banho"
      ],
      "status": "Escolhido",
      "note": "Na cozinha e lavanderia, acabamento fosco com resistência à limpeza escolhido. Conferir tinta existente, linha e amostra. Tom digital aproximado."
    },
    {
      "id": "offwhite",
      "name": "Off-white fosco",
      "color": "#eeeae1",
      "type": "solid",
      "rooms": [
        "sala",
        "escritorio",
        "quarto"
      ],
      "status": "Escolha para o projeto",
      "note": "Frentes lisas e claras. Código de chapa/amostras ainda a definir."
    },
    {
      "id": "inox",
      "name": "Inox Look",
      "color": "#aeb5b5",
      "type": "solid",
      "rooms": [
        "cozinha",
        "lavanderia"
      ],
      "status": "Escolhido",
      "note": "Acabamento escolhido para IB6S e LG VC4. Comparar tons e aparência reais entre as marcas antes da compra."
    },
    {
      "id": "beige",
      "name": "Bouclê bege-claro · Bonnie",
      "color": "#d9c9b1",
      "type": "fabric",
      "rooms": [
        "sala"
      ],
      "status": "Escolhido",
      "note": "Modelo e versão de referência escolhidos. Conferir tecido do vendedor."
    },
    {
      "id": "grey",
      "name": "Cinza-claro · Daiane",
      "color": "#aeb1b2",
      "type": "fabric",
      "rooms": [
        "escritorio"
      ],
      "status": "Escolhido",
      "note": "Cinza-claro aprovado. Versão comercial e tecido ainda a conferir."
    },
    {
      "id": "head",
      "name": "Bege / greige estofado",
      "color": "#c9bbaa",
      "type": "fabric",
      "rooms": [
        "quarto",
        "sala"
      ],
      "status": "Proposta a conferir",
      "note": "Cabeceira clara aprovada como composição. Banco de jantar ainda sem tecido final."
    },
    {
      "id": "sage",
      "name": "Portobello Vivant Sauge Mate",
      "color": "#78846a",
      "type": "tile",
      "rooms": [
        "banho"
      ],
      "status": "Escolhido",
      "note": "RB-01 · 7 × 24,4 cm · parede focal do box."
    },
    {
      "id": "greige",
      "name": "Travertino Reale Greige",
      "color": "#c6bcaa",
      "type": "stone",
      "rooms": [
        "banho"
      ],
      "status": "Escolhido",
      "note": "Biancogres PB-01 Satin 90 × 90 cm. PB-01B EXT no box."
    },
    {
      "id": "ivory",
      "name": "Eliane Iseo Marfim AC",
      "color": "#dcd4c3",
      "type": "stone",
      "rooms": [
        "lavanderia"
      ],
      "status": "Escolhido",
      "note": "PL-01 · 90 × 90 cm. Entrega cerâmica. Este é acabamento de reforma."
    },
    {
      "id": "black",
      "name": "Preto / grafite",
      "color": "#282d2e",
      "type": "solid",
      "rooms": [
        "all"
      ],
      "status": "Escolhido",
      "note": "Metais, pedestal, eletrônicos e detalhes."
    },
    {
      "id": "vinyl",
      "name": "Tarkett Ambienta Design Olmo · 24192727",
      "color": "#c9b99d",
      "type": "wood",
      "rooms": [
        "sala",
        "quarto",
        "escritorio",
        "cozinha"
      ],
      "status": "Opção preferida",
      "note": "Vinílico em toda a casa, exceto banheiro/lavanderia. Olmo é a preferência. Aveia e Bétula ficam para comparar na loja. Réguas de 20,845 × 123,03 cm no modelo. Cor e veios aproximados. Direção e juntas desenhadas são simulação, com paginação e amostra a conferir."
    },
    {
      "id": "bathbeige",
      "name": "Arauco Beige Matt · banheiro",
      "color": "#c9bca8",
      "type": "solid",
      "rooms": [
        "banho"
      ],
      "status": "Escolhido",
      "note": "Código escolhido em 24/10/2026. Frentes fechadas e foscas, sem ripado nem puxadores salientes. Tom digital aproximado. Amostra e composição com Branco TX a conferir."
    },
    {
      "id": "lightwood",
      "name": "Arauco Louro Freijó Poro · laterais do banheiro",
      "color": "#c8a77d",
      "type": "wood",
      "rooms": [
        "banho"
      ],
      "status": "Escolhido",
      "note": "Código escolhido em 24/10/2026 para laterais aparentes do gabinete e espelheiro. Poro tem leve brilho acetinado. Amostra a conferir. Interiores Branco TX preservados."
    }
  ]
};
const ITEMS=[
  {
    "id": "bonnie",
    "room": "sala",
    "name": "Sofá Bonnie SoftGel · Cama inBox",
    "kind": "sofa",
    "dimensions": "180 × 110 fechado / 136 aberto cm",
    "choice": "Aprovado",
    "measure": "Medida informada pelo fabricante",
    "material": "beige",
    "source": "F126 / F149",
    "notes": "Retrátil, reclinável e com baú. Confirmar área útil para dormir, braços, abertura completa e afastamento traseiro. Altura 100 cm apenas gabarito.",
    "budget": "R$ 3.000 sem frete"
  },
  {
    "id": "panel",
    "room": "sala",
    "name": "Painel liso da TV",
    "kind": "panel",
    "dimensions": "115 cm L · 2 cm P no ensaio",
    "choice": "Aprovado",
    "measure": "Medida a confirmar",
    "material": "offwhite",
    "source": "F139 / F149",
    "notes": "Parede ~120 cm é estimativa gráfica. Altura do painel 165 cm ilustrativa. Confirmar corredor, cortina, montagem e Ambilight."
  },
  {
    "id": "racks",
    "room": "sala",
    "name": "Uma prateleira acima e outra abaixo da TV",
    "kind": "rack",
    "dimensions": "110 × 35 cm inferior / 110 × 25 cm superior · ensaio",
    "choice": "Aprovado",
    "measure": "Posições a definir",
    "material": "wood",
    "source": "F148 / F149 / F159",
    "notes": "A disposição vigente tem uma prateleira acima e outra abaixo da TV, sem gavetas. A implantação anterior com as duas abaixo foi superada. Alturas, equipamentos, cargas e fixação ainda precisam de conferência de encaixe e montagem."
  },
  {
    "id": "power",
    "room": "sala",
    "name": "Compartimento da régua",
    "kind": "power",
    "dimensions": "20 × 15 × 12 cm · gabarito",
    "choice": "Aprovado",
    "measure": "Hipótese",
    "material": "wood",
    "source": "F147–149",
    "notes": "Oculto, acessível e ventilado, lateral ao console. Tamanho depende da régua e fontes. Não ocupar a ventilação do PS5."
  },
  {
    "id": "tv50",
    "room": "sala",
    "name": "TV 50″ · preferência Ambilight",
    "kind": "tv",
    "dimensions": "111,1 × 64,9 × 8,8 cm de referência",
    "choice": "Parcial",
    "measure": "Duas candidatas. Modelo final pendente",
    "material": "black",
    "source": "17/10/2026",
    "notes": "Preferência principalPhilips Ambilight50PUG8100/78. Usuário aceitaStremioLite e quer aplicativos diretamente naTV, sem aparelho externo. Segunda candidataTCL50P7K comGoogle TV eStremioAndroidTV. Nenhuma substitui a preferência ou aprova compra. Teste de uso pendente. Borda inferior77 cm é hipótese.",
    "budget": "Até R$ 3.000 · TV apenas"
  },
  {
    "id": "soundbar",
    "room": "sala",
    "name": "Soundbar futura",
    "kind": "soundbar",
    "dimensions": "90 × 10,5 × 7 cm · gabarito",
    "choice": "Futuro",
    "measure": "Hipótese",
    "material": "black",
    "source": "F137 / F149",
    "notes": "Compra adiada. Dimensões ilustrativas. Conferir portas, alto-falantes superiores e espaço abaixo da TV."
  },
  {
    "id": "ps5",
    "room": "sala",
    "name": "PS5 Slim Digital · um aparelho",
    "kind": "console",
    "dimensions": "35,8 × 21,6 × 8 cm · sem saliências",
    "choice": "Direção aprovada",
    "measure": "Medida informada pelo fabricante",
    "material": "offwhite",
    "source": "F96 / F153 / F154",
    "notes": "Uso nos dois ambientes. O controle de localização move o mesmo console. Folgas mínimas, apoios e cabos a conferir."
  },
  {
    "id": "table",
    "room": "sala",
    "name": "Mesa Berlin · pronta",
    "kind": "table",
    "dimensions": "110 / 170 × 80 cm · superfície a 79 cm no estudo",
    "choice": "Modelo escolhido",
    "measure": "Medidas gerais do desenho. Conferir produto",
    "material": "wood",
    "source": "Consolidação R43/R45",
    "notes": "Berlin substitui a mesa sob medida antiga. No cenário fechado, duas cadeiras nas pontas e uma na lateral. Na abertura de 170 cm, conferir o arranjo lateral e a proximidade do sofá. Estrutura e espessura industrial não definidas pelo volume do desenho. Não fabricar com base na superfície do modelo. Aparência de referência: tampo amadeirado aproximado Arenza e base preta. Conferir o acabamento comercial da Berlin."
  },
  {
    "id": "bench",
    "room": "sala",
    "name": "Banco baú · duas tampas",
    "kind": "bench",
    "dimensions": "Tampas 971 × 448 × 20 e 825 × 448 × 20 mm",
    "choice": "Direção aprovada",
    "measure": "Ferragens e ligações em estudo",
    "material": "head",
    "source": "FreeCAD R45 · 23/10/2026",
    "notes": "Duas tampas e duas almofadas removíveis, com armazenamento preservado. Retirar almofadas antes de abrir. Tampas presas por dobradiças: diretriz atual de dobradiça piano com suporte e trava (23/10/2026). Seleção, eixo e fixações ainda pendentes. Southco R47 fica como estudo histórico. A bandeja lateral antiga está superada. Não há capacidade liberada para fabricação."
  },
  {
    "id": "diningchairs",
    "room": "sala",
    "name": "Três cadeiras · cenário Berlin",
    "kind": "chairs",
    "dimensions": "Envelopes de uso; conferir produto real",
    "choice": "Aprovado como plano",
    "measure": "Encaixe e passagem pendentes",
    "material": "head",
    "source": "Consolidação R43/R45",
    "notes": "Cenário salvo com duas cadeiras nas pontas e uma na lateral da Berlin fechada. Na mesa aberta, alternativa de três na lateral para conferir fisicamente. O desenho não comprova circulação com pessoas. Madeira em aproximação Arenza e estofado claro, conforme consolidação R43."
  },
  {
    "id": "queen",
    "room": "quarto",
    "name": "Queen com baú futura · cenário do quarto",
    "kind": "bed",
    "dimensions": "Reserva 200 × 160 cm · colchão padrão 198 × 158",
    "choice": "Tamanho futuro escolhido",
    "measure": "Base futura e cama atual não medidas",
    "material": "offwhite",
    "source": "16/10/2026",
    "notes": "A cama existente é de viúvo com baú, para a mudança. Suas medidas são desconhecidas. Queen com baú foi escolhida para a troca posterior. O desenho usa volume do desenho de estudo160 ×200 cm e altura ilustrativa60, sem representar a cama atual nem uma compra. Manter o mesmo eixo para estudar as duas fases. Mala grande futura deve caber em compartimento real do baú. Não presumir soma de duas metades."
  },
  {
    "id": "wardrobe",
    "room": "quarto",
    "name": "Roupeiro 65 cm · interior aprovado e canto atual",
    "kind": "wardrobe",
    "dimensions": "200 ×65 cm · conjunto superior até 244 cm no cenário",
    "choice": "Aprovado",
    "measure": "Medidas a conferir",
    "material": "wood",
    "source": "FreeCAD R30/R31 · geometria consolidada",
    "notes": "Profundidade 65 cm preservada. Metade para cada pessoa, quatro gavetas, dez pares até 42, dois casacos longos e programa de cabides mantidos. Face inferior dos armários superiores alinhada em 213,2 cm. Canto com portas independentes conforme estudo atual. Portas de correr, ferragens e giros são propostas condicionadas. Modelo não libera fabricação."
  },
  {
    "id": "headboard",
    "room": "quarto",
    "name": "Cabeceira estofada em dois painéis",
    "kind": "headboard",
    "dimensions": "Composição em dois painéis · cotas de estudo no modelo",
    "choice": "Aprovado",
    "measure": "Dimensões em estudo",
    "material": "head",
    "source": "R25–R31 · consolidação20/10",
    "notes": "Composição clara preservada, dividida em dois painéis conforme FreeCAD. Preparada para a queen futura, mantendo cama de viúvo no mesmo eixo como direção de uso. Medidas da base atual, alcance dos apoios, conforto e fixação pendentes."
  },
  {
    "id": "bedcabinet",
    "room": "quarto",
    "name": "Aéreos em L alinhados · canto independente",
    "kind": "upper",
    "dimensions": "Profundidades65/25 cm · base213,2 · topo244 cm de estudo",
    "choice": "Aprovado para desenvolver",
    "measure": "Encontro e medidas em estudo",
    "material": "wood",
    "source": "FreeCAD R30/R31",
    "notes": "Armário sobre o guarda-roupa e armário superior da cabeceira alinhados na mesma face inferior, sem móvel extra empilhado. Canto com duas portas independentes. Quatro faixas da cabeceira e juntas4 mm conforme R30. Material, ferragens, movimentos, teto e medidas acabadas ainda precisam de conferência. Alturas205/215 diferentes da versão antiga foram superadas."
  },
  {
    "id": "desk",
    "room": "escritorio",
    "name": "Bancada de trabalho",
    "kind": "desk",
    "dimensions": "200 × 70 cm · topo 75 cm no ensaio",
    "choice": "Parcial",
    "measure": "Largura/altura em estudo",
    "material": "wood",
    "source": "F99",
    "notes": "Profundidade 70 cm escolhida. Altura, largura, estrutura e vão real dos braços da cadeira pendentes."
  },
  {
    "id": "drawers",
    "room": "escritorio",
    "name": "Duas gavetas à esquerda",
    "kind": "drawers",
    "dimensions": "40 × 45 × 24 cm total · proposta",
    "choice": "Parcial",
    "measure": "Dimensões em estudo",
    "material": "wood",
    "source": "F92 / F99",
    "notes": "Quantidade/lado/aparência aprovados. Abertura total, pega discreta. Não garantir abertura com cama preparada."
  },
  {
    "id": "setup",
    "room": "escritorio",
    "name": "Notebook + dois monitores + CH360",
    "kind": "setup",
    "dimensions": "2 telas 27″ · CH360 21,5 × 42,8 × 43,1 cm",
    "choice": "Aprovado",
    "measure": "Equipamentos parcialmente medidos",
    "material": "black",
    "source": "F99",
    "notes": "Notebook HP à esquerda, monitor principal à direita do secundário, gabinete à direita. Monitores AOC 27/240 Hz. Modelos e braços exatos pendentes."
  },
  {
    "id": "daiane",
    "room": "escritorio",
    "name": "Sofá-cama Daiane cinza-claro",
    "kind": "daybed",
    "dimensions": "140 × 90 fechado / 140 × 182 aberto cm",
    "choice": "Aprovado",
    "measure": "Medida informada pelo fabricante",
    "material": "grey",
    "source": "F92 / F100",
    "notes": "Braço junto à parede da porta no cotidiano. Cama gira para abrir rumo à janela. Desenho mostra posições finais, não valida trajetória.",
    "budget": "Até R$ 1.500"
  },
  {
    "id": "officechair",
    "room": "escritorio",
    "name": "Cadeira · cenário Ultra Comfort",
    "kind": "chair",
    "dimensions": "74,5 × 73 cm · altura 120 ilustrativa",
    "choice": "Em estudo",
    "measure": "Candidata",
    "material": "black",
    "source": "F89 / F94",
    "notes": "Ultra Comfort não escolhida. LiberNovo também candidata. Fica estacionada no escritório durante visitas. Altura mínima dos braços pendente."
  },
  {
    "id": "officecab",
    "room": "escritorio",
    "name": "Aéreo principal sobre sofá",
    "kind": "upper",
    "dimensions": "200 ×35 ×55 cm · base190 e topo245 no cenário",
    "choice": "Aprovado",
    "measure": "Projeto aprovado",
    "material": "offwhite",
    "source": "R28/R31 e decisão17/10/2026",
    "notes": "Aéreo20 mm mais baixo que a referência antiga, com 20 mm nominais de folga ao teto de 247 cm no cenário separado de forro do escritório, a confirmar. A hipótese geral de 260 cm para novos testes (Elias, 26/10/2026) não muda esse móvel nem valida o forro. Setor para um capacete, uma sapatilha e um kit de ferramentas, com prateleiras reguláveis e ferramentas no estojo. Não criar módulo baixo ou móvel para caixa do PC. Dimensões dos objetos, carga e alcance a conferir."
  },
  {
    "id": "officeshelf",
    "room": "escritorio",
    "name": "Prateleira alta dos consoles",
    "kind": "shelf",
    "dimensions": "110 × 35 cm · topo a 195 cm",
    "choice": "Parcial",
    "measure": "Altura aprovada",
    "material": "wood",
    "source": "F154 / F155",
    "notes": "Altura aprovada por circulação. Largura é reserva de estudo para possível Xbox. Sem armário acima. Acesso/carga/posição longitudinal a conferir."
  },
  {
    "id": "tv43",
    "room": "escritorio",
    "name": "Samsung 43″ existente",
    "kind": "tv",
    "dimensions": "97 × 56 × 5 cm · gabarito",
    "choice": "Existente",
    "measure": "Modelo não informado",
    "material": "black",
    "source": "F94 / F95",
    "notes": "Parede oposta ao sofá. Posição deslocada para evitar giro da porta é estudo. Medir aparelho e suporte."
  },
  {
    "id": "wheel",
    "room": "escritorio",
    "name": "Volante e pedais futuros",
    "kind": "accessory",
    "dimensions": "Dimensões / guarda pendentes",
    "choice": "Futuro",
    "measure": "Não dimensionado",
    "material": "black",
    "source": "F92",
    "notes": "Logitech pretendido, G29 candidato. Sem módulo baixo adicional. Não desenhado no piso para não inventar local de guarda."
  },
  {
    "id": "kitchenbase",
    "room": "cozinha",
    "name": "Gaveteiro e base em Arenza",
    "kind": "kitchen",
    "dimensions": "Módulo de cocção61,3 cm · bancada63 cm P e92 cm A",
    "choice": "Aprovado para desenvolver",
    "measure": "Redistribuição dimensional em estudo",
    "material": "wood",
    "source": "R30/R31 ·20/10/2026",
    "notes": "G1/G2/G3 preservados. Abertura total e amortecimento escolhidos, ferragens propostas no FreeCAD. Cocção com 613 mm externos e577 internos, abertura nominal560. Apoios e grelhas de estudo integrados, sem aprovação de carga ou fabricação. A bancada mantém63 cm de profundidade. Recortes e emenda com lavanderia dependem do executivo."
  },
  {
    "id": "sinkstorage",
    "room": "cozinha",
    "name": "Gabinete da pia · duas portas",
    "kind": "storage",
    "dimensions": "65 cm externos no estudo ampliado",
    "choice": "Aprovado para desenvolver",
    "measure": "Medida proposta. Instalações a conferir",
    "material": "wood",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Duas portas e duas superfícies amplas de guarda. Panelas acima. Pressão, tampas, frigideira, tábuas e escorredor abaixo. Prateleira de estudo a recortar para hidráulica. Desenvolver acesso externo às conexões do cooktop/forno por este gabinete, após conferir cuba/sifão, área seca e armazenamento. Não há janela técnica nem tomada/registro posicionados."
  },
  {
    "id": "lowdrawer",
    "room": "cozinha",
    "name": "Gaveta baixa · cabos fixos separados",
    "kind": "drawer",
    "dimensions": "118,7 × 40,6 × 8,8 cm úteis · proposta",
    "choice": "Aprovado para desenvolver",
    "measure": "6 rodas 38 mm + espaçadores 1 mm selecionados. Guias e carga a conferir",
    "material": "wood",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Vassoura e rodo guardados com as cabeças retiradas e cabos fixos. Sem ajustar comprimento. Referências de 112,5 cm cabem no ensaio. Percurso de 126,9 cm sob pia/gaveteiro. Termina antes do forno. Faixa de 18 cm e recuo frontal de 8 cm. Seis rodízios fixos Leão Aço de 38 mm + seis espaçadores rígidos de 1 mm: altura total de apoio 39 mm. Banda de PU conforme vendedor. Peça real, carga, guias e apoios a conferir."
  },
  {
    "id": "kitchenupper",
    "room": "cozinha",
    "name": "Aéreos A/B/C/D em Azul Petróleo",
    "kind": "upper",
    "dimensions": "80,1 + 69,7 + 54,7 + 65 cm · proposta R03",
    "choice": "Aprovado para desenvolver",
    "measure": "Transição com lavanderia a conferir",
    "material": "petrol",
    "source": "Decisões de 25–27/09/2026",
    "notes": "A/D com divisória vertical. B com uma prateleira. C com três. D continua com 65 cm e avança 2,5 cm rumo à lavanderia. C cresce a 54,7 cm na proposta. Topo 255 cm preservado. Teto 257 cm pertence ao cenário anterior; novos testes usam 260 cm, medida a confirmar (Elias, 26/10/2026). A diferença aritmética de 5 cm não valida instalação ou folga. Perfil preto fosco na borda inferior, dobradiças amortecidas. Abertura integral preservada junto ao plafon."
  },
  {
    "id": "fridge",
    "room": "cozinha",
    "name": "Geladeira Electrolux IB6S Inox Look",
    "kind": "fridge",
    "dimensions": "60,1 × 74,75 × 186,6 cm · referência da família",
    "choice": "Aprovado",
    "measure": "Código de compra a conferir",
    "material": "inox",
    "source": "F119 / F160 / F161",
    "notes": "Acabamento inox aprovado, substituindo o branco. Reserva de largura 80,1 cm e recuo traseiro de 10 cm são cenário. Abertura, medidas do código final e ventilação ainda precisam de validação."
  },
  {
    "id": "cooktop",
    "room": "cozinha",
    "name": "Cooktop Electrolux KE4GC",
    "kind": "cooktop",
    "dimensions": "60 × 45 cm · recorte 52 × 39 cm",
    "choice": "Aprovado",
    "measure": "Instalação ainda condicionada",
    "material": "black",
    "source": "Manual Electrolux · compatibilização19–20/10/2026",
    "notes": "KE4GC preservado, gás GN já confirmado. Mesa60 ×45. Recorte52 ×39 cm. Altura total13,1 não é projeção inferior instalada. No cenário conservador131 mm inteiros abaixo da bancada, restam219 mm até o forno;209 após10 de tolerância de estudo. Caixa, fixações, gás/cabo, pedra e ventilação ainda a conferir."
  },
  {
    "id": "oven",
    "room": "cozinha",
    "name": "Fischer Infinity 50 L · grill, sem turbo",
    "kind": "oven",
    "dimensions": "Frente de estudo 59,5 ×44,7 cm · nicho 56 ×44 ×58 cm",
    "choice": "Escolhido",
    "measure": "Instalação e medidas a conferir",
    "material": "black",
    "source": "19–20/10/2026 · Fischer 28349-64929 · R02",
    "notes": "Preto 127 V, elétrico 2061 W/16,22 A. Compra ainda não realizada. Substitui o Venax. Topo conservador 57 cm e base candidata 13,8 cm. Base plana apoiada em três nervuras até o piso, faixa traseira 45 ×560 mm e duas grelhas removíveis 600 ×90 mm, com 272,43 cm² abertos cada. Capacidade do apoio, montagem real, grelhas, circuito e temperatura não homologados. Manter 200 mm ao fundo do cooktop instalado."
  },
  {
    "id": "microwave",
    "room": "cozinha",
    "name": "Micro-ondas Electrolux ME23P",
    "kind": "microwave",
    "dimensions": "46,1 × 35,2 × 29 cm · referência",
    "choice": "Aprovado",
    "measure": "Conferência de encaixe e montagem pendente",
    "material": "black",
    "source": "F103 / F104 / 15/09",
    "notes": "127 V. Mantidos 10 cm acima como escolha de layout, apesar da divergência com os 30 cm do manual. Instalação não validada."
  },
  {
    "id": "hood",
    "room": "cozinha",
    "name": "Depurador Suggar DE61IX",
    "kind": "hood",
    "dimensions": "60 × 30 × 17,6 cm fechado",
    "choice": "Aprovado",
    "measure": "Nicho e retorno de ar em estudo",
    "material": "inox",
    "source": "Decisões de 25–27/09/2026",
    "notes": "127 V em modo depurador. Vão mínimo 60,3 × 30,5 × 13,7 cm. Módulo de 60 cm externos não atende. Armário superior D de 65 cm deslocado 2,5 cm e base do aparelho a 174 cm são propostas. Preservar retorno de ar, filtros e acesso."
  },
  {
    "id": "airfryer",
    "room": "lavanderia",
    "name": "Philips Walita RI9252/91",
    "kind": "airfryer",
    "dimensions": "26,4 × 36 × 29,5 cm · referência",
    "choice": "Aprovado",
    "measure": "Uso a conferir",
    "material": "black",
    "source": "F103 / F162",
    "notes": "Permanece desligada sobre a pedra da lavanderia. Sem roupas no varal, pode ser usada ali. Com roupas, vai temporariamente para a bancada próxima à geladeira. Folgas, calor, tomadas e convivência com a cafeteira ainda a conferir."
  },
  {
    "id": "coffeemaker",
    "room": "lavanderia",
    "name": "Cafeteira Mondial existente",
    "kind": "appliance",
    "dimensions": "Modelo e dimensões adiados",
    "choice": "Existente",
    "measure": "Conferência posterior",
    "material": "black",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Faz café por caneca. Rotina para duas canecas. Uso previsto na lavanderia sem roupas no varal. Espaço a definir: modelo e dimensões adiados; sem volume no desenho e sem encaixe simultâneo demonstrado na bancada da cozinha. Não presumir funcionamento simultâneo com air fryer."
  },
  {
    "id": "sink",
    "room": "cozinha",
    "name": "Cuba Dora + torneira Apurema",
    "kind": "sink",
    "dimensions": "Zona de 65 cm no estudo · cuba 43 × 37 cm de referência",
    "choice": "Aprovado",
    "measure": "Recortes e mangueira a conferir",
    "material": "stone",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Torneira preta extensível e tábua parcial. Mini Plurale grafite em uso junto à cuba. Guardar limpo e seco no gabinete inferior. Barra discreta para o pano em uso próxima da pia. Comprimento, posição e fixação a detalhar."
  },
  {
    "id": "filter",
    "room": "cozinha",
    "name": "Purificador Electrolux PE12G grafite",
    "kind": "filter",
    "dimensions": "16 × 42 × 35 cm",
    "choice": "Aprovado",
    "measure": "Instalação a conferir",
    "material": "black",
    "source": "15/09/2026",
    "notes": "Modelo definido. Água natural, fria e gelada. Referência junto à geladeira. Reserva preliminar de 26 × 52 × 57 cm. Conferir alimentação de água, tomada, calor vizinho, acesso ao refil e posição final.",
    "budget": "Pesquisa até aproximadamente R$ 660"
  },
  {
    "id": "washer",
    "room": "lavanderia",
    "name": "LG VC4 CV5012PC4 Inox Look",
    "kind": "washer",
    "dimensions": "60 × 62 × 85 cm até porta fechada",
    "choice": "Aprovado",
    "measure": "Reservas e proteção térmica a conferir",
    "material": "inox",
    "source": "Decisões de 25–27/09/2026",
    "notes": "127 V. Reserva mínima de 64 cm de largura e 85,5 cm de altura, mais nivelamento; 72 cm da parede até porta fechada e 120 cm aberta. Pedra com apoios independentes. Junto ao forno a gás, manual pede painel isolante 850 × 600 mm com alumínio voltado ao calor. Solução ainda não especificada."
  },
  {
    "id": "laundrybase",
    "room": "lavanderia",
    "name": "Tanque integrado à pedra contínua",
    "kind": "kitchen",
    "dimensions": "38 × 35 × 20 cm internos · bancada 75 cm P",
    "choice": "Aprovado para desenvolver",
    "measure": "Hidráulica e apoios em estudo",
    "material": "stone",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Branco Itaúnas contínuo com a cozinha, com faixa de 10 cm na parede e arestas suavizadas. Telca Flex preta com cabeça extraível. Saída posterior com tampão, retentor removível e acabamento baixo. Reserva geométrica localizada de 7 cm para conexão na R08. Válvula, sifão e mangueira reais ainda não comprovados."
  },
  {
    "id": "laundryupper",
    "room": "lavanderia",
    "name": "Superiores da lavanderia em Arenza",
    "kind": "upper",
    "dimensions": "Faixa de 133 cm · módulos e alturas em estudo",
    "choice": "Aprovado",
    "measure": "Hipótese",
    "material": "wood",
    "source": "F158",
    "notes": "Transição após o cooktop. Testeira alinhada ao topo da cozinha. Espaço do aquecedor e varal preservado como estudo, com ventilação, exaustão e mecanismo a detalhar."
  },
  {
    "id": "heater",
    "room": "lavanderia",
    "name": "Rinnai E21 GN REU-E211 FEH",
    "kind": "heater",
    "dimensions": "35 × 15,7 × 53 cm · referência a conferir",
    "choice": "Aprovado",
    "measure": "Instalação pendente",
    "material": "offwhite",
    "source": "F106 / F107",
    "notes": "GN confirmado. Aparelho e exaustão continuam candidatos de conferência de encaixe e montagem. Não foi comprado. Reserva desenhada não comprova funcionamento, ventilação ou instalação. Pressão/vazão e projetos da unidade pendentes."
  },
  {
    "id": "drying",
    "room": "lavanderia",
    "name": "Varal vertical · quadro inteiro manual",
    "kind": "drying",
    "dimensions": "Grelha 100 × 50 cm",
    "choice": "Aprovado para desenvolver",
    "measure": "Mecanismo, carga e fixações pendentes",
    "material": "wood",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Movimento vertical, acionamento manual por manivela. Placa de ocultação removida na R35. Sem caixa fechada. Tanque limpo e livre serve de apoio à roupa da máquina. Curso, retenção, carga pretendida de 30 kg, janela e E21 a conferir. Alturas de uso mostradas são cenários."
  },
  {
    "id": "bathvanity",
    "room": "banho",
    "name": "Gabinete com portas de correr",
    "kind": "vanity",
    "dimensions": "Frente removível 600 × 70 × 543 mm; folhas 292 × 500 × 18 mm",
    "choice": "Aprovado",
    "measure": "Ferragens e hidráulica pendentes",
    "material": "bathbeige",
    "source": "BC43 incorporado à R45",
    "notes": "Duas folhas de correr e quadro removível. Trilhos RM026 e RO25 são referências de estudo. Quatro M6 × 100 na proposta de fixação da frente. Abertura frontal livre 507 mm conforme R45. Quatro dobradiças antigas excluídas. Instalação, resistência, tolerâncias e hidráulica continuam a conferir."
  },
  {
    "id": "basin",
    "room": "banho",
    "name": "Cuba Deca Slim branca L.13040.17",
    "kind": "sink",
    "dimensions": "40 × 30 × 13,5 cm",
    "choice": "Primeira opção aprovada",
    "measure": "Encaixe a conferir",
    "material": "offwhite",
    "source": "18/09/2026",
    "notes": "Cuba de apoio retangular. Prioridade de limpeza fácil e amplitude. Bancada de 60 × 45 cm é hipótese: 10 cm laterais e 10 atrás + 5 à frente. Conferir torneira e armário."
  },
  {
    "id": "bath tap",
    "room": "banho",
    "name": "Addra Arion Black · bica alta",
    "kind": "tap",
    "dimensions": "Altura ~30 cm · desenho de instalação pendente",
    "choice": "Aprovado",
    "measure": "Instalação a conferir",
    "material": "black",
    "source": "18/09/2026",
    "notes": "Água quente e fria. Centralizada atrás da cuba, entre cuba e espelho. Base, alcance, alavanca e fixação ainda precisam de ficha/peça real. Modelo representado de forma aproximada.",
    "budget": "Teto da torneira: R$ 750; oferta final não confirmada"
  },
  {
    "id": "bathmirror",
    "room": "banho",
    "name": "Armário raso, todo espelhado",
    "kind": "upper",
    "dimensions": "60 cm L × 12–15 cm P externos · ensaio",
    "choice": "Aprovado",
    "measure": "Dimensões e divisões em estudo",
    "material": "lightwood",
    "source": "18/09/2026",
    "notes": "Frente toda espelhada, laterais Arauco Louro Freijó Poro e interior Branco TX. Duas portas e duas prateleiras removíveis preservadas. Desenho de montagem do projeto separado de 12Minifix para a caixa. Oito apoios.711 mantidos. Fixação dos espelhos e fixação na parede a dimensionar. Protótipo pendente. Teto3000 K, espelho 4000 K e indireta 3000 K, com comandos separados."
  },
  {
    "id": "bathlight",
    "room": "banho",
    "name": "Teto 3000 K +espelho 4000 K +indireta 3000 K",
    "kind": "lighting",
    "dimensions": "Firefly25 W; espelho2×550 mm /13,2 W; indireta até2 m /9,6 W",
    "choice": "L02: componentes R$612,64 à vista; custo-benefício",
    "measure": "Montagem e posições a validar. Frete/instalação fora do total",
    "material": "offwhite",
    "source": "24/10/2026",
    "notes": "Teto Galaxy Firefly9605 branco IP44,3000 K. Espelho: mesma Cristallux COB CLX-FT331240,4000 K,IRC>90,1,10 m. Indireta: Cristallux SMD CLX-FT200530,3000 K,4,8 W/m,IRC>80,até 2 m.2 fontes Opus OPS31002 12 V/3 A/36 W/IP67,2 perfis MOV4329 com difusores. Três comandos separados. Total de componentesR$612,64 à vista, rolos inteiros incluídos;R$202,45 abaixo da L01 com espelho precificado. Perfil IP20 não viraIP65 pela fita. Encaixe interno, terminais, dissipação e luz no rosto a conferir. Barra inferior depende da torneira. Reservar até 276 mm por fonte até conferir o lote. Links: Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html. Sem compra ou alteração no CAD."
  },
  {
    "id": "shower",
    "room": "banho",
    "name": "Box transparente + Addra Livo Black Matte",
    "kind": "shower",
    "dimensions": "Faixa 80 × 124 cm brutos · hipótese",
    "choice": "Direção aprovada",
    "measure": "Box e instalações em estudo",
    "material": "sage",
    "source": "BAN-003 / 18/09/2026",
    "notes": "Ducha Livo BRS2003-BK / SKU2193038 escolhida, redonda de 13,2 cm, com desviador e duchinha. Uma única parede verde: fundo/chuveiro. Parede da janela clara. Vidro transparente com perfis pretos finos. Abertura, altura e medidas do box pendentes.",
    "budget": "Teto do conjunto Livo: R$ 850, sem registros/instalação"
  },
  {
    "id": "bath shelf",
    "room": "banho",
    "name": "Prateleira do box em Branco Itaúnas",
    "kind": "shelf",
    "dimensions": "25–30 × 10 cm · proposta",
    "choice": "Direção aprovada",
    "measure": "Posição e medidas em estudo",
    "material": "stone",
    "source": "18/09/2026",
    "notes": "Apoio para shampoo e sabonete. Prateleira escolhida em vez de nicho embutido. Não autoriza recorte de parede. É distinta da possível prateleira sobre a caixa do vaso."
  },
  {
    "id": "bathshaft",
    "room": "banho",
    "name": "Enchimento técnico existente",
    "kind": "technical",
    "dimensions": "Geometria e altura não medidas",
    "choice": "Entrega",
    "measure": "Volume ilustrativo",
    "material": "greige",
    "source": "P01 / 18/09/2026",
    "notes": "P01 identifica enchimento. A faixa de 30 cm e altura mostrada são apenas reserva gráfica. Elias informa fechamento de gesso e propõe acessar o ramal quente nessa região. Não remover automaticamente nem inferir o traçado exato das tubulações."
  },
  {
    "id": "toilet",
    "room": "banho",
    "name": "Celite VIP branco · kit 1977230012300",
    "kind": "toilet",
    "dimensions": "37,5 L × 59 P × 80 A cm",
    "choice": "Aprovado",
    "measure": "Esgoto e afastamentos a conferir",
    "material": "offwhite",
    "source": "18/09/2026",
    "notes": "Caixa acoplada, assento PP de queda amortecida e Rimless. Substitui Elite. Frente nominal 65 cm na profundidade de 124 cm, ganho de 7 cm sobre Elite. Resultado instalado depende de eixo/folga traseira."
  },
  {
    "id": "hygiene",
    "room": "banho",
    "name": "Ducha higiênica preta quente e fria",
    "kind": "shower",
    "dimensions": "Modelo e posição ainda não definidos",
    "choice": "Direção aprovada",
    "measure": "Percurso e funcionamento pendentes",
    "material": "black",
    "source": "18/09/2026",
    "notes": "Com mistura de temperatura e fechamento próprio. Posição desenhada é ilustrativa. Orçamento e modelo pendentes. Rinnai E21 exige 3,9 L/min para acionar: conferir fluxo pelo aquecedor, estabilidade e espera pela água quente."
  },
  {
    "id": "hotwater",
    "room": "banho",
    "name": "Água quente oculta: quatro caminhos em estudo",
    "kind": "technical",
    "dimensions": "Enchimento → pia e ducha higiênica",
    "choice": "Em estudo",
    "measure": "Nenhum percurso aprovado",
    "material": "paint",
    "source": "18/09/2026",
    "notes": "Comparados: acima do forro existente. Faixa fechada no canto do teto. Sob prateleira elevada de pedra. Percurso baixo atrás do vaso. Prioridade de estudo: forro existente, com descida junto ao espelho/gabinete. A faixa de gesso é alternativa. Prateleira acima da caixa precisa de nível superior ao tampo de 76,5 cm e acesso à tampa. Não avançar o vaso. Memorial restringe alterações hidráulicas. Derivação no enchimento precisa de avaliação técnica."
  },
  {
    "id": "bathfinish",
    "room": "banho",
    "name": "Algodão Egípcio, teto branco e uma parede verde",
    "kind": "finish",
    "dimensions": "Amostras, paginação e áreas a conferir",
    "choice": "Direção aprovada",
    "measure": "Produtos complementares pendentes",
    "material": "paint",
    "source": "18/09/2026",
    "notes": "Paredes fora do box em Algodão Egípcio. Teto branco. Vivant Sauge Mate apenas na parede do chuveiro. Parede clara do box, rejunte, tinta e acessórios exatos a definir. Piso Travertino Reale Greige, Satin fora/EXT dentro conforme adequação técnica."
  },
  {
    "id": "mirror",
    "room": "quarto",
    "name": "Espelho de corpo inteiro Cebrace prata",
    "kind": "mirror",
    "dimensions": "50 × 180 cm · 5 mm",
    "choice": "Aprovado",
    "measure": "Fixação a conferir",
    "material": "inox",
    "source": "15/09/2026",
    "notes": "Centralizado na lateral de 60 cm do guarda-roupa, com margens nominais de 5 cm e base a 20 cm do piso. Sem moldura ou bisotê. Bordas lapidadas e cantos levemente arredondados. Conferir painel e fixador próprio."
  },
  {
    "id": "dishrack",
    "room": "cozinha",
    "name": "Escorredor Tramontina Mini Plurale grafite",
    "kind": "accessory",
    "dimensions": "27,8 × 19,9 × 12,6 cm · 9 pratos",
    "choice": "Aprovado",
    "measure": "Guarda a conferir",
    "material": "black",
    "source": "15/09/2026",
    "notes": "Referência 61537000. Tradicional compacto, porta-talheres removível e bandeja inclinada. Usar junto à cuba e guardar limpo e seco no gabinete inferior. Substitui a esteira Mimo."
  },
  {
    "id": "pressurecooker",
    "room": "cozinha",
    "name": "Panela de pressão Vancouver Effect preta",
    "kind": "accessory",
    "dimensions": "3 L · 18,1 cm A × 23,1 cm L · Ø 20 cm",
    "choice": "Aprovado",
    "measure": "Comprimento com cabo a conferir",
    "material": "black",
    "source": "15/09/2026",
    "notes": "Tramontina 20593420. Preparo de 1 kg de feijão em mais de uma rodada, respeitando o limite de enchimento. Guarda no nível inferior da pia. Conferir manobra e instalações."
  },
  {
    "id": "trash",
    "room": "cozinha",
    "name": "Lixeira comum Biovis Coleta 15 L",
    "kind": "bin",
    "dimensions": "21 × 34 × 47 cm",
    "choice": "Aprovado",
    "measure": "Implantação a conferir",
    "material": "inox",
    "source": "15/09/2026",
    "notes": "Inox escovado, pedal e balde removível. No chão, na parede externa do banheiro, voltada para a mesa, no ponto verde aprovado. Substitui a Loop 12 L. Passagem nominal de ~107 cm até a mesa. Conferir rodapé, tampa e pedal."
  },
  {
    "id": "recycling",
    "room": "lavanderia",
    "name": "Lixeira de recicláveis Tramontina Loop 20 L",
    "kind": "bin",
    "dimensions": "29 × 29 × 43,7 cm",
    "choice": "Aprovado",
    "measure": "Implantação a conferir",
    "material": "inox",
    "source": "15/09/2026",
    "notes": "Referência 94547020. Inox polido, pedal, fechamento suave e balde removível. No chão da lavanderia, no ponto vermelho aprovado. Libera o armário sob o tanque para o cesto de roupas. Conferir tampa, pedal e circulação."
  },
  {
    "id": "kitchenfinish",
    "room": "cozinha",
    "name": "Pedra, pintura e pegas",
    "kind": "finish",
    "dimensions": "Faixa de pedra 10 cm · referência visual",
    "choice": "Aprovado",
    "measure": "Encontros e produtos a detalhar",
    "material": "paint",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Branco Itaúnas com borda reta e arestas suavizadas. Acima, Algodão Egípcio fosco resistente à limpeza, contínuo na lavanderia. Perfil estreito de alumínio preto fosco nas bordas das frentes. Conferir tinta existente, linhas, fixações e recortes."
  },
  {
    "id": "tower",
    "room": "cozinha",
    "name": "Torre automática de tomadas",
    "kind": "technical",
    "dimensions": "Saída 20 A · compatível com 127 V",
    "choice": "Aprovado para desenvolver",
    "measure": "Modelo e encaixe sob a pedra pendentes",
    "material": "black",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Sobe ao pressionar, tampa preta e posição na área seca. Conferir potência total, cabo/plugue e circuito para air fryer de 1400 W. Saída 20 A não garante a capacidade do conjunto. Não presumir uso junto com cafeteira. Furação e volume recolhido ainda sem posição."
  },
  {
    "id": "kitchenlight",
    "room": "cozinha",
    "name": "Plafon quadrado branco",
    "kind": "light",
    "dimensions": "Referência 41 × 41 × 3,8 cm · 3000 K",
    "choice": "Aprovado para desenvolver",
    "measure": "Formato aceito. Modelo/posição em estudo",
    "material": "offwhite",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Formato aprovado desde que preserve a abertura livre dos armários superiores. Stella EVO STH21967/30 é candidato. Na posição de estudo sobre a passagem, folga de cerca de 13 cm até o giro nominal da maior porta. Confirmar dobradiças, pegas e medidas. Posição longitudinal ilustrativa e cobertura ainda sem cálculo. Teto com liga/desliga próprio."
  },
  {
    "id": "counterlight",
    "room": "cozinha",
    "name": "Luz regulável da bancada",
    "kind": "light",
    "dimensions": "3000 K · comando independente",
    "choice": "Aprovado para desenvolver",
    "measure": "Fita, perfil, fonte e controle pendentes",
    "material": "offwhite",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Ligar, desligar e regular a intensidade da luz de preparo/pia. Dois trechos sob os armários superiores em estudo, respeitando bases e recuos. Não atravessar a zona quente do depurador nem ocupar sua ventilação ou a do micro. Comprimentos de corte ainda não definidos."
  },
  {
    "id": "laundrybasket",
    "room": "lavanderia",
    "name": "Cesto basculante com saco removível",
    "kind": "storage",
    "dimensions": "45 × 25 × 45 cm · abertura 55° de referência",
    "choice": "Aprovado para desenvolver",
    "measure": "Ferragem e retirada a conferir",
    "material": "wood",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Frente lisa Arenza, pega superior e ventilação discretas, mantendo continuidade da cozinha. Saco removível e lavável com alças e engates simples. Armação/frente também removíveis para manutenção do sifão. A geometria da R08 preserva os tamanhos. Mecanismo e peças hidráulicas continuam pendentes."
  },
  {
    "id": "laundrypower",
    "room": "lavanderia",
    "name": "Tomada fixa discreta e acessível",
    "kind": "technical",
    "dimensions": "20 A · 127 V para a air fryer",
    "choice": "Aprovado para desenvolver",
    "measure": "Ponto exato e circuito pendentes",
    "material": "black",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Conferir alcance do cabo, distância do tanque, móveis, máquina e varal. Aparelhos só operam na lavanderia sem roupas no varal. A torre fica prevista na cozinha."
  },
  {
    "id": "laundrylight",
    "room": "lavanderia",
    "name": "Plafon branco coordenado à cozinha",
    "kind": "light",
    "dimensions": "3000 K · liga/desliga independente",
    "choice": "Aprovado para desenvolver",
    "measure": "Modelo e posição em seleção",
    "material": "offwhite",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Cor e aparência geral escolhidas. Testar posição fora da projeção da grelha para reduzir sombras das roupas, sem interferir em portas, chapa ou E21. Par definitivo ainda não escolhido. Não há ponto executivo representado."
  },
  {
    "id": "laundryfinish",
    "room": "lavanderia",
    "name": "Continuidade de pedra e pintura",
    "kind": "finish",
    "dimensions": "Branco Itaúnas + Algodão Egípcio fosco",
    "choice": "Aprovado",
    "measure": "Linha da tinta e encontros pendentes",
    "material": "paint",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Mesma faixa baixa de pedra de referência 10 cm e pintura fosca acima, com resistência à limpeza. Cesto liso e superiores Arenza. Pegas pretas foscas coordenadas."
  }
];
const INTERNALS={
  "kitchenupper": {
    "title": "Armários superiores da cozinha · interiores atuais",
    "status": "Módulos P09 a P12 · modelo R45",
    "rows": [
      [
        "A · geladeira",
        "Divisória central. Dois vãos de 373,5 mm nominais."
      ],
      [
        "B · micro-ondas",
        "Uma prateleira e dois níveis. Pratos de visitas e mantimentos conforme programa de guarda."
      ],
      [
        "C · pia",
        "Três prateleiras e quatro níveis: pratos diários. Copos e canecas. Potes e panos. Reserva."
      ],
      [
        "D · depurador",
        "Divisor na faixa dianteira de 118 mm. Reserva posterior para o duto."
      ]
    ],
    "note": "Prévia derivada dos quatro módulos atuais. Profundidade externa nominal 350 mm. Conferir duto, ventilação, alcance e compatibilidade dos eletrodomésticos. O desenho não comprova instalação."
  },
  "sinkstorage": {
    "title": "Gabinete da pia · interior atual",
    "status": "Prateleira de estudo. Hidráulica a conferir",
    "rows": [
      [
        "Nível superior",
        "Programa: duas pilhas de panelas, cada uma com pequena e média."
      ],
      [
        "Nível inferior",
        "Panela de pressão, tampas, frigideira, tábuas e escorredor seco."
      ],
      [
        "Prateleira",
        "Topo a 500 mm do piso no modelo. Vão inferior 284 mm e superior 400 mm nominais."
      ],
      [
        "Portas e instalações",
        "Duas portas. Sem lixeira interna. Preservar sifão e mangueira da torneira."
      ]
    ],
    "note": "P05: 650 × 610 × 720 mm. A prateleira ainda requer recorte para a hidráulica. Os utensílios são programa de guarda. Cabimento real a conferir."
  },
  "kitchenbase": {
    "title": "Gaveteiro da cozinha · três gavetas",
    "status": "Modelo P06. Guias e úteis a conferir",
    "rows": [
      [
        "G1 · superior",
        "Talheres e facas com proteção."
      ],
      [
        "G2 · intermediária",
        "Utensílios de preparo."
      ],
      [
        "G3 · inferior",
        "Mantimentos e bebidas. Temperos em organizador removível."
      ],
      [
        "Corpo",
        "619 × 610 × 720 mm nominais. Três caixas de gaveta no modelo atual."
      ]
    ],
    "note": "A prévia representa as caixas e frentes atuais, sem inventar divisórias para utensílios. Folgas, guias, carga e descontos de fabricação continuam na ficha."
  },
  "lowdrawer": {
    "title": "Gaveta baixa · vassoura e rodo",
    "status": "Modelo P08. Guias e apoios em estudo",
    "rows": [
      [
        "Utensílios",
        "Cabos fixos. Retirar as cabeças para guardar. Referências de 1.125 mm."
      ],
      [
        "Reserva do conjunto",
        "1.269 × 530 × 180 mm nominais. Não é a medida útil da caixa."
      ],
      [
        "Implantação",
        "Abaixo dos gabinetes, sem extensão sob o forno."
      ]
    ],
    "note": "Kit Leão Aço selecionado: 6 fixos de 38 mm + 6 espaçadores metálicos de 1 mm = 39 mm. Útil 1187 × 406 × 88 mm preservado. Conferir peça recebida, fixação, guias, carga e percurso antes de fabricar."
  },
  "wardrobe": {
    "title": "Guarda-roupa · interior atual",
    "status": "Modelo R45. Medidas e ferragens a conferir",
    "rows": [
      [
        "Divisão",
        "Duas metades, uma para cada pessoa."
      ],
      [
        "Gavetas e sapateiras",
        "Duas gavetas em cada extremidade, acima dos três níveis de sapateira. Quatro gavetas e seis prateleiras de sapateira no total."
      ],
      [
        "Cabides",
        "Varões superiores de 973 mm por metade. Varões baixos de 332 mm nos setores intermediários. Vãos longos junto à divisória central."
      ],
      [
        "Prateleiras curtas",
        "705 × 550 mm, com topo próximo de 1.100 mm. Não atravessam o vão longo."
      ]
    ],
    "note": "Corpo P01: 2.000 × 644 × 2.132 mm no modelo. Armário sobre o guarda-roupa e canto são módulos separados, disponíveis em “armários superiores do quarto e canto”. O desenho usa as mesmas peças do 3D. Capacidade, alcance e ferragens continuam a conferir."
  },
  "laundrybase": {
    "title": "Gabinete do tanque e cesto · modelo atual",
    "status": "Modelo P14. Hidráulica e movimento a conferir",
    "rows": [
      [
        "Tanque",
        "Escolha funcional: 38 × 35 × 20 cm internos. A reserva geométrica de 420 × 390 mm não equivale ao produto."
      ],
      [
        "Cesto",
        "Guarda removível e acesso frontal. Conferir saco, ferragem e percurso."
      ],
      [
        "Manutenção",
        "Preservar a região posterior e superior reservada para conexões, mangueira e retirada."
      ]
    ],
    "note": "Conjunto nominal 590 × 630 × 920 mm. Reservas e volumes do modelo não comprovam giro, mangueira ou instalação dos produtos reais."
  },
  "laundryupper": {
    "title": "Armário superior da lavanderia · interior atual",
    "status": "Modelo P15 · vão único",
    "rows": [
      [
        "Interior",
        "Vão nominal 799 × 312 × 544 mm, sem divisória ou prateleira intermediária no modelo."
      ],
      [
        "Acabamento",
        "Arenza nas partes visíveis e Branco TX nos interiores, conforme ficha."
      ],
      [
        "Conferências de montagem",
        "Preservar varal, ventilação e manutenção do aquecedor."
      ]
    ],
    "note": "835 × 350 × 580 mm externos. Divisórias futuras exigem definição. Não estão representadas como existentes."
  },
  "officecab": {
    "title": "Armário superior do escritório · interior atual",
    "status": "Modelo P17 · quatro vãos",
    "rows": [
      [
        "Divisão",
        "Quatro vãos longitudinais de 482 / 464 / 482 / 464 mm. Apoio central duplo."
      ],
      [
        "Prateleiras",
        "Prateleiras reguláveis são intenção de uso. Não há prateleiras horizontais adicionais no modelo atual."
      ],
      [
        "Ciclismo",
        "Capacete, sapatilha e kit de ferramentas no próprio armário superior. Conferir cabimento."
      ]
    ],
    "note": "2.000 × 350 × 550 mm nominais. A prévia mostra os apoios presentes no CAD. Carga, alcance e distribuição de guarda continuam a conferir."
  },
  "drawers": {
    "title": "Gaveteiro do escritório · interior atual",
    "status": "Modelo P16 · duas gavetas",
    "rows": [
      [
        "Gavetas",
        "Duas caixas no conjunto atual. Sem divisórias de organização modeladas."
      ],
      [
        "Frentes",
        "Arenza. Pega discreta na borda."
      ],
      [
        "Corrediças",
        "Abertura total. Conferir ferragem, folgas e espaço dos braços da cadeira."
      ]
    ],
    "note": "400 × 450 × 240 mm nominais no conjunto. A prévia preserva as peças atuais. Não define capacidade ou amortecimento."
  },
  "bathvanity": {
    "title": "Gabinete do banheiro · portas de correr",
    "status": "Modelo P18 · quadro frontal removível",
    "rows": [
      [
        "Frente",
        "Duas folhas de correr e quadro frontal removível. Folhas ocultas no corte."
      ],
      [
        "Interior",
        "Caixa com base e vão livre, sem prateleira interna modelada."
      ],
      [
        "Instalações",
        "Preservar acesso ao sifão e à água quente/fria."
      ]
    ],
    "note": "Modelo BC43 incorporado à R45: conjunto 600 × 470 × 545 mm e abertura frontal nominal de 507 mm. Trilhos, fixações, hidráulica e tolerâncias ainda exigem conferência."
  },
  "bathmirror": {
    "title": "Espelheiro · interior atual",
    "status": "Modelo P19 · duas prateleiras",
    "rows": [
      [
        "Divisão",
        "Duas prateleiras removíveis, formando três vãos de 226 mm nominais."
      ],
      [
        "Prateleiras",
        "560 × 104 × 18 mm no modelo, com folgas laterais e posteriores."
      ],
      [
        "Frentes e luz",
        "Duas portas espelhadas, sem nichos abertos. Luz frontal 4000 K e indireta 3000 K."
      ]
    ],
    "note": "600 × 150 × 750 mm externos. Conferir capacidade, alcance, fixação e eventual passagem de tubulação. A prévia segue o modelo atual."
  },
  "bedcabinet": {
    "title": "Armários superiores do quarto e canto em L",
    "status": "Módulos atuais P02, P03 e P04",
    "rows": [
      [
        "Canto P02",
        "Corpo em L com duas portas em faces diferentes. Faixas fixas frontais ocultas na consulta do interior."
      ],
      [
        "Armário sobre o guarda-roupa P03",
        "Módulo separado sobre o guarda-roupa, com portas de correr."
      ],
      [
        "Cabeceira P04",
        "Quatro portas e apoios internos. A vista em corte oculta as quatro folhas."
      ]
    ],
    "note": "Use Perspectiva para ver os dois braços. As faixas fixas continuam presentes na vista normal e na lista de peças. Medidas do projeto e ligações na ficha de cada módulo."
  }
};
const ROOM_NOTES={
  "all": "Orientação da planta oficial (Torre 2, final 06). Consolidado com FreeCAD R45 e decisões até 24/10/2026. Todos os ambientes devem ficar prontos antes da mudança. Aparelhos escolhidos, ainda sem compra. Medidas e instalações reais pendentes.",
  "sala": "Elias não gostou da bandeja lateral: a preferência é retomar depois a guarda convencional abrindo o baú. Apenas anotado em 20/10, sem aplicar a reversão agora. Até três jogos futuros; organização de aspirador, balde, potes e bebidas preservada. TV com apps na própria tela, Ambilight preferida e TCL alternativa.",
  "quarto": "Queen com baú escolhida para o futuro; cama atual de viúvo, ainda não medida, para a mudança. Roupeiro 65 cm, aéreos alinhados em 213,2 cm e canto independente conforme modelo atual. Mala grande futura no baú, sem cabimento comprovado.",
  "escritorio": "Prioridade de trabalho e Daiane preservadas. Aéreo com20 mm nominais de folga ao teto no cenário; ciclismo no próprio armário, com prateleiras reguláveis. Quantidades confirmadas, dimensões/carga/alcance pendentes.",
  "cozinha": "Fischer Infinity com grill sem turbo substitui o Venax. Módulo613 mm, base em três nervuras e grelhas removíveis integrados como estudo. KE4GC preservado; GN confirmado. Falta conferir montagem real, elétrica, gás/conexões, pedra e temperatura.",
  "lavanderia": "Tanque integrado 38 × 35 × 20 cm, cesto de frente lisa Arenza com saco removível e varal vertical 100 × 50 cm com chapa única. Continuidade da pedra e pintura fosca; tomada fixa 20 A e luz 3000 K independente. Air fryer/cafeteira só operam aqui sem roupas. Hidráulica, ferragens, E21 e pontos ainda em estudo.",
  "banho": "Espelho4000 K e indireta3000 K, com comandos separados. VIP, Slim, Arion, gabinete fechado, uma parede verde e Livo preservados. Água quente, medidas de box/porta, luminárias e instalações ainda em desenvolvimento."
};
const SOURCES=[
  [
    "20/10 · consolidação R11 / FreeCAD R31",
    "Fischer, apoios e grelhas, banco híbrido, armários superiores/guarda-roupa, cama atual/futura, ciclismo, inventário, luz do banheiro e TV. Escolhas separadas de propostas técnicas."
  ],
  [
    "25–27/09 · cozinha e lavanderia",
    "Gavetas, cabos fixos, tanque/cesto, bancada de 63 cm em estudo, pegas, ferragens, pintura, tomadas e iluminação."
  ],
  [
    "P01 · Planta oficial",
    "Contorno, medidas e distribuição original."
  ],
  [
    "F126–135",
    "Bonnie e guarda-roupa interno R02."
  ],
  [
    "F139–159",
    "TV 50″, mesa e prateleiras acima/abaixo da TV."
  ],
  [
    "F150–155",
    "Cabeceira, armário superior do escritório e prateleira dos consoles."
  ],
  [
    "F158–161",
    "Correções de implantação e acabamentos Inox Look."
  ],
  [
    "F162 · 15/09",
    "Organização da cozinha/lavanderia e rotina dos aparelhos."
  ],
  [
    "Consolidação 15/09",
    "Armários superiores A/B/C/D, gabinete da pia e gaveta baixa com rodas."
  ],
  [
    "F103–116",
    "Equipamentos, limitações de instalação e ciclo do varal."
  ],
  [
    "18/09 · banheiro",
    "VIP, Slim, Arion, gabinete/espelho, cores, luz e rotas de água quente."
  ],
  [
    "15/09 · pisos",
    "Vinílico, Olmo como preferência. Aveia/Bétula para amostras."
  ]
];
