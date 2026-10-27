# Ferramentas

Scripts do projeto. Rode a partir da raiz do repositório (`guedala-park/`).

O verificador bloqueia pastas datadas fora de `06_Entregas/` e `02_Modelo_3D/Historico/`, inclusive em Componentes e no site. Teste de regressão em 27/10/2026: três pastas temporárias com arquivo (Componentes, site e Inventario_dimensional) reprovaram com saída 1; removidas, a verificação passou. Não há exceção ampla para Componentes ou site.

Na raiz de `ferramentas/` só ficam `verificar_*.py` e `test_*.py`; scripts de estudo vão para `ferramentas/estudos/` ou para a pasta do tema (o `verificar_tudo.py` reprova script novo solto).

Pacote de cotação: `python -B ferramentas/estudos/gerar_pedidos_cotacao.py` gera as páginas por destinatário, checklist e ZIP com fichas R15; não envia mensagens nem altera CAD.

| Comando | O que faz | Tempo |
|---|---|---|
| `python -B ferramentas/aereos/preparar_ensaios_p04.py` | Pacote PDF de quatro páginas, cinco retalhos T0/oito Minifix e 15 registros vazios; ReportLab/NumPy no Python embutido, sem ensaio físico | segundos |
| `python -B ferramentas/aereos/conferir_ensaios_p04.py` | Confere recorte, sequência por eixos, campos vazios, fontes e páginas PDF; NumPy/pypdf, sem abrir CAD | segundos |
| `python -B ferramentas/aereos/validar_p04.py` | Quatro acessos SW4 curta, calços R52, implantação candidata e 765 equilíbrios 3D/1530 vetores; gera desenho/casos para qualificação, sem ensaio físico | segundos |
| `python -B ferramentas/aereos/conferir_p04.py` | Confere envelopes contínuos/controles negativos e equilíbrio independente, sem abrir CAD ou demonstrar capacidade | segundos |
| `python -B ferramentas/aereos/reconciliar_lote_b.py` | P17/P04/P12: premissas respondidas, cinco geometrias, 47 contatos R00 e 16 entradas inferiores antigas; fundo inteiro separado da R52 (NumPy/Pillow) | segundos |
| `python -B ferramentas/aereos/detalhar_lote_b.py` | Metas 20/10/10 kg: 585 casos de massa/demanda e 60 Minifix de acesso interno; quatro corredores P04 restritos, sem capacidade demonstrada | segundos |
| `python -B ferramentas/aereos/conferir_lote_b.py` | Conferência independente de hashes/contatos/canecos, pinos, acesso e demandas; registra restrições, sem ensaio físico | segundos |
| `python ferramentas/verificar_tudo.py` | Roda todas as verificações rápidas abaixo de uma vez | segundos |
| `python -B ferramentas/aereos/detalhar_ligacoes.py` | Lote P09/P11/P15: 96 interfaces nominais, 696 casos/4176 vetores e 12 zonas de acesso só contra madeira; preserva R52, sem produto/usinagem/capacidade demonstrados (NumPy/Pillow) | segundos |
| `python -B ferramentas/aereos/conferir_ligacoes.py` | Confere contato positivo, rejeita ligação pela aresta, reconcilia contagens e equilíbrio independente dos 2088 pares de grupos; não é ensaio físico | segundos |
| `python -B ferramentas/aereos/selecionar_ferragem.py` | Bigfer 04.02.058 candidata: envelopes≈60 mL/par, 6 cantos e 4176 vetores na implantação proposta; sem montagem/capacidade homologadas | segundos |
| `python -B ferramentas/aereos/conferir_selecao.py` | Confere fontes/ocupação e equilíbrio independente da pré-seleção; CAD preservado, sem ensaio físico | segundos |
| `python -B ferramentas/aereos/analisar_apoio_caixa.py` | Faixas 18×60 nas laterais, 4176 reações inferiores e 8 casos de corpo de prova fundo–laterais; sem contato/resistência comprovados (NumPy/Pillow) | segundos |
| `python -B ferramentas/aereos/conferir_apoio_caixa.py` | Confere áreas nominais/equilíbrio e rejeita copiar T para C do mesmo lado ou fechar torção por uma única coluna pontual | segundos |
| `python -B ferramentas/aereos/test_fontes.py` | Regressão de hashes: LF/CRLF equivalentes só em textos; alterações de conteúdo e binários continuam detectadas | segundos |
| `python ferramentas/verificar_modelo/verificar_modelo.py` | Modelo FreeCAD: arquivo vigente, cores (GuiDocument.xml), SHA do release, backups esquecidos | segundos |
| `python ferramentas/verificar_modelo/verificar_modelo.py --completo [--relatorio]` | Abre o modelo no FreeCADCmd **sem salvar** e confere: invariantes (`invariantes.json`), nada novo fora do apartamento, aparência por objeto, **106 cenários de movimento** (`movimentos.json`), objetos removidos, formas inválidas, expressões perdidas e colisões novas. Com `--relatorio` escreve `02_Modelo_3D/Relatorio_mudanca.md`. Atualizar a base exige `--atualizar-base --aprovado-por "Elias, dd/mm: ..."` | ~8 min |
| `python ferramentas/verificar_consistencia.py` | Documentos batem entre si (datas, versões, caderno × site) | segundos |
| `python ferramentas/verificar_links.py` | Links locais quebrados nos `.md` | segundos |
| `python ferramentas/verificar_tamanho.py` | Limites de leitura: README ≤ 16 KB, `.md` ≤ 60 KB, HTML ≤ 1 MB, dados ≤ 3 MB. Os que já passavam estão congelados em `limites_base.json` (podem encolher, não crescer) | segundos |
| `python ferramentas/verificar_privacidade.py` | CPF, cartão (Luhn), chaves/tokens, senhas, chave privada e qualquer arquivo de `guedala-pessoal/`; avisa e-mail pessoal e telefone. O repositório e o site são públicos. Achados antigos revisados: `privacidade_base.json` | segundos |
| `python ferramentas/verificar_afirmacoes.py` | Nas linhas **novas** de `.md`: barra "Elias aprovou…" sem data/F-código/aspas/Registro e "liberado para fabricação" ou "capacidade aprovada" sem ressalva | segundos |
| `python ferramentas/verificar_fatos.py` | Documentos vigentes não contradizem os fatos de `fatos.json` (verba, área, 127 V, gás natural, forno, mesa, medidas-chave, revisões do release). Linhas que falam de histórico/substituição não contam | segundos |
| `python ferramentas/verificar_site.py` | Testes do site e build como o CI faz, em pasta temporária (hook de pre-push) | ~10 s |
| `python -B ferramentas/site/construir.py` | Regenera o site a partir de `ferramentas/site/src/` | segundos |
| `python -B 04_Moveis/Proximas_decisoes/Cinematica/consultar_r52.py --listar` | Consulta das folhas articuladas da fotografia R52; motor em `ferramentas/cinematica/`; não é simulador geral de gavetas/colisões | segundos |
| `python -B ferramentas/roupeiro/analisar_caixa_superior.py` | Cortes P02/P03, mapa de juntas e desenho do estudo separado (NumPy/Pillow); geometria extraída por `roupeiro/extrair_caixa_superior.py` no FreeCADCmd, sem salvar CAD | segundos |
| `python -B ferramentas/roupeiro/verificar_caixa_superior.py` | Confere certificados de equilíbrio, cortes analíticos do retorno e geometria C01/topo; não dimensiona juntas nem libera carga | segundos |
| `python -B ferramentas/roupeiro/estudar_malas.py` | Confere envelopes de duas/três malas P03, reservas de acesso e gera prancha; usa dados salvos, sem abrir FreeCAD (Pillow) | segundos |
| `python -B ferramentas/roupeiro/detalhar_portas_maleiro.py` | Detalhe nominal das folhas, quatro barras, varredura das frentes e consulta de fixação P03; não altera FreeCAD nem homologa ferragens (NumPy/Pillow) | segundos |
| `python -B ferramentas/roupeiro/avaliar_alternativa_650.py` | Compara folhas 672/650, frentes, malas, 72 cortes P03→P01 e 1038 resultantes da união adicional; gera comparação PNG/JSON, sem abrir CAD ou comprovar resistência (NumPy/Pillow) | segundos |
| `python -B ferramentas/roupeiro/avaliar_abertura_A.py` | A escolhida para desenvolvimento: corredor por ângulo, avanço da folha, 16 trajetórias de mala/envelope e demandas dos grupos com extremos 148/202; sem capacidade homologada ou alteração do CAD | segundos |
| `python -B ferramentas/roupeiro/avaliar_dobradicas_A.py` | Seleção candidata 6 dobradiças/6 calços/6 limitadores, centros de canecos/calços, afastamentos nominais e demandas; sem pilotos, capacidade de fixação ou usinagem aprovados | segundos |
| `python -B ferramentas/roupeiro/especificar_chapa_P03.py` | MDFBP Greenplac 18/Arenza nas duas faces P03; duas pecas 18+15 podem ter cores distintas; SKU e capacidade de fixação pendentes, sem abrir CAD | segundos |
| `python -B ferramentas/roupeiro/calcular_caixa_P03.py` | Cascas/juntas/apoios reduzidos P03-P01: 29 configurações, 464 casos 20 kg, comparação 18/25 e rigidezes hipotéticas; não demonstra capacidade física (NumPy) | ~2 min |
| `python -B ferramentas/roupeiro/conferir_caixa_P03.py` | Equilíbrio, contatos, massas, malha e CSV; registra encontro traseiro e conflito da longarina com reservas P01, gera síntese PNG; sem abrir CAD (Pillow) | segundos |
| `python -B ferramentas/roupeiro/ligar_P02_P03.py` | P02/P03 e P01 com cascas/juntas/contatos; 18 configurações/1728 casos, C01 e caminho da divisória ao piso; rigidezes hipotéticas, sem capacidade física ou alteração CAD (NumPy; BLAS1 por padrão) | ~4 min |
| `python -B ferramentas/roupeiro/conferir_ligacao_P02_P03.py` | Confere cortes P02/divisória, CSV, malha e área/CG da chapa L; gera desenho da ligação/caminho nominal e síntese JSON (Pillow) | segundos |
| `python -B ferramentas/corte/reconciliar_acabamentos.py` | Reagrupa 249 peças conforme regra por chapa física; 215 no ensaio/34 excluídas, reconcilia auditoria 248 e P13 pendente, gera dados/SVG e roda conferência de margens/serra/IDs; sem alterar CAD/fichas/custos | segundos |

