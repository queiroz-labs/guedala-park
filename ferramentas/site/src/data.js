/* Dados atuais do projeto. Medidas em centímetros, salvo indicação. */
const PROJECT={
  "revision": "Consulta de marcenaria · FreeCAD R54 · iluminação CB02",
  "date": "27 outubro 2026",
  "mirrored": false,
  "name": "Guedala Park",
  "area": "40,18 m²",
  "unit": "Torre 2 · final 06",
  "ceiling": 260.0,
  "heightStudy": "Pé-direito: 2,60 m nos cômodos e 2,50 m no banheiro, medida a confirmar no imóvel. Valores para estudo, não fabricação.",
  "note": "Projeto completo do apartamento, para ficar pronto antes da mudança. Medidas, produtos e detalhes de fabricação ainda serão conferidos.",
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
      "sub": "Cama viúva atual e armazenamento",
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
      "note": "Composição clara com estrutura amadeirada. Conferir tecido e acabamento do produto real."
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
      "note": "Armários superiores contínuos da geladeira ao cooktop. A lavanderia fica em Arenza. Duratex Azul Profundo é a alternativa."
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
      "note": "Frentes fechadas e foscas, sem ripado nem puxadores salientes. Tom digital aproximado; conferir amostra e combinação com o Branco TX."
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
      "note": "Laterais aparentes do gabinete e do armário com espelho. Leve brilho acetinado. Interior em Branco TX. Conferir amostra."
    }
  ],
  "ceilingByRoom": {
    "quarto": 260.0,
    "cozinha": 260.0,
    "lavanderia": 260.0,
    "escritorio": 260.0,
    "banho": 250.0,
    "sala": 260.0,
    "circulacao": 260.0
  }
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
    "notes": "Uma prateleira acima e outra abaixo da TV, sem gavetas. Faltam definir alturas, equipamentos, peso suportado e fixação."
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
    "name": "TV Philips Ambilight 50″ · 50PUG8100/78",
    "kind": "tv",
    "dimensions": "111,1 × 64,9 × 8,8 cm sem base · VESA 200 × 100",
    "choice": "Escolhido",
    "measure": "Testar o Stremio no prazo de troca",
    "material": "black",
    "source": "Elias, 29/10/2026: “sim fechar phillips ambilight”",
    "notes": "Ambilight em três lados, Titan OS com os aplicativos na própria TV, eARC na HDMI 1, saída óptica e Bluetooth. O Stremio Lite não toca torrent direto, mas abre links do Real-Debrid; testar com a conta do Torrentio logo após a compra. Referência de preço: R$ 2.188,98 na Amazon em 29/10/2026. A altura da borda inferior, 77 cm, ainda é uma hipótese.",
    "budget": "Até R$ 3.000 · TV apenas"
  },
  {
    "id": "soundbar",
    "room": "sala",
    "name": "Soundbar Philips TAB4000",
    "kind": "soundbar",
    "dimensions": "76 × 6,5 × 10,5 cm · reserva de 90 sob a TV",
    "choice": "Escolhido",
    "measure": "Conferir o código /78 e o suporte de parede",
    "material": "black",
    "source": "Elias, 29/10/2026: “Philips TAB4000”",
    "notes": "Barra 2.0, 30 W RMS, ligada à TV pela HDMI 1 (eARC) com um cabo; o controle da TV comanda o volume. Bluetooth e USB; sem entrada óptica. Suporte próprio sob a TV, saídas de som livres. Referência R$ 330 a 360 (Amazon e Simonetti, 29/10/2026); fora do orçamento R44, a incluir."
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
    "notes": "Mesa pronta, extensível de 110 para 170 cm. Fechada, recebe duas cadeiras nas pontas e uma na lateral. Aberta, falta conferir o arranjo das cadeiras e a distância até o sofá. Tampo amadeirado próximo ao Arenza e base preta; conferir o acabamento do produto."
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
    "notes": "Duas tampas com almofadas removíveis e espaço de guarda embaixo. Retire as almofadas antes de abrir. Cada tampa abre com dobradiça contínua, suporte e trava; modelo, eixo e fixações ainda a definir."
  },
  {
    "id": "diningchairs",
    "room": "sala",
    "name": "Três cadeiras de jantar",
    "kind": "chairs",
    "dimensions": "Envelopes de uso; conferir produto real",
    "choice": "Aprovado como plano",
    "measure": "Encaixe e passagem pendentes",
    "material": "head",
    "source": "Consolidação R43/R45",
    "notes": "Com a mesa fechada, duas cadeiras nas pontas e uma na lateral. Com a mesa aberta, as três vão para a lateral, arranjo a testar no local. O desenho não comprova a passagem com pessoas sentadas. Madeira em tom próximo ao Arenza e estofado claro."
  },
  {
    "id": "bed",
    "room": "quarto",
    "name": "Cama viúva com baú · atual",
    "kind": "bed",
    "dimensions": "128 × 188 × 64 cm · baú 42 (pés 5) + colchão 22",
    "choice": "Existente",
    "measure": "Conferir a cama real e a mala no baú",
    "material": "head",
    "source": "Elias, 29/10/2026: “vamos considerar que agr eu tenho uma cama de viuvo” · anúncio Casas Bahia 1500699729",
    "notes": "Box com baú viúva e colchão Anjos Classic de molas ensacadas. Vai na mudança e fica por um bom tempo. No eixo da cabeceira: 16 cm a mais de passagem diante do guarda-roupa e 12 cm a mais aos pés do que a queen. Baú com 37 cm de altura e 25 cm de profundidade útil: conferir se a mala grande cabe deitada."
  },
  {
    "id": "queen",
    "room": "quarto",
    "name": "Cama queen com baú · troca futura",
    "kind": "bed",
    "dimensions": "Reserva 200 × 160 cm · colchão padrão 198 × 158",
    "choice": "Tamanho futuro escolhido",
    "measure": "Modelo a escolher perto da troca",
    "material": "offwhite",
    "source": "16/10/2026",
    "notes": "Troca prevista bem depois da mudança. O desenho mostra a reserva de 160 × 200 cm, translúcida, no mesmo eixo da cama atual. O guarda-roupa e a passagem foram dimensionados para ela. A mala grande deve caber no baú."
  },
  {
    "id": "wardrobe",
    "room": "quarto",
    "name": "Guarda-roupa de 65 cm e armário de canto",
    "kind": "wardrobe",
    "dimensions": "200 ×65 cm · conjunto superior até 244 cm no cenário",
    "choice": "Aprovado",
    "measure": "Medidas a conferir",
    "material": "wood",
    "source": "FreeCAD R30/R31 · geometria consolidada",
    "notes": "Profundidade de 65 cm. Metade para cada pessoa, com quatro gavetas, espaço para dez pares de sapatos até o número 42, dois casacos longos e cabides. A face inferior dos armários superiores fica a 213,2 cm. O armário de canto tem portas próprias. Portas de correr e ferragens ainda a conferir."
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
    "notes": "Cabeceira clara estofada, em dois painéis. Foi pensada para a futura queen e funciona também com a cama de viúvo, no mesmo eixo. Faltam as medidas da cama atual, o conforto e a fixação."
  },
  {
    "id": "bedcabinet",
    "room": "quarto",
    "name": "Armários superiores em L",
    "kind": "upper",
    "dimensions": "Profundidades 65 e 25 cm · base a 213,2 cm · topo a 244 cm",
    "choice": "Aprovado para desenvolver",
    "measure": "Encontro e medidas em estudo",
    "material": "wood",
    "source": "FreeCAD R30/R31",
    "notes": "O armário sobre o guarda-roupa e o da cabeceira ficam alinhados pela mesma face inferior, sem móvel empilhado. O canto tem duas portas independentes. A cabeceira tem quatro faixas com juntas de 4 mm. Material, ferragens, abertura das portas e folga até o teto ainda a conferir."
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
    "notes": "Duas gavetas à esquerda, com abertura total e puxador discreto. Com a cama de hóspedes aberta, a abertura das gavetas não é garantida."
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
    "name": "Cadeira Ercathe A01 Mesh Premium · preta",
    "kind": "chair",
    "dimensions": "Assento 50 × 50 cm a 50–57 cm do piso · topo dos braços ~62–76 cm (estimativa por foto) · envelope 74,5 × 73 mantido",
    "choice": "Escolhido",
    "measure": "Confirmar a altura mínima dos braços com a loja",
    "material": "black",
    "source": "Elias, 29/10/2026: “será Cadeira Ergonômica Mesh Ercathe A01 Premium”",
    "notes": "100% mesh, lombar com ajuste de altura e profundidade, braços 3D, encosto até 145° e apoio de pés retrátil; até 150 kg e 1,95 m. Durante visitas, fica no próprio escritório. Nenhuma fonte informa a altura dos braços a partir do piso, e o “29–36 cm” do anúncio não bate com a foto de perfil, que mostra o braço ~19 cm acima do assento. Estimativa: topo dos braços entre ~62 e 76 cm. Com bancada de 75 cm e tampo de 3 cm (~72 livres), deve passar com braço e assento no mínimo, mas com folga de poucos centímetros: confirmar com a loja ou medir na entrega. R$ 2.290,90 na Sensetup em 29/10/2026, fora do orçamento.",
    "budget": "R$ 2.290,90 · fora do orçamento"
  },
  {
    "id": "officecab",
    "room": "escritorio",
    "name": "Armário superior sobre o sofá-cama",
    "kind": "upper",
    "dimensions": "200 ×35 ×55 cm · base190 e topo245 no cenário",
    "choice": "Aprovado",
    "measure": "Projeto aprovado",
    "material": "offwhite",
    "source": "R28/R31 e decisão17/10/2026",
    "notes": "Topo a 245 cm, 15 cm abaixo do pé-direito de projeto de 2,60 m (a confirmar no imóvel). Guarda o equipamento de ciclismo, com capacete, sapatilha e kit de ferramentas, em prateleiras reguláveis. Faltam o acabamento superior, a montagem, o peso suportado e o alcance."
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
    "notes": "Altura definida para não atrapalhar a passagem. A largura deixa espaço para um possível Xbox. Sem armário acima. Acesso, peso e posição a conferir."
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
    "notes": "Três gavetas com abertura total e fechamento amortecido. O vão do forno tem 613 mm externos, 577 mm internos e abertura de 560 mm, com base e grelhas removíveis. A bancada tem 63 cm de profundidade. Recortes e a emenda com a lavanderia dependem do desenho de fabricação."
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
    "name": "Armários superiores em Azul Petróleo",
    "kind": "upper",
    "dimensions": "80,1 + 69,7 + 54,7 + 65 cm · proposta",
    "choice": "Aprovado para desenvolver",
    "measure": "Transição com lavanderia a conferir",
    "material": "petrol",
    "source": "Decisões de 25–27/09/2026",
    "notes": "Armários A e D com divisória vertical, B com uma prateleira e C com três. O D tem 65 cm e avança 2,5 cm em direção à lavanderia; o C tem 54,7 cm. Topo a 255 cm, com pé-direito de projeto de 2,60 m a confirmar. Perfil preto fosco na borda inferior e dobradiças com amortecimento. As portas abrem livres junto ao plafon."
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
    "notes": "Acabamento Inox Look. Reserva de 80,1 cm de largura e 10 cm de recuo atrás. Conferir a abertura da porta, as medidas do código final e a ventilação."
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
    "notes": "Gás natural. Mesa de 60 × 45 cm e recorte de 52 × 39 cm. Com 131 mm abaixo da bancada, restam cerca de 209 mm livres até o forno, já com margem. Conferir caixa, fixações, ligação de gás, pedra e ventilação."
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
    "notes": "Preto, 127 V, elétrico (2061 W / 16,22 A). Ainda não comprado. Topo a 57 cm e base de 13,8 cm, apoiada em três nervuras até o piso, com faixa traseira de 45 × 560 mm e duas grelhas removíveis de 600 × 90 mm para ventilação. Manter 200 mm até o fundo do cooktop. Apoio, circuito e temperatura ainda a conferir."
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
    "notes": "127 V. Fica com 10 cm livres acima, embora o manual indique 30 cm. A instalação ainda precisa ser conferida."
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
    "notes": "Faz café por caneca, duas por vez. Será usada na lavanderia quando o varal estiver sem roupas. O desenho não reserva espaço para ela: modelo e medidas ficam para depois. Não usar junto com a air fryer."
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
    "notes": "Pedra Branco Itaúnas contínua com a cozinha, com faixa de 10 cm na parede e arestas suavizadas. Torneira Telca Flex preta com bica extraível. Saída de água atrás, com tampão e retentor removíveis. Válvula, sifão e mangueira a conferir."
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
    "notes": "Transição após o cooktop. Testeira alinhada ao topo da cozinha. Espaço reservado para o aquecedor e o varal, com ventilação, exaustão e mecanismo a detalhar."
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
    "notes": "Gás natural. Aparelho e exaustão ainda a conferir; não foi comprado. O espaço desenhado não comprova ventilação nem instalação. Faltam os dados de pressão e vazão do prédio."
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
    "notes": "Varal que sobe e desce por manivela, sem caixa fechada. Com o tanque limpo, ele serve de apoio para as roupas da máquina. Faltam curso, trava, carga prevista de 30 kg e a relação com a janela e o aquecedor. As alturas mostradas são exemplos."
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
    "notes": "Duas portas de correr e frente removível para manutenção. Trilhos RM026 e RO25 como referência e quatro parafusos M6 × 100 para prender a frente. Abertura frontal livre de 507 mm. Instalação, folgas e hidráulica a conferir."
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
    "notes": "Frente toda espelhada, laterais Arauco Louro Freijó Poro e interior Branco TX. Duas portas e duas prateleiras removíveis. A caixa é unida por 12 conectores Minifix. Fixação do espelho e da parede a definir; protótipo pendente. Luz de teto 3000 K, espelho 4000 K e indireta 3000 K, com comandos separados."
  },
  {
    "id": "bathlight",
    "room": "banho",
    "name": "Teto 3000 K +espelho 4000 K +indireta 3000 K",
    "kind": "lighting",
    "dimensions": "Firefly25 W; espelho2×550 mm /13,2 W; indireta até2 m /9,6 W",
    "choice": "Escolhido · custo-benefício",
    "measure": "Montagem e posições a validar. Frete/instalação fora do total",
    "material": "offwhite",
    "source": "24/10/2026",
    "notes": "Teto: Galaxy Firefly 9605 branco, IP44, 3000 K. Espelho: fita Cristallux COB CLX-FT331240, 4000 K, IRC acima de 90, 1,10 m. Indireta: fita Cristallux SMD CLX-FT200530, 3000 K, 4,8 W/m, até 2 m. Duas fontes Opus OPS31002 de 12 V e dois perfis MOV4329 com difusores. Três comandos separados. Componentes: R$ 612,64 à vista, sem frete e instalação. Faltam conferir o encaixe, os terminais, a dissipação de calor e a luz no rosto."
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
    "notes": "Enchimento indicado na planta oficial, fechado em gesso. A faixa de 30 cm e a altura mostradas são aproximadas. Há a proposta de acessar o ramal de água quente por ali; o traçado real das tubulações precisa ser conferido."
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
    "notes": "Caixa acoplada, assento com queda amortecida e bacia Rimless. Frente a 65 cm, na profundidade de 124 cm do banheiro. O resultado depende do eixo do esgoto e da folga traseira."
  },
  {
    "id": "hygiene",
    "room": "banho",
    "name": "Ducha higiênica preta quente e fria",
    "kind": "shower",
    "dimensions": "À esquerda do vaso, entre o box e o vaso; modelo e cotas de instalação pendentes",
    "choice": "Direção aprovada",
    "measure": "Percurso e funcionamento pendentes",
    "material": "black",
    "source": "Elias, 28/10/2026; 03_Ambientes/Banheiro/README.md",
    "notes": "À esquerda do vaso, entre o box e o vaso, com a papeleira sozinha à direita (Elias, 28/10/2026). Com mistura de temperatura e fechamento próprio. Orçamento, modelo e cotas de instalação pendentes. Rinnai E21 exige 3,9 L/min para acionar: conferir fluxo pelo aquecedor, estabilidade e espera pela água quente."
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
    "notes": "Referência 61537000. Compacto, com porta-talheres removível e bandeja inclinada. Usar junto à cuba e guardar limpo e seco no gabinete inferior."
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
    "notes": "Inox escovado, pedal e balde removível. No chão, na parede externa do banheiro, voltada para a mesa. Deixa cerca de 107 cm de passagem até a mesa. Conferir rodapé, tampa e pedal."
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
    "notes": "Referência 94547020. Inox polido, pedal, fechamento suave e balde removível. Fica no chão da lavanderia e deixa o armário sob o tanque livre para o cesto de roupas. Conferir tampa, pedal e circulação."
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
    "notes": "Frente lisa Arenza, com puxador superior e ventilação discretos, em continuidade com a cozinha. Saco removível e lavável, com alças e engates simples. A armação e a frente também saem para a manutenção do sifão. Mecanismo e peças hidráulicas a conferir."
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
    "notes": "Cor e aparência geral escolhidas. Testar uma posição fora da projeção do varal para reduzir a sombra das roupas, sem interferir nas portas nem no aquecedor. Modelo ainda a escolher."
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
    "title": "Armários superiores da cozinha · por dentro",
    "status": "Módulos P09 a P12",
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
    "note": "Prévia dos quatro módulos. Profundidade externa nominal 350 mm. Conferir duto, ventilação, alcance e compatibilidade dos eletrodomésticos. O desenho não comprova instalação."
  },
  "sinkstorage": {
    "title": "Gabinete da pia · por dentro",
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
    "note": "Kit Leão Aço selecionado: 6 fixos de 38 mm + 6 espaçadores metálicos de 1 mm = 39 mm. Espaço útil de 1187 × 406 × 88 mm. Conferir peça recebida, fixação, guias, carga e percurso antes de fabricar."
  },
  "wardrobe": {
    "title": "Guarda-roupa · por dentro",
    "status": "Medidas e ferragens a conferir",
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
    "title": "Armário superior da lavanderia · por dentro",
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
    "title": "Armário superior do escritório · por dentro",
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
    "title": "Gaveteiro do escritório · por dentro",
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
    "note": "400 × 450 × 240 mm nominais no conjunto. Não define capacidade ou amortecimento."
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
    "note": "Conjunto de 600 × 470 × 545 mm e abertura frontal nominal de 507 mm. Trilhos, fixações, hidráulica e tolerâncias ainda exigem conferência."
  },
  "bathmirror": {
    "title": "Espelheiro · por dentro",
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
    "note": "600 × 150 × 750 mm externos. Conferir capacidade, alcance, fixação e eventual passagem de tubulação. "
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
  "all": "Planta oficial da Torre 2, final 06. Todos os ambientes ficam prontos antes da mudança. Aparelhos escolhidos, ainda sem compra. Medidas e instalações reais a conferir no imóvel.",
  "sala": "Sofá-cama Bonnie, mesa extensível Berlin e banco com baú. Espaço de guarda para até três jogos, aspirador, balde, potes e bebidas. TV com aplicativos na própria tela: Philips Ambilight preferida, TCL como alternativa.",
  "quarto": "Cama viúva com baú (128 × 188) na mudança; queen com baú bem depois. Guarda-roupa de 65 cm, armários superiores alinhados a 213,2 cm e armário de canto independente. A mala grande deve caber no baú da cama.",
  "escritorio": "Prioridade para o trabalho, com o sofá-cama Daiane para hóspedes. O armário superior guarda o equipamento de ciclismo em prateleiras reguláveis. Medidas, peso e alcance a conferir.",
  "cozinha": "Forno Fischer Infinity com grill, cooktop Electrolux KE4GC a gás natural, armários superiores em Azul Petróleo e base em Arenza. Faltam conferir montagem, elétrica, gás, pedra e ventilação.",
  "lavanderia": "Tanque integrado de 38 × 35 × 20 cm, cesto de frente lisa Arenza com saco removível e varal vertical de 100 × 50 cm. Pedra contínua e pintura fosca; tomada fixa de 20 A e luz 3000 K independente. Air fryer e cafeteira só funcionam aqui sem roupas no varal. Hidráulica, ferragens, aquecedor e pontos em estudo.",
  "banho": "Luz de espelho 4000 K e indireta 3000 K, com comandos separados. Bacia VIP, cuba Slim, torneira Arion, gabinete fechado, ducha Livo e uma parede verde no box. Água quente, box, luminárias e instalações em desenvolvimento."
};
const SOURCES=[
  [
    "Planta oficial",
    "Contorno, medidas e distribuição original."
  ],
  [
    "Sala e quarto",
    "Sofá Bonnie, TV 50″, mesa, prateleiras, cabeceira e guarda-roupa."
  ],
  [
    "Escritório",
    "Armário superior, prateleira dos consoles, sofá-cama e ciclismo."
  ],
  [
    "Cozinha e lavanderia",
    "Aparelhos, gavetas, tanque, cesto, varal, pedra, pintura, tomadas e iluminação."
  ],
  [
    "Banheiro",
    "Bacia, cuba, gabinete, espelho, cores, luz e água quente."
  ],
  [
    "Pisos",
    "Vinílico Olmo como preferência; Aveia e Bétula para comparar."
  ]
];
