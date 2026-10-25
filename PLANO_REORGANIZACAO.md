# Plano de reorganização (temporário)

Status: **planejado, nada foi movido.** Executar só quando nenhuma outra sessão estiver trabalhando na pasta. Apagar este arquivo depois de executado.

Decisões já tomadas por Elias (25/10/2026):
- Reorganizar tudo, inclusive os caminhos que o site e o ZIP usam (atualizar os links).
- Estudo superado sai da pasta; fica recuperável só pelo histórico do git. Nada vai para "arquivo morto" visível.
- Regras permanentes em [AGENTS.md](AGENTS.md).

## Situação de partida (25/10)

- ~19.300 arquivos, 7 GB. Só o necessário ao projeto é uma fração disso.
- `01_Projeto` tem ~95 itens: pastas por sessão (`Compatibilizacao_2026-09-28` … `_10-08`), por revisão de modelo (R45 a R52, cada uma com cópia do .FCStd de ~23–60 MB) e por cálculo de móvel (P01_…, P15_…).
- Várias "páginas de entrada" competindo: `README.md`, `Estado_atual.md`, `Retomada_25_10_2026.md`, `Resumo.md`, `Painel_de_decisoes.md`, `Plano_execucao_ate_31_10_2026.md`, `Continuidade_pre_entrega_2026-10-23.md`, `Execucao_ate_07h_2026-10-25.md`.
- 585 arquivos `.md` fora de `tmp`/`.site`.
- Ferramentas misturadas ao projeto: `tmp/` (2 GB), `outputs/`, venv Python, `node_modules`, código-fonte do FreeCAD MCP.

## Estrutura alvo

```
guedala-park/
  AGENTS.md                 regras (CLAUDE.md só importa este)
  README.md                 menu curto para pessoas
  ESTADO_ATUAL.md           única fonte de verdade: versões vigentes, pendências, próximos passos
  01_Programa_e_decisoes/   programa, registro de decisões, especificações, convenção/memorial Cury, plano de reforma NBR 16280
  02_Modelo_3D/             SÓ o .FCStd vigente + README (como abrir, o que mudou na última revisão)
  03_Ambientes/             Cozinha, Banheiro, Lavanderia, Sala_e_jantar, Escritorio, Quarto, Iluminacao
                            cada um com README.md = decisão vigente daquele ambiente
  04_Moveis/                P01 … P20: uma pasta por móvel com README.md (estado, cálculos, ferragens, pendências)
                            + dados/ (JSON/CSV dos cálculos)
  05_Orcamento_e_cronograma/
  06_Entregas/              o que foi enviado/publicado (fichas, planta cotada, pranchas, ZIP), uma versão por item
  07_Imovel/                visita, fotos, levantamento de medidas, roteiro das chaves
  08_Contratos_e_atraso/
  09_Referencias/           plantas oficiais, manuais de aparelhos, moodboard, renders aprovados
  ferramentas/              gerador do site (Estudo_interativo/src), scripts Python, verificador de consistência
```

`.site/` continua como saída gerada do site (não editar à mão). Pastas fora do repositório (`../tmp`, `../outputs`, `../.firecrawl`, `../mt.txt`, `../debug.log`, `../freecad_estado.json`) são limpas ou movidas para fora da pasta do projeto.

## Fase 0 — preparação

1. Confirmar com `git status` que nenhuma outra sessão tem trabalho em andamento; pedir a Elias para pausar as outras sessões.
2. Commit de segurança com tudo o que está pendente hoje (68 alterações, incluindo as pastas de 25/10), e tag `antes-reorganizacao`. É por essa tag que qualquer arquivo removido volta.
3. Conferir que o push para o GitHub funciona (senão o histórico só existe neste computador).

## Fase 1 — entradas únicas (maior ganho para a IA)

Fundir em `ESTADO_ATUAL.md` o que ainda vale de:
`Estado_atual.md`, `Retomada_25_10_2026.md`, `Resumo.md`, `Painel_de_decisoes.md`, `Plano_execucao_ate_31_10_2026.md`, `Continuidade_pre_entrega_2026-10-23.md`, `Roteiro_para_projeto_oficial.md`.

Remover (o conteúdo é histórico ou já está fundido): `Resumo_historico_ate_R28.md`, `Painel_de_decisoes_historico_ate_R28.md`, `Execucao_ate_07h_2026-10-25.md`, `Organizacao_no_Notion.md`, `Revisao_piso_e_armarios_2026-09-25.md`, `Fechamento_cozinha_lavanderia_2026-09-27.md`, `Verificacao_consistencia.md` (é gerado), `INDICE_DE_ARQUIVOS.md` (a estrutura passa a se explicar sozinha).

O `README.md` raiz encolhe para o menu de pessoas, sem o histórico R46→R52 no topo (isso fica no git log e no README do modelo).

## Fase 2 — modelo 3D

