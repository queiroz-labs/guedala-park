# Banquinho: alternativa baixa sob a TV do escritório

30/09/2026. Estudo autônomo com os arquivos existentes, sem Firecrawl ou outra pesquisa externa. [Prancha interativa](Banquinho_alternativa.html).

## Conclusão

A guarda sob a TV **cabe estaticamente sob condições**, mas ainda não demonstra o acesso fácil exigido por Elias. Manter como candidato para gabarito; não instalar suporte nem acrescentar marcenaria. A faixa baixa junto à janela da lavanderia continua descartada conforme o estudo anterior, compreendido por Elias. Isso não descarta a lavanderia inteira.

Preservados banquinho BTF ESC0071, sofá, cadeira no escritório durante visitas, prateleira dos consoles a 195 cm e posições vigentes de estudo. Não usar baú ou exigir retirada de móveis como solução de guarda. Não há novo aceite do usuário para esta localização.

## Bases e coordenadas

Todas as medidas em centímetros. Escritório 230 × 295; origem na janela, x da esquerda à direita e y rumo à entrada.

- [Modelo e alcance do banquinho](../Lavanderia/Banquinho_modelo_e_alcance_2026-09-25.md): corpo fechado 39,5 × 19,5 × 75; reserva original 45 × 25 × 85. Referência documental, sem atualização comercial.
- [Sofá e porta R11](../Escritorio/Sofa_e_porta_R11.md): cama x=2–142, y=110–292; cadeira nas visitas x=150–224,5, y=75–148; eixo hipotético da porta (220,295), folha de referência 75.
- [TV e PS5 R08](../Escritorio/TV_e_PS5_R08.md): centro de TV proposto a 110 e envelope vertical 58, borda inferior 81. Altura ainda não aprovada. Prateleira 110 × 35, topo 195 aprovado; posição longitudinal ainda de estudo.
- [Modelo interativo](../Estudo_interativo/src/app.js): sofá fechado x=2–92, y=152–292; cadeira diária x=112,75–187,25, y=80–153; bancada x=15–215, y=0–70. TV do modelo projeta até x=218 e tem borda inferior 82. Usado **81**, mais restritivo, para a altura; projeção 218 continua hipótese, especialmente com suporte articulado.

## Posição candidata e contas

Reserva em planta x=205–230, y=165–210: 25 de projeção × 45 ao longo da parede. O corpo real deixa 5,5 cm na profundidade e 5,5 no comprimento para distribuição entre afastamentos e ferragens; não são folgas garantidas sem conhecer rodapé e suporte.

| Relação | Conta | Resultado |
|---|---|---|
| Passagem residual junto à cama, guardado | 205 − 142 | 63 |
| Redução da faixa bruta | 88 − 63 | 25 |
| Distância longitudinal à cadeira nas visitas | 165 − 148 | 17 |
| Distância longitudinal à cadeira diária | 165 − 153 | 12 |
| Topo do corpo sobre apoio baixo | 75 + 3 | 78 |
| Folga até TV do estudo | 81 − 78 | 3 |
| Reserva antiga de 85 sobre o piso | 85 − 81 | 4 de sobreposição |

Não se reduziu silenciosamente a reserva antiga: a altura de 85 deixa de servir aqui. O novo ensaio depende de um berço baixo com apoio a **no máximo 3 cm**, sem caixa envolvente e sem ferragem superior que interfira na TV. A liberação deve ocorrer horizontalmente; não há curso demonstrado para desengatar para cima. Tipo de retenção, pega e estabilidade do banquinho fechado continuam a definir. Não é desenho de fabricação.

## Retirada: objeto e pessoa são conferências diferentes

Translação reta de 15 para a esquerda leva a reserva a x=190–215, y=165–210. A face posterior fica 3 à frente da projeção da TV em x=218. Só depois desse deslocamento se considera levantar, ainda dependendo de cabos, suporte e mãos. Folga residual à cama: 190−142=48. Ao sofá fechado: 190−92=98.

O script confere 151 posições da translação contra cama, cadeira estacionada e bancada, sem interseções dos retângulos. Como a faixa longitudinal do banquinho permanece y=165–210, ela fica após cadeira/bancada durante todo o percurso; sua menor coordenada x=190 também fica fora da cama até x=142. Essa separação analítica complementa as amostras. A distância mínima ao eixo da porta é 85: sobra 10 para folha 75 e 5 para folha 80. Usar o disco inteiro é conservador em relação ao setor idealizado; maçaneta, eixo real e espessuras não modelados.

**48 não é passagem livre validada para uma pessoa carregando o banquinho.** Não foram simulados braços, corpo, rotação, transporte até a saída ou mecanismo de abrir/fechar o sofá. As posições finais do sofá não provam que o banquinho possa permanecer nesse local durante sua transformação. Esses limites impedem declarar a guarda resolvida ou incorporá-la ao modelo vigente.

## Gabarito preparado para a próxima conferência física

1. Marcar no piso o retângulo de 45 × 25 na parede direita, entre 165 e 210 da janela. Representar a cama e cadeira nas coordenadas acima, sem retirar a cadeira do escritório.
2. Usar corpo leve de 39,5 × 19,5 × 75, com reserva externa de planta 45 × 25; marcar TV real e projeção do suporte/cabos. Conferir se apoio de até 3 e topo a 78 preservam a folga vertical.
3. Testar pega e retirada inicial de 15 sem levantar, com a cama aberta. Registrar espaço ocupado pela pessoa e eventual contato; não contar a faixa de 48 como demonstração prévia de conforto.
4. Testar transporte e transformação completa do sofá, mantendo o gabarito guardado. Se exigir mover o banquinho sempre que preparar a cama, a alternativa perde prioridade pelo requisito de acesso simples.
5. Conferir porta, maçaneta e rodapé reais. Se qualquer condição falhar, procurar outro local; não elevar a TV nem diminuir móveis automaticamente.

O gabarito está especificado, **não executado**. A alternativa é mais promissora no uso diário, porém ainda não satisfaz de forma comprovada todos os modos de uso. A trajetória rígida do sofá fechado foi confrontada abaixo; a próxima confirmação depende da operação real, antes de detalhar ferragens.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/banquinho_alternativa.cjs`. Gera a prancha e [resultados numéricos](Resultados_banquinho.json). Sem compras, publicação ou alteração de escolhas aprovadas.

## Conferência adicional da manobra rígida do sofá

A sequência F93/F94 do [R07](../Escritorio/Ajuste_sofa_e_UltraComfort_R07.md) leva o centro (47,222) a (87,205), gira 90° e segue a (72,247). Na primeira translação o limite direito é 87+45=132; no giro inteiro, o círculo envolvente de raio √(45²+70²)=83,2166 limita x a 170,2166; na segunda translação, o limite é 87+70=157. O banquinho guardado começa em x=205: separação mínima conservadora de **34,7834 cm**, válida para toda a rotação, sem depender de amostragem.

Isso prova ausência de nova colisão com o banquinho na trajetória rígida proposta. Não revalida as folgas antigas entre sofá e cadeira/porta, não inclui o operador e não modela o mecanismo intermediário de abertura. A cama final x≤142 também não intercepta a guarda.


**Continuação de 30/09:** [Sequência com gabarito de pessoa](Banquinho_operacao.md) acrescenta aproximação, retirada e transporte até antes da soleira. Hipótese de corpo 40 × 50 deixa 5 cm à cama, mas apenas 2 cm de um lado do vão ideal na trajetória escolhida. Candidato secundário; não há validação física de acesso.
