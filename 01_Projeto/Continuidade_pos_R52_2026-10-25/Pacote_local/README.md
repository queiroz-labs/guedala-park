# Pacote R17 selado — registro da entrega anterior

**Publicação corrente R52/R18:** [pacote R18](../../../05_Entregas/Publicacao/Guedala_Park_R18.zip) · [estado do envio e conferência remota](../../Estado_atual.md). O R17 documentado abaixo fica selado, com bytes e hash preservados. Os comandos e verificações abaixo são o registro do preparoR17; a configuração corrente passa àR18 e não deve ser usada para regenerar este ZIP histórico.

25/10/2026. **Entregue um novo pacote local R17 com o FreeCAD R52**, as fichas R14 atuais, a planta, o caderno de especificações e o visualizador que funciona sem internet. Nenhum envio, commit, push ou deploy foi realizado. R16, aliases antigos e a pasta `.site` anterior foram preservados byte a byte.

[Baixar/abrir o ZIP R17](../../../05_Entregas/Compartilhar_R17/Guedala_Park_R17.zip) · [instruções para extrair](../../../05_Entregas/Compartilhar_R17/LEIA-ME.md) · [nota sobre CAD e fichas P20](../../../05_Entregas/Compartilhar_R17/NOTAS_CAD_E_FICHAS.md)

Extraia o ZIP inteiro e abra `Guedala_Park_R17/COMECE_AQUI.html`. O menu leva ao modelo editável, ao visualizador offline, às 20 fichas, à planta cotada e às pendências. Não exige novas medidas do apartamento para consulta; fabricação, carga e instalação permanecem condicionadas às fichas e ao levantamento posterior.

| Conferência | Resultado |
|---|---|
| Revisão do pacote | R17 local |
| Modelo editável | R52, sem modificar a geometria ou salvar novamente o CAD |
| Arquivos no ZIP | 142 |
| Tamanho | 27.016.117 bytes, aproximadamente25,8MiB |
| CRC | Todos os 142 arquivos aprovados |
| SHA256 das entradas | 141 entradas conferidas pelo manifesto; o manifesto também consta do inventário externo |
| Navegação HTML local | 272 referências conferidas, nenhuma quebrada |
| Links externos | 314 ocorrências; exigem internet se forem abertas |
| Referências locais fora do recorte | 26 ocorrências estáticas desativadas e identificadas no manifesto |
| Conteúdo privado/contratos/e-mails/protocolos | Nenhum caminho incluído; seleção técnica explícita |
| Idempotência | Repetir o build com os mesmos insumos mantém bytes e mtime do ZIP |
| Navegador offline | Computador1440×1000 e celular412×915; zero errosJS e zero pedidosHTTP |
| Cópia web isolada |387 peças carregadas porworker e fichaP20 porJSON; zero errosJS ou acessoexterno |
| Preservação |331 arquivos /390.575.076bytes deR16,aliasR14 e.site mantidos;11backups de fontes verificados |

SHA256 do ZIP:

`2e8b9167d4a2b4db8a38f477e27239e728a63ff6f6fdfe1539d9d0b32525a7ea`

SHA256 do FreeCAD R52 incluído:

`941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`

## Fonte única para as próximas gerações

[`current_release.json`](../../Estudo_interativo/current_release.json) concentra revisão, caminho e SHA do CAD; revisão/destino/nome do pacote; revisões de fichas, aparência e iluminação; data e condição local. [`current_release.py`](../../Estudo_interativo/current_release.py) valida o SHA real e a concordância com `CAD_DATA` e `PROJECT`, recusando geração com dados divergentes.

Os geradores do pacote, dos documentos, da cópia web e os textos da biblioteca agora consultam essa configuração. A revisãoR49 permanece apenas onde identifica o material anterior publicado ou um registro histórico. O download do CAD corrente e a navegação do pacote usam o caminho efetivo daR52, sem um alvoR49 escondido por um rótulo novo.

`build_share_package.py` não copia ou substitui os aliasesR14/R16. O pacote é imutável: se um arquivoR17 existente tiver bytes diferentes dos que seriam gerados, o build para e pede uma nova revisão de pacote. Com os mesmos insumos, não regrava o ZIP. A imutabilidade foi verificada no ambiente local; alterações de conteúdo ou de representação dos insumos exigem uma revisão nova.

