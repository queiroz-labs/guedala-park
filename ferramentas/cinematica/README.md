# Cinemática das folhas para cálculos sem abrir o FreeCAD

Motor numérico e memória de extração R51, de25/10/2026. **O modelo vigente é R52**; usar a [fotografia e consulta vinculadas à R52](../../04_Moveis/Proximas_decisoes/Cinematica/README.md) para a continuidade. Os dados R51 abaixo são a origem histórica do motor; não foram rebatizados ou sobrescritos. A fotografia R52 já demonstrou igualdade das folhas/planilhas, conforme sua própria conferência.

O módulo carrega uma fotografia de aproximadamente154 KB, com867 células de quatro planilhas e24 folhas. A consulta normal inclui22 visíveis; duas folhas antigas ocultas continuam identificadas e são excluídas por padrão. Não se reativou abertura antiga do gabinete do banheiro nem se substituiu o mecanismo atual.

## O que foi resolvido

A extração anterior de528 referências exigiu cálculos nativos do FreeCAD. Os próximos estudos podem usar os dados salvos e repetir a matemática sem reabrir o arquivo completo ou recalcular planilhas na interface. O módulo entrega a matriz de transformação da folha e o CG das frentes recortadas.

Foram conservadas as translações e rotações das **quatro barras existentes**, inclusive o eixo nativo−Z desta fotografia e a transformação dos módulos no apartamento. Usar apenas um giro em torno de um pino, ou trocar o eixo por+Z, mudaria os resultados.

O interpretador aceita somente a aritmética necessária, referências presentes na fotografia e as funções`sin`, `cos`, `atan2`, `sqrt`, `min` e`max`. Não usa`eval`/`exec` e rejeita chamadas/atributosPython externos. Graus e milímetros seguem as expressões extraídas; isto não é um interpretador geral de toda a linguagem do FreeCAD. Novas fórmulas, operadores ou unidades exigem nova conferência.

## Verificação e tempo medido

| Conferência | Resultado |
|---|---|
| 522 poses nativas P04/P15, seis folhas de0 a86° | Erro máximo do CG ≈1,82×10⁻¹² mm |
| Seis referências adicionais R12, duas folhas em0/45/86° | Erro máximo ≈9,09×10⁻¹³ mm |
| 24 folhas na posição fechada original | CG idêntico à fotografia nativa |
| 22 visíveis ×87 ângulos | 1914 matrizes finitas, rotação ortogonal e determinante1 |
| Três expressõesPython fora do escopo | Rejeitadas |
| R51 | SHA256 preservado |

Na medição local, após carregar a fotografia, calcular os522 CG levou aproximadamente **0,05 segundo**, mediana de três rodadas. O [registro de verificação](Verificacao.json) contém os tempos exatos. É tempo da rotina de cálculo, não novo tempo de abertura do projeto nem promessa de desempenho de outro computador. Não foi feita comparação percentual com a extração nativa, que inclui operações diferentes.

## Como consultar a memória R51

Requer Python e NumPy; os próximos cálculos não precisam do FreeCAD instalado. A extração inicial já está salva.

```powershell
python consultar.py --listar
python consultar.py --folha Folha014 --angulo 86
python verificar.py
```

Executar na pasta deste relatório. A consulta retorna apenas os dados necessários. A opção`--incluir-ocultas` permite consulta histórica explícita; não modifica o projeto. O intervalo validado é0–86°, respeitando também os limites que as próprias fórmulas da fotografia aplicam. O curso de estudo não comprova batente físico.

Em outro script local:

```python
from cinematica import Engine
engine = Engine()
centros = engine.centers('Folha014', 86)
matriz = engine.placement('Folha014', 86)
```

Ao modificar geometria, controles ou fórmulas no CAD, gerar nova fotografia com as folhas fechadas e validar de novo. Não sobrescrever entradas de um estudo anterior como se ainda fossem a mesma revisão. O extrator apenas lê a fonte; a referência adicional R12 usa e fecha somente seu documento temporário próprio.

## Aplicação e limites

A rotina fornece massa/centro de gravidade para estudos com fonte identificada. Na continuidade vigente, usar a consulta R52 acima; não repetir varreduras dos estudos já condicionados a produto/oficina. [P04/P15](../../04_Moveis/P04/Suspensao_P04_P15/README.md) já fornecem referências verificadas e cenários de parede. O mecanismo completo inclui braços de dobradiça com movimentos próprios: não atribuir a posição da frente a todas as massas de ferragem.

A rotina não verifica BREP em colisão, resistência, parafusos, tolerâncias, fabricação ou conforto de uso. Massas reais e propriedades dos produtos continuam pendentes nos respectivos estudos. A R51 não foi salva ou animada para esta entrega; nenhum movimento, detalhe ou acabamento foi removido.

[Fotografia da R51](Snapshot_R51.json) · [motor numérico](cinematica.py) · [consulta](consultar.py) · [referência nativa complementar](Referencia_nativa_R12.json) · [verificador](verificar.py).
