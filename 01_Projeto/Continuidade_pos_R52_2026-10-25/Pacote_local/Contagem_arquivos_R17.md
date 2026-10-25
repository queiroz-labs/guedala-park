# Contagem de arquivos: visualizador e ZIP R17

A conferência direta do ZIP selado confirma **142 entradas**, também relacionadas no manifesto e no inventárioCRC/SHA. O campo `metadata.files=140` do QA do navegador mede outra lista: `GUEDALA_PACKAGE.files`, usada apenas como lista de caminhos de conteúdo permitidos na navegação do visualizador.

Essa lista é montada por `build_share_package.py` antes de acrescentar os dois arquivos gerados na raiz do pacote:

- `COMECE_AQUI.html`;
- `manifest.json`.

Assim, **140 caminhos de conteúdo +2 arquivos do pacote =142 entradas do ZIP**. Todos os140 caminhos estão presentes. A diferença entre o ZIP e a lista do visualizador contém exatamente esses dois nomes, sem outros arquivos ausentes. A interface não apresenta os140 caminhos como total de arquivos do ZIP; o nome curto `files` aparece somente na evidência do teste.

Não existe defeito de conteúdo ou navegação nessa diferença e não foi necessário gerar outra revisão. O R17 foi somente lido e mantém SHA256`2e8b9167d4a2b4db8a38f477e27239e728a63ff6f6fdfe1539d9d0b32525a7ea`. Nenhuma alteração foi feita no ZIP, no manifesto interno ou nos geradores nesta conferência.

[Evidência da comparação](semantica-contagem-r17.json).
