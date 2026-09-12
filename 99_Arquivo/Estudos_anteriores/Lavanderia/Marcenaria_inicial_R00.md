# A04.1 — Lavanderia · Partido de marcenaria e regras dimensionais

> **Documento histórico.** Para continuar, usar [A04.2 R01 — decisões e estudo atual](../../../01_Projeto/Lavanderia/Decisoes_da_lavanderia_R01.md) e a base A01.2. A interpretação das cotas, as hipóteses de cabimento e a faixa de 15 cm deste estudo foram substituídas. Em 09/09/2026 Elias esclareceu que a faixa faz retorno em L junto à janela. O conteúdo original abaixo foi preservado como histórico, não como instrução atual de execução.

**Guedala Park III · Torre 02 · Final 06 · R00 · 08/09/2026**

**Status:** partido funcional definido e travado. Desenho executivo **bloqueado** por medidas reais e modelos de equipamento. Nenhuma medida deste documento é medida de projeto: são *equações* e *verificações*, a serem preenchidas com o levantamento do Anexo A.

---

## 0. Hierarquia de fontes adotada

| Ordem | Fonte | Papel |
|---|---|---|
| 1 | PDF da construtora (P01) | Verdade geométrica. Não alterado. |
| 2 | `Projeto_Apartamento_Elias_Documentacao_Detalhada_v2.pdf` (08/09/2026) | Verdade das decisões — documento **mais recente**. |
| 3 | `C02.1 R04` (07/09/2026) | Verdade das decisões anteriores. Onde conflita com o item 2, **prevalece o item 2** e o conflito está registrado na §2. |
| 4 | `A01.1 R01` — levantamento | Evidência visual; unidade filmada provavelmente **espelhada**. Posições não transportáveis. |
| 5 | Imagens geradas | Conceito. Nunca fonte dimensional. |

---

## 1. Decisões fechadas aplicáveis à lavanderia (não reabertas)

- Lava e seca **de unidade única** — não é torre lavadora + secadora.
- Máquina **integrada à marcenaria**, com folgas, ventilação, acesso frontal e manutenção.
- Bancada em **pedra contínua**, atravessando visualmente do **fim da geladeira (cozinha) até a parede da janela da lavanderia**.
- Apoio sobre a máquina pode ocupar **toda a largura da máquina**.
- Trecho adicional de **~15 cm no canto voltado para a janela**, para apoio esporádico. **Não é a largura da bancada sobre a máquina.**
- **Parede da janela livre.**
- **Tanque esculpido na pedra**, preservando continuidade do material.
- **Cesto embaixo do tanque**: removível, extraível, transportável inteiro até a máquina, ventilado, **nunca em compartimento totalmente fechado**.
- **Aquecedor a gás**: marcenaria contorna o equipamento, com acesso técnico, ventilação e afastamentos do fabricante/normas.
- **Varal alto**, retrátil/recolhível, **oculto** dentro ou atrás do móvel quando fora de uso.
- Armários **aéreos até o teto**; módulos específicos para produtos de limpeza; separação uso diário × estoque.
- Piso **PL-01 — Eliane Iseo Marfim AC 90×90**.
- Composição: **azul na parte superior + Greenplac Arenza na inferior** — confirmada em 08/09 (CF-01), superando a ressalva do C02.1 §4.1. *A solução técnica continua prevalecendo sobre a estética.*
- Bancada em **Granito Branco Itaúnas** (CF-02), com tanque em **cuba montada em granito** (CF-03).
- Móvel tratado como **peça técnica única** em 4 zonas.

---

## 2. Conflitos documentais entre C02.1 R04 e o PDF v2

Detectados na leitura cruzada. **CF-01, CF-02 e CF-03 foram decididos por Elias em 08/09/2026 e passam a ser decisão fechada.**

