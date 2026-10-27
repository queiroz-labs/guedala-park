# Guedala Park · projeto do apartamento

**Pé-direito de projeto: cômodos 2,60 m; banheiro 2,50 m, medidas a confirmar (Elias, 27/10/2026).** Inclui escritório e circulação; substitui o cenário de 2,47 m. [Fonte e limites](01_Programa_e_decisoes/Pesquisa_pe_direito.md).

Projeto de interiores e marcenaria do apartamento. **Para entender o projeto, comece pelo [Estado atual](ESTADO_ATUAL.md).** Para continuar uma sessão, use a [retomada curta T09](ESTADO_ATUAL.md#como-trabalhar-nesta-pasta): versões, cinco decisões recentes, responsáveis, próximo passo e verificações comprovadas.

**[Abrir o site interativo →](https://queiroz-labs.github.io/guedala-park/)** · **[Baixar o pacote para o montador ↓](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R23.zip)**

## Como a pasta está organizada

| Pasta | Conteúdo |
|---|---|
| [ESTADO_ATUAL.md](ESTADO_ATUAL.md) | Versões vigentes, decisões, pendências e próximos passos |
| [01_Programa_e_decisoes](01_Programa_e_decisoes) | Programa, registro de decisões, especificações, convenção, plano de reforma |
| [02_Modelo_3D](02_Modelo_3D) | Modelo FreeCAD vigente (R52), conferências e componentes de ferragens |
| [03_Ambientes](03_Ambientes) | Cozinha, banheiro, lavanderia, sala, escritório, quarto, iluminação, plantas |
| [04_Moveis](04_Moveis/README.md) | Cálculos e estudos por móvel (P01…P20), cargas, ligações, inventário dimensional |
| [05_Orcamento_e_cronograma](05_Orcamento_e_cronograma) | Orçamento, cronograma e plano de execução |
| [06_Entregas](06_Entregas/README.md) | O que foi entregue ou publicado: fichas, planta cotada, pranchas, pacote |
| [07_Imovel](07_Imovel/README.md) | Visita, fotos, roteiro do dia das chaves |
| [08_Contratos_e_atraso](08_Contratos_e_atraso) | Contrato e pesquisa sobre atraso |
| [09_Referencias](09_Referencias/README.md) | Plantas oficiais, manuais, moodboard, referências visuais |
| [ferramentas](ferramentas) | Gerador do site, cinemática e verificador de consistência |

Regras para manter a organização: [AGENTS.md](AGENTS.md). Commite cedo, um assunto por commit, adicionando arquivos por caminho; atualize o README da área e o estado atual juntos. Antes do commit, execute `python ferramentas/verificar_tudo.py` e o hook; antes do push, valide com `python ferramentas/verificar_tudo.py --ci` em clone limpo criado por `git clone --local`. Versões antigas estão no histórico do git (tag `antes-reorganizacao`).

## Menu do projeto

| Quero… | Acessar |
|---|---|
| **Executar as prioridades até 31/10** | [Plano de execução até 31/10](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md) |
| Explorar o apartamento e os móveis em 3D | [Site interativo](https://queiroz-labs.github.io/guedala-park/) |
| Abrir ou editar o projeto no FreeCAD | [Modelo R53 completo (.FCStd)](02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd) · [correções e conferências](02_Modelo_3D/README.md) · salvamento otimizado |
| Ver medidas, espessuras, acabamentos e ferragens | [Fichas dos 20 móveis · R14](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/index.html) |
| Consultar furações e suas referências | [Escolher o móvel e abrir “Furação” na ficha](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/index.html) |
| Consultar distâncias entre paredes | [Planta cotada](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Planta_cotada/index.html) |
| **Entender o projeto em uma página** | [Estado atual](ESTADO_ATUAL.md) |
| Ler o que cada ambiente precisa ter | [Programa de necessidades R01](01_Programa_e_decisoes/Programa_de_necessidades.md) · [planta mobiliada R02](03_Ambientes/Planta_mobiliada/README.md) |
| Consultar marcas, modelos e acabamentos | [Caderno de especificações R01](01_Programa_e_decisoes/Caderno_de_especificacoes.md) |
| Preparar a aprovação da reforma no condomínio | [Rascunho do plano de reforma](01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md) |
| Pedir orçamento de marcenaria | [Pacote de cotação R01](05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md) |
| Ver tomadas, luzes, água e gás previstos | [Planta de pontos preliminar](03_Ambientes/Planta_pontos/README.md) |
| Preparar o dia da entrega das chaves | [Roteiro do dia das chaves](07_Imovel/Roteiro_dia_das_chaves_R01.md) |
| Ver o cronograma da obra e o que comprar antes | [Cronograma](05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) |
| Imprimir as pranchas (A3) | [Caderno de pranchas R00 (PDF)](06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R00.pdf) |
| Escolher luminárias | [Lista curta](03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md) |
| Ver luminárias nos ambientes | [Simulações CB02](https://queiroz-labs.github.io/guedala-park/docs/09_Referencias/Iluminacao_CB02/Galeria.md.html) · [quarto smart, custo e condições de uso](03_Ambientes/Iluminacao/Fechamento_custo_beneficio/Revisao_quarto_CB02.md) |
| Ver o que falta para virar projeto oficial | [Roteiro para projeto oficial](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md) |
| Conferir o que falta resolver | [Pendências de projeto, oficina e apartamento](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/Pendencias.html) |
| Continuar antes de receber o apartamento | [Avanços, resultados e pendências sem medidas reais](04_Moveis/Proximas_decisoes/README.md) |
| Anotar as medidas reais do apartamento | [Folha de levantamento por móvel](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/Levantamento.html) |
| Conferir os acabamentos definidos | [Um padrão por chapa física; interiores separados quando detalhados](https://queiroz-labs.github.io/guedala-park/docs/ferramentas/site/fabrication/Decisao_acabamentos_R13.md.html) |
| Consultar a planta de origem | [Planta oficial em PDF](https://queiroz-labs.github.io/guedala-park/docs/09_Referencias/Plantas_e_manuais/Planta_oficial.pdf) |

## Para encaminhar ao montador

1. Baixe o **[pacote ZIP](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R23.zip)** e envie como arquivo ou compartilhe este link.
2. Extraia o ZIP inteiro e abra **COMECE_AQUI.html** no navegador. Ele funciona como menu da pasta.
3. Para editar o modelo, abra **02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd** pelo menu **Arquivo → Abrir** do FreeCAD. Fichas, planta e tabelas abrem sem o FreeCAD.

**Revisões:** R23 identifica o pacote, R52 o modelo, R14 as fichas e R16 a aparência. Furos, forma comercial da FGVTN 500 e a piano do banco continuam fora da geometria; produtos, juntas e protótipos ainda condicionam a execução. As cores são aproximações visuais.

As fichas distinguem medidas nominais, decisões técnicas, verificações na oficina e medidas a levantar no apartamento. Consulte as pendências antes de cortar ou furar; o pacote não é liberação integral de fabricação.

Revisão local27/10: **FreeCAD R53, fichas R15 e pacote R25** incorporam as decisões P02/P13/TV/lixeiras. [Integração e limites](02_Modelo_3D/README.md). Publicação R53/R25 autorizada por Elias em 27/10/2026; conferência remota registrada em [Entregas](06_Entregas/README.md).
