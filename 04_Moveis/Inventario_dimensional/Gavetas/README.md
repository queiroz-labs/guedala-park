# Gavetas — conferência vigente P01/P06

T05, 26/10/2026. Sete gavetas conferidas na base persistida R52 contra a [instrução FGVTN arquivada](../../Avanco_pendencias/Ferragens/FGVTN_Oculta_ET_montagem_Set24.png), linha **500 mm**. [Dados por gaveta e hashes](Conferencia_P01_P06.json). Modelo não aberto nem alterado; nenhum ensaio físico. Relatórios antigos de carga/alternativas nesta pasta permanecem evidências históricas, não aprovação da montagem.

## Resultado dimensional

| Grandeza | P01: quatro gavetas | P06: três gavetas |
|---|---:|---:|
| Vão interno A do móvel | 355 mm | 583 mm |
| Profundidade interna do móvel | 550 mm | 572 mm |
| Margem sobre P1 mínimo 520 | 30 mm | 52 mm |
| Profundidade das laterais salvas | 490 mm | 490 mm |
| Profundidade P na linha FGVTN 500 | 500 mm | 500 mm |
| Largura interna entre laterais salva | 313 mm | 541 mm |
| Nominal do desenho A−41 | 314 mm | 542 mm |
| Intervalo do desenho +1/−0,5 | 313,5–315 mm | 541,5–543 mm |
| Espessura das laterais | 15 mm | 15 mm |
| Folga atual até fundo do móvel | 52 mm | 84 mm |

**Há espaço em profundidade, mas a caixa salva não corresponde integralmente à receita FGVTN 500:** faltam 10 mm na profundidade e a largura interna fica 0,5 mm abaixo do limite inferior transcrito. As laterais 15 mm estão abaixo do máximo 16 do desenho; isso não encerra a geometria vertical.

A comparação histórica com caixas candidatas 344/572 mm de largura externa e 500 mm de profundidade não foi incorporada à R52. A geometria atual continua com largura externa 343/571 e profundidade 490. Acrescentar 10 mm apenas para trás deixaria 42/74 mm até o fundo, mas isso é aritmética de espaço: recortes, furação, engates, frente e armazenamento devem ser compatibilizados antes de qualquer mudança.

Os 14 objetos de engate nas sete gavetas ainda trazem referência **T51.7601**. São evidência da representação existente, não configuração FGVTN demonstrada. Não usar os corpos nem os furos dessa referência como gabarito da FGVTN.

## Curso, engates e manutenção

O desenho arquivado distingue **P=500**, **P1 mínimo=520** e **C=475 ±3 mm**. Logo, 500 mm de comprimento nominal não equivale a curso 500. Antes de integrar a ferragem, reconciliar os controladores com C e confirmar a variante efetiva; não alterar controles somente para fazer esta tabela coincidir.

A instrução exige **destrave simultâneo dos dois lados** para retirar a gaveta. O próximo desenho deve reservar acesso sob os dois cantos frontais com a gaveta aberta e apoiada, sem exigir retirar previamente uma frente ou peça que bloqueie o próprio destrave. O volume real das mãos, a ferramenta, a sequência de desengate e eventual levantamento não foram obtidos dessa imagem; não inventar uma altura de retirada.

| Interface pendente | Próximo trabalho verificável |
|---|---|
| Caixa 500 e largura A−41 | Preparar alternativa paramétrica com as sete frentes e úteis preservados; conferir todas as peças/rasgos, não apenas alongar o envelope |
| Engates FGVTN | Identificar referência e desenho próprios da variante 500; mapear posição, fixação e destrave sem copiar T51.7601 |
| Vertical/recortes | Conferir os datums das cotas 38 mínimo, 27, 12, 11 e 7 do desenho em um corte da montagem correta; não importar as cotas MOVENTO do P16 |
| Ajuste +3 mm | Conferir folgas em toda a faixa, inclusive frentes e gaveta acima; a indicação de ajuste não garante espaço livre |
| Furação | Usar a linha 500 e a face de referência do desenho; D=224/E=64 não são a receita da variante 400. Piloto/parafuso dependem do painel/produto |
| Retirada | Representar engates reais e acessos simultâneos; depois conferir percurso completo, apoio e remontagem |

As sete faces laterais e planos de fundo usados no levantamento antigo foram reconferidos numericamente na base atual. Não se repetiu o ensaio de raios nem se tratou a caixa envolvente como inspeção de furos. Capacidade, rigidez, fabricação e compatibilidade de ferragem continuam pendentes.

Reproduzir na raiz: `python -B ferramentas/conferir_gavetas_p01_p06.py`. Usa somente a biblioteca padrão, confere hash R52 e as faces de referência; gera os dados sem abrir CAD.
