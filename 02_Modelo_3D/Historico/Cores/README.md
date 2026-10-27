# FreeCAD com cores atualizadas · R16

23/10/2026. Modelo principal: `Guedala_Park_R45_Cores_R16.FCStd` (binário removido em 26/10/2026; recuperável no git).

A geometria continua sendo a consolidação R45. Esta revisão aplica ao FreeCAD a paleta visual R15 do site e os acabamentos registrados nas fichas R14. Abra o arquivo no FreeCAD 1.1 ou versão compatível. A gravação e a conferência foram feitas com FreeCAD 1.1.4 / 20260928.

## Acabamentos representados

| Elemento | Aparência |
|---|---|
| Faces internas identificadas nas fichas | Branco TX |
| Marcenaria amadeirada, roupeiro, inferiores da cozinha, lavanderia e apoio do micro | Arenza como escolha ou referência de composição, conforme cada ficha |
| Aéreos da cozinha | Guararapes Azul Petróleo |
| Aéreo do escritório | Off-white |
| Banheiro | Frentes bege, laterais em madeira clara e espelho aplicado separado |
| Mesa Berlin | Tampo amadeirado e base preta |
| Cadeiras Lina | Estrutura amadeirada, assento e encosto em tecido claro |
| Cabeceira e estofados do banco | Bege / greige, conforme direção registrada |

270 componentes e 2.302 faces foram conferidos; 257 componentes tiveram alguma cor alterada. Pisos, paredes, sofás e demais elementos que já correspondiam à representação do site foram preservados. Ferragens e volumes sem acabamento documentado não receberam uma escolha nova.

As cores digitais são aproximadas: iluminação do FreeCAD, tela, amostra e lote alteram a percepção. No quarto e em outras direções ainda sem produto fechado, a cor representa a composição; não fecha código de chapa ou tecido.

## O que permanece pendente

As fichas técnicas continuam na revisão R14. As novas seleções de ferragens e tabelas de furação não foram todas incorporadas à geometria. Medidas no apartamento, tolerâncias, fitas de borda, sentido de veio e fechamentos técnicos continuam conforme as fichas. Esta atualização não libera corte, usinagem ou montagem.

A superfície superior das tampas sob as almofadas do banco permanece cinza neutro onde o acabamento não foi escolhido. A face voltada para o interior é Branco TX. Cinza de pendência não significa chapa cinza escolhida.

A aplicação de Branco TX reproduz as faces de consulta identificadas no site. Em 40 faces curvas contínuas de furos/recortes, a superfície atravessa mais de uma orientação: o FreeCAD mantém a cor de referência da peça, sem dividir sua geometria para imitar a coloração por triângulo do site. A cor desses recortes não especifica revestimento ou acabamento de usinagem.

## Preservação e conferência

- Arquivo R45 original preservado.
- 1.757 arquivos de geometria BREP e os dados dos 5.840 objetos idênticos ao original, byte a byte no arquivo final.
- Posições, expressões, grupos, controles e visibilidade preservados.
- Aparências geradas pela API do FreeCAD, sem interpretar ou reescrever manualmente o formato binário dos materiais.
- Cópia final reaberta no FreeCAD para conferir as aparências, a ordem das faces e a transparência.

O salvamento intermediário do FreeCAD normaliza dados antigos do documento. Por isso o arquivo final recebe somente os registros de aparência gerados pelo aplicativo; os demais dados vêm intactos do original. Os campos históricos de material da base R45 ficam preservados; para acabamento por face, consulte a aparência R16 e as fichas R14.

Registros para conferência: [plano de cores](Plano_de_cores.json), [verificação das aparências](Verificacao_cores.json) e [verificação da geometria](Verificacao_geometria.json).

SHA256 do arquivo atualizado: `b69f8c3eafde2bc9c926b8d63ca4f40c5a97acecfdc8564de5fae2bebfabdbbb`.
