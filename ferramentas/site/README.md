# Apartamento interativo — R54 e pacote R29

**Oficina:** [PDF e ZIP](../../06_Entregas/Ensaios_oficina/README.md), ensaios pendentes. Publicação R29 (navegação por cômodo) autorizada por Elias em 28/10/2026: “Sim, publicar”. R28: “pode fazer o push e atualizar o site com essas infos”.

**Berlin R54, 27/10/2026:** pedestal preto aproximado nos dois estados; cadeira lateral +15 mm. 106 cenários sem colisões novas. Elias: “Se passar sem colisões novas, pode salvar como R54, atualizar a base e publicar no site.” [Relatório](../../02_Modelo_3D/Relatorio_mudanca.md) · [publicação](../../06_Entregas/README.md). Publicado e conferido em 28/10/2026. Controle da mesa acessível na sala. Malha da cadeira preservada: só mudou a diagonal de uma face plana; materiais reconciliados. Testes em `test_scene_revision.cjs`.

**Textos públicos:** o site é visto por outras pessoas. Fichas, Escolhas, Planta e Documentos descrevem o estado atual, sem datas, códigos de revisão, "substitui"/"anterior" nem atribuições. Fontes (`source` em `src/data.js`) ficam nos dados, fora da tela. Registros internos e "o que mudou" saem da biblioteca via `INTERNAL_DOCS` em `plain_language.py`, mas seguem no repositório e nas fichas que os citam.

**Pé-direito, 27/10/2026:** Elias solicitou 2,60 m em todos os cômodos e 2,50 m no banheiro, com commit/push e atualização do site. CSV `07_Imovel/Medidas_e_impactos.csv` alimenta paredes, guia e pranchas; medido prevalece sobre nominal. Medidas a confirmar. Escritório 2,47 m substituído; mobiliário e FCStd R53 preservados. R25 inclui caderno A3 R02 atualizado. Publicado e conferido em 27/10: alturas remotas corretas, PDF e ZIP com 295 entradas íntegros; [evidência](../../06_Entregas/README.md).

Planta R23: lavanderia 1,29 × 1,54 m e circulação compatibilizadas; fechamentos do banheiro de 16/17 cm são reconstruídos. Portas/janelas e instalações continuam a conferir.

A configuração corrente é `current_release.json`: FreeCAD R54, pacote R29, fichas R15 e iluminação CB02. Em 26/10, metadados e ZIP remoto R23 foram conferidos: 251 entradas, CRC e hashes sem falhas. `lastPublishedPackageRevision` foi reconciliado para R23. O ZIP local R20 é histórico. [Evidências e limites](../../06_Entregas/README.md). Estudos separados não são incorporados automaticamente à geometria.

