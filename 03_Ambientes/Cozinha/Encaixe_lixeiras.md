# Lixeiras — proposta de encaixe sem alterar o FreeCAD

Agenda27/10, preparada em26/10/2026. **Proposta documental, não aplicada.** Mantém Biovis Coleta15L na parede externa do banheiro voltada à mesa e Tramontina Loop20L fora do gabinete da lavanderia. As sobreposições6/5cm são da reconstrução do site R23, não medidas de obra. [Estado e fonte da correção](../../ESTADO_ATUAL.md).

## Encaixe nominal proposto

Coordenadas abaixo em **cm do desenho do site**, origem/axes de `ferramentas/site/src/app.js`; não são cotas de locação do FreeCAD nem medidas do apartamento. Foram lidas somente as linhas `walls`, `add('trash'...)` e `add('recycling'...)`, sem editar o site.

| Item | Reserva atual, corpo fechado | Fechamento conflitante | Proposta para teste físico | Resultado localizado |
|---|---|---|---|---|
| Biovis15L | x474–508; y508–529; altura47 | Parede banheiro x464–480, y395–546 | Transladar todo o conjunto **+7cm em x**, sem girar: corpo x481–515, y508–529; pedal x512–517, y514–523 | Remove6cm de sobreposição e deixa1cm nominal entre corpo e face x480. Avança7cm em direção à mesa |
| Loop20L | x257–286; y541–570; altura43,7 | Parede banheiro x255–480, y529–546 | Transladar todo o conjunto **+6cm em y**, sem girar: corpo x257–286, y547–576; pedal x267–276, y574–579 | Remove5cm de sobreposição e deixa1cm nominal à face y546. Corpo/pedal permanecem no piso desenhado da lavanderia x255–384/y546–700 |

[Esquema em planta](Encaixe_lixeiras.svg). A folga1cm é **provisão de teste**, não afastamento exigido por fabricante. Rodapé, corpo/tampa real e folga do mecanismo podem exigir mais. Relação geral: deslocamento ≥ sobreposição + projeção do rodapé/acessório + folga efetiva requerida. Se esses termos não couberem na provisão, aumentar o afastamento somente após conferir circulação e operações.

**Cozinha:** a passagem antiga de~107cm era nominal até a mesa ([detalhamento](Detalhamento_dimensional.md)). Com a mesma referência e avanço7cm do corpo, restariam~100cm; essa subtração não cobre pedal, pessoa acionando, cadeira puxada, mesa estendida ou retirada do balde. Medir a menor passagem no conjunto real. Não recuar/encolher mesa ou eliminar cadeira para declarar encaixe.

**Lavanderia:** deslocar6cm resolve apenas a parede. O [encontro do varal com roupa longa](../Lavanderia/Varal.md#t05--percurso-nominal-com-roupa-26102026) foi calculado na posição salva da R52 e continua aberto; não transportar aqueles números para a nova posição do site. Para o teste, manter a lixeira solta e prever retirá-la temporariamente da faixa do varal ao baixar/carregar, com destino fora da passagem e acesso hidráulico. Esse destino ainda deve ser marcado no gabarito real; não presumir que mover para a cozinha seja viável. Sem local de guarda temporária e sem demonstrar roupa/varal livres, esta rotina não está fechada.

## Conferência com gabaritos, sem nova varredura

1. Marcar no piso as faces acabadas e rodapés; medir a Biovis21×34×47 e Loop29×29×43,7 como referências documentais. Medir corpo real, pedal, tampa totalmente aberta e altura de retirada do balde; os envelopes fechados não bastam.
2. Posicionar a Biovis com a traseira livre da parede e pedal voltado à mesa. Testar sentar/levantar com três cadeiras, mesa normal/estendida, acionar pedal e retirar balde sem deslocar móvel fixo.
3. Posicionar a Loop afastada da parede do banheiro. Conferir janela, banquinho sendo retirado, lavadora aberta, saco/cesto P14 a55° e acesso ao sifão. Não reduzir o saco para acomodar a lixeira.
4. Com roupa longa representativa, executar a sequência do varal; demonstrar o destino temporário da Loop se necessário e medir passagem remanescente. Não definir novo batente do varal por essa proposta.
5. Registrar abaixo. Se não atender, apresentar a Elias alternativa de implantação ou lixeira mais estreita com perda de volume e preço; **não trocar os produtos automaticamente**.

| Campo | Cozinha | Lavanderia |
|---|---|---|
| Data / configuração / foto | | |
| Rodapé saliente (mm) | | |
| Corpo real L×P×A (mm) | | |
| Envelope pedal acionado e tampa aberta (mm) | | |
| Folga real à parede / rodapé (mm) | | |
| Menor passagem com operações simultâneas (mm) | | |
| Retirada balde / saco sem desmontagem | | |
| Destino temporário fora da passagem (se necessário) | | |
| Resultado e responsável pela conferência | | |

**Pergunta LIX para Elias, após gabarito:** A — manter os modelos e aceitar o avanço7/6cm e, se demonstrada, a retirada temporária da Loop durante uso do varal; B — preservar a posição/rotina sem essa concessão e pedir alternativa mais estreita, com volume e custo para nova decisão. Resposta=__; data/fonte=__. A pergunta não autoriza interferência; ambas exigem passagem e operação verificadas.

Dependência física: produto/pedal/tampa e gabarito de uso. Dependência do imóvel: parede acabada, rodapé, portas, janela e passagem real. **Nenhuma mudança no FCStd, no desenho publicado ou nos envelopes de referência; proposta ainda não demonstra compatibilização completa.**
