# Regras do projeto Guedala Park

Valem para qualquer pessoa ou IA (Claude, Codex…) que trabalhe nesta pasta. Seguir sempre, sem precisar pedir.

## 0. Como ler este projeto gastando poucos tokens

- Leia, nesta ordem e só até achar a resposta: [ESTADO_ATUAL.md](ESTADO_ATUAL.md) (~10 KB) → o `README.md` da pasta do assunto → o arquivo específico que ele indicar.
- **Nunca leia inteiros:** `01_Programa_e_decisoes/Registro_de_decisoes.md` (~475 KB; use busca por palavra ou data), arquivos `.json` grandes e `.html` gerados. Use `rg`/`jq` ou um script de `ferramentas/`.
- O arquivo `.ignore` na raiz faz o Grep/ripgrep pular fontes brutas, gerados e dados enormes. Para procurar neles de propósito, passe o caminho exato ou use `--no-ignore`.
- Mapa das pastas: seção 9. Cada pasta de topo e cada ambiente tem um README que diz o que há nela.
- Antes de mexer no modelo FreeCAD, leia [02_Modelo_3D/README.md](02_Modelo_3D/README.md) e rode as verificações (seção 10).

## 1. Comece pela fonte de verdade

- Leia primeiro [ESTADO_ATUAL.md](ESTADO_ATUAL.md). Ele diz qual versão vale de cada coisa.
- Depois leia só o README da área em que vai trabalhar. Não percorra a pasta inteira.
- Em caso de divergência, vale o `ESTADO_ATUAL.md`. Se ele estiver errado, corrija-o.

## 2. Organize pelo apartamento, não pela sessão

- Uma pasta por **assunto permanente**: ambiente (Cozinha, Banheiro…), móvel (P01…P20), disciplina (orçamento, entregas, referências).
- **Nunca** crie pasta com data ou número de sessão no nome (`Compatibilizacao_2026-10-04`, `Calculo_P11_2026-10-24`, `Execucao_ate_07h`). Um estudo novo vai para dentro da pasta do móvel ou ambiente a que pertence.
- Nomes: `Maiuscula_com_underline`, sem acentos nem espaços, curtos e descritivos.

## 3. Uma versão vigente por item

- Cada item tem **um** arquivo vigente. Ao revisar, edite-o ou substitua-o; não crie `_R53`, `_novo`, `_final`, `_v2` ao lado.
- O histórico fica no **git** (commit com mensagem clara), não em cópias na pasta. Não existe pasta de arquivo morto: o superado é removido no mesmo commit em que é substituído.
- Número de revisão (R52, R14…) aparece no texto do README/ESTADO_ATUAL e, se preciso, no nome do arquivo entregue a terceiros, nunca no nome de pasta.
- Exceção: `06_Entregas/` guarda exatamente o que foi enviado ou publicado, uma versão por entrega, até ser substituída por nova entrega.

## 4. Documentação curta e atual

- Cada pasta tem no máximo um `README.md`, que descreve o **estado atual** daquele assunto: decisão, medidas, por quê, pendências. Nada de diário ("às 03h fizemos…").
- Antes de criar um `.md` novo, verifique se o conteúdo cabe num existente. Prefira atualizar a criar.
- Ao terminar um trabalho: atualize o README da área e a linha correspondente no `ESTADO_ATUAL.md`; apague `.md` que ficaram superados.
- Escreva para leitura rápida: tabela ou lista no topo com o que vale, detalhe depois. Dados numéricos grandes vão em JSON/CSV ao lado, referenciados pelo README, não colados no texto.
- Pendência resolvida sai da lista de pendências (vira decisão no README). Não acumule "~~riscado~~".

## 5. Ferramentas fora do projeto

- Scripts do projeto ficam em `ferramentas/` (gerador do site em `ferramentas/site`). Não deixe `.py`/`.cjs` de uso único espalhados pelas pastas de conteúdo.
- Nunca dentro do projeto: ambientes virtuais, `node_modules`, `__pycache__`, código-fonte de ferramentas de terceiros, saídas de testes, downloads de pesquisa brutos (`.firecrawl`). Use a pasta temporária da sessão e apague ao final.
- `.site/` é gerado; não edite à mão. `guedala-pessoal/` (dados pessoais) nunca vai para o site nem para o repositório público.

