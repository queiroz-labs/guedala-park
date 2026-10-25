# Pendências e avanços depois da R52

25/10/2026. Trabalho realizado sem medidas reais do apartamento. **A R52 permanece intacta**; os cálculos e a alternativa do micro ficam separados. As fichas receberam a correção textual da composiçãoP20. A publicação corrente R52/R18 foi autorizada; o pacoteR17 anterior permanece selado. [Estado do envio e conferência remota](../Estado_atual.md).

## O que avançou agora

| Frente | Entrega concreta | O que este resultado fecha |
|---|---|---|
| Caixa superior P01/P03 | [54 cenários, interfaces BREP e12 equilíbrios por painel](P01_P03/README.md) | Pesos próprios de topo/fundo/laterais/portas separados; forças/momentos compartilhados na travessa e no fundo. Identificado também contato traseiro324mm² sob uma lateral. Não é cálculo de flecha ou resistência. |
| Corte e formato | [249 painéis atuais e36 propostas triados; arranjos de210 painéis](Corte_e_formatos/README.md) | Requisito útil do fundoP01 e orientação corretos, margem/refilo e exclusões por peça.39 painéis ainda sem definição suficiente para este arranjo. Não é compra ou plano executivo. |
| Micro-ondas | [Alternativa FreeCAD separada para300mm superiores](Instalacao_e_P16/README.md) | Apoio/aparelho200mm mais baixos cabem nominalmente sem cortar o aéreoB. A posição F104 com100mm continua na R52; a alternativa não foi adotada. |
| Ferramenta de cálculo | [Fotografia e consulta offline da própria R52](Cinematica_R52/README.md) |4 planilhas/867 células/24 folhas extraídas;66 poses nativas R52 e528 referências anteriores verificadas;1.914 matrizes testadas. Próximos cálculos podem usar o arquivo numérico sem abrir o CAD completo. |
| Entrega compartilhável | [Pacote R18](../../05_Entregas/Publicacao/Guedala_Park_R18.zip) · [preparo anterior R17 selado](Pacote_local/README.md) | Publicação R52/R18 autorizada; confirmação remota no Estado atual. O R17 não foi regenerado. |
| Composição das tampasP20 | [Ficha P20 corrente](../../05_Entregas/Fichas_fabricacao_R13/P20.html) | Retiradas das notas atuais/CSV as referências ao receptorR47; composição, recessos e fixação continuam a detalhar para piano/trava. Sem mudança de dimensão ou escolha fictícia de painel. |

## O que ainda resta, separado por dependência

| Pendência | Situação agora | Próxima evidência necessária | Depende de medir o apartamento? |
|---|---|---|---|
| Juntas da caixa superiorP03 e ligação à P01/P02 | Equilíbrio e demandas nominais disponíveis; contatos sem juntas não fecham o modelo | Topologia real de juntas, conectores, constituição da chapa e curvas/capacidades nas orientações de uso. A caixa internaP02 ainda precisa de detalhamento próprio. |Não para esse desenvolvimento; ancoragem/execução final sim |
| Apoio inferiorP01/soco | Propostas e caminhos analisados, ainda separados | Escolha do desenho, retenção/uniões, compatibilidade da caixa e comprovação do conjunto |Parte de projeto pode avançar; contato/nivelamento real do piso fica para o imóvel |
| FundoP01 inteiro | Orientação e janela útil demonstradas;2750×1850 não comporta o atual | Produto18mm, faces, direção permitida, dimensão útil, fornecimento e transporte. Emenda só com projeto próprio |Não para selecionar produto/solução; acesso real para entrega/montagem sim |
|39 painéis fora do arranjo preliminar |IDs e motivos listados | Fechar substrato, faces, composição/espessura e processo; depois completar corte/contornos/fita |Não |
| Bancada e gaveteiroP16 | Proposta de cinco painéis e cenários de estabilidade existentes | Constituição/massa do tampo30, juntas positivas tampo–pedestal–travessa, carga de uso, resistência/deformação e protótipo |Produto/projeto/oficina podem avançar; piso/fixação real são posteriores |
| InterfaceMOVENTO400/fundo | Furos e18 regiões localizados; nenhum corte arbitrário feito | Configuração individual400, datum/regulagem do STEP e montagem piloto do produto/engates reais |Não |
| BancoP20 e cestoP14 | Direção piano/trava preservada; massa/esforços condicionais já calculados | Painéis e massas completos, geometria de ferragens/terminais, apoio, parada/retenção e ensaio cheio/vazio |Não para produto e protótipo; implantação final sim |
| AéreosP04/P09/P11/P12/P15/P17 | Demandas e estudos disponíveis | Material, juntas, suspensão, adaptação do depurador e ligações compartilhadas; P15 ainda precisa de processo composto permitido/demonstrado |Não para a caixa; substrato e ancoragens finais dependem do imóvel |
| MicroME23P |300mm confirmados no manual;100mm da F104 não atendem; alternativa pronta | Avaliação da outra altura, apoio/fixação, acesso e tolerâncias, se a alternativa for considerada. Não houve troca automática de escolha |Decisão/projeto podem avançar; instalação final depende de conferência |
| Cafeteira e reservas de produto | Espaço explicitamente não demonstrado, sem bloco inventado | Dimensões/ventilação do aparelho real e compatibilização de bancada |Não |
| Cotação/ orçamento | Listas de peças/ferragens atuais disponíveis; corte ainda condicionado | Propostas de fornecedores/oficina com materiais, serviços e exclusões reconciliados; preços antigos não são cotações atuais |Não para cotar com condições; corte/liberação final sim |
| Vãos, pisos, instalações e ancoragens reais | Base continua documental | Medições, material/condição das paredes, água/esgoto/gás/eletricidade, percursos e apoios reais |Sim, depois de acesso ao apartamento |

