# Protocolo de datum — proposto

Folha para imprimir e preencher; nenhuma medição feita. Unidade: mm. Não marcar “datum confirmado” no celular até documentar o vínculo com o referencial nominal.

**Referencial documental:** [regras](../04_Moveis/Dependencias/regras.json): X espelhado pela PR-EIXO-X nominal, Y da planta, Z vertical. [Cotas, pranchas.frame](../06_Entregas/Planta_cotada/Cotas.json): X cresce à direita e Y para baixo no desenho; Z sobe desde o piso acabado. A conversão nominal é **X CAD = 7400 − X planta; Y CAD = Y planta; Z CAD = Z planta** (PR-EIXO-X = 7400 mm); não inverter X duas vezes. O formulário recebe coordenadas da planta, não coordenadas CAD espelhadas. [Orientação](../03_Ambientes/Conforto_ambiental/Orientacao.json): alto da imagem com azimute adotado 245° ± 4°; isso orienta a folha, não localiza sua origem nem comprova alinhamento físico.

**Origem física ainda ambígua.** Proposta de campo: M0 no canto interno junto à porta de entrada, com projeção no piso acabado como Z=0. Marcar M1 numa direção paralela à parede da fachada principal: M0→M1 define +X de campo; desenhar +Y perpendicular, voltado ao interior, e registrar o lado. Marcar as faces e fotografar M0/M1 com escala. Esse datum local não coincide automaticamente com a planta/CAD: registrar coordenadas nominais correspondentes, translação, rotação e eventual reflexão; conferir com outro ponto antes de converter. Manter PR-* sem aplicação enquanto esse vínculo estiver pendente.

**Procedimento:** transferir a linha horizontal a **1000 mm do piso acabado** com nível; medir faces acabadas nessa linha com laser/trena. Identificar em croqui M0/M1 e E1/E2 de cada pano; registrar distâncias e azimutes desde M0→M1, instrumento e fotos. Medir alturas e desníveis desde o mesmo piso de referência; anotar se o acabamento estiver ausente. Não converter distância absoluta em avanço de parede sem transformação comum.

**Janelas:** 1 quarto, 2 escritório, 3 sala, 4 lavanderia, 5 banheiro (pranchas.openings). Para cada uma, anotar largura livre entre ombreiras acabadas, altura livre entre peitoril e verga e peitoril desde o piso acabado; repetir nas extremidades/centro e fotografar as faces. Largura/altura ficam no croqui/observação, não substituem PR-X/Y. A associação do canto/face de PR-JANELA-X/Y/Z permanece descrição pendente: **ver protocolo de datum**, identificar o marco antes de preencher; não presumir centro nem eixo do caixilho. DEP-COZ-PRUMO: duas leituras na mesma parede atrás da bancada, baixa e na altura dos aéreos, com alturas anotadas; positivo avança para dentro do vão.

```text
Data: __________  Instrumento: __________  Piso/face: __________
M0 / foto: _________________  M1 / foto: _______________________
M0→M1: ______ mm  Direção +X: ______  Lado +Y: _________________
+------------------------------------------------------------+
|                                                            |
|          Croqui: entrada, fachada, M0/M1, +X/+Y, E1/E2       |
|                                                            |
|                                                            |
+------------------------------------------------------------+
Janela nº: ___  largura: ___/___/___  altura: ___/___/___ mm
Peitoril: ___/___/___ mm  faces/fotos: _________________________
Vínculo à planta (marcos/transformação/conferência): ___________
```

---

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
