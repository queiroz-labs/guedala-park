# Unificação das pastas — 25/09/2026

[Início do projeto](../../README.md) · [Arquivo histórico](../README.md)

O projeto passa a ter uma única pasta: **guedala-park**. A estrutura mais recente foi mantida, junto com o repositório Git e as alterações locais que já existiam. O conteúdo da antiga pasta `Guedala Park` foi comparado por SHA-256 e incorporado sem substituir versões atuais por versões antigas.

## Resultado

| Destino dos arquivos antigos | Quantidade |
|---|---:|
| Cópias idênticas representadas por arquivos já existentes na estrutura organizada | 520 |
| Originais históricos preservados em ZIP | 32 |
| Vídeo, backup e pacotes exclusivos incorporados | 6 |
| Arquivos dos metadados Git antigos preservados em ZIP | 56 |
| **Total conferido da pasta antiga** | **614** |

Dos 32 originais históricos, 12 também existiam apenas em temporários da base. Foram arquivados em local permanente para não depender de uma futura limpeza de `tmp`. Os demais preservam versões diferentes, nomes e configurações originais. A redução líquida é de aproximadamente **120 MB**, já considerando os arquivos de conferência; backups anteriores foram mantidos.

Os 2.962 arquivos de conteúdo da base foram conferidos: 2.955 permaneceram idênticos e sete documentos receberam somente ajustes de navegação, links e informações sobre a unificação. Suas versões anteriores estão preservadas em ZIP. O conteúdo do estudo interativo, as decisões atuais e as alterações locais preexistentes foram mantidos. Nenhuma publicação ou commit foi realizado.

## Arquivos incorporados

- [Vídeo original da unidade espelhada](../../04_Visita_ao_apartamento/Video_Apartamento_Espelhado.mp4).
- [Backup original de 09/09/2026](../Backups/Guedala_Park_Backup_2026-09-09.zip).
- [Pacote do levantamento R00](../Pacotes_originais/A01.1_Pacote_R00.zip).
- [Pacote do levantamento R01](../Pacotes_originais/A01.1_Pacote_R01.zip).
- [Pacote complementar R02](../Pacotes_originais/A01.1_Extracao_adicional_R02.zip).
- [Pacote original do manual Venax](../Pacotes_originais/manual_oficial_26019.zip).

## Histórico e rastreabilidade

- [Mapa da unificação](Mapa_da_unificacao.json): caminho de origem, destino, tamanho, SHA-256 e, quando aplicável, entrada dentro do ZIP e versão organizada correspondente.
- [Originais anteriores](Originais_anteriores.zip): textos, dados, scripts, relatórios e configurações da pasta antiga, preservados byte a byte. São históricos; seus caminhos internos refletem a organização anterior.
- [Metadados Git anteriores](Metadados_Git_anteriores.zip): conteúdo completo de `.git` e `.git_alt` da pasta antiga, preservado como arquivo histórico. O Git ativo continua sendo o da pasta `guedala-park`.
- [Navegação anterior](Navegacao_antes.zip) e [registro dos ajustes](Ajustes_de_navegacao.json): versões anteriores e assinaturas dos sete documentos atualizados.
- [Inventário inicial](Inventario_antes.json), [conferência anterior aos ajustes de navegação](Conferencia_antes_navegacao.json) e [verificação final](Verificacao_integridade.json).
- [Verificador de integridade](Verificar_integridade.ps1): permite repetir a conferência dos destinos e links; a opção `-CheckCurrent` também verifica a base contra este inventário. Após futuras edições legítimas, essa comparação passará a apontar as mudanças.

Foram corrigidos 53 links locais que já estavam quebrados em três documentos históricos. Os links locais Markdown foram conferidos novamente após a unificação. Endereços externos e links internos dos arquivos históricos compactados não fazem parte dessa verificação.

Vídeos e ZIPs continuam ignorados pelo Git, conforme a configuração existente. Para transportar também o histórico e o vídeo, copie a pasta completa; um clone do Git não inclui esses arquivos locais. Temporários e versões diferentes foram preservados; somente cópias com conteúdo comprovadamente idêntico foram eliminadas.
