# Caderno formal A3 — R02

[Abrir caderno](index.html) · [PDF R02](Guedala_Park_Pranchas_R02.pdf) · [Alterações e avisos](Impacto.html). R00 preservado em [PDF histórico](Guedala_Park_Pranchas_R00.pdf), sem substituição publicada.

Gerar na raiz do repositório:

```powershell
python ferramentas/pranchas/gerar.py
```

Produz 20 folhas SVG, HTML com páginas de 420 × 297 mm e PDF vetorial. Plantas 1:50, elevações e detalhe 1:25. Imprimir a 100%, sem ajustar à folha; a barra deve medir 50 mm no papel. O PDF e o SVG partilham as mesmas primitivas em milímetros, sem redimensionar imagens. Requer Python e ReportLab; usa automaticamente o runtime local do Codex quando disponível, ou instalar `python -m pip install reportlab`.

## Atualizar uma medida em três linhas

1. Abra `07_Imovel/Medidas_e_impactos.csv` e localize `codigo_medida` (pé-direito: PD-QUA, PD-COZ, PD-LAV, PD-ESC, PD-BAN ou PD-SAL).
2. Preencha `valor_medido` com unidade, por exemplo `2470 mm`, e registre origem/data em `evidencia_campo`; preserve o nominal.
3. Rode o comando acima e abra `Impacto.html` e o PDF R02; confira avisos antes de encaminhar.

`valor_medido` preenchido vence `valor_nominal_atual`. Vazio significa pendência. Entradas inválidas interrompem a geração com o código da medida. Cotas.json é o mapa entre contornos, cotas e códigos CSV; seus arrays antigos continuam como evidência da planta oficial, não são outra entrada de campo do gerador R02. Para medir posições PR, use os eixos X/Y indicados em PL1; não confundir coordenada com distância ao móvel. PR-WALLS identifica cada retângulo de parede da reconstrução; PR-PORTA/PR-JANELA identifica vão e peitoril. A medição de largura de ambiente não é suficiente para determinar todos os alinhamentos de paredes e vãos: levantar também esses registros.

## Índice

| Folhas | Conteúdo |
|---|---|
| 00 | Índice, fontes e critérios |
| PL1–PL3 | Paredes/aberturas; layout R53; pontos R01 |
| PT1–PT2 | Os 53 códigos R01: coordenadas, alturas e funções |
| E01–E02 | Cozinha: bancada/aéreos e face oposta da lixeira |
| E03–E04 | Lavanderia e banheiro |
| E05–E07 | Roupeiro/maleiro, retorno P02, cabeceira/P04 |
| E08–E10 | Escritório: bancada/P16, P17, TV/prateleira |
| E11–E12 | Sala/TV e banco P20 |
| NC1 | Triagem de vãos entre planos horizontais dos módulos |
| DT1 | Detalhe-tipo de fechamento ao teto |

## Origem e parametrização

- N em ocre e linha de cota tracejada: nominal/planta, incluindo CAD. M em verde e linha contínua: medido. Cota derivada só é M quando todas as parcelas forem medidas. O carimbo conta os registros de cota nominal da folha; repetições do mesmo identificador contam uma vez. RT permanece em branco. Todas as folhas: **ESTUDO — NÃO EXECUTAR**.
- Geometria.json contém envelopes de objetos visíveis e módulos P01–P20, posições, tamanhos e folgas nominais na exportação, com SHA256 do FCStd. Coordenadas globais FreeCAD são espelhadas em X para a planta. Não substitui contornos de usinagem; peças internas aparecem como referência geométrica, sem cálculo de carga/ligação.
- FCStd R53 preservado: SHA256 `fedd9d1d0604fabb93af47f9e2b70e1892f06d7e0d6ba9eb6f3f4785e281ae7f`. Verificação completa: 5.832 objetos, 1.133 formas ativas, 1.362 pares de caixas, 106 cenários; Modelo OK. A exportação abriu oculto, não recalculou nem salvou. `python ferramentas/pranchas/exportar.py` só é necessário quando houver outra revisão CAD autorizada; depois executar a verificação completa.
- Caixas cinza preservam a R53. Traço azul é estudo: topo = pé-direito atual − folga nominal da exportação; altura do aéreo/maleiro = topo − base R53. DT1 usa fechamento = pé-direito atual − topo R53. Resultado negativo gera aviso e não vira retângulo negativo. Peça fixa que ultrapassa o teto é denunciada, mesmo quando existe alternativa paramétrica.
- Ultima_geracao.json guarda cotas/fontes da geração anterior. Impacto.json e Impacto.html comparam valor, origem, prancha e móvel: antes → depois. A primeira geração registra inclusões. Nova execução sem mudanças produz zero alterações; os avisos persistem. Não apagar o retrato para esconder diferenças.

## Pendências que não impedem a geração

Medidas de campo, coordenação com RT, posição Q06/S05/E05 e E06 adiada. A face oposta da cozinha não contém módulo de marcenaria na R53; E02 mostra somente a interface da lixeira. Pergunta para levantamento: há outra marcenaria desejada nessa face? Não foi inventada.

Paredes/vãos continuam reconstituídos. Conferir alinhamentos compartilhados entre ambientes quando mudar cotas horizontais; o gerador não resolve uma rede topológica arquitetônica nem deforma o mobiliário rígido para fazê-lo caber. As elevações mostram os pontos do ambiente em projeção; PT1/PT2 preservam suas coordenadas completas, inclusive pontos de outras faces. A projeção não define parede de instalação. Rever implantação e acesso dos pontos com RT.

NC1 é triagem por envelopes de planos horizontais: não certifica vãos úteis de portas, gavetas e ferragens. Furação, ferragens, ligações, cortes finais e revisão técnica são externos a este caderno.

## Verificações

A3 conferido em PDF (20 páginas). Teste paramétrico externo e revisão visual final registrados após sua execução; não usar este parágrafo como comprovação de teste ainda pendente.
