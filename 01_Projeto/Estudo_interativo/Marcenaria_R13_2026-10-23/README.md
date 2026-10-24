# Fichas R13, planta cotada e interação 3D

As 20 fichas organizam 249 painéis com dimensões nominais, espessura geométrica, acabamento por face, ferragens quantificadas, montagem e fontes. Cada ficha tem três projeções de envelopes, impressão e CSV. As projeções não representam recortes ou furação executiva.

Decisão de 23/10/2026: Branco TX nos interiores; padrões escolhidos nas faces aparentes. Foram registradas faces para 248 painéis, inclusive aplicações parciais explicitamente marcadas. Dos 128 painéis originalmente sem referência de acabamento, 120 receberam definição para as faces identificadas; oito continuam parciais. Código comercial, substrato, composição de faces, bordas e usinagem não foram inferidos da cor.

O levantamento do apartamento está separado das definições técnicas das fichas. A planta cotada diferencia valores escritos na planta oficial e medidas da reconstrução, incluindo a divergência de 1,54 m versus 1,61 m na área de serviço e os trechos da circulação.

O visualizador usa representação simplificada apenas durante movimento e retoma a geometria completa ao parar. Na visão geral, o teste CPU passou de 128.580 para 1.264 faces durante o gesto; cache de cena, malhas e iluminação evita reconstruções redundantes. O benchmark Node exclui GPU e composição do navegador e não representa FPS real. Detalhe, seleção e isolamento foram verificados separadamente.

## Reprodução

Execute `python 01_Projeto/Estudo_interativo/preparar_pages.py`. Os dados de evidência estão em `fabrication/`; os scripts `build_fabrication.py` e `build_floorplan.py` geram os documentos e dados do site. O FCStd R45 permanece intacto, com SHA256 verificado. As revisões documentais não aprovam automaticamente corte, fixações ou capacidade de carga.

Saídas: `05_Entregas/Fichas_fabricacao_R13/`, `05_Entregas/Planta_cotada_R13/` e `.site/`. O workflow GitHub Pages publica apenas a lista explícita de documentos e ativos.
