# Apartamento interativo — R54 e pacote R29

**Oficina:** [PDF e ZIP](../../06_Entregas/Ensaios_oficina/README.md), ensaios pendentes. Publicação R29 (navegação por cômodo) autorizada por Elias em 28/10/2026: “Sim, publicar”. R28: “pode fazer o push e atualizar o site com essas infos”.

**Modelo R54:** pedestal Berlin e cadeira lateral +15 mm; 106 cenários sem colisões novas. [Relatório e limites](../../02_Modelo_3D/Relatorio_mudanca.md). Publicação anterior em28/10/2026; alterações locais de30/10 não estão publicadas.

**Textos públicos:** estado atual, sem datas/revisões/atribuições. Fontes em `src/data.js`; registros internos preservados no git/fichas, retirados da biblioteca por `INTERNAL_DOCS` em `plain_language.py`.

**Box verde:** duas paredes, chuveiro e janela; outra interna clara (Elias, 30/10/2026: “quero que esteja na parede da janela tbm”). Quantidades são hipóteses; R44 intacto. Estado/README de referências reservados ao commit do Elias.

**Pé-direito nominal:**2,60m nos cômodos/2,50m no banheiro, Elias27/10/2026; [fonte e precedência do medido](../../07_Imovel/README.md). Forros/instalações/móveis condicionados ao levantamento; não alterar o FCStd automaticamente.

Planta R23: lavanderia 1,29 × 1,54 m e circulação compatibilizadas; fechamentos do banheiro de 16/17 cm são reconstruídos. Portas/janelas e instalações continuam a conferir.

`current_release.json` conserva CAD R54, pacote R29, fichas R15 e iluminação CB02. [Histórico de publicação e ZIPs](../../06_Entregas/README.md). Estudos separados não alteram geometria automaticamente.

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

A interface mantém fichas, visitas e movimentos; limites físicos nas fontes vigentes. [Verificação inicial](Verificacao_interface_R08.json): teclado, computador/celular e21 vistas. Revisões e autorizações anteriores ficam no git e não autorizam publicar alterações novas.

[Apartamento](Guedala_Park_Interativo.html) · [Moodboard](../../09_Referencias/Moodboard_atualizado_R01.html) · [Estado atual](../../ESTADO_ATUAL.md).

## Como usar

1. Escolha o ambiente e a vista: superior, 3D ou lateral. A vista lateral tem quatro direções e pode ocultar a metade oposta do ambiente para facilitar a leitura.
2. Arraste para girar o 3D; use a roda do mouse ou pinça com dois dedos para aproximar. Nas vistas superior/lateral, arrastar desloca o desenho. “Enquadrar” restaura a câmera.
3. Toque ou clique em um móvel para abrir sua ficha, com dimensões, material, origem da decisão e o que falta conferir. No celular, também existe “Ver móveis deste ambiente”.
4. “Mesa extensível” alterna 150/180 cm, com centro/banco fixos e três cadeiras na lateral. As transições de Bonnie, escritório, cadeiras, PS5 e varal são conceituais; encaixe e mecanismos seguem pendentes nas fichas.
5. Consulte as passagens e expanda “Ajustar hipóteses de circulação” para testar afastamento do sofá, profundidade do apoio da TV e espessura da cabeceira. Esses ajustes são simulações; recarregar restaura as decisões.
6. Use “Interiores em corte” para retirar as frentes dos armários detalhados. Em “Organização dos armários”, consulte desenhos e conteúdo de guarda; as fichas também têm acesso direto. Divisões ainda não escolhidas aparecem como pendentes.
7. Em “Moodboard”, veja paletas, móveis e dimensões por ambiente. Em “Decisões”, filtre escolhas aprovadas ou itens com decisões/medidas pendentes. O esquema interno aprovado R02 está incorporado à ficha do guarda-roupa.

HTML: salvar cópia completa, exportar escolhas, imprimir moodboard e salvar imagem da vista no computador.

## No S24 Plus