| # | Tema | C02.1 R04 (07/09) | PDF v2 + briefing (08/09) | Situação |
|---|---|---|---|---|
| **CF-01** | Cor da lavanderia | "O azul petróleo terá **uso mínimo ou nenhum** na lavanderia"; areia mineral + madeira mel | "Preferência por **azul superior** + Arenza inferior" | ✅ **FECHADO — azul superior + Greenplac Arenza inferior.** O C02.1 §4.1 fica superado. |
| **CF-02** | Material da bancada | Cinza quente médio; famílias-alvo sinterizado/porcelânico ou quartzo | **Granito Branco Itaúnas** | ✅ **FECHADO — Granito Branco Itaúnas**, em cozinha, lavanderia e banheiro. O C02.1 §3.2 fica superado quanto a cor e família de material. |
| **CF-03** | Tanque | "Integrado/**embutido** na bancada" | "**Esculpido na pedra**" | ✅ **FECHADO — cuba montada em granito** (opção A da §6.3): laterais e fundo colados, cantos boleados, chapa de 2 cm. |
| **CF-04** | Ancoragem do varal | "Atravessa a lavanderia e **trava/ancora na parede oposta**" | "**Parede da janela livre**" | ⚠️ **Aberto por dependência física** — só fecha quando P-01/P-02 disserem qual parede é qual. Solução proposta na §8.3. |
| **CF-05** | Nomenclatura de MDF | Cores por hex (#29434D azul, #C2AE92 areia) | Padrões nomeados (**Guararapes Azul Petróleo**, **Greenplac Arenza**) | ⚠️ Aberto. Tratar os hex como **referência de tom** e o padrão nomeado como **especificação**. Confirmar contra amostra física. |

**Desdobramentos da decisão CF-02 (Branco Itaúnas) a propagar nos demais documentos:**
- O backsplash da cozinha, que o C02.1 previa em continuidade da bancada, passa a ser **branco**, não cinza quente. Reavaliar contraste com o azul petróleo dos aéreos.
- Granito é **poroso**: impermeabilização/resina e reaplicação periódica entram no memorial de manutenção — crítico na lavanderia (sabão, alvejante, amaciante) e junto ao cooktop.
- O nicho do box do banheiro, previsto no C02.1 §9.1 "com a mesma pedra da bancada", passa a ser Branco Itaúnas sobre base travertino greige. Conferir a combinação em amostra.

---

## 3. Base geométrica disponível e seus limites

| Dado | Valor | Origem | Limite de uso |
|---|---|---|---|
| Área de serviço | **1,29 × 1,54 m** | P01 (oficial) | Cota comercial. A própria folha ressalva que medidas mudam conforme acabamento. **Não é medida de fabricação.** |
| Cozinha / frente inferior | **3,52 m**; transversal **1,55 m** | P01 | Não é largura livre de marcenaria. |
| Janela da A.S. | Existe, em uma lateral | P01 + vídeo | Vão, peitoril e altura **não cotados**. |
| Pé-direito | 2,60 m | **Estimativa** de `apartamento_dados.json` | **Não confirmado.** Bloqueia todo o dimensionamento vertical. |
| Enchimentos / forro | Indicados na legenda de P01, junto ao banho e ao tanque | P01 | Alturas e espessuras pendentes. |
| Ralo, caimento, soleira | Vistos em vídeo | A01.1 | Unidade provavelmente espelhada. Posição não transportável. |

**Consequência direta:** o desenho executivo da lavanderia **não pode ser iniciado** com o que existe hoje. O que este documento entrega é o partido travado + as equações que o levantamento vai fechar.

---

## 4. Partido — móvel técnico único, 4 zonas

Um único volume de marcenaria, leitura visual contínua, subdividido funcionalmente:

| Zona | Conteúdo | Faixa vertical |
|---|---|---|
| **Z1 — Lavagem** | Bancada de pedra contínua, lava e seca embutida, tanque esculpido, apoio de ~15 cm | Do piso ao topo da bancada |
| **Z2 — Inferior** | Cesto extraível ventilado sob o tanque + módulo de produtos de uso diário | Sob a bancada, ao lado da máquina |
| **Z3 — Superior** | Aéreos até o teto: estoque, panos, ferramentas, baixa frequência + **nicho do varal** | Do topo do backsplash ao teto |
| **Z4 — Técnica** | Aquecedor a gás contornado, ripado ventilado, acesso frontal total | Faixa dedicada, posição a definir |

**Regras de partido (travadas):**

1. Z4 tem **prioridade absoluta** sobre Z1/Z2/Z3. Onde o aquecedor e sua ventilação exigirem espaço, a marcenaria recua.
2. A pedra é **uma leitura só**: mesmo material, mesma espessura aparente, mesmo alinhamento de topo da cozinha à lavanderia.
3. Nada da marcenaria **encosta na parede da janela** — nem lateral, nem aéreo, nem varal (ver §9.2, há razão normativa além da estética).
4. Frentes: **linguagem lisa**, puxador perfil embutido, sem puxadores aparentes — coerente com cozinha e escritório.

---

## 5. Equações dimensionais (preencher com o Anexo A)

Variáveis a levantar:

| Símbolo | O que é | Fonte |
|---|---|---|
| `Lp` | Largura da parede da bancada, **acabada**, medida no piso e na altura da bancada | Obra |
| `Pp` | Profundidade útil da lavanderia, acabada | Obra |
| `Hpd` | Pé-direito acabado (e altura sob forro/sanca, se houver) | Obra |
| `LM`, `PM`, `HM` | Largura, profundidade e altura da lava e seca | Manual do modelo comprado |
| `PMa` | Profundidade com **porta aberta a 90°** | Manual |
| `fL`, `fT`, `fS` | Folgas lateral, traseira e superior exigidas pelo fabricante | Manual — **nunca estimar** |
| `Hh` | Altura do ponto de água/esgoto do tanque existente | Obra |
| `Aq(x,y,l,h,p)` | Posição e volume do aquecedor + afastamentos do manual | Obra + manual |

**E-01 — Cabimento horizontal da zona de lavagem**

```
Ltanque + (LM + 2·fL) + 15 cm  ≤  Lp
```

Esta é a verificação decisiva. Faixa de referência de mercado (**não é medida de projeto, é só para antecipar o risco**): lava e seca de unidade única costuma ter 60 cm de largura; um tanque esculpido funcional dificilmente fica abaixo de ~50 cm. Somando os 15 cm de apoio, a demanda tende a **~1,25–1,35 m** de parede só na lavanderia.

Contra `1,29 × 1,54 m`:
- Se a parede da bancada for a de **1,54 m** → cabe, com folga apertada. Cenário provável.
- Se for a de **1,29 m** → **não cabe** com tanque, máquina e os 15 cm na mesma parede. Nesse caso o tanque migra para o trecho da pedra que já está na cozinha (fim da geladeira), o que **preserva** a continuidade da pedra e o cesto embaixo dele, mas muda o desenho da cozinha.

→ **Definir qual parede recebe a bancada é a primeira medida a levantar.**

**E-02 — Altura da bancada**

```
Hbanc = HM + fS + e_estrutura
```

**Regra travada: a pedra nunca apoia sobre a máquina.** O vão sobre a lava e seca é vencido pelos apoios laterais/travessas; a máquina vibra na centrifugação e transmitiria esforço e ruído à pedra e à junta do tanque.

**Bifurcação B1 — depende de `HM`:**
- Se `Hbanc` resultar em **~90 cm**: ergonomia normal, tanque na mesma bancada, tudo fecha.
- Se `HM` for alta e `Hbanc` passar de ~100 cm: o tanque fica alto demais para uso confortável. Nesse caso o tanque **sai da faixa sobre a máquina** e desce para altura ergonômica própria, com **desnível na pedra** — o que exige decidir se a continuidade visual aceita um degrau. Trade-off a resolver quando `HM` for conhecido.

**E-03 — Profundidade do móvel**

```
Pmóvel = PM + fT  (nunca menor)
Circulação livre restante = Pp − Pmóvel ≥ PMa suficiente para abrir a porta e retirar o cesto
```

**E-04 — Faixa superior**

```
H_aéreos = Hpd − Hbanc − h_backsplash − e_pedra
```

Aéreos vão **até o teto** (ou até o forro/sanca, se existir na A.S.). Sem rodapé de armário, sem faixa morta no topo.

---

## 6. Z1 — Zona de lavagem

### 6.1 Bancada de pedra contínua

- Percurso: **fim da geladeira (cozinha) → lavanderia → encosta na parede da janela.**
- **Alerta de execução:** chapas de granito têm comprimento útil limitado. Um percurso cozinha + lavanderia muito provavelmente **exigirá emenda colada**. "Contínua" deve ser lida como *leitura visual contínua*, não *peça única*. Posicionar a emenda em ponto discreto — recomendação: **no eixo da divisória cozinha/lavanderia**, onde a mudança de ambiente já justifica a linha.
- Espessura, tipo de borda e acabamento (polido × acetinado): pendente, decidir junto com a cozinha.
- **Granito é poroso** — impermeabilização/resina e reaplicação periódica entram no memorial de manutenção. Relevante justamente numa lavanderia (sabão, alvejante, amaciante).

### 6.2 Lava e seca embutida

| Item | Definição |
|---|---|
| Fechamento frontal | **Nicho aberto, sem porta.** Uso diário, carga e descarga frequentes, dissipação de calor da secagem e acesso a filtro/mangueiras. Porta frontal seria um estorvo diário e um risco térmico. |
| Laterais e fundo | Folgas `fL`/`fT` **do manual**, nunca estimadas. |
| Topo | Vão livre `fS` sob a pedra; **sem contato**. |
| Base | Piso acabado nivelado; pés reguláveis acessíveis. Máquina **não** sobre estrado de MDF. |
| Manutenção | A máquina precisa poder ser **puxada inteira para fora** sem desmontar marcenaria. Nenhuma lateral fixa pode travar a retirada. |
| Elétrica | Tomada **fora** do nicho fechado e acessível sem retirar a máquina; circuito e corrente conforme o modelo. |

### 6.3 Tanque esculpido — solução fechada

**Decisão CF-03 (08/09/2026): opção A — cuba montada em Granito Branco Itaúnas.** Laterais e fundo em chapa de 2 cm, colados, cantos boleados. Execução de marmoraria comum, custo e prazo controlados, continuidade total do material.

Opções descartadas, registradas para histórico:

| Opção descartada | Motivo |
|---|---|
| **B. Bloco maciço esculpido** | Peça monolítica sem juntas e aparência superior, mas peso alto (exigiria verificação de apoio), custo bem maior, prazo longo e poucos fornecedores. |
| **C. Tanque industrial sob a pedra** | Mais barato e com esfregador de fábrica, mas rompe a decisão fechada de tanque esculpido na pedra. |

**Requisitos de execução da opção A:**
- **Vedação das juntas coladas** especificada e registrada no memorial de manutenção — é o ponto fraco da solução e precisa de reaplicação periódica.
- Granito Branco Itaúnas é **poroso**: impermeabilização obrigatória, com atenção a alvejante e produto de limpeza concentrado.
- **Esfregador desenhado explicitamente** na peça — a cuba montada não traz um de fábrica.

**Restrições obrigatórias do tanque:**
- Profundidade útil **reduzida deliberadamente**, para liberar altura ao cesto embaixo (§7.1).
- **Válvula/sifão deslocado para o fundo ou para o canto**, nunca no centro do vão do cesto.
- Área de esfregador desenhada explicitamente — sem ela o tanque vira só uma cuba funda.
- Ponto de água e esgoto existentes conferidos **antes** de fixar a posição: o A01.1 registra tubulação, válvula e sifão ocupando volume real sob o tanque atual.

### 6.4 Os 15 cm no canto da janela

- Trecho de pedra de **~15 cm** entre o fim da máquina e a parede da janela.
- Função: apoio esporádico (frasco de produto, celular, cesto pequeno). **Não é área de trabalho.**
- **Não vira armário.** Abaixo dele: nada de módulo fechado encostando na parede da janela — mantém-se livre e ventilado.
- Se `Lp` fechar com folga maior que 15 cm, a folga vai para **as folgas técnicas da máquina**, não para aumentar este apoio.

---

## 7. Z2 — Cesto e produtos

### 7.1 Cesto extraível ventilado

| Requisito | Solução |
|---|---|
| Removível e transportável | Cesto **solto**, em material lavável e leve (tela/lona rígida ou trama), com alças. Sai do corrediço e vai inteiro até a máquina. |
| Extraível | Corrediça telescópica com **extração total**, carga nominal adequada a roupa molhada. Frente reta integrada ao móvel. |
| Ventilado | **Fundo e laterais do módulo perfurados/vazados**, com entrada de ar baixa e saída alta. O módulo **não** pode ser caixa fechada. |
| Discrição | A ventilação fica no fundo e nas laterais, não na frente — a fachada segue lisa. |
| Altura | Limitada por `Hbanc − profundidade do tanque − sifão`. **É esta a conta que define o tamanho do cesto**, não o contrário. |

**Risco identificado:** o sifão do tanque e o cesto disputam exatamente o mesmo volume. Se o levantamento mostrar o ponto de esgoto alto, o cesto perde altura útil. Mitigações, em ordem: (1) tanque mais raso, (2) sifão de perfil baixo deslocado ao fundo, (3) cesto migra para o módulo ao lado da máquina — **última opção**, porque contraria a decisão "cesto embaixo do tanque".

### 7.2 Produtos de limpeza

- **Uso diário** (sabão, amaciante, alvejante, multiuso): módulo baixo, ao alcance da bancada, **em gaveta**, não em porta de bater — gaveta evita produto esquecido no fundo.
- Base do módulo com **bandeja estanque removível** — vazamento de produto é o dano mais comum nesse móvel.
- **Estoque**: sobe para Z3.
- Vassoura/rodo/mop: módulo vertical, conforme C02.1 §4.2 — posição depende do que sobrar após E-01. **Pendência**: em 1,29 × 1,54 m com máquina + tanque + aquecedor, o módulo vertical pode não caber na lavanderia e precisar migrar para a circulação ou para o fim da cozinha.

---

## 8. Z3 — Superior: estoque e varal

### 8.1 Aéreos

- **Até o teto** (ou até o forro), sem faixa morta.
- Divisão em **duas alturas**: prateleira inferior alcançável em pé (uso ocasional) e faixa superior de estoque real (escada).
- Portas de abrir com **pistão a gás** ou portas retas — evitar folha muito larga em ambiente estreito, que colide com quem está de pé na bancada.
- Iluminação **sob os aéreos**, 4000 K, circuito independente da cozinha (C02.1 §4.4 — mantido).

### 8.2 Nicho do varal

- Varal **retrátil**, alojado em nicho na faixa superior do móvel, **invisível quando recolhido**.
- Fixação do mecanismo e do receptor **no substrato/parede**, nunca no MDF (C02.1 §4.3 — mantido e reforçado).
- **Atenção ao aviso do A01.1**: há registro de parede em drywall na área do aquecedor com limitação de profundidade de fixação. Se o varal ancorar em drywall, exige **reforço embutido** definido antes do fechamento da parede — ou seja, é decisão de **obra**, não de marcenaria.

### 8.3 Eixo do varal — resolução do conflito CF-04

- O varal **não pode** ancorar na parede da janela: ela deve ficar livre e, muito provavelmente, é a parede que carrega a ventilação permanente do ambiente (§9.2).
- **Recomendação:** varal recolhido no móvel e estendido **paralelo à parede da janela**, sobre a faixa da bancada/máquina, ancorando na parede oposta ao móvel.
- **Consequência assumida, dita com clareza:** em 1,29 × 1,54 m, **roupa estendida ocupa a lavanderia**. Não existe posição em que o varal em uso não passe sobre alguma coisa. A exigência "não bloquear bancada, máquina, portas ou circulação" deve ser lida como: **não bloquear permanentemente, não bloquear a porta e não impedir a saída**. Estendido sobre a faixa da pedra é a melhor posição possível — pinga sobre material impermeável e perto do ralo, não sobre marcenaria nem sobre a circulação.
- Múltiplas linhas paralelas (C02.1 §4.3 — mantido), com carga nominal declarada pelo fabricante.

---

## 9. Z4 — Zona técnica do aquecedor

### 9.1 Regras inegociáveis

- A marcenaria **contorna**, não encerra. Nenhum módulo fechado sobre, sob ou ao redor do aquecedor sem respeitar os afastamentos do manual.
- Ocultação visual por **ripado em madeira mel** (C02.1 §4.2 — mantido), com **área livre de ventilação declarada** e **remoção sem ferramenta especial** para manutenção.
- Frente do aquecedor: acesso técnico **total**, incluindo registro de gás, comando e conexões.
- Nenhuma prateleira, produto ou têxtil dentro da faixa de afastamento.

### 9.2 A parede da janela e a ventilação — razão normativa

O A01.1 registra, na unidade filmada, **janela com faixa venezianada superior e grelha inferior** na área de serviço, além de aviso de instalação de aquecedor a gás natural.

Isso significa que a exigência "**parede da janela livre**" provavelmente não é só estética: em ambiente com aparelho a gás, veneziana e grelha constituem a **ventilação permanente**, e obstruí-las é infração normativa (NBR 13103 e correlatas), além de risco direto. **A regra fica reforçada e passa a ter justificativa técnica, não só de projeto.**

**Pendência crítica:** a posição do aquecedor **não está determinada**. Se ele estiver na parede da janela, há colisão entre "parede livre" e "aquecedor contornado pela marcenaria" — e o partido do móvel muda. **Esta é a segunda medida a levantar.**

### 9.3 Validação obrigatória antes de qualquer desenho executivo

Marcenaria em torno de aparelho a gás **não se resolve por bom senso**. Antes do executivo:
1. Modelo do aquecedor definido e manual em mãos.
2. Afastamentos, exigência de exaustão e área de ventilação conferidos no manual.
3. Instalação validada por **profissional habilitado** e conforme as regras da construtora/condomínio.
4. Só então a marcenaria fecha o contorno.

---

## 10. Compatibilização técnica a amarrar

| Sistema | Ponto de atenção |
|---|---|
| Hidráulica | Água quente/fria e esgoto do tanque; alimentação e dreno da lava e seca; sifão sob o cesto; acesso a registros **nunca bloqueado**. |
| Gás | Ponto registrado entre pia e tanque no A01.1 (unidade espelhada — **não copiar posição**). Registro acessível. Aquecedor conforme §9. |
| Elétrica | Circuito da lava e seca dimensionado ao modelo; tomada acessível; **tomada de 20 A** conforme diretriz geral do projeto; LED sob aéreos em circuito independente. |
| Ventilação | Veneziana/grelha da janela **desobstruídas**; ventilação do cesto; ventilação do nicho do aquecedor; dissipação de calor da secagem. |
| Piso e ralo | PL-01 Eliane Iseo Marfim AC 90×90. Conferir caimento e posição do ralo — define onde o varal pode pingar e onde o rodapé do móvel precisa ser estanque. |
| Divisória cozinha × lavanderia | C02.1 §4.5 prevê folha fixa + folha de correr em vidro canelado fumê. **Compatibilizar com a pedra contínua**: o trilho inferior cairia sobre a bancada. Definir se a divisória arranca da pedra, se corre acima dela, ou se a divisória é revista. **Pendência de projeto.** |
| Estrutural | Peso da pedra (especialmente na opção B do tanque) e fixação do varal em drywall com reforço embutido. |

---

## 11. Matriz de pendências

| # | Pendência | Por que importa | Como resolver |
|---|---|---|---|
| P-01 | **Qual parede recebe a bancada** (1,29 ou 1,54 m) | Define se tanque + máquina + 15 cm cabem (E-01) | Medir em obra na orientação de P01 |
| P-02 | **Posição do aquecedor** | Pode colidir com "parede da janela livre" e reorganizar o móvel | Medir em obra + manual |
| P-03 | **Modelo da lava e seca** | `LM`, `PM`, `HM`, `fL`, `fT`, `fS` — nada de Z1 fecha sem isso | Escolher modelo e obter manual |
| P-04 | **Pé-direito real** | Toda a faixa superior e o nicho do varal | Medir em obra (2,60 m é estimativa não confirmada) |
| P-05 | **Altura dos pontos hidráulicos do tanque** | Define a altura útil do cesto | Medir em obra |
| ~~P-06~~ | ~~CF-01 — cor da lavanderia~~ | — | ✅ Fechado 08/09: azul superior + Arenza |
| ~~P-07~~ | ~~CF-02 — material da bancada~~ | — | ✅ Fechado 08/09: Granito Branco Itaúnas |
| ~~P-08~~ | ~~CF-03 — técnica do tanque~~ | — | ✅ Fechado 08/09: cuba montada em granito |
| P-09 | Compatibilização pedra × divisória | Trilho sobre bancada | Projeto |
| P-10 | Módulo vertical de vassouras | Pode não caber na lavanderia | Depende de P-01 e P-02 |
| P-11 | Andar da unidade dentro do intervalo 4º–16º | Aplicabilidade de P01 | Conferir contrato |
| P-12 | Forro/sanca na área de serviço | Altura final dos aéreos | Medir em obra |
| P-13 | CF-05 — padrão nomeado × hex de cor | Especificação de compra do MDF | Conferir amostra física (C02.3) |
| P-14 | Backsplash branco × aéreos azuis (efeito de CF-02) | Contraste da cozinha muda com a bancada branca | Reavaliar no moodboard |

---

## Anexo A — Checklist de levantamento em obra (lavanderia)

Levar: trena a laser, trena de fita, nível, papel milimetrado, câmera. Medir **sempre no piso acabado** e registrar foto de cada ponto medido.

**Geometria**
1. Largura de cada uma das quatro paredes da A.S., medidas **no rodapé, a 90 cm e no teto** (paredes não são paralelas).
2. Diagonais do retângulo — confere esquadro.
3. Pé-direito em 3 pontos. Existe forro/sanca/rebaixo? Altura livre sob ele.
4. Ressaltos, enchimentos e tubulações aparentes: posição, largura, profundidade, altura.

**Janela**
5. Vão (largura × altura), altura do peitoril, profundidade da mocheta.
6. **Existe faixa venezianada e/ou grelha? Medir e fotografar.** Registrar se são fixas.
7. Sentido de abertura e envelope de giro/projeção.

**Porta / passagem**
8. Vão livre da passagem cozinha↔lavanderia; existe batente, soleira ou desnível.
9. Envelope de giro de qualquer folha existente.

**Instalações**
10. Água fria e quente: altura do piso e distância da parede lateral, de cada ponto.
11. Esgoto do tanque: altura e posição. Esgoto/dreno da máquina: altura e posição.
12. Ponto de gás: altura, posição, tipo de registro, espaço livre exigido à frente.
13. Ponto do aquecedor: posição marcada na parede, tipo de parede (**alvenaria ou drywall**), presença de reforço, avisos afixados — fotografar o aviso inteiro.
14. Tomadas e ponto de luz existentes: altura e posição.
15. Ralo: posição, diâmetro, sentido do caimento (jogar água e observar).

**Equipamentos**
16. Modelo definitivo da lava e seca → do manual: largura, profundidade fechada, **profundidade com porta aberta**, altura, folgas laterais/traseira/superior, peso, corrente, requisitos de nivelamento.
17. Modelo do aquecedor → do manual: dimensões, afastamentos, exigência de exaustão, área de ventilação do ambiente.

**Registrar como resposta direta:**
- P-01: a bancada corre na parede de ____ m.
- P-02: o aquecedor está na parede ____, a ____ cm do canto ____.
- P-04: pé-direito acabado = ____ cm; altura sob forro = ____ cm.
- P-05: esgoto do tanque a ____ cm do piso acabado.

Com essas quatro respostas + os dois manuais, o A04.1 avança para **R01 com desenho executivo** (planta, elevações, cortes e lista de módulos).

---

*Documento gerado como continuidade do handoff. Nenhuma decisão fechada foi alterada. Nenhuma medida foi inventada: onde não há dado, há equação ou pendência.*
