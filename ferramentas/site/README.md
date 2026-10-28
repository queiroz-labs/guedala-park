# Apartamento interativo — R54 e pacote R26

**Berlin R54, 27/10/2026:** pedestal preto aproximado nos dois estados; cadeira lateral +15 mm. 106 cenários sem colisões novas. Elias: “Se passar sem colisões novas, pode salvar como R54, atualizar a base e publicar no site.” [Relatório](../../02_Modelo_3D/Relatorio_mudanca.md) · [publicação](../../06_Entregas/README.md). Publicado e conferido em 28/10/2026. Controle da mesa acessível na sala. Malha da cadeira preservada: só mudou a diagonal de uma face plana; materiais reconciliados. Testes em `test_scene_revision.cjs`.

**Textos públicos:** o site é visto por outras pessoas. Fichas, Escolhas, Planta e Documentos descrevem o estado atual, sem datas, códigos de revisão, "substitui"/"anterior" nem atribuições. Fontes (`source` em `src/data.js`) ficam nos dados, fora da tela. Registros internos e "o que mudou" saem da biblioteca via `INTERNAL_DOCS` em `plain_language.py`, mas seguem no repositório e nas fichas que os citam.

**Pé-direito, 27/10/2026:** Elias solicitou 2,60 m em todos os cômodos e 2,50 m no banheiro, com commit/push e atualização do site. CSV `07_Imovel/Medidas_e_impactos.csv` alimenta paredes, guia e pranchas; medido prevalece sobre nominal. Medidas a confirmar. Escritório 2,47 m substituído; mobiliário e FCStd R53 preservados. R25 inclui caderno A3 R02 atualizado. Publicado e conferido em 27/10: alturas remotas corretas, PDF e ZIP com 295 entradas íntegros; [evidência](../../06_Entregas/README.md).

Planta R23: lavanderia 1,29 × 1,54 m e circulação compatibilizadas; fechamentos do banheiro de 16/17 cm são reconstruídos. Portas/janelas e instalações continuam a conferir.

A configuração corrente é `current_release.json`: FreeCAD R54, pacote R26, fichas R15 e iluminação CB02. Em 26/10, metadados e ZIP remoto R23 foram conferidos: 251 entradas, CRC e hashes sem falhas. `lastPublishedPackageRevision` foi reconciliado para R23. O ZIP local R20 é histórico. [Evidências e limites](../../06_Entregas/README.md). Estudos separados não são incorporados automaticamente à geometria.

