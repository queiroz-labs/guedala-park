# Cinemática R54 — interferências e mínimos amostrados

Pedido de 28/10/2026; conferência em 28–29/10. Estudo nominal, sem salvar o FreeCAD, alterar ferragens ou atualizar a base de verificação. Não serve para fabricação. **Amostras não demonstram continuidade entre posições.**

## Resultado vigente

- R54: SHA256 `4a2996ee63dd6f2f3dc302025a73fb65011b3339bae510130732859706049528`, preservado após as leituras. Snapshot com 4 planilhas/867 células e 1.134 sólidos visíveis.
- 33 controles: 24 de portas (incluindo duas do canto), de 0 a 86° a cada 1°; nove gavetas nos cursos nominais de 400/500 mm, a cada 10 mm, incluindo extremos. P08/rodízios permanece fora do estudo.
- 614 corpos, 273 móveis, 130.221 pares. Combinações independentes são avaliadas em produto cartesiano; peças do mesmo controle usam o mesmo estado. Não se somam movimentos incompatíveis de uma mesma peça.
- Validação no FreeCAD: 99 poses/819 matrizes, erro máximo 9,095×10⁻¹³; volumes constantes nas poses verificadas. O avaliador passou a respeitar propriedades locais de Extensao; controle sem corpo móvel agora interrompe a varredura. O resultado anterior que mantinha gavetas paradas foi substituído.
- Triagem: 852 pares de caixas candidatos. Destes, 312 são internos à mesma dobradiça e ficaram fora da classificação de choque de uso; isso não demonstra compatibilidade interna da ferragem.
- BREP dos 540 candidatos restantes: 52 pares já intersectados na posição inicial; 28 com penetração detectada durante movimento; oito desses não constam dos 106 cenários nativos. Nos pares inicialmente intersectados não se procurou a maior penetração posterior. Limiar geométrico do estudo: volume comum >0,01 mm³, não tolerância de fabricação.
- **Folgas: 129.909 pares contabilizados, sem duplicados ou lacunas na tabela.** Dos 1.805 pares próximos, 1.528 têm mínimo BREP nas amostras e 277 somente intervalo certificado; 128.104 pares distantes conservam limite inferior de caixas. Nenhuma chamada nativa excedeu o limite de interrupção. Isso não equivale a determinar a folga exata de todos os pares.

[Interferências e estados](Interferencias_R54.csv) · [Resumo, cobertura e hashes externos](Resultado_R54.json). As 252 distâncias mínimas iguais a zero incluem contatos e penetrações; não representam 252 defeitos novos.

Os oito pares adicionais são fundos/frentes das quatro gavetas do P01 contra Peca247/Peca248 **com as portas de correr fechadas**. Exemplos: GavetaComumR005 × Peca247 em 50 mm; GavetaComumR029 × Peca248 em 20 mm. São primeiras amostras positivas visitadas, não máximo de penetração nem instante contínuo de início. Isso registra a tentativa de puxar a gaveta sem deslocar a porta; não demonstra impossibilidade de uso na sequência correta. A tabela vigente de interferências registra os controles e estados positivos, sem chamar esse volume de máximo.

## Distâncias: método e cobertura

A distância entre caixas é um **limite inferior**, não a folga física entre sólidos. O cálculo BREP de mínimos ordena esses limites e elimina somente estados que não podem melhorar o melhor valor, com tolerância numérica de 10⁻⁷ mm. Uma interseção BREP comprovada fornece distância zero, que já é mínimo da distância não assinada; não fornece profundidade de penetração.

O detalhamento usa pares cujo limite inferior AABB é até **25 mm**. Esse valor é filtro computacional, não exigência de folga ou aprovação de montagem. Os demais conservam apenas seu limite inferior, com estado correspondente claramente rotulado. A tentativa inicial sobre todos os pares não produziu linhas persistidas antes da interrupção; não há resultado inferido dessa tentativa. Os checkpoints válidos foram preservados na retomada, dividida em quatro partições sem sobreposição. A união confere SHA, pares esperados, ausência de duplicados e cobertura.

