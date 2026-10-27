# Varal — especificação consolidada sem placa de ocultação

Atualização de 21/10/2026. A placa de madeira próxima à entrada foi removida na R35 por solicitação de Elias. Ela não integra o escopo vigente e não deve voltar em desenho, orçamento ou instalação. Os estudos R08/R09 de ocultação são históricos.

## Configuração escolhida

Grelha de 100 × 50 cm, quadro inteiro, elevação vertical no mesmo lugar e acionamento manual por manivela. A referência de manivela removível permanece a confirmar no produto. Não foram escolhidos motor, varetas individuais ou extração horizontal.

Tanque limpo e livre serve de apoio temporário à roupa retirada da máquina. Sequência aprovada: retirar a roupa e fechar a máquina → baixar o quadro vazio → carregar do fundo para a entrada → sair e subir para secar → baixar e retirar da entrada para o fundo → subir vazio. Conferir a operação com peças pequenas, toalhas e peças longas no espaço real.

E21 GN em 127 V, LG VC4, tanque/cesto e lixeira permanecem referências do ambiente. A remoção desta placa não altera por si só outros painéis ou eventual estudo de ripado do aquecedor.

## Requisitos para fechar a ferragem

| Item | Conferência necessária |
|---|---|
| Acionamento | Operável junto ao acesso da cozinha, fora da projeção do quadro cheio; evitar manivela permanentemente saliente na passagem. |
| Retenção | Manter a posição durante carga e descarga sem segurar continuamente o comando; descida controlada conforme conjunto do fabricante. |
| Curso e posições | Confirmar manuseio, secagem e recolhimento vazio, incluindo roupa e pregadores. Não deduzir curso apenas da grelha. |
| Envelope completo | Obter roldanas, suportes, cabos, comando e altura mínima recolhida; conferir janela, armários, sanca, E21 e duto. |
| Carga | Os 30 kg citados em estudos anteriores são uma meta proposta, não capacidade aprovada. Verificar carga útil, distribuição e condições do conjunto completo. |
| Instalação | Identificar base resistente, esforços e ancoragem. Forro, aquecedor e duto não são suportes presumidos. Não selecionar bucha por classificação genérica da planta. |
| Manutenção | Acesso a comando, cabos, roldanas e guarda da manivela, sem depender de abrir armário bloqueado por roupa. |

Setor de 129 × 154 cm e altura sugerida de manuseio de 190–200 cm são referências de estudo, não levantamento acabado nem cotas executivas. Grelha 100 × 50 cm é escolha dimensional; o envelope do produto permanece pendente.

Modelo comercial, materiais, carga, curso e fixação ainda não fechados. A retirada da placa está concluída no modelo; os requisitos de instalação do varal permanecem em desenvolvimento.

Fontes do projeto: sequência aprovada R10, [retirada da placa na R35](../../02_Modelo_3D/Componentes/Movimentos/Movimentos_R35_README.md), conferências de campo.

## T05 — percurso nominal com roupa, 26/10/2026

[Trinta cenários e candidatos de encontro](Varal_percurso.json), calculados da base salva R52 sem abrir CAD. O objeto `Peca157` é um gabarito 1000 × 500 × 30 mm em X3705–4705/Y5650–6150/Z2310–2340. A expressão do controlador admite descida até **860 mm**; isso leva a face inferior a **1450 mm**. A referência anterior de manuseio 1900–2000 mm corresponde somente a 310–410 mm de descida, tomando a mesma face como referência.

Foram conferidos os percursos completos de descida 310/410/860 mm, primeiro com quadro vazio e depois com envelopes hipotéticos de roupa de 500/800/1200 mm abaixo da face inferior e acréscimos laterais de 0/50/100 mm por lado. As roupas são envelopes conservadores, não tecidos simulados ou comprimentos escolhidos para uso. Pregadores, posição real das barras e oscilação precisam de confirmação própria.

| Descida | Face inferior do quadro | Ponta do envelope de roupa de 1200 mm | Distância vertical à tampa da lixeira Z437 |
|---|---:|---:|---:|
| 310 mm | 2000 mm | 800 mm | 363 mm |
| 410 mm | 1900 mm | 700 mm | 263 mm |
| 860 mm | 1450 mm | 250 mm | −187 mm: intervalos verticais sobrepostos |

**Encontro identificado:** nos três cenários com descida 860/roupa 1200, as caixas encontram `Peca147` e `Peca148`, corpo/tampa da lixeira. Mesmo sem acréscimo lateral, existe sobreposição em planta de 165 × 50 mm. Na hipótese de roupa de 1200 mm, o contato com o topo Z437 começa em descida 673 mm; acima disso há sobreposição vertical. Esse valor é um limite matemático do gabarito, **não posição de batente ou curso recomendado**. Com folga adicional m, a condição vertical seria descida menor que `673 − m`; m e a distribuição real da roupa não foram definidos.

Os outros 27 cenários não têm candidatos de volume no conjunto testado. Sobreposição de caixas é triagem, não prova de colisão do tecido real. A ausência de candidatos também não comprova alcance, manuseio ou afastamento térmico. A lixeira já tem encaixe com fechamentos pendente na planta; sua posição salva foi preservada, sem movê-la para eliminar este resultado.

**Consequência para a sequência de uso:** manter o carregamento do fundo para a entrada e a retirada inversa, mas distinguir o percurso vazio do percurso carregado. Antes de escolher posições do comando, conferir o maior comprimento pendente das roupas e sua distribuição em planta. Não tratar os 860 mm do controlador como curso carregado disponível. Não recolocar placa de ocultação.

O teste usa caixas de peças sólidas Part/PartDesign com visibilidade na cadeia de pais salva; contêineres agregados não são obstáculos duplicados. Movimentos de janela, portas, máquina e cesto não foram combinados. Cordas, roldanas, suportes, comando, pessoas e volumes comerciais ausentes continuam por representar. A base conserva alturas anteriores: a hipótese geral de 2600 mm não foi aplicada silenciosamente à R52. Nenhum afastamento de gases/calor, capacidade, retenção ou ancoragem foi validado.

Reproduzir: `python -B ferramentas/estudos/conferir_interfaces_t05.py`. O script confere o hash do modelo, varre caixas por translação e inclui controles de obstáculo intermediário e contato tangente. Nenhum ensaio físico.
