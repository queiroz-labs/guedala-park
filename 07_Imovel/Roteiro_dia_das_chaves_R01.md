# Folha de campo — 15 verificações prioritárias

Nominal. Marcar panos e pontos no croqui, medir faces acabadas e repetir leituras. Itens com descrição pendente não devem ser medidos por uma coordenada de computador. O projeto precisa identificar seus marcos físicos.

| Item | O que medir, de onde até onde | Instrumento / altura | Leitura / foto |
|---|---|---|---|
| 1 | cozinha: ângulo entre os dois panos acabados de cada canto que receberá móvel; marcar o canto e os dois panos no croqui; registrar o maior desvio de 90°. | laser angular ou esquadro aferido com duas bases de1m; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 2 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 3 | Avanço da parede acabada atrás da bancada da cozinha entre a leitura baixa e a leitura na altura dos aéreos; positivo para dentro do vão do móvel. | nível laser vertical + régua/trena perpendicular à parede; registrar as duas alturas de leitura | ______ |
| 4 | Descrição pendente: associar cada eixo da cota oficial às duas faces acabadas efetivas no croqui; medir entre essas faces a 1 m do piso, em três posições; não confundir faixa de planta com parede física. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 5 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 6 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 7 | quarto principal: ângulo entre os dois panos acabados de cada canto que receberá móvel; marcar o canto e os dois panos no croqui; registrar o maior desvio de 90°. | laser angular ou esquadro aferido com duas bases de1m; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 8 | Descrição pendente: associar cada eixo da cota oficial às duas faces acabadas efetivas no croqui; medir entre essas faces a 1 m do piso, em três posições; não confundir faixa de planta com parede física. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 9 | banheiro: ângulo entre os dois panos acabados de cada canto que receberá móvel; marcar o canto e os dois panos no croqui; registrar o maior desvio de 90°. | laser angular ou esquadro aferido com duas bases de1m; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 10 | lavanderia: ângulo entre os dois panos acabados de cada canto que receberá móvel; marcar o canto e os dois panos no croqui; registrar o maior desvio de 90°. | laser angular ou esquadro aferido com duas bases de1m; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 11 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 12 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 13 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 14 | Descrição pendente: identificar em croqui a parede/face e o marco físico comum antes de medir este código. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |
| 15 | Descrição pendente: associar cada eixo da cota oficial às duas faces acabadas efetivas no croqui; medir entre essas faces a 1 m do piso, em três posições; não confundir faixa de planta com parede física. | laser de distâncias + trena; nível laser para transferir o datum; 1.000 mm do piso acabado, para medidas horizontais | ______ |

O mapeamento de escritório e a tabela completa foram separados da folha: [descrições físicas](../04_Moveis/Dependencias/Descricao_fisica.csv) e [546 códigos](../04_Moveis/Dependencias/Criticidade_por_codigo.csv). A ordem será atualizada pelo modelo de paredes com datum comum. Limiares geométricos não são tolerâncias de obra.

Após preencher CSV externo com codigo_medida,valor_medido,evidencia_campo, executar da raiz do repositório:

```powershell
python -B 04_Moveis/Dependencias/orquestrar.py --medidas C:/Temp/campo.csv
```

Saída temporária externa. Não altera caixas nem incorpora medidas na base.
