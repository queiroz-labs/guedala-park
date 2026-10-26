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

## Proposta dimensional FGVTN 500 — não aplicada

Proposta preparada em 26/10/2026 a pedido de Elias nesta conversa: “preparando a proposta de correção sem alterar o FreeCAD por enquanto”. [Mapa das 42 peças em CSV](Pecas_proposta_FGVTN_500.csv) e [coordenadas, verificações e exceções](Proposta_FGVTN_500.json). São envelopes globais **X mínimo/Y mínimo/Z mínimo/X máximo/Y máximo/Z máximo**, em mm; não são lista de corte nem geometria de usinagem. A auditoria acima continua descrevendo a R52 intacta.

| Resultado proposto | P01 (4 caixas) | P06 (3 caixas) |
|---|---:|---:|
| Largura externa | 344 mm | 572 mm |
| Largura interna nominal | 314 mm | 542 mm |
| Profundidade das laterais | 500 mm | 500 mm |
| Folga lateral simétrica até carcaça | 5,5 mm por lado | 5,5 mm por lado |
| Folga traseira até fundo do móvel | 42 mm | 74 mm |
| Comprimento entre frente interna e traseira | 469 mm (antes 459) | 469 mm (antes 459) |

A largura interna proposta coincide com A−41 e deixa 0,5 mm até o limite inferior e 1 mm até o superior do desenho. Essas são margens da receita, não tolerâncias de fabricação já distribuídas. Medidas acabadas, espessuras e esquadro ainda precisam compor a cadeia real.

| Peça por caixa | Correção proposta no sistema global |
|---|---|
| Lateral em X maior | Deslocar +0,5 mm em X; alongar 10 mm só para trás (+Y); manter espessura 15 e altura |
| Lateral em X menor | Deslocar −0,5 mm em X; mesmo alongamento de 10 mm |
| Fundo | Ampliar 0,5 mm em cada borda X e 10 mm na borda traseira; manter Z |
| Traseira | Ampliar 1 mm total em X e deslocar 10 mm para trás; manter espessura e Z |
| Frente interna | Ampliar 1 mm total em X; manter Y/Z |
| Frente decorativa | Preservar forma, posição e dimensões |

São **35 envelopes a corrigir e sete frentes preservadas**. Mantêm-se centro da caixa, altura e frente; o espaço entre paredes cresce 1 mm na largura e 10 mm na profundidade. O fundo permanece 12 mm acima da borda inferior das laterais e penetra nominalmente 5 mm de cada lado, inferido pelos envelopes. Preservar esse encaixe exige reconstruir/conferir os rasgos e suas terminações: alongar o envelope não demonstra a usinagem. Furos e recortes existentes não entram automaticamente na proposta.

**Exceção P06/G2 (`Gaveta005`):** o fundo `MontagemG2R019` tem envelope vertical 613–629,196 mm, enquanto traseira/frente interna começam em Z628. Não reduzir isso a uma chapa prismática de 16,196 mm nem escalar a peça importada inteira. As duas bandejas ficam nas posições atuais; a folga traseira passa de 2 para 12 mm e as folgas laterais crescem 0,5 mm, sem reduzir as frontais (2 mm). Há sobreposição vertical prévia de envelopes de 1,196 mm com o fundo: a forma real e o apoio precisam de inspeção antes de afirmar interferência ou encaixe. A proposta não resolve essa particularidade.

### Sequência antes de aplicar no CAD

1. Confirmar variante comercial FGVTN 500 e engates esquerdo/direito, desenhos completos, fixadores e acesso simultâneo ao destrave. As cotas D224/E64 não definem sozinhas todos os furos.
2. Resolver corte vertical e datums do conjunto, rasgos, recortes traseiros e furos; conferir o fundo importado G2 e o apoio das bandejas. Manter a largura nominal proposta no centro do intervalo documental.
3. Conferir ajuste vertical +3, frentes vizinhas, corpos reais, abertura/retirada e acesso às mãos. As folgas desta tabela valem para a caixa fechada, sem ferragens novas; não comprovam percurso.
4. Apresentar a solução de montagem para decisão sobre aplicação. Somente após pedido de alteração do modelo, editar os parâmetros/peças e executar a verificação completa, sem alterar a base para ocultar falhas.

Reproduzir a proposta: `python -B ferramentas/propor_caixas_fgvtn.py`. O script confere hashes do CAD, base e desenho contra a auditoria, relações entre as 42 peças, frentes e Z preservados e folgas horizontais das bandejas. Não abre o FreeCAD, não calcula capacidade nem valida colisões de sólidos.

Os 14 objetos de engate nas sete gavetas ainda trazem referência **T51.7601**. São evidência da representação existente, não configuração FGVTN demonstrada. Não usar os corpos nem os furos dessa referência como gabarito da FGVTN.

## Curso, engates e manutenção

O desenho arquivado distingue **P=500**, **P1 mínimo=520** e **C=475 ±3 mm**. Logo, 500 mm de comprimento nominal não equivale a curso 500. Antes de integrar a ferragem, reconciliar os controladores com C e confirmar a variante efetiva; não alterar controles somente para fazer esta tabela coincidir.

A instrução exige **destrave simultâneo dos dois lados** para retirar a gaveta. O próximo desenho deve reservar acesso sob os dois cantos frontais com a gaveta aberta e apoiada, sem exigir retirar previamente uma frente ou peça que bloqueie o próprio destrave. O volume real das mãos, a ferramenta, a sequência de desengate e eventual levantamento não foram obtidos dessa imagem; não inventar uma altura de retirada.

| Interface pendente | Próximo trabalho verificável |
|---|---|
| Caixa 500 e largura A−41 | Mapa dimensional das 42 peças preparado acima; resolver usinagem e exceção G2 antes de parametrizar no CAD |
| Engates FGVTN | Identificar referência e desenho próprios da variante 500; mapear posição, fixação e destrave sem copiar T51.7601 |
| Vertical/recortes | Conferir os datums das cotas 38 mínimo, 27, 12, 11 e 7 do desenho em um corte da montagem correta; não importar as cotas MOVENTO do P16 |
| Ajuste +3 mm | Conferir folgas em toda a faixa, inclusive frentes e gaveta acima; a indicação de ajuste não garante espaço livre |
| Furação | Usar a linha 500 e a face de referência do desenho; D=224/E=64 não são a receita da variante 400. Piloto/parafuso dependem do painel/produto |
| Retirada | Representar engates reais e acessos simultâneos; depois conferir percurso completo, apoio e remontagem |

As sete faces laterais e planos de fundo usados no levantamento antigo foram reconferidos numericamente na base atual. Não se repetiu o ensaio de raios nem se tratou a caixa envolvente como inspeção de furos. Capacidade, rigidez, fabricação e compatibilidade de ferragem continuam pendentes.

Reproduzir na raiz: `python -B ferramentas/conferir_gavetas_p01_p06.py`. Usa somente a biblioteca padrão, confere hash R52 e as faces de referência; gera os dados sem abrir CAD.
