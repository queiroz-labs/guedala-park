# Luz suave e sombras de contato — primeira etapa

Implementado no visualizador WebGL existente em 17/10/2026, sem nova biblioteca. Publicação autorizada por Elias em 18/10/2026.

[Abrir o site atualizado](../Guedala_Park_Interativo.html) · [Capturas antes e depois](Comparacao.html).

Na **sala** ou **cozinha**, na vista **3D**, usar **Luz e sombras → Antes / Depois**. A troca conserva câmera, zoom, seleção e configuração dos móveis. A opção Depois é a inicial nesses dois ambientes. Planta, lateral, visão geral, outros ambientes, miniaturas e fichas conservam a iluminação original.

## O que mudou

- Luz ambiente e preenchimento conforme a normal, mais uma direção principal fixa no ambiente. A luz não gira com a câmera.
- Contornos discretamente mais suaves, mantendo o destaque do móvel selecionado.
- Contatos suaves em superfícies horizontais próximas: piso, bancada e apoios. Calculados a partir das faces inferiores dos móveis já transformados/animados, e das superfícies receptoras atualmente visíveis.
- O maior contato prevalece quando partes se sobrepõem, evitando acumular manchas escuras.
- Distância de suporte limitada: um aéreo distante do piso não produz uma mancha de contato no chão.
- Até 48 contatos, com limite menor automático conforme a capacidade de uniforms do WebGL do aparelho.

É uma aproximação de contato por retângulos envolventes e altura de apoio. Não calcula iluminação física, sol, luminárias reais, oclusão global nem sombras projetadas longas. Vidros não lançam contatos. A suavização não substitui a geometria dos móveis. Na alternativa Canvas sem WebGL, a nova luz continua disponível, mas os contatos não são desenhados.

## Personalizar

Editar somente o objeto `LIGHTING_CONFIG` em [src/lighting.js](../src/lighting.js):

| Parâmetro | Uso |
|---|---|
| `ambient`, `hemisphere` | Claridade geral e preenchimento |
| `key.direction` | Direção em coordenadas do apartamento: x, altura, z |
| `key.intensity`, `key.tint` | Força e tom da luz principal |
| `edges` | Contraste dos contornos |
| `contact.strength` | Escurecimento máximo, inicialmente 0,25 |
| `contact.softness` | Faixa suave em centímetros, inicialmente 3 |
| `contact.maxGap` | Distância máxima ao apoio, inicialmente 22 cm |
| `contact.maxPatches` | Limite de contatos; teto do shader: 48 |

Depois executar `construir.py` para regenerar os HTML autônomos, ou `preparar_pages.py` para também preparar `.site`. Medidas, materiais e controles continuam nas fontes existentes. Ajustar luz não requer editar geometria.

## Verificado

- `node test_lighting.cjs`: fatores originais exatos em Antes; escopo restrito; 29 contatos na sala e 29 na cozinha no cenário inicial; contatos mudam com sofá/mesa/cadeiras; índices e intensidades dos contatos finitos e limitados; objetos suspensos não geram contato distante.
- Navegador: shaders em WebGL (`data-renderer=depth`), alternância Antes/Depois, sofá esticado e mesa aberta preservados ao comparar; interiores em corte e móveis altos; planta sem o seletor de iluminação; exportação pelo botão Imagem.
- Layout 1440 × 1100 e 412 × 915. Na viewport estreita: largura do documento 397 px para viewport 412 px, sem transbordamento horizontal; renderização WebGL. Isso é emulação de layout, não teste físico no S24 Plus.
- Sem erros ou avisos no console da sessão final de conferência.
- HTML principal e moodboard regenerados pelo fluxo existente. O arquivo continua autônomo e a pasta de publicação conserva sua lista permitida de cinco arquivos.

As capturas são registros reais da interface. `cozinha-antes-exportada.png` foi produzida pelo botão Imagem do próprio site. As capturas documentam a conferência local anterior à publicação.
