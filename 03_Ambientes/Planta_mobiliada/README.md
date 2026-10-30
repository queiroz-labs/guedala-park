# Planta mobiliada geral

## R03 — vigente · 30/10/2026

Capturada do estudo interativo com a **geometria FreeCAD R54** e a apresentação atual das cores R16/acabamentos do site, incluindo Sauge na parede da janela do box. Nenhum FCStd, orçamento ou decisão foi alterado. A imagem e as sete vistas substituem as capturas R02 da R45; o histórico fica no git.

- [Planta mobiliada R03 (vista superior)](Planta_mobiliada_R03.png)
- Vistas 3D por ambiente: [apartamento](Vistas/00_Apartamento.png) · [sala e jantar](Vistas/01_Sala_e_jantar.png) · [quarto](Vistas/02_Quarto.png) · [escritório](Vistas/03_Escritorio.png) · [cozinha](Vistas/04_Cozinha.png) · [lavanderia](Vistas/05_Lavanderia.png) · [banheiro](Vistas/06_Banheiro.png)

As imagens servem para o estudo preliminar e para mostrar o layout. Cores e materiais são aproximados, e as medidas não foram conferidas no apartamento. Não são prancha executiva. O programa correspondente está em [Programa de necessidades R01](../../01_Programa_e_decisoes/Programa_de_necessidades.md).

### Diferenças visíveis em relação à R02

Comparação lado a lado das oito imagens, com o mesmo quadro de 1005 × 649 px, câmeras, zoom e deslocamento. São diferenças da representação já existente no site, não escolhas novas ou comprovação física.

| Vista | O que mudou na imagem |
|---|---|
| Planta superior | Pedestal Berlin indicado pela projeção tracejada sob o tampo; cadeira lateral na posição R54 (+15 mm); cama viúva atual menor que a reserva queen; lixeiras nas posições atuais; topos brancos visíveis. |
| Apartamento | Reúne essas mudanças, a parede verde da janela do box e a apresentação atual das chapas. |
| Sala e jantar | Cadeira lateral +15 mm e envelope atual da soundbar Philips TAB4000; o tampo oculta grande parte do pedestal nesta direção. |
| Quarto | Cama viúva atual no cotidiano, em vez da antiga representação da queen; topos/fechamentos brancos da extração atual. Queen permanece reserva futura nos dados. |
| Escritório | Monitores e TV43 com os envelopes/posições já presentes na cena atual; diferenças pequenas, sem nova implantação proposta nesta captura. |
| Cozinha | Biovis deslocada +7 cm no eixo da cena; topos brancos e detalhamento frontal da extração atual. |
| Lavanderia | Loop deslocada +6 cm no eixo da cena; topo branco do aéreo. Varal continua recolhido. |
| Banheiro | Sauge também no pano da janela; ducha higiênica entre box e vaso; topo branco do espelheiro. |

Todas as oito vistas foram refeitas; nenhuma ficou marcada como desatualizada. Chapas, acessórios e pisos continuam simplificados pelo renderizador. Conferência de enquadramento não demonstra medidas, montagem, resistência ou conformidade. A aparência verde vem do site; não se atribui alteração ao arquivo CAD R54.

## Procedimento de captura

`node ferramentas/estudos/capturar_planta_mobiliada.cjs --output-dir ../captura_planta` abre o HTML gerado no Edge via Playwright local. Ajuste `NODE_PATH` para a instalação local existente; `--browser` aceita outro executável. Não é etapa do build/CI e não instala dependências.

Captura somente o quadro da cena, em 1005 × 649 px e escala de tela 1, com câmeras da R02 recuperadas de `1b4aeaa:01_Projeto/Estudo_interativo/src/app.js`: inclinação 0,92; giros −0,62 (geral/sala/escritório), −2,4 (quarto), 2,8 (cozinha/banheiro) e 2,5 (lavanderia); planta perpendicular. Zoom 1 e deslocamento zero. O envelope óptico histórico `ymax=247` conserva o enquadramento: não é pé-direito e não altera a geometria.

Cena cotidiana: sofá/mesa fechados, escritório em trabalho, PS5 na sala, varal recolhido, móveis altos visíveis, sem paredes completas, seleção, cotas ou corte interno. [Metadados da R03](Captura.json): navegador, câmera, SHA do HTML/PNGs e limites projetados. As comparações ficam fora do git. Confira as oito imagens antes de substituir as vigentes. O script recusa gravar dentro do repositório ou sobre imagens existentes; nenhum FreeCAD é aberto.

## R01 — histórico

