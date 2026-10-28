# Mesa Berlin e varal — validação dimensional R45

23/10/2026. Estudo a partir da R44 e documentos vigentes; nenhuma alteração no modelo compartilhado. Cotas do projeto não são levantamento do apartamento. Ferragens dos produtos prontos pertencem ao produto: não somar mecanismos avulsos históricos ao orçamento.

## Mesa Berlin LATM-522BERLIN

**Pedestal visual na R54 — 27/10/2026.** Pedido explícito de Elias nesta tarefa: acrescentar pedestal nos cenários fechado e aberto. Criados `Fechada_110Pedestal` e `Aberta_cadeira_lateralPedestal`: sólidos em tronco de pirâmide, base 330 × 500 mm no piso e topo 230 × 400 mm a Z750, centro X875/Y4650. Dimensões menores no eixo transversal X; maiores no longitudinal Y. Cor escura da respectiva sapata, com `MaterialReferencia = black`. Altura e formato são aproximados, sem desenho técnico, como consta nos rótulos; os 40 mm entre Z750 e a superfície Z790 reservam hipoteticamente tampo e estrutura, sem modelá-los. Tampos, sapatas, banco e demais cadeiras preservados. Só `Fechada_110Lateral` foi afastada 15 mm em +X, de X1015 para X1030: menor afastamento a 0,01 mm sem volume de interseção (14,99 mm ainda intersecta). Os 106 cenários passaram sem colisões novas. Elias, 27/10/2026, nesta tarefa: “Afaste só a cadeira lateral o mínimo necessário para não colidir com o pedestal e rode a verificação completa de novo. Se passar sem colisões novas, pode salvar como R54, atualizar a base e publicar no site.” [Relatório e aprovação condicional](../../../02_Modelo_3D/Relatorio_mudanca.md). O site representa o pedestal preto nos dois estados da mesa.

