# Publicação do estudo — 13/09/2026

- Site: https://queiroz-labs.github.io/guedala-park/
- Moodboard: https://queiroz-labs.github.io/guedala-park/moodboard/
- Commit publicado: `a439989575531b8f6caf0895a70148fc3c053bb1`.
- Publicação concluída: https://github.com/queiroz-labs/guedala-park/actions/runs/34775941883.

Elias escolheu explicitamente publicar apenas o site e o moodboard, preservando os demais documentos novos localmente. O commit completo `8f0a2ae` foi salvo, mas não foi enviado. A publicação usa um commit separado com 14 arquivos de HTML, fontes, imagem, SVG do interior incorporado, instruções e configuração. Nenhum novo PDF, áudio, pesquisa ou registro do apartamento foi incluído nesse envio. Arquivos que já estavam no repositório remoto antes desta solicitação não foram removidos.

## Continuidade

A cópia principal do projeto mantém o histórico completo local. A branch `codex/pages-publication`, no diretório de trabalho `tmp/pages-publication`, contém a versão pública e foi enviada a `origin/main`. As duas linhas de histórico têm escopos diferentes: não enviar nem mesclar o histórico completo local para o remoto sem nova autorização explícita para os documentos.

Para atualizar o site, transferir somente as mudanças pertinentes aos arquivos públicos para a branch de publicação, reconstruir e conferir o artefato `.site`, criar o commit e enviar a `origin/main`. O fluxo do GitHub publica automaticamente os dois HTML e a imagem. A pasta `.site` local e auxiliares em `tmp` são ignorados pelo Git.

Verificação final no endereço público: página principal e moodboard abriram; estados e conta de circulação funcionaram; imagem de materiais respondeu; layouts de computador e celular sem transbordamento horizontal nem erro JavaScript nos testes. Validação em emulação de 1440 × 1000 e 412 × 915 pixels lógicos.
