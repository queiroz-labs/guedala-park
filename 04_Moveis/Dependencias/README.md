# Medidas, dependências e roteiro de campo

Base nominal R54: [469 regras](regras.json), 72 dimensões fixas de 20 módulos e 4 bancadas. Referências variáveis e nove fechamentos não são peças de corte. FCStd preservado; a cadeia usa somente exportações existentes.

| Consulta | Arquivo |
|---|---|
| Folha para imprimir | [15 verificações e comando](../../07_Imovel/Roteiro_dia_das_chaves_R01.md) |
| Código → levantamento físico | [Descrição por código](Descricao_fisica.csv) |
| Tabela de 546 códigos retirada da folha | [Criticidade por código](Criticidade_por_codigo.csv) |
| Regeneração externa | [Orquestrador](orquestrar.py) |

PR-FLOORS e outras coordenadas de exportação não têm marco físico demonstrado: descrição pendente. Não converter nomes de objetos em instrução de campo. Medidas horizontais propostas a 1 m do piso acabado; laser/trena e croqui identificam panos. Prumo usa nível laser vertical; esquadro usa laser angular ou esquadro aferido. Essas descrições não são medições feitas.

`python -B 04_Moveis/Dependencias/orquestrar.py --medidas C:/Temp/campo.csv`

A saída externa contém peças preservadas, furação, conflitos, quantitativos, formatos e comparação quantitativa de orçamento. Sem regra por ID, recortes e fechamentos viram pendência; preços ausentes não são zero. Entradas: codigo_medida,valor_medido,evidencia_campo; unidades explícitas e ambos os eixos DIM. Testes de integração: `python -B 04_Moveis/Dependencias/test_cadeia.py`.

## Folgas e paredes

[34 folgas ≤ 15 mm](Folgas_ate_15.csv): inclui 4 negativas nominais. Onde não há pano correspondente, o lado é limite de retângulo de referência, não parede comprovada. Caixas e folgas originais preservadas.

[Modelo de 26 panos](Paredes.csv), [ranking por variância explicada](Ranking_15.csv), [índices por módulo](Variancia_por_modulo.csv) e [resumo](Sensibilidade.json). `python -B 04_Moveis/Dependencias/sensibilidade.py --saida C:/Temp/paredes` gera 5000 pares A/B (10.000 amostras), deslocamento normal±20mm/rotação±1° por pano, datum comum; teto±20mm e piso0–10mm. Retas vêm de PR-WALLS, não das origens independentes dos pisos. Panos compartilhados usam uma única variável. Partes abertas não viram paredes. A identificação física permanece pendente onde o cache não fornece nome inequívoco.

Ranking Sobol de primeira ordem (pick-freeze), ponderado pela variância da menor folga de cada módulo. Estimador bruto preservado; índice exibido truncado0–1 por erro amostral. Interações não se somam à primeira ordem. Brutos ficam externos; hash no resumo. Testes de datum/translação/pano compartilhado em test_sensibilidade.py.

**Pergunta para Elias:** adotar folga de montagem de 10 mm com arremate nos lados hoje com 0 mm? [Impacto por móvel](Pergunta_folga_zero.csv): perda de largura útil e profundidade, sem alterar cotas. Distinguir panos abertos/parede antes de adotar; os conflitos negativos existentes não são resolvidos pela pergunta. Paredes/ancoragem e resistência continuam fora do estudo.
