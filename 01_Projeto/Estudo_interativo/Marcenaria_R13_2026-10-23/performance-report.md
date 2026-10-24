# Otimização do visualizador — 23/10/2026

Arquivos alterados: `app.js`, `cad-sync.js`, `depth-renderer.js`, `lighting.js`.

- Visão geral durante giro/zoom: envelopes dos módulos, com cor do painel/frente dominante, e objetos de contexto simplificados. São apenas uma representação temporária para navegar; não alteram o CAD nem medidas.
- Ambiente e móvel isolado: painéis de até 96 triângulos continuam exatos; superfícies densas recebem envelope durante movimento.
- Após 180 ms sem evento de câmera, retorna a tesselação completa, resolução até DPR 2 e iluminação original. Gestos, roda, botões e teclado usam essa regra.
- Cache fraco por identidade da geometria e variante de posição/cor/opacidade. Trocar geometria/revisão não reutiliza malha antiga. Variantes por peça limitadas a quatro.
- A câmera não reconstrói a cena inteira a cada quadro. Trigonometria calculada uma vez por câmera. Iluminação de faces estáticas memorizada.
- Canvases não são redimensionados se o tamanho permanece igual. Removida ordenação opaca redundante: WebGL resolve profundidade por pixel; fallback 2D continua ordenado. Picking continua calculando profundidade interpolada por triângulo.

## Medição reproduzível

`node outputs/fabricacao-r13/benchmark-renderer.cjs`

Execução Node/VM do código verdadeiro de cena, projeção e montagem dos buffers WebGL, 1000 × 680, três aquecimentos e sete amostras. As chamadas GL são no-op. Não mede GPU, composição, latência de entrada nem FPS de navegador.

| Estado | Mediana CPU | Faces |
|---|---:|---:|
| Antes, gesto | 1849,24 ms | 128.580 |
| Depois, gesto na visão geral | 17,29 ms | 1.264 |
| Depois, detalhe parado | 690,40 ms | 128.580 |

No ensaio, custo CPU do gesto caiu 106,95 vezes. Esses tempos absolutos incluem o overhead do VM e não representam tempos/FPS de um navegador. O quadro detalhado continua mais caro; é produzido apenas ao encerrar o gesto.

## Regressões verificadas

`node outputs/fabricacao-r13/verify-renderer.cjs`

- Mesmos móveis selecionados em 45 pontos de tela antes/depois.
- Isolamento dos 20 módulos sem objetos de outro módulo.
- Retorno de todas as 383 peças CAD e 126.220 faces CAD.
- Malhas simples reutilizadas sem simplificação na vista de ambiente/isolado.
- Geometria com identidade nova não reutiliza cache anterior.
- `node --check` aprovado nos quatro arquivos.

Faces coplanares do mesmo móvel podem resolver para outra peça após remover a ordenação por profundidade média; o móvel continua o mesmo e a seleção do módulo permanece ativa. Validação visual no navegador e dispositivos reais cabe ao fluxo principal. O canvas expõe `data-quality`, `data-faces` e `data-renderer` para verificar a transição sem chamar funções internas.