A busca também usa separação projetada nos seis eixos das caixas orientadas como limite conservador. As 20.656 matrizes de deslocamento passaram por conferência de finitude, ortogonalidade e determinante unitário. Foram registradas 59.368 avaliações de distância BREP. Na etapa final, cada par teve orçamento de 32 avaliações ou 2 s, verificado entre chamadas; o supervisor interromperia uma chamada nativa acima de 60 s (nenhuma ocorreu). Os checkpoints anteriores incluem buscas sem esse orçamento. Esses limites computacionais não são critérios físicos.

Nos 277 casos sem mínimo determinado, `distancia_minima_amostrada_mm` fica vazia: `limite_inferior_certificado_mm` e `limite_superior_amostrado_mm` delimitam o mínimo possível **da malha discreta**. Os estados indicados nesses casos são os da melhor distância já avaliada, não um ângulo comprovado de mínimo. Em 103 intervalos o limite inferior é zero: não se declara ausência de choque. A maior largura de intervalo é 6,776 mm. Não foi refinado um resultado dependente de geometria real ausente.

Mínimos são sobre as amostras; não garantem ausência de choque entre passos de 1°/10 mm. Distância zero pode ser contato ou penetração; a tabela de volume comum distingue os casos examinados. Contatos e sobreposições em fixações não são automaticamente defeitos de uso. Cotas do modelo não substituem tolerâncias e montagem real.

## Limites que permanecem

- `FaixaFixaEstudo` usa ternário de `ControleCanto.Recuo`, não suportado pelo avaliador aritmético. Esse controle não integra a varredura; a faixa fica na posição capturada, sem simular seu ajuste.
- Portas de correr do P01 permanecem fechadas. Não se inventou curso, mecanismo ou posição alternativa.
- Sem puxador individual identificado por nome/label entre sólidos ativos; Peca141 é envelope genérico de pedra/pintura/pegas. Seu contorno não prova a folga de uma pega móvel real.
- Eletros e espelhos efetivamente modelados entram pelos vínculos gravados. Não se inventou geometria interna ausente nem se extrapolou STEP de 400 para 500 mm. Curso gravado é nominal.
- Excluídos os 312 pares internos à mesma dobradiça e movimentos condicionados do P08. Paredes reais, ancoragem, resistência e suspensão não são avaliadas.
- Pergunta técnica restante: qual geometria e curso correspondem às portas de correr e às pegas efetivas? Não exige nova escolha estética de Elias; depende de desenho e vínculo documentado.

## Reprodução e rastreabilidade

Dados grandes ficam em `../outputs/Cinematica_estudo/`, fora do Git: snapshot, candidatos, pares de caixas, BREP e distâncias. Apenas resumos/CSV pequenos entram no repositório. Os scripts de estudo ficam em `ferramentas/estudos/`.

1. Definir `GP_CINEMATICA_OUT` com a pasta externa absoluta; rodar `FreeCADCmd.exe ferramentas/estudos/extrair_cinematica.py`.
2. `python -B ferramentas/estudos/varrer_articulacoes.py --cad 02_Modelo_3D/Guedala_Park_R54_Berlin.FCStd --snapshot ../outputs/Cinematica_estudo/Snapshot.json --out ../outputs/Cinematica_estudo`.
3. Rodar o verificador completo e copiar seu `$env:TEMP/gp_retrato_ultimo.json` para `../outputs/Cinematica_estudo/Retrato_nativo_R54.json`; o script confere o SHA da fonte. No FreeCADCmd, executar `validar_articulacoes_nativas.py` e, depois, `confirmar_articulacoes.py`, nos caminhos de ferramentas/estudos. O cache opcional só reaproveita pares com o mesmo SHA, matrizes, estados e candidatos; não é necessário para reproduzir o resultado.
4. `FreeCADCmd.exe ferramentas/estudos/executar_folgas_freecad.py`: padrão serial, filtro de 25 mm. `GP_FOLGA_PARTS` e `GP_FOLGA_PART` dividem por índice; `GP_FOLGA_RESUME` aponta CSV previamente conferido e seu sidecar de SHA. A retomada é opcional. Para a execução com supervisor usada aqui: `powershell -NoProfile -File ferramentas/estudos/executar_particoes_folgas.ps1 -Parts 4`, no ambiente do computador com FreeCAD 1.1.4 instalado. O supervisor exige o checkpoint `Folgas_retomada.csv` e não inicia se já houver trabalhador ativo. Não repetir sobre resultados incertos.
5. Com quatro partes e a retomada desta execução: `python -B ferramentas/estudos/unir_folgas_cinematica.py --out ../outputs/Cinematica_estudo --resume ../outputs/Cinematica_estudo/Folgas_retomada.csv --parts 4`.
6. `python -B ferramentas/estudos/resumir_articulacoes.py --source ../outputs/Cinematica_estudo --out 04_Moveis/Proximas_decisoes/Cinematica`.
7. Testes: unittest discover em ferramentas/estudos para `test_articulacoes_cinematica.py`, `test_varrer_cinematica.py` e `test_folgas_cinematica.py`. Após qualquer abertura: `python -B ferramentas/verificar_modelo/verificar_modelo.py --completo`.