- Manter só `Correcao_integral_R52_2026-10-25/Guedala_Park_R52_Corrigido.FCStd` → `02_Modelo_3D/Guedala_Park_R52.FCStd`.
- O que ainda vale dos READMEs das revisões (R45 consolidação, R46 fichas no CAD, R48, R49, R50 otimização, R51 sem tubos, R52) vira uma seção "O que o modelo contém" no README do modelo.
- Remover: `Modelo_FreeCAD/` (657 MB de modelos antigos), `Modelo_leve_R49`, `Otimizacao_FreeCAD_R50`, `Revisao_sem_tubos_R51`, `Gavetas_escritorio_R49`, `Depurador_sem_canal_R48`, `Fichas_no_CAD_R46`, `Cores_FreeCAD_R16`, `Consolidacao_R45`, `Estudo_dimensional_R45`.
- **Atenção:** o site, o ZIP R16 e o `Abrir_no_FreeCAD.ps1` apontam para a R49. Ou se publica a R52 junto, ou se guarda a R49 em `06_Entregas/` como "versão publicada". Decidir antes de executar.

## Fase 3 — cálculos por móvel (P01 … P20)

Agrupar em `04_Moveis/Pxx/`, um README por móvel com o estado vigente e as condições abertas (a matriz de `Cargas_e_ligacoes_R50_2026-10-25/Andamento_20_moveis.md` vira o índice de `04_Moveis/README.md`):

| Origem | Destino |
|---|---|
| `P01_apoios_ao_piso`, `P01_massas_equilibrio`, `P01_P03_caminho_superior` | `04_Moveis/P01` (e P03) |
| `P04_P15_suspensao`, `P15_composicao_parcial` | `P04`, `P15` |
| `Calculo_P11`, `Reforco_P11`, `P11_ligacoes_sem_tubos` | `P11` (só o resultado sem tubos; versões com tubo foram canceladas por Elias) |
| `P14_reacoes_e_operacao`, `Banco_cesto_simples`, `Ferragens_banco_R46`, `Southco_banco_R47` | `P14`/`P20` (banco e cesto) |
| `P16_gavetas_estabilidade`, `P16_interface_guia_fundo` | `P16` |
| `P17_base_fundo_ligacoes`, `Aereos_suspensao_P09_P11_P12_P17` | `P17`, `P09`, `P12` |
| `P20_assento_fechado` | `P20` |
| `Bancada_marcenaria`, `Solucoes_marcenaria_sem_tubos`, `Mapa_conectores_R00` | móveis correspondentes + `04_Moveis/README.md` (critérios gerais) |
| `Cargas_e_ligacoes_R50`, `Plano_cargas_e_ligacoes`, `Quantitativos_estudos` | `04_Moveis/README.md` + `dados/` |
| `Cinematica_offline` | `ferramentas/cinematica/` |

## Fase 4 — ambientes

- Cada pasta de ambiente fica só com a decisão vigente. Ex.: `Cozinha/` tem hoje ~40 arquivos datados (`_2026-09-25`, `_R00`…`_R03`); vira um `README.md` com layout, aparelhos, gavetas e organização interna vigentes, mais as imagens aprovadas.
- Remover depois de extrair o que vale: `Compatibilizacao_2026-09-28` … `_10-08` (7 pastas), `Avanco_pendencias_2026-10-21`, `Auditoria_*`, `Caderno_visual_2026-10-12`, `Detalhamento_construtivo_R30`, `Estudos_interativos_2026-09-27`, `Estudo_Berlin_FGVTN` (se a decisão FGVTN 500 já está registrada), `Conferencia_torneiras`, `Conferencia_entrega_25_10_2026`, `Pesquisa_comparativa_Cury` (fica o resumo em `09_Referencias`).
- `Orcamento_R30` sai; `Orcamento_R43` + `Complemento_orcamento_vigente_R41.md` + `Cronograma_obra_e_compras_R00.md` → `05_Orcamento_e_cronograma/`.
- `03_Referencias`: manter só imagens aprovadas (`*_referencia_aprovada_*`, moodboard R01); remover `*_pendente.png` e propostas R01/R02 superadas pela R03.

## Fase 5 — entregas e site

- `05_Entregas/Fichas_fabricacao_R13` (conteúdo R14) → `06_Entregas/Fichas_fabricacao/`; `Compartilhar_R14` sai (o R16 já é o alias); `Compartilhar_R16` → `06_Entregas/Pacote_montador/`.
- Atualizar `ferramentas/` (geradores, `pages.yml`, `construir.py`, links internos) para os novos caminhos e regenerar `.site`.
- Links já enviados a outras pessoas (ZIP R16, fichas) vão quebrar: deixar páginas de redirecionamento nos endereços antigos do site (GitHub Pages não faz redirecionamento sozinho) e avisar o montador do link novo.

## Fase 6 — limpeza fora do projeto

- Remover `99_Arquivo/` inteiro (636 MB) — o conteúdo fica na tag `antes-reorganizacao`.
- Remover `guedala-park/tmp/`, `../tmp/` (2 GB; manter fora da pasta do projeto só o que o FreeCAD MCP usa, conferindo antes com a memória de configuração), `../outputs/`, `__pycache__`, `node_modules`.
- Worktrees antigos (`codex/documentacao-cozinha`, `codex/pages-r03`) apontam para `C:/Users/Elias/Documents/guedala-park/tmp/...`: `git worktree prune` se não existirem mais.
- `guedala-pessoal/` fica como está (dados pessoais, fora do site).

## Fase 7 — verificação

- Verificador de links quebrados em todos os `.md` e no `.site` gerado.
- `verificar_consistencia.py` passa.
- Site abre localmente; ZIP novo extrai e o `COMECE_AQUI.html` funciona.
- Contagem final de arquivos e tamanho, comparada com a de partida.
- Commit único "Reorganiza projeto" (mais commits por fase, se ficar grande) e push.
