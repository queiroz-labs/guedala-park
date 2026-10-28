# Caderno formal A3 — R02

**Fonte vigente R54, 27/10/2026:** SHA e caminho sincronizados com o pedestal Berlin e afastamento de 15 mm da cadeira lateral. Os 24 envelopes usados no recálculo dimensional permanecem iguais; fórmulas e medidas nominais preservadas.

[Abrir caderno](index.html) · [PDF R02](Guedala_Park_Pranchas_R02.pdf) · [Alterações e avisos](Impacto.html). R00 preservado em [PDF histórico](Guedala_Park_Pranchas_R00.pdf); R02 incluído no pacote R26.

Gerar na raiz do repositório:

```powershell
python ferramentas/pranchas/gerar.py
```

Produz 20 folhas SVG, HTML com páginas de 420 × 297 mm e PDF vetorial. Plantas 1:50, elevações e detalhe 1:25. Imprimir a 100%, sem ajustar à folha; a barra deve medir 50 mm no papel. O PDF e o SVG partilham as mesmas primitivas em milímetros, sem redimensionar imagens. Requer Python e ReportLab; usa automaticamente o runtime local do Codex quando disponível, ou instalar `python -m pip install reportlab`.

## Atualizar uma medida em três linhas

1. Abra `07_Imovel/Medidas_e_impactos.csv` e localize `codigo_medida` (pé-direito: PD-QUA, PD-COZ, PD-LAV, PD-ESC, PD-BAN, PD-SAL ou PD-CIR).
2. Preencha `valor_medido` com unidade, por exemplo `2470 mm`, e registre origem/data em `evidencia_campo`; preserve o nominal.
3. Rode o comando acima e abra `Impacto.html` e o PDF R02; confira avisos antes de encaminhar.

`valor_medido` preenchido vence `valor_nominal_atual`. Vazio significa pendência. Entradas inválidas interrompem a geração com o código da medida. Cotas.json é o mapa entre contornos, cotas e códigos CSV; seus arrays antigos continuam como evidência da planta oficial, não são outra entrada de campo do gerador R02. As dimensões oficiais usam os registros DIM-* existentes, inclusive cotas compostas (`2450 × 2950 mm`); cada eixo é vinculado em Cotas.json sem duplicar a entrada. Para medir posições PR, use os eixos X/Y indicados em PL1; não confundir coordenada com distância ao móvel. PR-WALLS identifica cada retângulo de parede da reconstrução; PR-PORTA/PR-JANELA identifica vão e peitoril. A medição de largura de ambiente não é suficiente para determinar todos os alinhamentos de paredes e vãos: levantar também esses registros.

## Índice

| Folhas | Conteúdo |
|---|---|
| 00 | Índice, fontes e critérios |
| PL1–PL3 | Paredes/aberturas; layout R54; pontos R01 |
| PT1–PT2 | Os 53 códigos R01: coordenadas, alturas e funções |
| E01–E02 | Cozinha: bancada/aéreos e face oposta da lixeira |
| E03–E04 | Lavanderia e banheiro |
| E05–E07 | Roupeiro/maleiro, retorno P02, cabeceira/P04 |
| E08–E10 | Escritório: bancada/P16, P17, TV/prateleira |
| E11–E12 | Sala/TV e banco P20 |
| NC1 | Triagem de vãos entre planos horizontais dos módulos |
| DT1 | Detalhe-tipo de fechamento ao teto |

## Alturas vigentes — 27/10/2026

Elias solicitou 2,60 m em todos os cômodos e 2,50 m no banheiro. CSV atualizado como nominal/planta, sem preencher medição fictícia. O cenário de 2,47 m do escritório foi substituído. Site e pranchas leem a mesma fonte; caixas R53 continuam como referência, e as cotas dependentes do teto são recalculadas.

## Origem e parametrização