| `python -B ferramentas/roupeiro/padronizar_acabamentos.py` | Regra por chapa física, auditoria por ID e fontes documentais; permite cores diferentes em duas peças 18+15 identificadas, sem criar geometria | segundos |

## Triagem de geometria FreeCAD

`verificar_modelo/triar_geometria.py` roda no FreeCADCmd, lê o CAD corrente sem recalcular/salvar e grava [Triagem_geometria.json](../02_Modelo_3D/Triagem_geometria.json). Separa peças com geometria própria (`Part::Feature` e derivados) de contêineres: os últimos ficam em `agregados_invalidos`, informativos, conforme `3cdf795`. Com BOP habilitado, checa as fontes afetadas e as peças das fichas P06/P07; os grandes agregados recebem apenas a checagem básica detalhada. Pode levar vários minutos. Não altera a base de aceitação.

```powershell
$env:GP_TRIAGEM_BOP = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
& "$env:LOCALAPPDATA/Programs/FreeCAD-1.1.4/bin/freecadcmd.exe" ferramentas/verificar_modelo/triar_geometria.py
```

O aprofundamento `verificar_modelo/analisar_bop.py` usa o mesmo FreeCADCmd e grava [Analise_bop.json](../02_Modelo_3D/Analise_bop.json), com pcurvas amostradas, testes de cópias, cortes de controle e comparação ao estudo R02. Não analisa os STEPs recebidos. `GP_BOP_SAIDA` permite outro destino.