A página exata da [Berlin de madeira no Cantão](https://www.cantaodogarimpo.com.br/moveis-para-casa/mesa-de-jantar-berlin-elastica-110-170cm-com-tampo-de-madeira-pinhao) confirma a referência LATM-522BERLIN, dimensões 110/170 × 80 × 79 cm, base superior 23 × 40 cm e inferior 33 × 50 cm. É informação do vendedor sobre sua oferta. O texto apresenta contradição: título/itens inclusos dizem madeira e uma linha da descrição diz madeira com vidro. Não usar essa linha para mudar o tampo escolhido. O [catálogo LAF 2019/2020, página 3](https://prolardeangra.com.br/wp-content/uploads/2020/06/catalogo-virtual-laf-moveis.pdf) distingue ref. 522 madeira de 523 vidro com a mesma dimensão; isso corrobora a família antiga, sem provar fabricante/configuração atual da unidade Woods anunciada.

Não se encontrou desenho técnico atual que fixe espessura, altura inferior da estrutura, posição das travessas, curso do mecanismo ou altura do pedestal. O mecanismo é integrado à Berlin pronta; retirar da futura lista de compra as corrediças Pöttker/Häfele e folha adicional de 300 mm da antiga mesa sob medida. A extensão Berlin é 600 mm; não reutilizar os controles da mesa histórica.

| Conferência | Resultado reproduzível no projeto |
|---|---|
| Tampo fechado | X475–1275; Y4100–5200; Z790. Superfície sem espessura, não tampo sólido validado. |
| Tampo aberto | X475–1275; Y3800–5500; Z790. Centro X875/Y4650 conservado. |
| Sobreposição em planta com banco | 550−475 = 75 mm. Isso não é colisão sozinho; banco e tampo ficam em alturas diferentes. |
| Banco até face superior da mesa | 790−470 = 320 mm. Altura livre real sobre assento = 320−d, onde d é a profundidade vertical da estrutura sob o tampo. Não confundir 320 mm com vão livre para pernas. |
| Balanço lateral em relação à base superior | (800−230)/2 = 285 mm, condicionado à orientação 230 transversal. Em relação à sapata: (800−330)/2 = 235 mm. Não valida joelhos/pés porque altura e perfil do pedestal são desconhecidos. |
| Balanço nas pontas, base superior | Fechada (1100−400)/2 = 350 mm; aberta (1700−400)/2 = 650 mm, condicionados à centralização/orientação. |
| Balanço nas pontas, sapata | Fechada 300 mm; aberta 600 mm. Dimensões planas não certificam conforto. |
| Três cadeiras laterais abertas | 3×440 = 1320 mm; sobra total 380 mm. Arranjo atual tem centros a 566,67 mm, intervalos 126,67 mm e margens 63,33 mm. São envelopes Lina, não largura de ocupantes. |
| Cadeiras nas pontas com mesa aberta | Arranjo histórico colide 60 mm com sofá; não é o arranjo vigente de três laterais. |

Fontes locais: `Estudo_Berlin_FGVTN_2026-10-21/CAD/Conferencia_Berlin.json`, `LEIA-ME.txt` e exportação R44 `Inventario/Folhas_ativas_globais_R44.json`. A inserção das cadeiras de 260 mm e projeção externa de 210 mm continuam hipóteses. Fechada, a folga até sofá é 240 mm e até geladeira 742,5 mm no estudo; aberta, tampo até sofá 150 mm e até geladeira 652,5 mm. Nenhuma delas é largura livre garantida de circulação com pessoa sentada.

## Varal: escolha vigente e comparação técnica

Manter quadro inteiro 1000 × 500 mm, elevação vertical por manivela, sem placa de ocultação. Não trocar por motor nem por barras que descem individualmente. O rótulo de Peca157 ainda menciona placa, mas a placa foi removida na R35. A reserva atual mede 1000 × 500 × 30 mm em X3705–4705, Y5650–6150, Z2310–2340; os 30 mm são gabarito, não espessura certificada do conjunto comercial.

| Candidato concreto | Evidência e compatibilidade | Estado |
|---|---|---|
| Priscila 0020 / SóVarais | [Página do fornecedor original](https://www.loja.sovarais.com.br/acessorios/manivela-para-varal-de-teto-priscila): 15 kg e retenção automática, adapta-se a varal tradicional. | Nacional, mas acessório isolado: faltam quadro 1000×500, curso, cordagem, envelope e definição se os 15 kg incluem peso próprio. Não homologar o conjunto pela manivela. |
| Efegete Ceiline Manivela 100 cm | [Fabricante](https://www.tendederosefegete.es/p/ceiline-manivela-largo-100cm-tendedero-de-techo-efegete) confirma 100×50. [Família](https://www.tendederosefegete.es/c/ceiline-manivela) confirma movimento conjunto, cinco barras com separação de 100 mm e parada automática. | Alternativa técnica importada, não adotada nem compra aprovada. Atendimento/entrega Brasil não confirmados. |
| Ceiline Manual 100 cm | O [fabricante diferencia explicitamente](https://www.tendederosefegete.es/i/preguntas-frecuentes) o modelo Manual, de barras independentes, do modelo Manivela. | Excluir desta seleção: função diferente apesar da dimensão igual. |

Para o Ceiline Manivela, a [ficha técnica de autoria do produto hospedada no El Corte Inglés](https://sgfm.elcorteingles.es/SGFM/dctm/MEDIA03/202402/19/00117201100652____9_.pdf) especifica, na coluna 100 cm: peso próprio 3 kg, roupa 20 kg, teto até 3,3 m e 5 m de linha. Isso separa 20 kg úteis de 23 kg suspensos. Não transportar anúncios de 40 kg de outros revendedores nem os 25 kg da manivela isolada para a capacidade da grelha. A ficha pôde ser lida pela ferramenta web; a cópia local foi recusada pelo servidor.

O [guia Efegete](https://m.media-amazon.com/images/I/81LEhOs%2BLIL.pdf), salvo em `Fontes/Efegete_Ceiline_Manivela_guia.pdf`, mostra dois perfis de teto, quadro, cordas, redirecionador e comando de parede. O [FAQ do fabricante](https://www.tendederosefegete.es/i/preguntas-frecuentes) admite comando até 2 m do quadro e margem mínima de 100 mm às paredes. O guia ilustra comando a 1100 mm do piso; isso é referência do fornecedor, não aprovação ergonômica para o usuário. Não há confirmação de manivela removível.

### Cálculos que já independem do apartamento real

- Reserva de curso entre o fundo atual do quadro Z2310 e referência de manuseio Z1900–2000: **310–410 mm**, se ambas as cotas representarem o mesmo ponto da grelha. Não equivale ao curso comercial máximo; falta cotar barras e suportes.
- O conjunto de referência 20 kg de roupa + 3 kg próprio resulta em **225,55 N** de peso estático. Dividir por quatro daria 56,39 N por suspensão apenas para distribuição perfeitamente simétrica. Polias introduzem forças vetoriais e desigualdade de carga; isso não dimensiona buchas nem permite apoiar no forro.
- Grelha 1000 mm num setor nominal de 1290 mm deixa 290 mm totais; centralizada, 145 mm por lado. Passa pela margem de 100 mm do fabricante em planta, mas depende da posição dos perfis e da leitura correta do setor. Pelas referências X3520/4850 da lavanderia e quadro X3705/4705, folgas laterais nominais seriam 185/145 mm. Aberturas, duto, sanca, aquecedor e giro de janela precisam entrar no envelope final.
- A extremidade do quadro Y6150 fica a 100 mm da bancada iniciando em Y6250. Roupa pode ultrapassar a projeção de barras; esse número não é garantia de afastamento da roupa.
- A operação aprovada continua: descarregar máquina no tanque vazio, fechar máquina, baixar quadro vazio, carregar do fundo à entrada, sair e elevar; na retirada, descarregar da entrada ao fundo. Isso não exige retomar a placa de ocultação.

Pendências de produto que podem ser fechadas antes do levantamento: manual completo com furação/diâmetros, posição dos pontos de suspensão, percurso e comprimento de cada corda, curso máximo real, envelope recolhido, retenção e manivela removível. Dependentes da obra: substrato/ancoragens, cotas acabadas, redes ocultas e afastamentos do aquecedor/duto/janela. A antiga meta proposta de 30 kg não é capacidade aprovada e estes candidatos de 15/20 kg não a satisfazem automaticamente.
