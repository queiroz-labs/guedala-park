# Composição do moodboard

`python -B ferramentas/moodboard/gerar.py` produz os arquivos vigentes em `09_Referencias/`: dois painéis 4K/PNG leve, PDF de dois painéis, PDF de seis páginas A3 e galeria Dia/Noite. Requer Python com Pillow e ReportLab; Poppler (`pdftoppm`) no PATH. Se o TEMP padrão estiver restrito, configure TEMP/TMP para uma pasta temporária gravável fora do repositório.

As 12 imagens aprovadas são entradas imutáveis de 1536 × 1024 px. Nunca ampliar nem recortar as cenas; escala de composição do painel: 1050 × 700 px. PDF mantém 1536 × 1024 px, compressão JPEG qualidade 95/sem subamostragem, fontes Vera incorporadas e texto vetorial; PNG é renderizado do mesmo PDF. WebP mantém dimensões, qualidade 90, com acesso ao PNG original na galeria. `Moodboard.json` registra hashes e aprovação.

Paleta, quatro amostras por ambiente e legendas estão em `ROOMS`/`PALETTE` no gerador. São aproximações digitais, não amostras comerciais. Direção: briefing de Elias (grade 3 × 2 e gêmeos Dia/Noite), imagens aprovadas, tipografia neutra e contraste legível. A pesquisa externa Refero estava indisponível; foram usadas as referências do projeto e a orientação local de tipografia da skill. Fundo claro fixo, títulos escuros, sem sombras/cartões decorativos; cor aparece nas cenas e amostras. O painel nunca passa por geração de IA.

Para nova seleção: substituir somente o PNG explicitamente aprovado, registrar fonte/data no README da área, regenerar e conferir o PDF/PNG e o comparador. Para integrar ao site: `python -B ferramentas/site/construir.py`; `build_web.mjs` publica os arquivos em `/galeria/`. Rótulo visual: “Aparência aprovada em 28/10/2026”; falas específicas no registro interno do README de referências. Não atribuir o resumo de seleção como citação de Elias. A3 em retrato com cenas de 680 × 453,33 pt, proporção 3:2; textos de processo ficam apenas nesta documentação.

Validação: `python -B ferramentas/moodboard/verificar.py`, inspeção visual dos painéis e A3, interação nos seis controles da galeria, `python -B ferramentas/verificar_tudo.py`. Revisão concluída: Elias, 28/10/2026, “Aprovado, pode commitar e dar push.” [Registro](../../09_Referencias/README.md).