T09, 26/10/2026: entradas antigas de consulta R12/R45 encaminham agora às fichas R14 e ao estado atual. [Manifesto e referências ainda divergentes](../../06_Entregas/README.md#referências-antigas--triagem-t09). Fontes e artefatos do site preservados; revisão documental não confirma a publicação remota.

Para gerar uma cópia autorizada, sem alterar a `.site` anterior:

```powershell
python -B ferramentas/site/preparar_pages.py --output-dir "../outputs/Publicacao/Site" --publication-ready --package-mode auto
```

Execute a partir da raiz `guedala-park`. O modo `auto` verifica o ZIP selado quando já existe; só constrói se estiver ausente. Textos são normalizados para UTF8/LF, binários preservados, e a conferência de fontes usa hashes canônicos sem recompressão no CI. Mudanças de conteúdo exigem outra revisão de pacote. Publicação efetiva é tarefa do workflow Pages, após commit/push autorizados; o gerador não faz deploy.

`build_workshop_docs.py --sources-only` atualiza somente os dados de consulta. `--regenerate-sources` é uma opção explícita para reconstruir fichas/planta; o fluxo normal usa as fontes correntes já verificadas. Testes ficam nesta pasta e saídas temporárias fora do repositório.

Atualização 26/10: biblioteca e fichas P17/P12 apontam para os estudos de suspensão separados, desenhos e requisitos; matriz 20/20 disponível. Pacote R21 inclui esses documentos. Geometria R52 e comprovações físicas continuam conformeEstadoAtual.

**Integração 27/10:** `exportar_cad.py` lê o documento vigente aberto na GUI, sem salvá-lo, e extrai os 20 módulos/249 painéis com eixos e SHA. Fichas R15 incorporam P02/P13; lixeiras no site seguem os deslocamentos R53. Mapas de furação R14 mantêm fontes e condições; produto/oficina e ensaios pendentes. Publicação R24 autorizada por Elias em 27/10/2026: “Pode fazer push e publicar a R53 com as fichas R15 e o pacote R24”; conferência remota em [Entregas](../../06_Entregas/README.md).

## Registros anteriores

Histórico; prevalecem a configuração corrente e o estado atual.

## Luz e sombras de contato — 17/10/2026

Sala e cozinha receberam comparação **Antes / Depois** na vista 3D, com luz suave e contatos aproximados calculados sobre os móveis atuais. Controles e personalização preservados; configuração visual separada em `src/lighting.js`. [Comparação e conferências](Luz_e_contato/README.md). HTML e artefato Pages regenerados. Publicação da R10 autorizada por Elias em 18/10/2026.

## Revisão R09 — cozinha e lavanderia, 27/09/2026

Site e moodboard atualizados com as decisões até o aceite do formato quadrado do plafon, condicionado à abertura livre dos aéreos. Fichas, materiais e interiores incluem gavetas 16/16/40 cm, cabos fixos com cabeças retiradas, cesto liso com saco removível, ferragens, pintura fosca, faixa de pedra, tomadas 20 A e três comandos de luz 3000 K. O desenho usa o cenário de bancada 63 cm e módulos 60/65/61,9 cm; aéreos C/D e frente do forno são estudos condicionais identificados nas fichas. Tanque 38 × 35 cm em planta, cesto em corte e chapa única do varal atualizados. Torre, tomada da lavanderia e sua luminária não recebem posições inventadas no 3D. Plafon da cozinha tem eixo transversal conferido; posição longitudinal e cobertura ainda ilustrativas.

Nesta rodada, Elias autorizou também publicar todo o trabalho acumulado no repositório. Isso supera as restrições históricas de envio apenas do site/moodboard abaixo. Caches e temporários ficam locais; o artefato Pages permanece restrito aos arquivos do site.

## Navegação reformulada — 26/09/2026

A abertura apresenta o projeto e explica como explorar. Ambientes em cartões com ícones; mudanças de sofá, mesa, cadeiras, escritório, PS5 e varal em botões visuais, mostrados conforme o cômodo. No computador, o desenho permanece ao lado das opções. No celular, os controles ficam abaixo e “Ver no desenho” retorna à cena.

Visita guiada por seis ambientes, cenas “Dia a dia”, “Receber amigos” e “Hospedar”, botão Recomeçar e ajuda acessível a qualquer momento. A abertura não seleciona um móvel automaticamente. Medidas e ajustes ficam em seções expansíveis. Cores e materiais e Escolhas continuam disponíveis no menu.

Fichas da lavanderia atualizadas com tanque 38 × 35 × 20 cm úteis, cesto basculante removível 45 × 25 × 45 cm, Telca Flex preta e escoamento posterior com tampão/retentor removíveis. O percurso ilustrativo do varal é vertical; posições, alturas, fixações e encaixes continuam para conferência. Não foi produzido detalhamento executivo em 3D.

Verificação: [registro R08](Verificacao_interface_R08.json), incluindo 21 combinações de ambientes/vistas, tour completo, controles, fichas, teclado, abas e tamanhos de computador/celular. As seções abaixo descrevem a base geométrica e recursos mantidos; a experiência inicial e os seletores foram substituídos pela R08.

18/09/2026 · Navegação 3D com profundidade por pixel, transições animadas de estados, consulta aos interiores e decisões do banheiro/pisos incorporadas. O estudo mantém medidas e percursos hidráulicos pendentes identificados.

**GitHub Pages:** [site](https://queiroz-labs.github.io/guedala-park/) · [moodboard](https://queiroz-labs.github.io/guedala-park/moodboard/). O [registro inicial de publicação](Publicacao_GitHub_Pages.md) descreve uma etapa histórica; a autorização foi ampliada em 27/09, como registrado acima. A publicação da R10 de iluminação foi autorizada em 18/10/2026. Um push para `main` aciona a publicação automática do site e moodboard.

[Abrir o apartamento](Guedala_Park_Interativo.html) · [Moodboard com medidas](../../09_Referencias/Moodboard_atualizado_R01.html) · [Painel visual atualizado](../../09_Referencias/Moodboard_visual_atualizado_R01.png) · [Resumo do projeto](../../ESTADO_ATUAL.md)

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

Teste de oclusão com duas faces cruzadas e seleção pela profundidade real; órbita de 360° com 24 vistas; sete ambientes nas três vistas; animações intermediárias, finais e reversas, redução de movimento, 12 fichas de interiores, 59 decisões, cópia HTML independente e telas de 1440, 412 e 340 px. Renderização WebGL sem erros JavaScript. Animações são ilustrativas e não certificam colisões ou execução.

Caderno: preserva `ESPECIFICACOES_COMERCIAIS` manual.

## Organização das fontes

Componentes por tema; consulta R12 em `fabrication/Consulta`; R13 sem uso removida. ZIP: 264 entradas preservadas; CAD intacto. Pastas datadas bloqueadas no verificador.

## Galeria Dia/Noite

[Seis pares e exportações](../../09_Referencias/README.md), aparência aprovada em 28/10/2026. Galeria: `galeria/index.html`. `build_web.mjs` copia os arquivos de `ferramentas/moodboard/gerar.py`. Publicação autorizada por Elias, 28/10/2026.