`preparar_pages.py` e `build_web.mjs` aceitam um destino explícito isolado. Os padrões recusam sobrescrever uma `.site` já existente. A geração web isolada lê a versão corrente, prepara fontes, garante o pacote e exporta os documentos e assets na sequência, sem chamar deploy. O build de documentos também oferece `--sources-only`; a regeneração das fichas precisa da opção explícita correspondente.

Comandos, a partir da raiz `guedala-park`:

```powershell
python 01_Projeto/Estudo_interativo/build_share_package.py
python 01_Projeto/Estudo_interativo/test_current_release.py
python 01_Projeto/Estudo_interativo/preparar_pages.py --output-dir "../outputs/continuidade-pos-r52-2026-10-25/web-r17"
```

Nesta entrega a cópia web ficou somente em `outputs/continuidade-pos-r52-2026-10-25/web-r17`, fora da `.site` anterior. Esse registro descreve o momento anterior à autorização de publicação. A publicação R52/R18 foi autorizada depois; prevalece o Estado atual para envio/deploy, preservando este ZIPR17.

## Recorte do pacote e links

Incluídos: um CAD principalR52 e suas verificações selecionadas; o estudo separado de uniões nominaisP19, identificado como estudo; fichasR14 e respectivosHTML/SVG/CSV/JSON; planta oficial e cotada; visualizador autônomo; caderno; referências selecionadas de cores, rodízios e iluminação. O inventário completo está em [Arquivos_R17.csv](Arquivos_R17.csv), com tamanho, CRC32, SHA256 final e hash da fonte quando aplicável.

Não há varredura recursiva do acervo para compor o ZIP. São recusados caminhos privados, contratos, e-mails e protocolos. Os documentosMarkdown incluídos permanecem como fontes; versões`.md.html` foram geradas para consulta local. Os links estáticos dessas versões foram restritos aos arquivos incluídos. A biblioteca do visualizador também desativa documentos que não pertencem ao pacote e informa a ausência, em vez de direcionar a um arquivo inexistente. [Referências estáticas omitidas](Referencias_locais_omitidas.json).

A notaP20 diferencia a correção das fichas/CSV do CAD: foi retirado o resíduo textual de composição com receptorR47 das fontes operacionais, preservando dimensões e acabamentos escolhidos. A conferência direta de`Document.xml` mostrou `EspecificacaoR14` nas duas tampas apenas como BrancoTX nas faces internas, sem receptorR47 nesse campo. Não foi necessária alteração do CAD; composição real, fixação e capacidade continuam pendentes. Não se declara sincronização integral de todos os metadados históricos do CAD com estudos posteriores.

## Evidências e preservação

- [Verificação do ZIP](verificacao-pacote.json), [QA offline](qa-browser-pacote.json), [QA da cópia web](qa-web-isolada.json), [conferência das tampas no XML](conferencia-xml-tampas.json) e [preservação dos arquivos anteriores](verificacao-preservacao.json).
- Sete testes de configuração, concordância, proteção de destinos, seleção técnica e imutabilidade aprovados em`test_current_release.py`.
- Origens anteriores às edições preservadas em`outputs/continuidade-pos-r52-2026-10-25/originais`, com`manifesto-originais.json`; os98backups de fabricação constam do manifesto separado desse agente.
- Dois pacotes preliminares deQA foram preservados nos subdiretórios`R17_pre_QA_metadata` e`R17_pre_QA_precisao_P20` dos outputs. O primeiro revelou rótulosR49 ainda sobrepostos pelo módulo de linguagem; o segundo permitiu retirar uma ressalva genérica imprecisa sobre metadados doCAD. Ambos são rascunhos, não a entrega final. Os bytes doR17 final acima foram mantidos após o fechamento.

O trabalho desta etapa não altera os índices gerais, não pede medidas reais, não muda a seleção física do projeto e não libera produção ou compras.

## Nota sobre a contagem do QA

`metadata.files=140` é a lista de conteúdo usada para navegação do visualizador. O menu inicial e o manifesto raiz são adicionados depois:140+2=142 arquivos no ZIP. [Explicação e comparação direta](Contagem_arquivos_R17.md). O ZIP selado não foi modificado.
