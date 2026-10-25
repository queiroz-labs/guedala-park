# Purangi + Cornalina: verificação de vedação e abertura

23/10/2026. **Resultado: compatibilidade integral não comprovada; troca não liberada.** A autorização de atualizar projeto e orçamento dependia de tudo estar correto. Os dados encontrados não permitem atender a essa condição. R45 principal e valores definitivos preservados.

## Fontes verificadas

Página oficial da Purangi baixa preta HTC0757, desenho cotado, cinco fotos adicionais e manual que inclui o SKU. A foto Purangi_5.webp mostra alavanca levantada, porém não contém escala, posição do eixo ou ângulo máximo. Não medir curso mecânico a partir de fotografia em perspectiva.

- [Produto](https://www.pingoo.casa/torneira-para-banheiro-misturador-monocomando-purangi-baixa-preto-preto).
- [Manual oficial](https://www.pingoo.casa/upload/produto/arquivo/torneira-para-banheiro-misturador-monocomando-purangi-baixa-preto-preto-2696.pdf), cópia Fontes/Purangi_manual.pdf.
- [Desenho](https://www.pingoo.casa/upload/produto/imagem/b_torneira-para-banheiro-misturador-monocomando-purangi-baixa-preto-8.webp).

## Vedação: pendência objetiva

Furo Cornalina Ø37 mm; base Purangi45×45 mm. Centrados, há4 mm de cobertura lateral por lado. Isso demonstra cobertura geométrica da base, não largura de contato do vedante.

O manual indica broca35 mm e mostra anel, arruela e porca sem dimensões. Não informa a faixa de furo admitida, diâmetros do anel, espessura máxima fixável ou espessura real da mesa da Cornalina. As fotos adicionais não mostram a face inferior nem o kit cotado. **Não é possível afirmar nem negar a vedação37 mm apenas com esses dados.** Não adaptar arruelas, vedantes ou furação sem especificação.

## Abertura e luminária: estudo no contexto R45

Foi identificada a consolidação R45 mais recente e usada como referência. Seu documento aberto tem nome interno Guedala_Park_R45_EM_REVISAO, mas o arquivo é Guedala_Park_R45_Consolidado.FCStd. As cotas do entorno permanecem iguais às da conferência anterior: mesa da cuba no estudo895 mm, luminária1110–1130 mm e base do espelheiro1150 mm.

Foi criado **Purangi_R45_SENSIBILIDADE.FCStd**, separado, com corpo simplificado, caixa envolvente da alavanca e contexto copiado da R45. A posição do furo da Cornalina continua hipotética, x3060/y5172 mm; não há gabarito executivo dessa posição.

| Ensaio | Luminária | Base do espelheiro |
|---|---:|---:|
| Torneira fechada |60 mm|100 mm|
| Hipótese de45°, pivô na cota127 mm acima da base e centralizado no corpo, sem giro lateral |19,005 mm|62,378 mm|

Distâncias são entre sólidos da simulação, não cotas certificadas da torneira aberta. Na hipótese45°, topo1091,650 mm. A diferença vertical até a luminária é18,350 mm; distância tridimensional mínima19,005 mm.

Foram calculadas135 combinações: elevação0/15/30/45/60°, giro lateral−45/0/+45°, pivôs em127/141/155 mm acima da mesa e posições em profundidade−17,5/0/+17,5 mm em relação ao eixo assumido. **As posições extremas são ensaios de sensibilidade, não posições documentadas do mecanismo.** O envelope inclui vazios da alavanca. Oito combinações extremas apresentam interseção desse envelope com a luminária; isso NÃO demonstra colisão da peça real, mas impede transformar as hipóteses em aprovação. Nenhum dos envelopes testados atingiu o espelheiro.

O espaço da mão não foi validado: ausência de colisão da peça não comprova ergonomia. Não se prescreve elevar o móvel ou reposicionar a luminária sem necessidade comprovada. Armazenamento preservado.

O arquivo de resultados contém parâmetros e todas as distâncias/interseções: **Purangi_abertura_R45.json**. Todas as formas do estudo são válidas; hash SHA256 do principal antes e depois idêntico. O estudo não foi incorporado ao principal.

## Orçamento

Oferta consultada R$284,90 Pix/boleto, sem frete, permanece cenário. Redução potencial465,10 contra provisão Arion750 ou355,10 contra meta640. Cornalina147,90 + Purangi284,90 =432,80, sem válvula e frete. Valores ainda não substituídos no orçamento definitivo; reserva10 mil e sofá Bonnie preservados.

## Dados necessários para resolver

Confirmação escrita da Pingoo ou medição do kit: compatibilidade explícita entre Purangi HTC0757 e Cornalina HLC0012-1 de furo37 mm, espessura fixável, desenho da alavanca totalmente aberta e espaço de operação. Confirmar também unidade da pressão “30–120” do anúncio. Não basta uma resposta genérica “serve em cuba de apoio”.

Mensagem técnica preparada em **Consulta_Pingoo.txt**, sem envio. Recebendo as medidas, substituir as hipóteses e repetir os testes antes de atualizar o principal e contabilizar economia.
