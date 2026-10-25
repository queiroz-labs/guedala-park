# Conferência da entrega e rotina leve de retomada

25/10/2026. Começar pela [entrada de retomada](../Retomada_25_10_2026.md). Esta rotina confere arquivos e referências sem recalcular placas, animar/reabrir o apartamento ou executar criadores de estudos.

Janela encerrada às07h; [automação pausada e confirmada](Automacao_pausa_confirmada.json). O manifesto de fechamento e a cópia local são gerados na sequência, preservando o conteúdo técnico concluído antes do prazo.

[Manifesto de integridade](Manifesto.json) · [resultado](Verificacao.json) · [diário e situação do encerramento](../Execucao_ate_07h_2026-10-25.md).

## Consultar e conferir

No diretório `guedala-park`, executar:

```powershell
python 01_Projeto/Conferencia_entrega_25_10_2026/verificar_entrada.py
```

A rotina compara tamanho/SHA256 com o snapshot; confere aR51 persistida com5833 objetos/7702 expressões e o hash daR50 histórica. Também verifica os links locais da entrada nova. O manifesto cobre relatórios, dados, scripts e estudos principais desta execução; não é backup integral de todo o repositório.

Se apontar diferença, ler o arquivo alterado e determinar sua origem antes de regenerar o snapshot. Mudança pode ser trabalho posterior legítimo, não prova automática de perda. Não apagar/reverter ou sobrescrever o modelo para “fazer passar”.

## Atualizar o snapshot após trabalho conferido

```powershell
python 01_Projeto/Conferencia_entrega_25_10_2026/montar_manifesto.py
python 01_Projeto/Conferencia_entrega_25_10_2026/verificar_entrada.py
```

`--encerrado` identifica o snapshot do fechamento desta janela e só é aceito a partir de25/10/2026,10:00UTC/07:00SãoPaulo. Na preparação anterior ao prazo, o manifesto permanece explicitamente em preparação. O estado da automação fica no diário; o manifesto não altera agendamentos.

Esta checagem não substitui os cálculos/limites dos relatórios nem confirma propriedades reais, capacidade ou fabricação. Não reexecuta verificações físicas inexistentes. Estudos parciais continuam separados e condicionados; o site/pacote publicado não foi atualizado nesta execução.

A conferência nativa de sessão, quando registrada, está em`Conferencia_sessao_R51.json`. Ela não salva o modelo ou descarta documentos abertos. Os quantitativos novos foram medidos dos arquivos gravados, evitando confundir mudanças de câmera da sessão com geometria incorporada.

## Cópia local do fechamento

`criar_copia.py` prepara a cópia local das entregas manifestadas depois do snapshot encerrado e conferido. Recusa executar antes das07h e recusa sobrescrever arquivo existente. O resultado, quando criado, fica registrado em`Copia_seguranca.json`, com caminho, tamanho, hash eCRC. Não inclui todo o código/histórico do repositório; não envia arquivos à internet.

O relatório da cópia não entra no próprioZIP ou no manifesto para evitar autorreferência. A checagem leve também confere seuSHA quando esse relatório existe. Preservar os arquivos-base originais; a cópia é adicional.
