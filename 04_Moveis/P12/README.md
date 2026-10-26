# P12 — caixa e suspensão acima da geladeira

Estudo nominal separado, 26/10/2026. Elias, 25/10/2026: “20 kg / 10 kg / 10 kg” na ordem P17/P04/P12; uso P12: utensílios grandes/leves de cozinha usados ocasionalmente. [Premissas](../Aereos_suspensao/Lote_B_premissas.json). Base limpa, sem cabeças/tampinhas aparentes por baixo. Nenhum ensaio físico ou capacidade demonstrada.

| Item | Estado vigente do estudo |
|---|---|
| Caixa | 801×330×584 mm externos; largura interna 765; laterais/base/tampo/divisor 18 |
| Fundo | Peca344,765×548×18 atual, preservado. A decisão de desenvolver fundos inteiros abrangeu P17/P04 |
| Conteúdo | Meta 10 kg total; cenários distribuídos/frontais e portas independentes herdados do lote B, sem carga por compartimento definida |
| Massa nominal | Madeira+conteúdo 32,75–41,51 kg; densidades/espessuras hipotéticas, sem ferragens reais |
| Ligações | 12 Minifix/9 Confirmat candidatos reconciliados com R00; não somar como compras novas |
| Suspensão | Bigfer 04.02.058 candidata nos dois cantos laterais/fundo 18; dois suportes são hipótese |

[Implantação e memória](../Aereos_suspensao/P12_suspensao.json) · [desenho](../Aereos_suspensao/P12_suspensao.png) · [conferência independente](../Aereos_suspensao/P12_verificacao_suspensao.json) · [requisitos preparados para produto/oficina](../Aereos_suspensao/P12_qualificacao_suspensao.txt).

## Posição e acesso

Coordenadas desde a esquerda interna, traseira para frente e base externa: assentos u40,5/724,5 e Z548. Metal envolvido por 49,5×37,8×16 por canto, aproximadamente 60 mL/par; sem cabeças/capa/reserva de ferramenta nesse volume. Fundo na posição atual, sem reduzir os 312 mm úteis nominais de profundidade.

A altura herdada H−58=526 colocava o corredor do auxiliar traseiro nos calços superiores. A proposta H−36=548 sobe 22 mm, deixa 10 mm entre metal e tampo e mantém os quatro calços fixos fora dos corredores. Os 12 acessos Minifix internos também foram conferidos. Acessos sem interseção das caixas nominais de madeira/calços não comprovam ferramenta real ou ergonomia.

**Auxiliar traseiro junto à lateral:** eixo u9,5/755,5; corredor Ø20 invade 0,5 mm a lateral. A reserva Ø12 deixa 3,5 mm nominais até a lateral e passa pelos calços na nova altura. Ponta/cabeça, corpo da ferramenta, mãos e acesso através do próprio suporte precisam de verificação após escolher os fixadores. Não é indicação de piloto Ø12 ou parafuso Ø12.

Montar a caixa e apertar conectores antes das portas; manutenção com portas desclipadas/removidas, mantendo os calços. Rasgos espelhados pedem deslocamentos opostos: rejeitado encaixe por uma translação única. Proposta de gabinete sustentado/nivelado e inserção/aperto pela frente, sujeita à confirmação do fabricante; retirada também com apoio. Corpos das dobradiças/portas em movimento não foram validados nesta etapa.

## Solicitações e caminho resistente

75 casos, 225 equilíbrios 3D,450 vetores de suporte. Compressão inferior de referência nas arestas existentes 18×60, Z60..120, centro 90; braço hipotético 458 mm. Fundo/laterais coplanares não garantem essa área ou centro: medir contato real antes de usar o braço no dimensionamento final.

No alvo 10 kg, máximos separados por suporte: **V262,11 N, T215,62 N e R332,32 N**. [Seis casos simultâneos de qualificação](../Aereos_suspensao/P12_qualificacao_suspensao.csv) conservam os controles V/T/R de cada lado; não combinar máximos de casos diferentes. [Reações inferiores](../Aereos_suspensao/P12_reacoes_inferiores.csv): compressão até 201,99 N, pressão sobre referência 1080 mm²≈0,187 MPa, sem valor admissível atribuído. Partilhas 0/50/100 são sensibilidades, não a rigidez real da montagem.

O conteúdo e os pesos da caixa/portas precisam chegar pelas juntas às laterais/fundo e aos cantos superiores. O fundo atual encontra base e tampo apenas pela aresta: nenhum apoio traseiro contínuo nem Confirmat horizontal novo foi creditado. Base/tampo–laterais/divisor usam os 12 Minifix candidatos; fundo–laterais/divisor usa os 9 Confirmat candidatos. Essas contagens não demonstram transferência, retenção, rigidez ou resistência.

