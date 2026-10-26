# Ferramentas

Scripts do projeto. Rode a partir da raiz do repositório (`guedala-park/`).

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
| `ferramentas/cinematica/consultar.py` | Posições de portas e gavetas sem abrir o FreeCAD | segundos |


## Triagem de geometria FreeCAD

`verificar_modelo/triar_geometria.py` roda no FreeCADCmd, lê o CAD corrente sem recalcular/salvar e grava [Triagem_geometria.json](../02_Modelo_3D/Triagem_geometria.json). Separa peças com geometria própria (`Part::Feature` e derivados) de contêineres: os últimos ficam em `agregados_invalidos`, informativos, conforme `3cdf795`. Com BOP habilitado, checa as fontes afetadas e as peças das fichas P06/P07; os grandes agregados recebem apenas a checagem básica detalhada. Pode levar vários minutos. Não altera a base de aceitação.

```powershell
$env:GP_TRIAGEM_BOP = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
& "$env:LOCALAPPDATA/Programs/FreeCAD-1.1.4/bin/freecadcmd.exe" ferramentas/verificar_modelo/triar_geometria.py
```

A variável opcional `GP_TRIAGEM_SAIDA` escolhe outro JSON. Leia a [interpretação dos resultados](../02_Modelo_3D/README.md#triagem-das-formas-inválidas--25102026), incluindo a diferença entre `isValid()`, `check()` e BOP.

**Camadas de defesa.** (1) Hook de commit (`ferramentas/hooks/pre-commit`): roda `verificar_tudo.py` (estrutura, modelo, links, tamanho, privacidade só nos arquivos do commit, consistência e afirmações) e bloqueia se houver erro. (2) Hook de push (`ferramentas/hooks/pre-push`): roda `verificar_site.py`. (3) CI (`.github/workflows/pages.yml`): roda `verificar_tudo.py --ci` e as afirmações dos commits do push **antes** de construir e publicar o site; pega quem usou `--no-verify`. Para ativar os hooks num clone novo: `git config core.hooksPath ferramentas/hooks`.

Detalhes do gerador do site: [site/README.md](site/README.md).

Revisão de espaços de 26/10/2026: o limite de 16 KB dos READMEs permanece; o índice dos aéreos teve apenas redundância e quebras de linha compactadas antes da correção.

## Espaços nos textos

`python -B ferramentas/verificar_espacos.py` examina os Markdown versionados e novos, exceto Registro de decisões, histórico e fontes brutas. Avisa sobre palavra minúscula colada a P/R/T/C com dois dígitos e número colado a palavra comum. Não altera textos; citações, código e destinos de links são preservados. Não é um corretor geral de português.

`espacos_excecoes.json` aceita exceções literais por `arquivo`, `trecho` e `motivo`; a lista começa vazia. `corrigidos` contém os arquivos que passaram limpos no disco e no Git. `verificar_tudo.py` usa `--bloquear-corrigidos`: falha apenas nesse conjunto; demais achados continuam avisos. Use `--bloquear` com caminhos explícitos para conferir uma nova revisão antes de ampliar a lista. P03 e Corte_e_formatos aguardam consolidação de trechos de outras sessões para entrar no bloqueio.

Teste: `python -B ferramentas/test_verificar_espacos.py`. Inclui detecção, nomes/códigos válidos, citações, links, exceções locais e códigos de saída dos modos aviso/bloqueio.


Análise BOP: `verificar_modelo/analisar_bop.py`; [resultado e limites](../02_Modelo_3D/README.md#análise-dos-alertas-bop--25102026). Não altera o modelo vigente.
