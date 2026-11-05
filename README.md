# Guedala Park · projeto do apartamento

**Pé-direito de projeto: cômodos 2,55 m; banheiro 2,30 m, medidas a confirmar (Elias, 01/11/2026).** Inclui escritório e circulação; substitui o cenário de 2,47 m. [Fonte e limites](01_Programa_e_decisoes/Pesquisa_pe_direito.md).

Projeto de interiores e marcenaria do apartamento. **Para entender o projeto, comece pelo [Estado atual](ESTADO_ATUAL.md).** Para continuar uma sessão, use a [retomada curta T09](ESTADO_ATUAL.md#como-trabalhar-nesta-pasta): versões, cinco decisões recentes, responsáveis, próximo passo e verificações comprovadas.

**[Abrir o site interativo →](https://queiroz-labs.github.io/guedala-park/)** · **[Baixar o pacote para o montador ↓](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R32.zip)**

## Continuar em outra máquina

Guia de retomada conferido em 05/11/2026. **Clone o repositório inteiro**, não apenas o pacote do montador. O Git contém CAD R55, fontes editáveis, pranchas/PDFs, cotações, histórico, scripts e regras. Leia `AGENTS.md`, depois `ESTADO_ATUAL.md`; a conversa não é necessária para recuperar o estado registrado.

No PowerShell, com Git e Python 3.12 disponíveis:

```powershell
git clone https://github.com/queiroz-labs/guedala-park.git
cd guedala-park
git config core.hooksPath ferramentas/hooks
git status
python -m venv ../guedala-ambiente
& ../guedala-ambiente/Scripts/python.exe -m pip install -r ferramentas/requisitos_retomada.txt
$env:PATH = (Resolve-Path ../guedala-ambiente/Scripts).Path + ';' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B ferramentas/verificar_tudo.py --ci
```

O ambiente fica fora do repositório. Em Linux/macOS, use `../guedala-ambiente/bin/python` e `source ../guedala-ambiente/bin/activate`. Na próxima sessão, reative o ambiente antes dos hooks. Para editar CAD, instale FreeCAD e abra o arquivo indicado no [README do modelo](02_Modelo_3D/README.md); não dependa de atalhos ou caminhos da máquina anterior. Não regenere CAD ou sua base para instalar o ambiente.

**Site, se for trabalhar nele:** Node/npm são necessários. As dependências JavaScript também podem ficar fora da pasta do projeto:

```powershell
New-Item -ItemType Directory -Force ../guedala-web | Out-Null
Copy-Item ferramentas/site/package.json,ferramentas/site/package-lock.json ../guedala-web/
npm ci --prefix ../guedala-web --ignore-scripts
$env:NODE_PATH = (Resolve-Path ../guedala-web/node_modules).Path
python -B ferramentas/verificar_site.py
```

Os caminhos `guedala-ambiente`/`guedala-web` são locais e não devem ser commitados. Poppler é opcional para renderizar e revisar PDFs; os PDFs emitidos já estão no Git. Scripts de estudos especializados podem exigir bibliotecas adicionais indicadas no README de cada área; esta instalação cobre verificadores, site e pacote do arquiteto.

**Pacotes:** a [cotação](06_Entregas/Cotacao/README.md) e o [PDF do arquiteto](06_Entregas/Arquiteto/Caderno_arquiteto.pdf) estão versionados. O ZIP externo do arquiteto pode ser recriado sem abrir CAD nem regenerar PDF, a partir das 21 fontes e hashes do manifesto:

```powershell
python -B ferramentas/estudos/pacote_arquiteto.py --somente-zip --zip ../outputs/Arquiteto/Guedala_Park_Arquiteto.zip
```

Use destino inexistente. Finais de linha LF/CRLF do checkout são conciliados somente quando reproduzem o hash e tamanho emitidos. O conteúdo emitido é preservado; o contêiner ZIP e suas instruções podem ter hash diferente. Se uma fonte divergir, o comando para: revisar a emissão, não ignorar a diferença. O site/pacote do montador é reconstruído pelo CI a partir das fontes versionadas.

**Não transferidos pelo Git público:** `guedala-pessoal`, documentos personalizados de fornecedores excluídos por privacidade, vídeos brutos, programas instalados, credenciais, caches e saídas temporárias. Vídeos têm relatórios/fotos selecionadas no projeto; pacotes antigos ignorados não são dependência da retomada. Se precisar dos originais ou dados privados, transfira-os por meio privado separado. Não adicionar essas pastas ao Git.

**Ponto de retomada:** materiais e luz revistos; orçamento consolidado; pacote do arquiteto emitido; [16 tarefas de uso/manutenção](03_Ambientes/README.md#revisão-de-uso-e-manutenção--04112026). Cotação ainda não enviada; medidas reais, produtos e RT seguem pendentes. A planilha financeira R43 é histórica: usar a abertura do consolidado indicado no estado atual.

## Como a pasta está organizada

| Pasta | Conteúdo |
|---|---|
| [ESTADO_ATUAL.md](ESTADO_ATUAL.md) | Versões vigentes, decisões, pendências e próximos passos |
| [01_Programa_e_decisoes](01_Programa_e_decisoes) | Programa, registro de decisões, especificações, convenção, plano de reforma |
| [02_Modelo_3D](02_Modelo_3D) | Modelo FreeCAD vigente (R55), conferências e componentes de ferragens |
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
| Abrir ou editar o projeto no FreeCAD | [Modelo R55 completo (.FCStd)](02_Modelo_3D/Guedala_Park_R55_Berlin.FCStd) · [correções e conferências](02_Modelo_3D/README.md) · salvamento otimizado |
| Ver medidas, espessuras, acabamentos e ferragens | [Fichas dos 20 móveis · R15](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/index.html) |
| Consultar furações e suas referências | [Escolher o móvel e abrir “Furação” na ficha](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/index.html) |
| Consultar distâncias entre paredes | [Planta cotada](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Planta_cotada/index.html) |
| **Entender o projeto em uma página** | [Estado atual](ESTADO_ATUAL.md) |
| Ler o que cada ambiente precisa ter | [Programa de necessidades R01](01_Programa_e_decisoes/Programa_de_necessidades.md) · [planta mobiliada R02](03_Ambientes/Planta_mobiliada/README.md) |
| Consultar marcas, modelos e acabamentos | [Caderno de especificações R01](01_Programa_e_decisoes/Caderno_de_especificacoes.md) |
| Preparar a aprovação da reforma no condomínio | [Rascunho do plano de reforma](01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md) |
| Perguntas para oficina, RT e fornecedor | [Perguntas](04_Moveis/Perguntas_para_oficina.md) · execução pendente |
| Pedir orçamento de marcenaria | [Pacote de cotação R01](05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md) |
| Ver tomadas, luzes, água e gás previstos | [Planta de pontos preliminar](03_Ambientes/Planta_pontos/README.md) |
| Preparar o dia da entrega das chaves | [Roteiro do dia das chaves](07_Imovel/Roteiro_dia_das_chaves_R01.md) |
| Ver o cronograma da obra e o que comprar antes | [Cronograma](05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) |
| Imprimir as pranchas (A3) | [Caderno de pranchas R02 (PDF)](06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R02.pdf) |
| Escolher luminárias | [Lista curta](03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md) |
| Ver luminárias nos ambientes | [Simulações CB02](https://queiroz-labs.github.io/guedala-park/docs/09_Referencias/Iluminacao_CB02/Galeria.md.html) · [quarto smart, custo e condições de uso](03_Ambientes/Iluminacao/Fechamento_custo_beneficio/Revisao_quarto_CB02.md) |
| Ver o que falta para virar projeto oficial | [Roteiro para projeto oficial](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md) |
| Conferir o que falta resolver | [Pendências de projeto, oficina e apartamento](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/Pendencias.html) |
| Continuar antes de receber o apartamento | [Avanços, resultados e pendências sem medidas reais](04_Moveis/Proximas_decisoes/README.md) |
| Anotar as medidas reais do apartamento | [Folha de levantamento por móvel](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Fichas_fabricacao/Levantamento.html) |
| Conferir os acabamentos definidos | [Um padrão por chapa física; interiores separados quando detalhados](https://queiroz-labs.github.io/guedala-park/docs/ferramentas/site/fabrication/Decisao_acabamentos_R13.md.html) |
| Consultar a planta de origem | [Planta oficial em PDF](https://queiroz-labs.github.io/guedala-park/docs/09_Referencias/Plantas_e_manuais/Planta_oficial.pdf) |

## Para encaminhar ao montador

1. Baixe o **[pacote ZIP](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R32.zip)** e envie como arquivo ou compartilhe este link.
2. Extraia o ZIP inteiro e abra **COMECE_AQUI.html** no navegador. Ele funciona como menu da pasta.
3. Para editar o modelo, abra **02_Modelo_3D/Guedala_Park_R55_Berlin.FCStd** pelo menu **Arquivo → Abrir** do FreeCAD. Fichas, planta e tabelas abrem sem o FreeCAD.

**Revisões:** R30 identifica o pacote, R55 o modelo, R15 as fichas e R16 a aparência. Furos, forma comercial da FGVTN 500 e a piano do banco continuam fora da geometria; produtos, juntas e protótipos ainda condicionam a execução. As cores são aproximações visuais.

As fichas distinguem medidas nominais, decisões técnicas, verificações na oficina e medidas a levantar no apartamento. Consulte as pendências antes de cortar ou furar; o pacote não é liberação integral de fabricação.

Revisão local27/10: **FreeCAD R53, fichas R15 e pacote R25** incorporam as decisões P02/P13/TV/lixeiras. [Integração e limites](02_Modelo_3D/README.md). R53/R25 publicado com autorização de Elias em 27/10/2026; alturas, PDF e ZIP conferidos, evidência registrada em [Entregas](06_Entregas/README.md).
