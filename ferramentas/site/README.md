# Apartamento interativo — R54 e pacote R29

**Oficina:** [PDF e ZIP](../../06_Entregas/Ensaios_oficina/README.md), ensaios pendentes. Publicação R29 (navegação por cômodo) autorizada por Elias em 28/10/2026: “Sim, publicar”. R28: “pode fazer o push e atualizar o site com essas infos”.

**R54:** [106 cenários e limites](../../02_Modelo_3D/Relatorio_mudanca.md); pedestal Berlin/cadeira +15 mm.

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

Na raiz do repositório, `auto` verifica o ZIP selado ou constrói quando ausente; texto UTF8/LF e binários preservados. Conteúdo novo exige revisão do pacote. O gerador só cria artefato local; deploy depende de commit/push autorizados.

`build_workshop_docs.py --sources-only` atualiza somente os dados de consulta. `--regenerate-sources` é uma opção explícita para reconstruir fichas/planta; o fluxo normal usa as fontes correntes já verificadas. Testes ficam nesta pasta e saídas temporárias fora do repositório.

**Integração:**20 módulos/249 painéis com eixos e SHA nas fichas. Produtos, furação, medidas reais e ensaios continuam condicionados; [histórico de publicação](../../06_Entregas/README.md).

## Referências e verificações

[Luz e contatos](Luz_e_contato/README.md): efeitos aproximados, controles e movimentos preservados. Prevalecem a configuração corrente e os limites atuais.

## Referências da interface

[Verificação inicial](Verificacao_interface_R08.json) e limites nas fontes vigentes; histórico não autoriza publicação nova.

[Apartamento](Guedala_Park_Interativo.html) · [Moodboard](../../09_Referencias/Moodboard_atualizado_R01.html) · [Estado atual](../../ESTADO_ATUAL.md).

## Como usar

1. Escolha o ambiente e a vista: superior, 3D ou lateral. A vista lateral tem quatro direções e pode ocultar a metade oposta do ambiente para facilitar a leitura.
2. Arraste para girar o 3D; use a roda do mouse ou pinça com dois dedos para aproximar. Nas vistas superior/lateral, arrastar desloca o desenho. “Enquadrar” restaura a câmera.
3. Toque ou clique em um móvel para abrir sua ficha, com dimensões, material, origem da decisão e o que falta conferir. No celular, também existe “Ver móveis deste ambiente”.
4. “Mesa extensível”, Bonnie, escritório, cadeiras, PS5 e varal alternam cenas conceituais; dimensões correntes nos dados/fichas, mecanismos pendentes.
5. Consulte passagens e simule afastamento do sofá, apoio da TV e espessura da cabeceira; recarregar restaura os dados do projeto.
6. Use “Interiores em corte” para retirar as frentes dos armários detalhados. Em “Organização dos armários”, consulte desenhos e conteúdo de guarda; as fichas também têm acesso direto. Divisões ainda não escolhidas aparecem como pendentes.
7. Em “Cômodos”, consulte paletas/móveis; em “Escolhas”, decisões e conferências. Esquema interno R02 na ficha do guarda-roupa.

HTML: salvar cópia completa, exportar escolhas, imprimir moodboard e salvar imagem da vista no computador.

## No S24 Plus

Salve **Guedala_Park_Interativo.html** e abra em navegador com suporte a HTML local. “Salvar cópia” embute o catálogo; a fonte usa `src/downloads-data.js`. Desenhos/interações funcionam sem rede; arquivos vinculados exigem rede ou cópia local.

Conferências anteriores não equivalem ao aparelho real.

## O que o modelo representa

Geometria reconstruída da P01, com volumes, texturas e mecanismos simplificados. Painel PNG ilustrativo com auxílio de geração de imagem. [Fontes e limites](../../02_Modelo_3D/README.md); medidas nas fichas são nominais.

