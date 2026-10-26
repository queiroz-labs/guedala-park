# P12 — caixa e suspensão acima da geladeira

Estudo nominal separado,26/10/2026. Elias,25/10/2026:“20 kg / 10 kg / 10 kg” na ordemP17/P04/P12; usoP12: utensílios grandes/leves de cozinha usados ocasionalmente. [Premissas](../Aereos_suspensao/Lote_B_premissas.json). Base limpa, sem cabeças/tampinhas aparentes por baixo. Nenhum ensaio físico ou capacidade demonstrada.

| Item | Estado vigente do estudo |
|---|---|
| Caixa | 801×330×584mm externos; largura interna765; laterais/base/tampo/divisor18 |
| Fundo | Peca344,765×548×18 atual, preservado. A decisão de desenvolver fundos inteiros abrangeuP17/P04 |
| Conteúdo | Meta10kg total; cenários distribuídos/frontais e portas independentes herdados do loteB, sem carga por compartimento definida |
| Massa nominal | Madeira+conteúdo32,75–41,51kg; densidades/espessuras hipotéticas, sem ferragens reais |
| Ligações | 12Minifix/9Confirmat candidatos reconciliados comR00; não somar como compras novas |
| Suspensão | Bigfer04.02.058 candidata nos dois cantos laterais/fundo18; dois suportes são hipótese |

[Implantação e memória](../Aereos_suspensao/P12_suspensao.json) · [desenho](../Aereos_suspensao/P12_suspensao.png) · [conferência independente](../Aereos_suspensao/P12_verificacao_suspensao.json) · [requisitos preparados para produto/oficina](../Aereos_suspensao/P12_qualificacao_suspensao.txt).

## Posição e acesso

Coordenadas desde a esquerda interna, traseira para frente e base externa: assentos u40,5/724,5 e Z548. Metal envolvido por49,5×37,8×16 por canto, aproximadamente60mL/par; sem cabeças/capa/reserva de ferramenta nesse volume. Fundo na posição atual, sem reduzir os312mm úteis nominais de profundidade.

A altura herdadaH−58=526 colocava o corredor do auxiliar traseiro nos calços superiores. A propostaH−36=548 sobe22mm, deixa10mm entre metal e tampo e mantém os quatro calços fixos fora dos corredores. Os12 acessosMinifix internos também foram conferidos. Acessos sem interseção das caixas nominais de madeira/calços não comprovam ferramenta real ou ergonomia.

**Auxiliar traseiro junto à lateral:** eixo u9,5/755,5; corredorØ20 invade0,5mm a lateral. A reservaØ12 deixa3,5mm nominais até a lateral e passa pelos calços na nova altura. Ponta/cabeça, corpo da ferramenta, mãos e acesso através do próprio suporte precisam de verificação após escolher os fixadores. Não é indicação de pilotoØ12 ou parafusoØ12.

Montar a caixa e apertar conectores antes das portas; manutenção com portas desclipadas/removidas, mantendo os calços. Rasgos espelhados pedem deslocamentos opostos: rejeitado encaixe por uma translação única. Proposta de gabinete sustentado/nivelado e inserção/aperto pela frente, sujeita à confirmação do fabricante; retirada também com apoio. Corpos das dobradiças/portas em movimento não foram validados nesta etapa.

## Solicitações e caminho resistente

75 casos,225 equilíbrios3D,450 vetores de suporte. Compressão inferior de referência nas arestas existentes18×60, Z60..120, centro90; braço hipotético458mm. Fundo/laterais coplanares não garantem essa área ou centro: medir contato real antes de usar o braço no dimensionamento final.

No alvo10kg, máximos separados por suporte: **V262,11N, T215,62N e R332,32N**. [Seis casos simultâneos de qualificação](../Aereos_suspensao/P12_qualificacao_suspensao.csv) conservam os controlesV/T/R de cada lado; não combinar máximos de casos diferentes. [Reações inferiores](../Aereos_suspensao/P12_reacoes_inferiores.csv): compressão até201,99N, pressão sobre referência1080mm²≈0,187MPa, sem valor admissível atribuído. Partilhas0/50/100 são sensibilidades, não a rigidez real da montagem.

O conteúdo e os pesos da caixa/portas precisam chegar pelas juntas às laterais/fundo e aos cantos superiores. O fundo atual encontra base e tampo apenas pela aresta: nenhum apoio traseiro contínuo nem Confirmat horizontal novo foi creditado. Base/tampo–laterais/divisor usam os12Minifix candidatos; fundo–laterais/divisor usa os9Confirmat candidatos. Essas contagens não demonstram transferência, retenção, rigidez ou resistência.

Por1kg adicional emv200: +9,807N vertical,+1,961Nm e+4,282N de tração total nesse braço. Incluir massa/centro reais das ferragens. MomentosrxF publicados são redução da mesma força ao canto, sem somar cargas extras ou dividir esforços pelo número de parafusos.

## Pendências objetivas

1. Produto/oficina: confirmar montagemBigfer com fundo18, fixadoresMDF/pilotos/profundidade/torque, passo12/borda9,5, cabeça/arruela/rasgo5, retenção, flexão/esmagamento e ferramenta efetiva. Fonte geométrica: catálogoBigferp235 já preservado no [estudo de seleção](../Aereos_suspensao/Selecao_ferragem.json); sem capacidade publicada para esta implantação.
2. Projeto/oficina: comprovar base/divisor, juntas e distorção da caixa/fundo até os cantos. Não transferir flecha ou rigidez deP17/P04 aoP12 nem dar resistência às cavilhas/atrito.
3. Laboratório/fabricante/RT: acordar protocolo, replicação, fatores/ciclos/duração e critérios antes de aplicar carga. Usar vetores simultâneos e montagem representativa; registrar deformações, deslizamento, residual e danos.
4. Imóvel/RT: medir parede/revestimento, instalações, contato inferior e posição final sobre a geladeira antes de definir ancoragens. Ventilação e manutenção do aparelho continuam na compatibilização de equipamentos.

Nenhuma mudança de aparência, volume ou uso exigiu nova decisão de Elias nesta etapa. Nenhuma compra, consulta enviada, execução de furos ou alteraçãoR52. Reproduzir na raiz: `python -B ferramentas/aereos/suspender_lote_b.py --movel P12` e `python -B ferramentas/aereos/conferir_suspensao_b.py --movel P12`. Hashes portáveis e solução independente de6 incógnitas conferem fontes/equilíbrio, sem validar as hipóteses físicas.
