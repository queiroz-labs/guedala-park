# Auditoria dos quantitativos — R41

21/10/2026. Contagem extraída do documento FreeCAD ativo, sem alterar peças ou movimentos. **56 conjuntos 71B3550, cada um com um calço 173H7100: 56 calços.** A matriz R38 dizia 54 e essa contagem foi repetida no complemento documental; ambos estão corrigidos. As duas dobradiças adicionais do aéreo C constam como terceira dobradiça de cada porta, já no modelo; não foram acrescentadas nesta auditoria.

## Contagem por móvel

| Móvel / conjunto | Dobradiças | Calços |
|---|---:|---:|
| Canto R04 - portas independentes - proposta simples | 4 | 4 |
| Gabinete da pia | 4 | 4 |
| D · acima do depurador | 4 | 4 |
| C · uso diário | 6 | 6 |
| B · acima do micro | 4 | 4 |
| A · acima da geladeira | 4 | 4 |
| Aéreo da lavanderia | 4 | 4 |
| Aéreo principal do escritório | 8 | 8 |
| Aéreo raso da cabeceira · alinhado | 8 | 8 |
| Gabinete do banheiro | 4 | 4 |
| Armário espelhado raso | 6 | 6 |
| **Total** | **56** | **56** |

Critério: contar os conjuntos App::Part identificados como 71B3550, não suas peças internas. Foram encontrados 86 rótulos começando com esse código, mas 30 são subpeças; contá-los como dobradiças geraria duplicação. Os 56 conjuntos estão com visibilidade própria ligada e cada um possui exatamente um calço, sem calço repetido entre conjuntos. A quantidade representa o estudo desenhado; não certifica carga, furação, acabamento ou seleção definitiva.

## Gavetas e composição dos kits

| Móvel / gaveta | Objeto | Curso de referência (mm) | Acoplamentos |
|---|---|---:|---:|
| Guarda-roupa · inferior R02 / Gaveta de roupa | Gaveta | 500 | 2 |
| Guarda-roupa · inferior R02 / Gaveta de roupa001 | Gaveta001 | 500 | 2 |
| Guarda-roupa · inferior R02 / Gaveta de roupa002 | Gaveta002 | 500 | 2 |
| Guarda-roupa · inferior R02 / Gaveta de roupa003 | Gaveta003 | 500 | 2 |
| Gaveteiro G1 / G2 / G3 / G3 · mantimentos | Gaveta004 | 500 | 2 |
| Gaveteiro G1 / G2 / G3 / G2 · utensílios | Gaveta005 | 500 | 2 |
| Gaveteiro G1 / G2 / G3 / G1 · talheres | Gaveta006 | 500 | 2 |
| Gaveteiro do escritório / Gaveta escritório 1 | Gaveta008 | 400 | 2 |
| Gaveteiro do escritório / Gaveta escritório 2 | Gaveta009 | 400 | 2 |

Confirmados 9 pares de guias: 7 de referência 500 mm e 2 de 400 mm, e 18 acoplamentos T51.7601, dois por gaveta. Os identificadores CAD dos acoplamentos estão preservados no inventário. Não somar outro par de acoplamentos quando o kit comercial já os incluir. Peças internas de uma guia telescópica não são pares extras de corrediça.

## Divergência de código que permanece aberta

Rótulos de peças importadas das guias incluem **760H5001S / 760H4001S**, enquanto as notas de seleção anteriores citam **760H5000S / 760H4000S**. Não se conclui equivalência apenas pela semelhança do nome ou comprimento. Isso fica identificado para conferir a documentação exata antes do pedido; não renomear a geometria importada para esconder a diferença. Não houve troca de ferragem ou validação de TIP-ON nesta etapa.

## Evidência e limites

[Inventário completo extraído](Inventario_extraido.json) · [Dobradiças por objeto](Dobradicas_por_objeto.csv) · [Gavetas por objeto](Gavetas_por_objeto.csv).

A auditoria resolve a contagem e o vínculo de cada calço/acoplamento ao conjunto. Não é lista de corte nem lista de compra liberada. Não inclui parafusos, limitadores, ferragens dos produtos comprados prontos ou uniões de marcenaria ainda não detalhadas. Os testes de movimento anteriores continuam com seus limites; não foram repetidos sem alteração geométrica.
