# Aéreo C — alternativa de ligação desmontável

Arquivo `AereoC_Minifix_R45_ESTUDO.FCStd`. Preserva a caixa externa e os quatro vãos internos, sem inserir suportes salientes. A R44 não foi editada. A alternativa trata as três prateleiras como fixas desmontáveis; não deve ser aplicada caso devam continuar reguláveis.

Seleção dimensional: Minifix 15 para painel 18 sem aba, natural 262.26.034, com pino S100 262.28.920, rosca especial para pré-furo 5, comprimento de rosca 8 e B34. Alojamento Ø15, profundidade 13,5+0,5, eixo A9. Passagem para cabeça Ø7. [Catálogo oficial Häfele, páginas impressas FF2.10, FF2.14 e FF2.17](https://hafelethailand.com/wp-content/uploads/2025/12/02-connector-technology-shelf-supports.pdf).

## Arranjo verificável

Cinco painéis horizontais Peca327–331, quatro conjuntos em cada: 20 caixas e 20 pinos. Dois pontos por extremidade, Y6730 e 6922, a 60 mm das bordas. Eixos das caixas X2400 e 2843, a 34 mm das extremidades. O eixo do pino fica 9 mm acima da face inferior do painel. Furação cega proposta dos pinos 8,5 mm; conferir ponta da ferramenta. Acesso às caixas pela face superior da base e inferior das demais peças. Coordenadas completas em `Minifix_C.json`.

| Verificação | Resultado |
|---|---|
| Madeira atrás da caixa com furo máximo 14 e chapa 18 | 4 mm nominal; 3,7 mm se a chapa medir 17,7 |
| Madeira atrás do piloto 8,5 em lateral 18 | 9,5 mm nominal, sem ponta de broca |
| Distância da caixa Ø15 à borda extrema da prateleira | 26,5 mm |
| Distância da caixa às bordas dianteira/traseira | 52,5 mm |
| Painéis após os cortes | Sete formas válidas |
| Alojamentos versus 38 sólidos de ferragens/frentes do módulo | Zero interseções volumétricas |
| Compartimentos internos | 511×312 mm; alturas 180 /192 /258 /298 mm preservadas |

As caixas e passagens são volumes de furação, não representações exatas do produto. O ensaio cobre interferência dos alojamentos, não ferramenta de montagem, percurso de fechamento da frente ou resistência da união. Cargas, contribuição do fundo e fixação à parede ainda requerem dimensionamento. A compra depende da disponibilidade brasileira do par exato.

Não copiar automaticamente esta furação para divisórias 18 com ligações dos dois lados: dois pilotos 8,5 deixam apenas 1 mm nominal entre fundos, antes das pontas das brocas. Desencontrar alturas/posições ou especificar solução própria; o divisor duplo 36 existente em alguns aéreos é outro caso.
