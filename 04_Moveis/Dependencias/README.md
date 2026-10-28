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

A sensibilidade de origens independentes e a antiga lista de criticidade foram identificadas como inadequadas para inferir tolerância física; o ranking será substituído por paredes em datum comum. Valores anteriores permanecem apenas como comparação até essa substituição. Nenhuma folga ou caixa foi alterada.
