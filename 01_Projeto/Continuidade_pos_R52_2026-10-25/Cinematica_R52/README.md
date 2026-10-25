# Cinemática offline vinculada à R52

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

Exige Python/NumPy para as consultas; **não exige FreeCAD para os cálculos de continuidade**. O extrator e a conferência nativa são rotinas de preparação, executadas por FreeCADCmd e sem salvar a fonte. A faixa validada permanece0–86°; folhas históricas são excluídas por padrão.

[Verificação offline](Verificacao_offline_R52.json) · [referências nativas R52](Verificacao_nativa_R52.json) · [extração](Extracao.json). SHA256 do modelo de origem: `941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`.

Esta entrega fecha a atualização da ferramenta de cálculo para a revisão corrente. Não verifica resistência, colisão contínua, montagem comercial nem massa real. Novas geometrias, fórmulas ou posições requerem nova extração/conferência; não reutilizar o hash como autorização de fabricação.