Entradas antigas encaminham às fichas e ao estado atual; [referências divergentes](../../06_Entregas/README.md#referências-antigas--triagem-t09).

Para gerar uma cópia autorizada, sem alterar a `.site` anterior:

```powershell
python -B ferramentas/site/preparar_pages.py --output-dir "../outputs/Publicacao/Site" --publication-ready --package-mode auto
```

Execute a partir da raiz `guedala-park`. O modo `auto` verifica o ZIP selado quando já existe; só constrói se estiver ausente. Textos são normalizados para UTF8/LF, binários preservados, e a conferência de fontes usa hashes canônicos sem recompressão no CI. Mudanças de conteúdo exigem outra revisão de pacote. Publicação efetiva é tarefa do workflow Pages, após commit/push autorizados; o gerador não faz deploy.

`build_workshop_docs.py --sources-only` atualiza somente os dados de consulta. `--regenerate-sources` é uma opção explícita para reconstruir fichas/planta; o fluxo normal usa as fontes correntes já verificadas. Testes ficam nesta pasta e saídas temporárias fora do repositório.

**Integração:**20 módulos/249 painéis com eixos e SHA nas fichas. Produtos, furação, medidas reais e ensaios continuam condicionados; [histórico de publicação](../../06_Entregas/README.md).

## Verificações anteriores

[Luz e contatos](Luz_e_contato/README.md): efeitos aproximados, controles e movimentos preservados. Prevalecem a configuração corrente e os limites atuais.

## Referências da interface

As revisões anteriores de iluminação, interiores e compatibilização ficam no git. Permanecem os controles de movimentos e as verificações de produtos, medidas, instalações e oficina descritas nas fichas atuais. As autorizações de publicação anteriores não se estendem a alterações locais novas.

## Navegação e referências anteriores

A navegação mantém ambientes, fichas, Materiais e Escolhas, visitas guiadas e controles de movimentos. [Verificação inicial](Verificacao_interface_R08.json): computador/celular, teclado, abas e21 combinações de vistas. Referências anteriores de planta e publicação ficam no histórico do git; prevalecem a configuração corrente e as instruções abaixo.

[Apartamento](Guedala_Park_Interativo.html) · [Moodboard](../../09_Referencias/Moodboard_atualizado_R01.html) · [Estado atual](../../ESTADO_ATUAL.md).

## Como usar

1. Escolha o ambiente e a vista: superior, 3D ou lateral. A vista lateral tem quatro direções e pode ocultar a metade oposta do ambiente para facilitar a leitura.
2. Arraste para girar o 3D; use a roda do mouse ou pinça com dois dedos para aproximar. Nas vistas superior/lateral, arrastar desloca o desenho. “Enquadrar” restaura a câmera.
3. Toque ou clique em um móvel para abrir sua ficha, com dimensões, material, origem da decisão e o que falta conferir. No celular, também existe “Ver móveis deste ambiente”.
4. Em “Mesa extensível”, alterne 150 cm recolhida e 180 cm aberta. O centro e o banco ficam fixos; as três cadeiras guardadas ficam na lateral livre, com a central mais para fora. As posições longitudinais acompanham a mesa. Cabeceira sem cadeira; cotas e fichas distinguem o plano da validação de encaixe. Folha removível prevista no banco; encaixe real pendente. Veja também as transições animadas ao alternar Bonnie fechado/aberto/baú, escritório em trabalho/hóspedes, três cadeiras guardadas na lateral/em uso, PS5 na sala/escritório e os três estados conceituais do varal.
5. Consulte as passagens e expanda “Ajustar hipóteses de circulação” para testar afastamento do sofá, profundidade do apoio da TV e espessura da cabeceira. Esses ajustes são simulações; recarregar restaura as decisões.
6. Use “Interiores em corte” para retirar as frentes dos armários detalhados. Em “Organização dos armários”, consulte desenhos e conteúdo de guarda; as fichas também têm acesso direto. Divisões ainda não escolhidas aparecem como pendentes.
7. Em “Moodboard”, veja paletas, móveis e dimensões por ambiente. Em “Decisões”, filtre escolhas aprovadas ou itens com decisões/medidas pendentes. O esquema interno aprovado R02 está incorporado à ficha do guarda-roupa.

O arquivo permite salvar uma cópia completa do HTML, exportar dados das escolhas, imprimir o moodboard e salvar uma imagem da vista no computador.

## No S24 Plus

Envie **Guedala_Park_Interativo.html** ao celular e salve o arquivo. Ele contém os estilos, desenhos e interações, sem arquivos auxiliares ou bibliotecas externas. Abra em um navegador que aceite HTML local; se o aplicativo de arquivos exibir apenas uma prévia, use “Abrir com” um navegador compatível. O tratamento de arquivos locais varia conforme o navegador e o gerenciador de arquivos.

A interface foi verificada em emulação de tela de 412 × 915 pixels lógicos com toque e em 915 × 412 na horizontal, além de computador em 1440 × 1100. Isso testa o layout e os gestos; não equivale a um teste físico no aparelho. A cópia HTML continua funcionando localmente, além da versão web.

## O que o modelo representa

Geometria em centímetros, reconstruída a partir da planta oficial P01 e dos estudos do projeto. Os volumes são proporcionais e podem ser girados; estofados, texturas, mecanismos e ferragens são simplificados. O painel visual PNG foi produzido como ilustração de ambiente com auxílio de geração de imagem e revisado pelas decisões atuais. Use as fichas do HTML para medidas e aprovação.

| Estudo | Representação atual | Conferência que permanece |
|---|---|---|
| Sala | Bonnie 180 cm, profundidades 110/136 cm; painel 115 cm; prateleiras 110 × 35 e 110 × 25 cm, topos 35/60 cm | Parede acabada, ventilação, afastamento do sofá, instalação, modelo final da TV/soundbar |
| Circulação da sala | 245 − 136 − 37 = 72 cm com retrátil aberto; 67 cm se houver mais 5 cm atrás do sofá | Medidas reais e obstáculos; cálculo de faixa reta, sem simular o trajeto de uma pessoa |
| Jantar | Mesa 150/180 × 75 cm, R15, extensão central; pedestal fixo; três cadeiras na lateral, central mais para fora | Cadeira e sapata são gabaritos compactos; não foi comprovado um conjunto comercial com esse encaixe |
| Quarto | Cama atual de viúvo com baú, sem medidas; queen futura com envelope 200 × 160 cm; armário e aéreos nativos R31, esquema funcional atualizado | Bases reais das camas, circulação, ferragens, conforto e fixação |
| Escritório | Mesa 200 × 70 cm; Daiane; TV 43″; aéreo 200 × 35 × 55 cm; topo da prateleira dos consoles a 195 cm | Largura/altura da mesa, cadeira, mecanismo e trajetória do sofá, porta, acesso aos consoles e ferragens |
| Cozinha/lavanderia | Sequência F38, equipamentos escolhidos, paleta vigente, interiores A/B/C/D e varal 100 × 50 cm | Ventilação dos equipamentos, ajustes de módulos, instalações, pé-direito, aquecedor e mecanismo do varal |
| Banheiro | VIP 59 cm, Slim como primeira opção, Arion atrás da cuba, gabinete fechado, espelho raso com luz frontal, uma parede verde, Livo e quatro percursos de água quente em estudo | Ducha à esquerda do vaso e papeleira à direita (Elias, 28/10/2026); cotas e hidráulica a conferir |

Há um único PS5 representado, deslocado pelo seletor de ambiente. Não existe módulo para a caixa do gabinete, TV no quarto ou ar-condicionado. Estados de abertura do baú e varal são demonstrações conceituais. Alterações dos controles não aprovam novas medidas ou móveis.

Portas, janelas, espessuras e trechos não cotados foram reconstruídos graficamente. Pé-direito nominal: 260 cm nos cômodos e 250 cm no banheiro, a confirmar (Elias, 27/10/2026). Forros e sancas não têm altura confirmada. Este é um estudo de layout, não desenho para fabricação. Piso vinílico definido, exceto banheiro/lavanderia; Olmo é a preferência, com Aveia/Bétula para comparar amostras. Cores digitais não substituem amostras físicas.

## Base documental e manutenção

- [Registro de decisões](../../01_Programa_e_decisoes/Registro_de_decisoes.md), [memorial Cury](../../01_Programa_e_decisoes/Memorial_Cury_impactos.md) e [P01](../../07_Imovel/referencias/P01_planta_oficial.png).
- [Painel e TV](../../03_Ambientes/Sala_e_jantar/Painel_e_TV.md), [mesa e três cadeiras R03](../../03_Ambientes/Sala_e_jantar/Mesa_e_cadeiras.md), [guarda-roupa R02](../../03_Ambientes/Quarto_e_portas/Guarda_roupa_interior.md) e [cabeceira](../../03_Ambientes/Quarto_e_portas/Cabeceira_e_armario_superior.md).
- [Escritório](../../03_Ambientes/Escritorio/README.md), [cozinha](../../03_Ambientes/Cozinha/README.md) e [lavanderia](../../03_Ambientes/Lavanderia/README.md).

As fontes editáveis ficam em `src`; `construir.py` gera os dois HTML autônomos. Atualizar os dados e os desenhos em conjunto quando uma decisão mudar. A planta anterior F118–F120 e o painel de materiais antigo são históricos.

O fluxo `.github/workflows/pages.yml` executa `preparar_pages.py` a cada push em `main` e publica o artefato `.site` com página principal, moodboard, imagem de materiais e identificação da versão. Pages usa GitHub Actions. Fotos da visita e registros ficam no repositório.

Verificação registrada em `Verificacao_completa_R01.json`: 21 combinações de ambientes/vistas, estados, fórmulas de circulação, gestos de toque, esquema R02 incorporado e cópia HTML reaberta. Sem erros JavaScript, requisições externas ou transbordamento horizontal nos cenários testados.

## Verificação R05

Verificação R05: oclusão, vistas, movimentos e controles, fichas e telas sem erros JavaScript. Mantém limites nominais e verificações físicas pendentes.

Caderno: preserva `ESPECIFICACOES_COMERCIAIS` manual.

## Organização das fontes

Componentes por tema; consulta R12 em `fabrication/Consulta`; R13 sem uso removida. ZIP: 264 entradas preservadas; CAD intacto. Pastas datadas bloqueadas no verificador.

## Galeria Dia/Noite

[Seis pares e PDFs](../../09_Referencias/README.md) em `galeria/index.html`. R27 atualiza HTML/especificações; R26 preservado. Elias, 28/10/2026: "Aprovado, pode commitar e dar push."

## Navegação e documentos

**Quatro abas** (28/10, local, não publicado): Apartamento (3D; *Planta com medidas* virou botão da barra, com volta), Cômodos (antiga Materiais: paleta, todos os itens com selo e *Documentos deste cômodo*), Escolhas (placar e detalhe de cada item, com *Ver no 3D*) e Documentos. `?aba=materiais|planta|ambientes` continuam válidos. Selo único em `app.js → STATUS_GROUPS`: Decidido, Em estudo, Futuro; "A conferir" mostra o texto de medida. Elias, 28/10/2026: "Confirmo" (ambíguos: para desenvolver, existente, entrega e 1ª opção → Decidido; tamanho futuro → Futuro). Teste: `test_navigation.cjs`.

**15 cartões** em `current_release.json → documentLibrary`; a grade inicial mostra 10 e os 5 de cômodo viram atalhos (busca e filtro ainda os listam). Páginas de agrupamento abrem na mesma aba, com trilha de volta; relatórios em `.md` abrem com os detalhes técnicos visíveis.

[Antes → depois das88 entradas](Documentos_antes_depois.csv). A fonte anterior tinha88 entradas,65 visíveis e23 internas. Três entradas sem arquivo viraram pendências em Antes de fabricar. Nove referências de histórico/estudos antigos ficam fora da lista pública, preservadas no repositório e nos vínculos existentes. Nenhum documento foi movido ou apagado. O catálogo técnico permanece separado dos cartões.

`document_library.py` gera14 páginas de agrupamento no build, nos mesmos tons, fontes e links do site; o15º acesso baixa o ZIP. O índice dos móveis reúne Estudos deste móvel para os20 módulos e furação por peça, sem alterar fichas, dimensões ou arquivos técnicos. As duas referências de mesa/varal apontam para uma única entrada por agrupamento. A busca consulta também os subitens; status dos cartões: Atual, Em estudo ou Pendente. No pacote extraído, o cartão do ZIP abre seu índice, sem tentar baixar o próprio arquivo.

As páginas geradas entram tanto em docs/ do preview quanto no pacote offline, com a mesma seleção explícita de fontes. Não escrever HTML à mão em .site/. Regerar: `python -B ferramentas/site/build_workshop_docs.py --sources-only` e `python -B ferramentas/site/construir.py`. Testes: `python -B ferramentas/site/test_document_library.py`, `node ferramentas/site/test_document_library.cjs` e `python -B ferramentas/verificar_site.py`. Os testes conferem88 destinos,15 cartões,20 móveis, links dos grupos, busca, filtros e navegação offline. ZIPs selados não são sobrescritos; o verificador usa uma reconstrução temporária. Nada nesta alteração autoriza publicação.

**Perguntas para Elias — documentos a reconciliar, sem alterar as fontes:**

- Guia de montagem: o arquivo ainda se chama Dossie_marcenaria_R45, mas seu conteúdo é um índice das fichas atuais. Manter esse atalho de compatibilidade? Continua dentro de Fichas dos20 móveis.
- A composição de iluminação CB01 se declara histórica comparativa e encaminha à opção econômica. Manter a comparação dentro de Iluminação ou apontar somente para a seleção atual? Sua função comparativa é indicada no link.
- O estudo de movimentos está vinculado à R52, enquanto o modelo atual é R54. Manter como referência numérica separada? Continua dentro das fichas, identificado como referência a conferir.
- O estado atual chama a composição de luz do banheiro L02 de histórica. Ela ainda é a referência de componentes/preços, ou há outra composição vigente? O link permanece no Banheiro e em Iluminação, sem tratar preço antigo como cotação atual.