O fechamento de produto e oficina pode ocorrer antes das chaves. As linhas dessa categoria não foram convertidas em “aguarda medidas do apartamento”; exigem dados/peças/ensaios que não estão no acervo. Não foram enviados pedidos a terceiros, feitas compras ou declarados ensaios físicos.

## Resultados que mudam a próxima decisão

- **FundoP01:** com refilo10mm/borda e sem sobremetal do blank, o bruto precisa permitir2116×1984 para o atual ou2134×1984 para o proposto. Em2750×2100, a dimensão2096/2114 deve acompanhar2750. “Caber” não seleciona padrão/faces/fornecedor. [Todas as margens e orientações](Corte_e_formatos/Requisito_fundo_P01.csv).
- **Corte:**16 chapas virtuais foram encontradas para210 painéis com rotação livre, contra17 no cenário de orientação nominalC. Ambos excluem39 painéis e as36 propostas; não são quantitativo de compra, aproveitamento ótimo ou autorização de girar veio.4.045 pares foram conferidos nos cenários principais.
- **Caixa superior:** apoio traseiro não garante alívio da travessa frontal; o efeito depende da ligaçãoP02↔P03. Um autoequilíbrio demonstrado mostra que a estática sozinha não fornece envelope finito de solicitações das juntas. Acrescentar molas/rigidez sem fonte produziria uma conclusão fictícia. [Detalhes e limites](P01_P03/README.md).
- **Micro:** o estudo leva o topo do aparelho a1640 e preserva o aéreo em1940, obtendo300mm. Reduz de612 para412mm a altura livre sob a prateleira sobre a bancada. Não há margem vertical além do mínimo e nenhuma adoção dessa alteração.

## Validação e preservação

R52 original desta etapa: SHA256`941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`. Suas posições, peças e movimentos não foram alterados. As cópias externas removidas na revisão anterior não foram reintroduzidas. Estudos anteriores e arquivos publicados foram preservados.

Scripts, resultados e verificadores ficam nas respectivas pastas. As novas fontes editadas possuem backups byte a byte em `outputs/continuidade-pos-r52-2026-10-25/originais`, na raiz do workspace, com manifestos. O estado corrente de entrega e os hashes estão em [Verificacao_continuidade.json](Verificacao_continuidade.json).

Os cálculos conferem os modelos e hipóteses declarados. Nenhum deles transforma material não escolhido, massa desconhecida, ensaio inexistente ou parede não levantada em capacidade comprovada. Não foram acrescentados tubos ou outra estrutura metálica sob chapas.
