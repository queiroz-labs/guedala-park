# Regras do projeto Guedala Park

Valem para qualquer pessoa ou IA (Claude, Codex…) que trabalhe nesta pasta. Seguir sempre, sem precisar pedir.

Enquanto a reorganização descrita em [PLANO_REORGANIZACAO.md](PLANO_REORGANIZACAO.md) não for executada, as pastas ainda estão na estrutura antiga: aplique estas regras a tudo o que for **novo** e não crie mais pastas no padrão antigo.

## 1. Comece pela fonte de verdade

- Leia primeiro `ESTADO_ATUAL.md` (hoje: `01_Projeto/Estado_atual.md`). Ele diz qual versão vale de cada coisa.
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

- Scripts do projeto ficam em `ferramentas/` (hoje: `01_Projeto/Estudo_interativo` e scripts soltos). Não deixe `.py`/`.cjs` de uso único espalhados pelas pastas de conteúdo.
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
