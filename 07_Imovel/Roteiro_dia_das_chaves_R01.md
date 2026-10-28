# Folha de campo — 15 medidas prioritárias

Medir faces acabadas a 1 m do piso. Marcar a estação M0, a direção M0→M1 e dois extremos E1/E2 de cada pano no croqui. Vínculo desses marcos ao datum nominal: descrição pendente; definir antes de converter leituras. Distância e azimute das duas visadas permitem reconstruir a reta no mesmo referencial.

| Item | Medida física | Instrumento / registro | Leitura / foto |
|---|---|---|---|
| 1 | Face acabada da parede atrás da bancada da cozinha e do tanque; marcar extremos do pano junto à cozinha e lavanderia. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 2 | Face acabada da parede atrás da bancada da cozinha e do tanque; marcar extremos do pano junto à cozinha e lavanderia. | Orientação da reta E1–E2 em relação a M0→M1: mesmas duas visadas com distância e azimute, altura1m; calcular no escritório. | d1____ az1____ d2____ az2____ foto____ |
| 3 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 4 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 5 | Face acabada da parede da cabeceira e aéreo P04 no quarto; marcar os dois extremos do pano no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 6 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 7 | Face acabada da parede da cabeceira e aéreo P04 no quarto; marcar os dois extremos do pano no croqui. | Orientação da reta E1–E2 em relação a M0→M1: mesmas duas visadas com distância e azimute, altura1m; calcular no escritório. | d1____ az1____ d2____ az2____ foto____ |
| 8 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 9 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 10 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Orientação da reta E1–E2 em relação a M0→M1: mesmas duas visadas com distância e azimute, altura1m; calcular no escritório. | d1____ az1____ d2____ az2____ foto____ |
| 11 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 12 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Orientação da reta E1–E2 em relação a M0→M1: mesmas duas visadas com distância e azimute, altura1m; calcular no escritório. | d1____ az1____ d2____ az2____ foto____ |
| 13 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Orientação da reta E1–E2 em relação a M0→M1: mesmas duas visadas com distância e azimute, altura1m; calcular no escritório. | d1____ az1____ d2____ az2____ foto____ |
| 14 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |
| 15 | Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui. | Visadas M0→E1 e M0→E2: distância e azimute desde M0→M1; laser de distâncias com base angular ou estação total. Altura1m. | d1____ az1____ d2____ az2____ foto____ |

[Mapeamento de códigos e marcos pendentes](../04_Moveis/Dependencias/Descricao_fisica.csv) · [tabela de 546 códigos](../04_Moveis/Dependencias/Criticidade_por_codigo.csv). Ordem por variância explicada da menor folga; não é tolerância de obra.

Depois de preencher o CSV de campo, executar da raiz:

```powershell
python -B 04_Moveis/Dependencias/orquestrar.py --medidas C:/Temp/campo.csv
```