Envie **Guedala_Park_Interativo.html** ao celular e salve o arquivo. Ele contém os estilos, desenhos e interações, sem arquivos auxiliares ou bibliotecas externas. Abra em um navegador que aceite HTML local; se o aplicativo de arquivos exibir apenas uma prévia, use “Abrir com” um navegador compatível. O tratamento de arquivos locais varia conforme o navegador e o gerenciador de arquivos.

Emulação anterior: 412 × 915 e 915 × 412 com toque; computador 1440 × 1100. Layout/gestos testados, sem equivaler ao aparelho real. A cópia HTML funciona localmente e na web.

## O que o modelo representa

Geometria em centímetros, reconstruída a partir da planta oficial P01 e dos estudos do projeto. Os volumes são proporcionais e podem ser girados; estofados, texturas, mecanismos e ferragens são simplificados. O painel visual PNG foi produzido como ilustração de ambiente com auxílio de geração de imagem e revisado pelas decisões atuais. Use as fichas do HTML para medidas e aprovação.

As dimensões e pendências por ambiente ficam nas fontes vigentes: [sala/mesa/TV](../../03_Ambientes/Sala_e_jantar/README.md), [quarto/cama/armários](../../03_Ambientes/Quarto_e_portas/README.md), [escritório](../../03_Ambientes/Escritorio/README.md), [cozinha](../../03_Ambientes/Cozinha/README.md), [lavanderia](../../03_Ambientes/Lavanderia/README.md) e [banheiro](../../03_Ambientes/Banheiro/README.md). A interface consulta os dados atuais; representação de pedestal, móveis, abertura, trajetórias e materiais é aproximada, sem validar produto, mecanismo, carga ou fabricação.

Há um único PS5 representado, deslocado pelo seletor de ambiente. Não existe módulo para a caixa do gabinete, TV no quarto ou ar-condicionado. Estados de abertura do baú e varal são demonstrações conceituais. Alterações dos controles não aprovam novas medidas ou móveis.

Portas, janelas, espessuras e trechos não cotados foram reconstruídos graficamente. Pé-direito nominal: 260 cm nos cômodos e 250 cm no banheiro, a confirmar (Elias, 27/10/2026). Forros e sancas não têm altura confirmada. Este é um estudo de layout, não desenho para fabricação. Piso vinílico definido, exceto banheiro/lavanderia; Olmo é a preferência, com Aveia/Bétula para comparar amostras. Cores digitais não substituem amostras físicas.

## Base documental e manutenção

- [Registro de decisões](../../01_Programa_e_decisoes/Registro_de_decisoes.md), [memorial Cury](../../01_Programa_e_decisoes/Memorial_Cury_impactos.md) e [P01](../../07_Imovel/referencias/P01_planta_oficial.png).
- [Painel e TV](../../03_Ambientes/Sala_e_jantar/Painel_e_TV.md), [mesa e três cadeiras R03](../../03_Ambientes/Sala_e_jantar/Mesa_e_cadeiras.md), [guarda-roupa R02](../../03_Ambientes/Quarto_e_portas/Guarda_roupa_interior.md) e [cabeceira](../../03_Ambientes/Quarto_e_portas/Cabeceira_e_armario_superior.md).
- [Escritório](../../03_Ambientes/Escritorio/README.md), [cozinha](../../03_Ambientes/Cozinha/README.md) e [lavanderia](../../03_Ambientes/Lavanderia/README.md).

Fontes em `src`; `construir.py` gera os HTMLs autônomos. Atualizar dados e desenhos juntos quando houver decisão. Planta F118–F120 e painel de materiais antigo são históricos.

O fluxo `.github/workflows/pages.yml` executa `preparar_pages.py` a cada push em `main` e publica o artefato `.site` com página principal, moodboard, imagem de materiais e identificação da versão. Pages usa GitHub Actions. Fotos da visita e registros ficam no repositório.

[Verificação anterior](Verificacao_completa_R01.json): 21 combinações, controles, fórmulas de circulação, toque, esquema R02 e cópia reaberta; sem erros, requisições externas ou transbordamento nos cenários testados.