**Histórico:** esta planta retrata F118–F120, antes da escolha do Bonnie e das revisões do quarto, jantar e painel. Para o layout atual, abra o [estudo interativo atualizado](../../ferramentas/site/Guedala_Park_Interativo.html). Os arquivos abaixo ficam preservados como registro da etapa anterior.

13/09/2026 · F118 · Vista de cima, cenário cotidiano.

- [Abrir planta ampliável](Planta_mobiliada_R01.html)
- [Imagem PNG](Planta_mobiliada_R01.png)
- [Desenho vetorial SVG](Planta_mobiliada_R01.svg)

Base: P01, representação da planta oficial do final06. Desenho reconstituído a partir do contorno e cotas documentais, preservando quartos, circulação, banheiro e área integrada. Portas e contornos sem cota específica são aproximações gráficas; não é levantamento acabado ou planta executiva.

### R01 — decisões representadas no estudo histórico

Escritório conforme F89/F99 e R07/R10: bancada de70 cm de profundidade, largura200 cm em estudo; notebook à esquerda, dois monitores e PC à direita; Daiane fechado na lateral esquerda próximo à entrada, TV43 oposta. Cadeira ilustrativa, sem modelo escolhido. Armários altos, consoles e gavetas sob tampo omitidos na vista do piso, não removidos do projeto. Tela e cadeira não comprovam curso ou circulação.

Quarto: cama queen existente, usando reserva200 ×160 cm do estudo anterior (não dimensão medida da cama); armário245 ×55 e implantação são hipóteses. Portas originais preservadas, sem incorporar recuo/camarão/portas de correr adiadas.

Sala/jantar: sofá180 ×90 e chaise60 ×70 são volumes de teste do R01, não modelos escolhidos; banco180 ×55 e mesa180 ×75 em estudo. Duas cadeiras no cotidiano e terceira tracejada apenas para cenário de seis pessoas, sem local de guarda resolvido. TV da sala não posicionada porque essa implantação não foi definida.

Cozinha: sequência escolhida preservada. Correção F119: incorporar F38/Layout_da_pia_R02: cocção65, pia60, preparo + air fryer61,9, reserva IB6 de80,1 e entrada85 cm. Purificador suspenso omitido com os aéreos, conforme complemento R03; acessórios de bancada são ilustrativos. Forno fica sob cooktop; ME23P e depurador não aparecem por serem altos. Profundidade desenhada do tampo não é especificação executiva. Corpo da IB6 fora do giro hipotético da entrada, conforme F38. A imagem anterior reintroduzia por erro o cenário antigo; corrigida nos mesmos arquivos. Abertura real, portas da própria geladeira e circulação continuam a conferir.

Lavanderia: tanque/cesto e VC4. Varal100 ×50 tracejado como projeção aérea na posição de estudo à frente da bancada; não representa nicho ou localização aprovada. Estado cotidiano pode ser guardado vazio; a projeção foi incluída para explicar o uso alto. E21 e ripado não fixados graficamente em posição inventada; seguem pendentes junto da caixa e mecanismo. Não confundir a omissão dos volumes aéreos com sua retirada.

Banheiro: louças, box e shaft representados esquematicamente a partir de P01, sem novas medidas de mobiliário ou alterações de pontos. A ducha escolhida não recebe implantação executiva por este desenho.

## Fontes locais

- [Planta oficial P01](../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf), referência visual em04_Visita_ao_apartamento/referencias/P01_planta_oficial.png.
- [Resumo vigente](../../ESTADO_ATUAL.md) e [Registro de decisões](../../01_Programa_e_decisoes/Registro_de_decisoes.md).
- Jantar R01.
- [Ordem da cozinha](../Cozinha/Ordem_dos_moveis.md) e [medidas](../Cozinha/Medidas_e_folgas.md).
- [Daiane R07](../Escritorio/Cadeira_e_sofa.md) e [setup R10](../Escritorio/Setup.md).
- [Quarto, estudo anterior](../Quarto_e_portas/Portas.md), usado apenas para envelopes de móveis, sem mudanças de portas.
- Varal, três estados R05.

Imagem e vetor gerados do mesmo desenho; PNG inspecionado visualmente. Esta revisão permite conversar sobre o conjunto e localizar conflitos, sem aprovar fabricação ou instalações.

**Correção F120:** parede entre banheiro e acesso ao quarto recomposta graficamente. Banheiro com apenas um vão de entrada pela circulação; porta do quarto representada separadamente. Arquivos atualizados no mesmo caminho, sem alteração física proposta.