As dimensões e pendências por ambiente ficam nas fontes vigentes: [sala/mesa/TV](../../03_Ambientes/Sala_e_jantar/README.md), [quarto/cama/armários](../../03_Ambientes/Quarto_e_portas/README.md), [escritório](../../03_Ambientes/Escritorio/README.md), [cozinha](../../03_Ambientes/Cozinha/README.md), [lavanderia](../../03_Ambientes/Lavanderia/README.md) e [banheiro](../../03_Ambientes/Banheiro/README.md). Representação aproximada; produto, mecanismo, carga e fabricação continuam condicionados.

Há um único PS5 representado, deslocado pelo seletor de ambiente. Não existe módulo para a caixa do gabinete, TV no quarto ou ar-condicionado. Estados de abertura do baú e varal são demonstrações conceituais. Alterações dos controles não aprovam novas medidas ou móveis.

Portas, janelas, espessuras e trechos não cotados foram reconstruídos graficamente. Pé-direito nominal: 260 cm nos cômodos e 250 cm no banheiro, a confirmar (Elias, 27/10/2026). Forros e sancas não têm altura confirmada. Este é um estudo de layout, não desenho para fabricação. Piso vinílico definido, exceto banheiro/lavanderia; Olmo é a preferência, com Aveia/Bétula para comparar amostras. Cores digitais não substituem amostras físicas.

## Base documental e manutenção

- [Registro de decisões](../../01_Programa_e_decisoes/Registro_de_decisoes.md), [memorial Cury](../../01_Programa_e_decisoes/Memorial_Cury_impactos.md) e [P01](../../07_Imovel/referencias/P01_planta_oficial.png).
- [Painel e TV](../../03_Ambientes/Sala_e_jantar/Painel_e_TV.md), [mesa e três cadeiras R03](../../03_Ambientes/Sala_e_jantar/Mesa_e_cadeiras.md), [guarda-roupa R02](../../03_Ambientes/Quarto_e_portas/Guarda_roupa_interior.md) e [cabeceira](../../03_Ambientes/Quarto_e_portas/Cabeceira_e_armario_superior.md).
- [Escritório](../../03_Ambientes/Escritorio/README.md), [cozinha](../../03_Ambientes/Cozinha/README.md) e [lavanderia](../../03_Ambientes/Lavanderia/README.md).

Fontes em `src`; `construir.py` gera os HTMLs autônomos. Atualizar dados e desenhos juntos quando houver decisão. Planta F118–F120 e painel de materiais antigo são históricos.

Pages usa o workflow após push autorizado; `preparar_pages.py` gera apenas artefato local.

[Histórico da interface](Verificacao_completa_R01.json); novas alterações exigem nova conferência.





## Organização das fontes

Componentes por tema; consulta em `fabrication/Consulta`. Histórico no git.

## Galeria Dia/Noite

[Seis pares e PDFs](../../09_Referencias/README.md): galeria e Dia/Noite nos cartões de Cômodos (`app.js → DAY_NIGHT`). Botões, arraste e alternância para 3D; sem rede, aviso na foto.

## Navegação e documentos

Downloads: `downloads-source.json` seleciona itens; `build_downloads_data.py` mede os bytes e publica em `docs/`. Catálogo fora do HTML evita autorreferência do ZIP. Entrada/Documentos usam o mesmo componente, com busca, revisão, formato, tamanho e situação. Pacotes têm escopos distintos; `downloads-manifest.json` lista destinos. `test_downloads.cjs` confere fontes, bytes, links e 8 imagens R03/SHA no CI.

Navegação: Apartamento, Cômodos, Escolhas e Documentos; planta cotada na barra do 3D. Aliases `?aba=materiais|planta|ambientes` preservados. Selos em `STATUS_GROUPS`: Decidido, Em estudo, Futuro; “A conferir” mantém medidas pendentes. Mapeamento: Elias, 28/10/2026, “Confirmo”; teste `test_navigation.cjs`.