## Verificação R05

Verificação R05: oclusão, vistas, movimentos e controles, fichas e telas sem erros JavaScript. Mantém limites nominais e verificações físicas pendentes.

Caderno: preserva `ESPECIFICACOES_COMERCIAIS` manual.

## Organização das fontes

Componentes por tema; consulta R12 em `fabrication/Consulta`; R13 sem uso removida. ZIP: 264 entradas preservadas; CAD intacto. Pastas datadas bloqueadas no verificador.

## Galeria Dia/Noite

[Seis pares e PDFs](../../09_Referencias/README.md) em `galeria/index.html`. Elias, 28/10/2026: "Aprovado, pode commitar e dar push." Na aba Cômodos (29/10, local), cada cartão abre com o par Dia/Noite (`_web.webp` de `galeria/`, carregado ao aparecer; arrastar, controle ou botões Dia/Noite) e alterna para o 3D; sem internet, aviso no lugar da foto. `app.js → DAY_NIGHT`.

## Navegação e documentos

**Consulta anterior em quatro abas** (28/10): Apartamento (3D; *Planta com medidas* virou botão da barra, com volta), Cômodos (antiga Materiais: paleta, todos os itens com selo e *Documentos deste cômodo*), Escolhas (placar e detalhe de cada item, com *Ver no 3D*) e Documentos. `?aba=materiais|planta|ambientes` continuam válidos. Selo único em `app.js → STATUS_GROUPS`: Decidido, Em estudo, Futuro; "A conferir" mostra o texto de medida. Elias, 28/10/2026: "Confirmo" (ambíguos: para desenvolver, existente, entrega e 1ª opção → Decidido; tamanho futuro → Futuro). Teste: `test_navigation.cjs`.

**15 cartões** em `current_release.json → documentLibrary`; a grade inicial mostra 10 e os 5 de cômodo viram atalhos (busca e filtro ainda os listam). Páginas de agrupamento abrem na mesma aba, com trilha de volta; relatórios em `.md` abrem com os detalhes técnicos visíveis.

[Antes → depois das88 entradas](Documentos_antes_depois.csv). A fonte anterior tinha88 entradas,65 visíveis e23 internas. Três entradas sem arquivo viraram pendências em Antes de fabricar. Nove referências de histórico/estudos antigos ficam fora da lista pública, preservadas no repositório e nos vínculos existentes. Nenhum documento foi movido ou apagado. O catálogo técnico permanece separado dos cartões.

`document_library.py` gera14 páginas de agrupamento no build, nos mesmos tons, fontes e links do site; o15º acesso baixa o ZIP. O índice dos móveis reúne Estudos deste móvel para os20 módulos e furação por peça, sem alterar fichas, dimensões ou arquivos técnicos. As duas referências de mesa/varal apontam para uma única entrada por agrupamento. A busca consulta também os subitens; status dos cartões: Atual, Em estudo ou Pendente. No pacote extraído, o cartão do ZIP abre seu índice, sem tentar baixar o próprio arquivo.

As páginas geradas entram tanto em docs/ do preview quanto no pacote offline, com a mesma seleção explícita de fontes. Não escrever HTML à mão em .site/. Regerar: `python -B ferramentas/site/build_workshop_docs.py --sources-only` e `python -B ferramentas/site/construir.py`. Testes: `python -B ferramentas/site/test_document_library.py`, `node ferramentas/site/test_document_library.cjs` e `python -B ferramentas/verificar_site.py`. Os testes conferem88 destinos,15 cartões,20 móveis, links dos grupos, busca, filtros e navegação offline. ZIPs selados não são sobrescritos; o verificador usa uma reconstrução temporária. Nada nesta alteração autoriza publicação.

**Reconciliação pendente; fontes preservadas:**