## 6. Arquivos pesados

- Só o `.FCStd` vigente fica na pasta. Backups de modelo antes de uma alteração arriscada ficam fora do projeto ou viram commit; apague-os quando a alteração for conferida.
- Imagens: guarde só as aprovadas ou as necessárias para explicar uma decisão. Remova renders e propostas "pendentes" superadas.

## 7. Git e sessões simultâneas

- Outras sessões podem estar editando a pasta ao mesmo tempo. Antes de mover, renomear ou apagar, rode `git status` e não toque em arquivos que você não criou nesta sessão sem confirmar com Elias.
- Faça `git add` só dos arquivos que você alterou, por caminho. Nunca `git add -A` às cegas.
- Mudança de estrutura (mover/renomear pastas) só com todas as outras sessões paradas.
- Ao mover arquivo usado pelo site, fichas ou ZIP, atualize os links e regenere o site no mesmo commit.

## 8. Antes de encerrar qualquer trabalho

- [ ] O resultado está na pasta do assunto, não numa pasta nova datada.
- [ ] README da área e `ESTADO_ATUAL.md` atualizados.
- [ ] Arquivos e `.md` superados removidos.
- [ ] Nenhum temporário, backup ou ferramenta deixado na pasta.
- [ ] Links verificados.

## 9. Estrutura das pastas

| Pasta | O que vai nela |
|---|---|
| `ESTADO_ATUAL.md` | Fonte única: versões vigentes, decisões, pendências, próximos passos |
| `01_Programa_e_decisoes/` | Programa, registro e painel de decisões, especificações, convenção, plano de reforma |
| `02_Modelo_3D/` | Só o `.FCStd` vigente, suas conferências e componentes de ferragens |
| `03_Ambientes/<Ambiente>/` | Decisões e estudos de cada ambiente |
| `04_Moveis/Pxx/` | Cálculos e estudos de cada móvel; temas que cruzam móveis na raiz de `04_Moveis/` |
| `05_Orcamento_e_cronograma/` | Orçamento, cronograma, plano de execução |
| `06_Entregas/` | Exatamente o que foi enviado ou publicado |
| `07_Imovel/` | Visita, fotos, levantamento, dia das chaves |
| `08_Contratos_e_atraso/` | Contrato e atraso da entrega |
| `09_Referencias/` | Plantas oficiais, manuais, moodboard, referências visuais aprovadas |
| `ferramentas/` | Gerador do site, cinemática, verificadores |

Pasta nova de topo só com motivo forte; prefira encaixar numa dessas.

## 10. Verificações obrigatórias

| Quando | Comando (na raiz) | Falha significa |
|---|---|---|
| Antes de todo commit (o hook roda sozinho) | `python ferramentas/verificar_tudo.py` | Estrutura, modelo (arquivo, cores, SHA), links ou consistência quebrados |
| Depois de **qualquer** trabalho que abriu ou alterou o modelo FreeCAD | `python ferramentas/verificar_modelo/verificar_modelo.py --completo` | Objeto removido, forma inválida, expressão perdida ou **colisão nova** em relação à base |
| Depois de mudar `ferramentas/site/src` | `python -B ferramentas/site/construir.py` e os testes de `ferramentas/site` | Site ou pacote fora de sincronia |

Regras do modelo FreeCAD:
- Só mude o modelo vigente com pedido explícito de Elias. Salve pela interface gráfica: o `FreeCADCmd` perde o `GuiDocument.xml`, onde ficam as cores (o verificador rápido detecta isso).
- Nunca deixe `.FCBak`, `.FCStd1` ou cópias do modelo na pasta do projeto: o verificador reprova.
- Mudança de modelo aprovada por Elias: rode `--completo --atualizar-base`, atualize `cadPath` e `cadSHA256` em `ferramentas/site/current_release.json` e o `ESTADO_ATUAL.md` no mesmo commit. Sem essa aprovação, **não atualize a base para fazer o erro sumir**.
- Se o verificador acusar erro que você não causou, pare e avise Elias, em vez de ajustar a base.
- `git commit --no-verify` só com autorização de Elias. Em clone novo, ative o hook: `git config core.hooksPath ferramentas/hooks`.