A variável opcional `GP_TRIAGEM_SAIDA` escolhe outro JSON. Leia a [interpretação dos resultados](../02_Modelo_3D/README.md#triagem-das-formas-inválidas--25102026), incluindo a diferença entre `isValid()`, `check()` e BOP.

**Camadas de defesa.** (1) Hook de commit (`ferramentas/hooks/pre-commit`): roda `verificar_tudo.py` (estrutura, modelo, links, tamanho, privacidade só nos arquivos do commit, consistência e afirmações) e bloqueia se houver erro. (2) Hook de push (`ferramentas/hooks/pre-push`): roda `verificar_site.py`. (3) CI (`.github/workflows/pages.yml`): roda `verificar_tudo.py --ci` e as afirmações dos commits do push **antes** de construir e publicar o site; pega quem usou `--no-verify`. Para ativar os hooks num clone novo: `git config core.hooksPath ferramentas/hooks`.

Detalhes do gerador do site: [site/README.md](site/README.md).

Revisão de espaços de 26/10/2026: o limite de 16 KB dos READMEs permanece; o índice dos aéreos teve apenas redundância e quebras de linha compactadas antes da correção.

## Espaços nos textos

`python -B ferramentas/verificar_espacos.py` examina os Markdown versionados e novos, exceto Registro de decisões, histórico e fontes brutas. Avisa sobre palavra minúscula colada a P/R/T/C com dois dígitos e número colado a palavra comum. Não altera textos; citações, código e destinos de links são preservados. Não é um corretor geral de português.

`espacos_excecoes.json` aceita exceções literais por `arquivo`, `trecho` e `motivo`; a lista começa vazia. `corrigidos` contém os arquivos que passaram limpos no disco e no Git. `verificar_tudo.py` usa `--bloquear-corrigidos`: falha apenas nesse conjunto; demais achados continuam avisos. Use `--bloquear` com caminhos explícitos para conferir uma nova revisão antes de ampliar a lista. P03 e Corte_e_formatos aguardam consolidação de trechos de outras sessões para entrar no bloqueio.

Teste: `python -B ferramentas/test_verificar_espacos.py`. Inclui detecção, nomes/códigos válidos, citações, links, exceções locais e códigos de saída dos modos aviso/bloqueio.


Análise BOP: `verificar_modelo/analisar_bop.py`; [resultado e limites](../02_Modelo_3D/README.md#análise-dos-alertas-bop--25102026). Não altera o modelo vigente.


Estudos P01/P02/P03: scripts em `roupeiro/`, com geometria extraída, conferências e hipóteses; [escopo vigente](../04_Moveis/P03/README.md). Os cálculos não substituem ensaio de juntas.

`consolidar_matriz.py` atualiza somente o controle CSV/Markdown: agenda 27/10 inclui kit P20/P14 e perguntas P02/P13; sem recalcular equilíbrio, gerar furação ou abrir CAD. [Matriz vigente](../04_Moveis/Cargas_e_ligacoes/README.md).

R53: `estudos/integrar_decisoes_r53.py` aplica somente decisões 27/10 na GUI sobre R52; `site/exportar_cad.py` extrai o CAD vigente para fichas/site sem salvar. Verificação completa e relatório obrigatórios.

`verificar_site.py` valida R24 como artefato local quando `publicationStatus=local_only`; não altera autorização. Teste específico mantém bloqueio de `--publication-ready` sem autorização.

[Recálculo de medidas](medidas/README.md): dependências R53, cenários isolados e reprodução obrigatória no verificador geral.