- Manter Dossie R45 como atalho às fichas atuais?
- Manter CB01 como comparação com a opção econômica ou mostrar só a seleção atual?
- Manter estudo de movimentos R52 como referência numérica separada, com o modelo R54?
- L02 histórica ainda é referência de componentes/preços do banheiro ou há outra composição vigente?

## Dia das chaves — local, sem publicação

Guia por cômodo: toque na planta ou escolha na lista; uma medida por vez, mini-planta, instruções, foto disponível, valor do projeto e campo grande; Pular/Voltar/Próxima e revisão final. “Ver todos” mantém a lista.
156 itens/162 campos do CSV, sem medidas novas; DIM conserva `/0`/`/1`. Guia e lista usam `guedala:medidas:v1` e o mesmo JSON v1/CSV; fallback, importação atômica e exportação continuam. Sem tolerância presumida. Textos dos 162 guias têm frases de até 20 palavras, sem jargão; códigos/fontes ficam em “Código e referência”.
[Guias por código](guias_campo.json): rascunho externo por `estudos/rascunhar_guias_campo.py`, seguido de edição dos textos. [Cobertura](Cobertura_guias.csv): 78 códigos só com cômodo; 128 sem foto. Alvos nominais vêm de Cotas.pranchas; descrição pendente remete ao protocolo proposto, disponível offline.
“Ponto de partida conferido” mantém a trava PR/datum por seção; sem confirmação, só evidência. A “Folha de início” explica a proposta; o protocolo técnico fica recolhido. Pontos/panos ficam recolhidos e opcionais no guia; MOV/ANC/PISO/COMP continuam anotações.
34 guias usam 14 quadros inspecionados: seis associações trocadas, 23 adicionadas. A cobertura descreve `foto_confere` e origem; sem marcas/reflexos ou cortes inadequados. JPEG 480 px; legendas distinguem unidade espelhada/Mobiliado. Associação dos dormitórios estimada no Complemento R02.
Cinco ícones ilustram altura/largura/distância/nível/prumo. Setas mostram direita/baixo e “Início (0)” sugerido junto à entrada, sem equiparar ao zero do projeto. O cartão “Antes de começar” lembra a dispensa em `guedala:guia:inicio:v1`, com fallback; não altera medidas.
[Guia leve offline](Dia_das_chaves.html) <1 MB, com fotos/planta/protocolo sem rede. HTML completo conserva CAD/dossiês e teto anterior (>5 MB); deduplicação e WebP sem perda reduzem tamanho. Sem capturas no git.
Fontes `build_field_data.py`, `build_field_guide.py`, `src/field-*`; regerar com `python -B ferramentas/site/construir.py`. Testes `test_field*.cjs` e importador em `verificar_site.py`; Playwright nos 162 passos a 375/1280 px: sem overflow, botões ≥44 px, campos ≥16 px, persistência e exportação idêntica entre modos. Referência visual: site existente/Refero; pesquisa remota indisponível por assinatura.

## Obra — local

Sexta aba: semanas 0–8 derivadas apenas de `Cronograma_obra_e_compras.md` §2 por `build_work_data.py`; ordem, dependências e observações preservadas. Etapas longas aparecem nas semanas correspondentes, com uma única marcação/contagem. Links da área e plano NBR 16280 acompanham as etapas; [seis dúvidas para o RT](../../05_Orcamento_e_cronograma/README.md#acompanhamento-da-obra-no-site), sem mudar a sequência.

“Feito” salva no aparelho (`guedala:obra:v1`), com fallback em memória e backup `Obra_real.json` por Exportar/Importar obra. Uma etapa cuja semana/condição mudou não herda a marca antiga. O HTML autônomo funciona sem rede; documentos externos exigem conexão ou inclusão na cópia. Fontes: `src/work-*`; testes `test_work.cjs` e `test_work_data.py`, incluídos em `verificar_site.py`. Sem publicação.

**Pergunta do guia:** qual ponto ou borda de cada janela, porta e ligação deve receber a ponta da trena, e como o início junto à entrada se relaciona com o desenho? A folha continua proposta; distâncias sem essa definição não são aplicadas.
