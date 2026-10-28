# Frente 2 — precedências e centros, 28/10/2026

Estudo R54 documental: **37 restrições ordenadas, zero ciclos nos 20 móveis, mínimo de trocas no grafo = 0**. [Sequenciador](../../ferramentas/estudos/sequenciar_furacao.py): instalar ambos os painéis → apertar conjunto → instalar bloqueador. P01/P03/P04/P06/P20 têm respectivamente 15/2/8/8/4 restrições. Demais: nenhuma restrição detectada, sem cobertura integral demonstrada. Encaixe/estabilidade/retirada da ferramenta exigem montagem em seco. Coordenadas/conectores preservados.

Antes → depois: **2.286 → 2.286 centros; 0 → 0 conflitos geométricos; 37 → 37 alertas estáticos; 4 → 4 portas fora da faixa**. Auditor permanece REPROVADO. Busca exata retorna trocas mínimas propostas em ciclos; ciclo sem aresta removível informa impossibilidade.

Novos centros continuam bloqueados pelas fontes vigentes, não por medida do apartamento:

- FGVTN500: quais IDs/faces de apoio, cotas verticais por gaveta e fixadores? `partIds` vazio; referências longitudinais não bastam para altura absoluta. Divergência H do catálogo/instrução permanece; STEP400 não demonstra500.
- MOVENTO400: qual datum de montagem das guias e engates nas peças atuais? `partIds` vazio e interferência residual registrada não autorizam deslocar a guia para gerar furos.
- Base173H7100: qual transformação local→montado de cada folha e respectivo ID/face de apoio? O mapa histórico fornece eixos locais; Geometria.json fornece somente caixas, insuficientes para transferir a linha sem espelhamento presumido.
- System32: quais início/fim e recuos nas prateleiras já reguláveis? Os oito pontos P19 em244/488 e20/86 permanecem; nenhuma linha nova foi inventada nem prateleira fixa convertida.

Fontes: [catálogos e páginas no README](README.md#fontes-e-limites-de-catálogo); technical-r14.json, hinge-drilling-maps.json, fichas e Geometria.json atuais. Nomes históricos não indicam revisão do modelo. Perguntas requerem desenho/catalogação, não escolha estética.

Reproduzir fora do git: `python -B ferramentas/estudos/sequenciar_furacao.py --saida ../outputs/Furacao_sequencia`. SHA256: Ordem_eventos.csv `c76b98311289debda302aa6b5a23bf30f56ddec48772faa99b0b5f4ac02034dc`; Arestas.csv `25e51451de14823187cb39e7596f1199eb5ea4df93e5a83cc10fce71bbd92683`; Ciclos.json `a5338d955b09046ec0b16f3a9625b7955c763aae07dc722e474e6078745f932f`. Resumo_montagem.json registra hashes das entradas. Testes: `python -B ferramentas/estudos/test_sequenciar_furacao.py` (6, inclusive comparação exaustiva de64 grafos); `test_furacao.py` (14). Ambos passam; conferência conserva código1 esperado.