**Comece aqui:** entrada padrão para qualquer visitante; `?perfil=arquiteto` e ids preservados. `?aba=`/hash reconhecidos têm prioridade; o endereço antigo do moodboard mantém Cômodos. “Como explorar” abre ajuda e leva ao 3D/visita. `build_architect_data.py` extrai resumo/9 etapas de ESTADO_ATUAL e revisão do release. `architect-source.json`: 3 caminhos iniciais (botões ≥56 px), 3 perguntas/atalhos e 8 disciplinas/6 documentos com fontes; UI em `src/architect-*`. Planta mobiliada R03: cena R54 e sete vistas recapturadas. Tokens do site/Refero.
esbuild existente compacta scripts sem mudar nomes globais. Teste `test_architect_entry.cjs` no verificador/CI.
“Quem decide” filtra disciplinas e conferências dos 65 itens. Papéis por móvel vêm de `quem_valida`, ligados por módulo no CSV de medidas; “Elias registra/identifica” não vira decisão técnica. Sem vínculo, “a definir”; selos também nas escolhas/cômodos. Fonte e medidas reais explícitas em cada registro.
Busca global: índice por palavras únicas em `build_search_index.py`, sem biblioteca nova. Pendências/papéis, escolhas, cômodos, P01–P20 e documentos; resultado abre aba/registro, `/` foca e Esc limpa. `test_search.cjs` no CI. [53 vínculos sem responsável](Responsaveis_pendentes.csv), sem atribuição presumida.
Faixas de até 2 linhas nas 7 abas e na planta explicam uso/revisão/limite nominal; aviso global e glossário pelo “?” (43 entradas com fonte; P01–P20, T0 e T01–T09), também pesquisável. Ids preservados; Ferramentas ao fim para todos; `#chaves`/`#obra` agora abrem as telas, preservando `data-tab`/`?aba=`. Resumos de etapas: ESTADO_ATUAL; normas/siglas: fontes no glossário, sem interpretação normativa nova.

A publicação usa `publicacao_documentos.json`: leitura inicial, arquivo técnico e páginas ocultas, cada uma com motivo. `publication.py` remove comandos, blocos de código e caminhos do corpo; nomes dos móveis substituem códigos, reunidos em “Fonte e códigos”. Fontes de trabalho e entregas permanecem completas. A mesma política atende biblioteca, entrada e downloads; links relativos preservam a consulta offline. 20 documentos em “Para ler”; demais destinos vigentes em “Arquivo técnico (para o projetista)”, recolhido. Busca alcança os dois e abre os resultados técnicos. Históricos continuam ocultos. A seleção explícita também alimenta o pacote offline. “Em resumo” extrai frases existentes; seções extensas ficam em “Ver detalhes”, a primeira aberta. Texto de 17 px/1,6, parágrafos separados em fim de frase; tabelas viram cartões até 600 px. Alteração local, sem push.

## Dia das chaves — local, sem publicação

