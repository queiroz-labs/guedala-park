# Revisão visual das cores · R15

23/10/2026. Correção da visualização do site; fichas técnicas permanecem R14 e geometria FreeCAD R45.

A importação recebia `#bbbdb7` quando o objeto não tinha `MaterialReferencia`. Assim, mesa, cadeiras, cabeceira, espelhos e forno apareciam cinza apesar das decisões documentadas. Os acabamentos por face das fichas também não eram aplicados à visualização.

## Aparência conferida

| Ambiente | Referência visual |
|---|---|
| Sala | Berlin com tampo aproximado Arenza e base preta; cadeiras com madeira e estofado claro distintos; banco amadeirado e estofado greige; Bonnie bege |
| Quarto | Armários amadeirados, referência Arenza; cabeceira bege/greige; interiores Branco TX |
| Escritório | Arenza na bancada e frentes de gavetas; aéreo off-white; Daiane cinza-claro preservada |
| Cozinha | Inferiores Arenza; superiores Guararapes Azul Petróleo; forno Fischer preto; Branco Itaúnas e inox preservados |
| Lavanderia | Marcenaria Arenza; pedra Branco Itaúnas; piso Iseo Marfim |
| Banheiro | Frentes bege; laterais madeira clara; camada de espelho distinta; Sauge e Travertino Greige preservados |

Os tons são aproximações. Madeira clara do banheiro não foi substituída por Arenza. Códigos comerciais pendentes continuam pendentes. Acabamento de verso oculto não especificado mantém apenas sua referência visual anterior; tampas sob almofadas continuam neutras por cima e TX por baixo. Nenhum gabarito desconhecido recebe madeira automaticamente.

## Fontes e implementação

- [Decisão Branco TX por face](../fabrication/Decisao_acabamentos_R13.md) e [atribuições por peça](../fabrication/finish-audit.json).
- Consolidação R43, `Modelo_FreeCAD/01_Consolidacao/Consolidacao_R43_LEIA-ME.md`, seção de correções da sala: Arenza, base preta e tecido claro.
- Cadeiras: 168 triângulos de madeira e 368 de tecido por cadeira. Faixas confirmadas com os sólidos originais e os arquivos ShapeAppearance do FCStd R45. [Mapa com hashes geométricos](../fabrication/chair-visual-faces.json).
- [Gerador visual](../build_visual_finishes.py) separado da geometria e das listas de fabricação. Faces internas/externas dos painéis são orientadas pelo eixo de espessura e posição na caixa; não é mapa executivo de revestimento ou bordas.

Conferidos seis ambientes, vista interna, materiais dos 383 componentes, destaque de peça e cores dos volumes simplificados durante o giro. Geometria, dimensões e arquivo FreeCAD preservados.