Por 1 kg adicional em v200: +9,807 N vertical, +1,961 Nm e+4,282 N de tração total nesse braço. Incluir massa/centro reais das ferragens. Momentos rxF publicados são redução da mesma força ao canto, sem somar cargas extras ou dividir esforços pelo número de parafusos.

## Pendências objetivas

### Caminho da caixa detalhado em 26/10

[Desenho](../Aereos_suspensao/P12_caminho_caixa.png) · [9 grupos de juntas](../Aereos_suspensao/P12_mapa_juntas.csv) · [21 posições](../Aereos_suspensao/P12_eixos_fixadores.csv) · [30 cortes de carga](../Aereos_suspensao/P12_cortes_carga.csv) · [memória](../Aereos_suspensao/P12_caminho_caixa.json) · [conferência](../Aereos_suspensao/P12_verificacao_caminho.json).

| Caminho nominal | Grupo candidato |
|---|---|
| Base → duas laterais | 4 Minifix; cortante vertical nos pinos horizontais e retenção transversal |
| Base → divisória → tampo | 2 + 2 Minifix; retenção axial nos pinos verticais e contato conforme o sentido da reação |
| Tampo → duas laterais | 4 Minifix; o tampo e suas juntas completam o caminho superior |
| Fundo ↔ laterais/divisória | 6 + 3 Confirmat; transferência vertical e fora do plano até os cantos |
| Cantos → suspensão | Bigfer e contatos inferiores ainda em qualificação |

**O fundo não recebe a base/tampo diretamente:** esses encontros são apenas arestas. Os 12 Minifix e 9 Confirmat mantêm a contagem R00. Estações novas de estudo para os Confirmat: laterais z70/292/514, divisor z88/292/496. São propostas geométricas, sem distância mínima resistente ou piloto demonstrados. Entrada pela lateral externa nas duas bordas; pela traseira no divisor. Comprimento 50 atravessa 18 e deixa 32 mm nominais na peça receptora; Ø7 não define a broca.

As 21 posições, 210 pares de envelopes e acessos contra madeira/calços/suspensores foram conferidos. Reservas externas Ø20×100 pedem espaço de bancada; ferramenta completa, mãos, cabeças, pinos e tolerâncias reais pendentes. Montar base/divisor, fechar tampo em z, encaixar cada lateral em u e instalar o fundo pela traseira. Apertar antes das portas; cabeça lateral aparente e embutimento traseiro precisam de detalhe.

No cenário ρ900 com 10 kg de conteúdo, a fronteira da base transmite V136,62 N; incluindo a divisória, V164,23 N. Para conteúdo frontal, momentos de 36,62/41,42 Nm em torno da origem traseira. O CSV preserva as resultantes simultâneas de cada corte; não são esforços por parafuso nem cargas extras a somar ao equilíbrio global. Um par colinear de Minifix não fecha sozinho um momento em torno da sua linha: a caixa e os contatos precisam participar. Resistência, rigidez e flecha do P12 ainda exigem modelo compatível e dados reais de junta; não se reutiliza a flecha do P17.

Reproduzir: `python -B ferramentas/aereos/mapear_caminho_caixa.py --movel P12` e `python -B ferramentas/aereos/conferir_caminho_caixa.py --movel P12`. Nenhum ensaio físico ou alteração R52.

### Comprovações restantes

1. Produto/oficina: confirmar montagem Bigfer com fundo 18, fixadores MDF/pilotos/profundidade/torque, passo 12/borda 9,5, cabeça/arruela/rasgo 5, retenção, flexão/esmagamento e ferramenta efetiva. Fonte geométrica: catálogo Bigfer p235 já preservado no [estudo de seleção](../Aereos_suspensao/Selecao_ferragem.json); sem capacidade publicada para esta implantação.
2. Projeto/oficina: comprovar base/divisor, juntas e distorção da caixa/fundo até os cantos. Não transferir flecha ou rigidez de P17/P04 ao P12 nem dar resistência às cavilhas/atrito.
3. Laboratório/fabricante/RT: acordar protocolo, replicação, fatores/ciclos/duração e critérios antes de aplicar carga. Usar vetores simultâneos e montagem representativa; registrar deformações, deslizamento, residual e danos.
4. Imóvel/RT: medir parede/revestimento, instalações, contato inferior e posição final sobre a geladeira antes de definir ancoragens. Ventilação e manutenção do aparelho continuam na compatibilização de equipamentos.

Nenhuma mudança de aparência, volume ou uso exigiu nova decisão de Elias nesta etapa. Nenhuma compra, consulta enviada, execução de furos ou alteração R52. Reproduzir na raiz: `python -B ferramentas/aereos/suspender_lote_b.py --movel P12` e `python -B ferramentas/aereos/conferir_suspensao_b.py --movel P12`. Hashes portáveis e solução independente de 6 incógnitas conferem fontes/equilíbrio, sem validar as hipóteses físicas.