Guia por cômodo: toque na planta ou escolha na lista; uma medida por vez, mini-planta, instruções, foto disponível, valor do projeto e campo grande; Pular/Voltar/Próxima e revisão final. “Ver todos” mantém a lista.
156 itens/162 campos do CSV, sem medidas novas; DIM conserva `/0`/`/1`. Guia e lista usam `guedala:medidas:v1` e o mesmo JSON v1/CSV; fallback, importação atômica e exportação continuam. Sem tolerância presumida. Textos dos 162 guias têm frases de até 20 palavras, sem jargão; códigos/fontes ficam em “Código e referência”.
[Guias por código](guias_campo.json): rascunho externo por `estudos/rascunhar_guias_campo.py`, seguido de edição dos textos. [Cobertura](Cobertura_guias.csv): 78 códigos só com cômodo; 128 sem foto. Alvos nominais vêm de Cotas.pranchas; descrição pendente remete ao protocolo proposto, disponível offline.
“Ponto de partida conferido” mantém a trava PR/datum por seção; sem confirmação, só evidência. A “Folha de início” explica a proposta; o protocolo técnico fica recolhido. Pontos/panos ficam recolhidos e opcionais no guia; MOV/ANC/PISO/COMP continuam anotações.
34 guias usam 14 quadros inspecionados: seis associações trocadas, 23 adicionadas. A cobertura descreve `foto_confere` e origem; sem marcas/reflexos ou cortes inadequados. JPEG 480 px; legendas distinguem unidade espelhada/Mobiliado. Associação dos dormitórios estimada no Complemento R02.
Cinco ícones ilustram altura/largura/distância/nível/prumo. Setas mostram direita/baixo e “Início (0)” sugerido junto à entrada, sem equiparar ao zero do projeto. O cartão “Antes de começar” lembra a dispensa em `guedala:guia:inicio:v1`, com fallback; não altera medidas.
[Guia leve offline](Dia_das_chaves.html) <1 MB, com fotos/planta/protocolo sem rede. HTML completo conserva CAD/dossiês e teto anterior (>5 MB); deduplicação e WebP sem perda reduzem tamanho. Sem capturas no git.
Fontes `build_field_data.py`, `build_field_guide.py`, `src/field-*`; regerar via `construir.py`. Testes `test_field*.cjs`/importador em `verificar_site.py`; Playwright: 162 passos, 375/1280 px, sem overflow, botões ≥44 px, campos ≥16 px; persistência/exportação entre modos.

## Obra — local

Sexta aba: semanas 0–8 derivadas apenas de `Cronograma_obra_e_compras.md` §2 por `build_work_data.py`; ordem, dependências e observações preservadas. Etapas longas aparecem nas semanas correspondentes, com uma única marcação/contagem. Links da área e plano NBR 16280 acompanham as etapas; [seis dúvidas para o RT](../../05_Orcamento_e_cronograma/README.md#acompanhamento-da-obra-no-site), sem mudar a sequência.

“Feito” salva no aparelho (`guedala:obra:v1`), com fallback em memória e backup `Obra_real.json` por Exportar/Importar obra. Uma etapa cuja semana/condição mudou não herda a marca antiga. O HTML autônomo funciona sem rede; documentos externos exigem conexão ou inclusão na cópia. Fontes: `src/work-*`; testes `test_work.cjs` e `test_work_data.py`, incluídos em `verificar_site.py`. Sem publicação.

**Pergunta do guia:** qual ponto ou borda de cada janela, porta e ligação deve receber a ponta da trena, e como o início junto à entrada se relaciona com o desenho? A folha continua proposta; distâncias sem essa definição não são aplicadas.

**UX móvel:** visual atual preservado; `mobile-ux-core.js`/`mobile-ux.js` e CSS final em `mobile-ux.css`. Até760 px, cabeçalho recolhe ao descer e reabre ao subir/topo/foco na busca; busca/abas ficam visíveis. Compensação conserva o fluxo. Medido203,2→98 px; desktop155,2 px inalterado. `tab-strip.js`: bordas indicam rolagem, aba ativa visível; setas/Home/End. Medição inclui painéis abertos e modo lista; lacunas de texto/alvos corrigidas. `test_mobile_ux.cjs` no verificador/CI.

**Selos:** toque ou Enter/Espaço abre explicação; Esc fecha, com foco de volta. `statusHelp` em `architect-source.json` alimenta glossário/busca. Legenda do [caderno](../../01_Programa_e_decisoes/Caderno_de_especificacoes.md): escolha registrada e detalhamento pendente; não confirma execução. Materiais são referências/opções e “Atual” indica revisão documental. Papéis vêm das fontes de cada pendência; ausentes ficam “Responsável a definir”. Fichas: compra, produto, montagem e protótipo pendentes têm ajuda com fonte na ficha. Dados originais preservados.