- N em ocre e linha de cota tracejada: nominal/planta, incluindo CAD. M em verde e linha contínua: medido. Cota derivada só é M quando todas as parcelas forem medidas. O carimbo conta os registros de cota nominal da folha; repetições do mesmo identificador contam uma vez. RT permanece em branco. Todas as folhas: **ESTUDO — NÃO EXECUTAR**.
- Geometria.json contém envelopes de objetos visíveis e módulos P01–P20, posições, tamanhos e folgas nominais na exportação, com SHA256 do FCStd. Coordenadas globais FreeCAD são espelhadas em X para a planta. Não substitui contornos de usinagem; peças internas aparecem como referência geométrica, sem cálculo de carga/ligação.
- FCStd R53 preservado: SHA256 `fedd9d1d0604fabb93af47f9e2b70e1892f06d7e0d6ba9eb6f3f4785e281ae7f`. Verificação completa: 5.832 objetos, 1.133 formas ativas, 1.362 pares de caixas, 106 cenários; Modelo OK. A exportação abriu oculto, não recalculou nem salvou. `python ferramentas/pranchas/exportar.py` só é necessário quando houver outra revisão CAD autorizada; depois executar a verificação completa.
- Caixas cinza preservam a geometria CAD. Traço azul é estudo: topo = pé-direito atual − folga nominal da exportação; altura do aéreo/maleiro = topo − base CAD. DT1 usa fechamento = pé-direito atual − topo CAD. Resultado negativo gera aviso e não vira retângulo negativo. Peça fixa que ultrapassa o teto é denunciada, mesmo quando existe alternativa paramétrica.
- Ultima_geracao.json guarda cotas/fontes da geração anterior. Impacto.json e Impacto.html comparam valor, origem, prancha e móvel: antes → depois. A primeira geração registra inclusões. Nova execução sem mudanças produz zero alterações; os avisos persistem. Não apagar o retrato para esconder diferenças.

## Pendências que não impedem a geração

Medidas de campo, coordenação com RT, posição Q06/S05/E05 e E06 adiada. A face oposta da cozinha não contém módulo de marcenaria na R53; E02 mostra somente a interface da lixeira. Pergunta para levantamento: há outra marcenaria desejada nessa face? Não foi inventada.

Paredes/vãos continuam reconstituídos. Conferir alinhamentos compartilhados entre ambientes quando mudar cotas horizontais; o gerador não resolve uma rede topológica arquitetônica nem deforma o mobiliário rígido para fazê-lo caber. As elevações mostram os pontos do ambiente em projeção; PT1/PT2 preservam suas coordenadas completas, inclusive pontos de outras faces. A projeção não define parede de instalação. Rever implantação e acesso dos pontos com RT.

NC1 é triagem por envelopes de planos horizontais: não certifica vãos úteis de portas, gavetas e ferragens. Furação, ferragens, ligações, cortes finais e revisão técnica são externos a este caderno.

## Verificações

**Teste externo 2,60 → 2,47 m, 27/10/2026: passou.** Cópia mínima descartável fora do repositório; seis registros PD receberam `valor_medido = 2470 mm`. As 12 elevações e DT1 mudaram; 99 cotas alteradas com antes/depois, prancha e móvel. P09–P12: folga de +50 para −80 mm, quatro avisos de ultrapassagem do teto. Suas alturas de estudo diminuíram 130 mm; as caixas R53 ficaram explícitas. Fechamento P03: 160 → 30 mm. Cópia apagada; CSV, FCStd e fatos originais conferidos por SHA.

Repetição sem mudanças: zero alterações e PDF binariamente idêntico. Entrada de pé-direito negativo foi recusada sem substituir PDF/retrato anterior. Conversões m/cm/mm, zero versus vazio, precedência do medido e origem nominal das derivadas mistas conferidas. A linha de 2470 mm na elevação mede exatamente 98,8 mm no SVG 1:25.

PDF: 20 páginas A3 (420 × 297 mm), carimbos em todas, textos dentro da moldura. Revisão visual por rasterização das folhas; chamadas de cotas distribuídas para eliminar sobreposição. PDF R00, FCStd e fatos sem diferença em relação ao início da tarefa.

Repetir o teste: `python ferramentas/pranchas/testar.py --temporarios CAMINHO_FORA_DO_REPOSITORIO`. O script cria e apaga somente a própria cópia, sem alterar a base.

**Pranchas formais: 80% estimados**, maturidade documental: fonte/rastreio 20, geração/escala 20, cobertura de plantas/elevações 25, impacto/ensaio 15. Os 20 restantes dependem de levantamento, fechamento das interfaces e revisão técnica. Não equivale a executivo de fabricação; o percentual de anteprojeto permanece separado.

Validação das alturas de 27/10/2026: banheiro 2600 → 2500 mm gerou nove alterações de cotas em E04/PT2 e nenhum conflito novo ao teto. Ensaio externo atualizado: sete registros PD para 2470 mm, 12 elevações/99 cotas alteradas e os quatro conflitos esperados P09–P12. Entradas inválidas, precedência, escala e repetição determinística passaram.