Os scripts e resumos intermediários criados nesta tarefa foram substituídos pela cobertura ampliada. O histórico R52 existente permanece abaixo.

Rastreabilidade: `Folgas_BREP.csv` SHA256 `2769c5242083229ad099ac48a3ff3ddbe48aab2eaafaa1def613211e738fea92`; `Folgas_resumo.json` SHA256 `9628e5154eb5045194ed60904712242908da4852285f3f17d99a5a5e0ed480ec`. Os demais hashes constam de `Resultado_R54.json`. O CSV externo contém estados e unidades por par, além do tipo de cobertura.

**Verificação final (29/10):** 17 testes da frente passaram. `verificar_modelo.py --completo`: **Modelo OK**, 480 s, 5.834 objetos, 1.134 formas ativas, 1.363 pares de caixas e 106 cenários nativos. `verificar_tudo.py`: **OK**, consistência 19 verificações/0 com atenção; 323 avisos preexistentes de espaçamento. SHA do CAD preservado; nenhuma alteração de geometria ou base de comparação. A aprovação dos verificadores de integridade não elimina os limites e interferências nominais descritos acima.

---

# Registro histórico da extração R52

25/10/2026. A fotografia numérica agora foi extraída diretamente do arquivo R52 gravado, sem alterar a sessão aberta ou salvar controles. [Snapshot R52](Snapshot_R52.json) · [consulta](consultar_r52.py).

- 4 planilhas,867 células,24 folhas,22 correntes e2 históricas ocultas.
- Todos os dados de folhas, planilhas e controles são **exatamente iguais** aos da fotografia R51. Mudaram arquivo-fonte, hash e contagem documental5832; não se tratou uma fotografia antiga apenas como se fosse nova.
-528 poses de referência preservadas: erro máximo de CG1,82×10⁻¹²mm. Mais1.914 matrizes testadas quanto a finitude, ortogonalidade e determinante.
-**66 poses nativas adicionais da própria R52**:22 folhas em0/45/86°, comparadas após recomputação em um processo temporário FreeCAD. Erro máximo1,82×10⁻¹²mm. Cada controle retornou a0 e o arquivo-fonte permaneceu com o mesmo hash.
- O motor aritmético existente foi reutilizado, sem duplicar sua implementação. As três tentativas de executar expressões Python fora do escopo foram rejeitadas.

Executar nesta pasta:

```powershell
python consultar_r52.py --listar
python consultar_r52.py --folha Folha014 --angulo 86
python verificar_r52.py
```

Exige Python/NumPy para as consultas; **não exige FreeCAD para avaliar poses discretas**. O extrator e a conferência nativa são rotinas de preparação, executadas por FreeCADCmd e sem salvar a fonte. A faixa validada permanece0–86°; folhas históricas são excluídas por padrão.

[Verificação offline](Verificacao_offline_R52.json) · [referências nativas R52](Verificacao_nativa_R52.json) · [extração](Extracao.json). SHA256 do modelo de origem: `941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`.

Esta entrega histórica atualizou a ferramenta para a R52, então corrente. Não verifica resistência, colisão contínua, montagem comercial nem massa real. Novas geometrias, fórmulas ou posições requerem nova extração/conferência; não reutilizar o hash como autorização de fabricação.
