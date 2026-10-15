# Biblioteca STEP dos armários — 13/10/2026

Download em lote solicitado por Elias. Quatro pacotes oficiais obtidos na conta conectada do [Blum E-SERVICES](https://e-services.blum.com/), em **Serviço de dados CAD/CAM → Pacotes → Produto único (3D)**. Formato STEP, nível MEDIUM, opção todos os produtos individualmente.

**4.211 entradas STEP; 468.712.519 bytes em ZIP (aproximadamente 469 MB).** O número inclui referências comerciais diferentes que compartilham um mesmo CAD, além de variantes de geometria e posições. Não representa 4.211 peças a instalar no apartamento.

| Pacote oficial | Arquivos STEP | Aplicação de estudo |
|---|---:|---|
| [CLIP top BLUMOTION](Pacotes/CLIP_top_BLUMOTION_STEP.zip) | 1.228 | Portas convencionais de abrir com amortecimento; variantes de dobradiças e calços |
| [CLIP top](Pacotes/CLIP_top_STEP.zip) | 1.188 | Canto conjugado, acessórios, limitador e variantes para compatibilização |
| [MOVENTO](Pacotes/MOVENTO_STEP.zip) | 542 | Corrediças para gavetas de madeira, acessórios e acoplamentos; família candidata |
| [TANDEM](Pacotes/TANDEM_STEP.zip) | 1.253 | Alternativa de corrediças para gavetas de madeira e acessórios; família candidata |

[Índice completo dos STEP](Indice_STEP.csv) · [Inventário com hashes e conferência](Inventario_downloads.json) · [Confirmação da origem](Blum_pacotes_download.png).

Todos os ZIPs passaram na leitura integral com verificação CRC. Todas as entradas STEP tiveram o cabeçalho ISO-10303-21 conferido. Esta checagem é de integridade dos downloads; não é auditoria de validade de todos os sólidos nem homologação de montagem.

## Referências já extraídas

Há **64 arquivos** em `Referencias`, correspondentes às diferentes entradas CAD dos seguintes códigos-base. Todas as variantes presentes com esses códigos-base exatos foram extraídas; outros códigos e sufixos permanecem nos ZIPs e no índice.

- CLIP top BLUMOTION: `71B3550`, `71B3650`, `71B3750`, `173H7100`, `173H7130`.
- CLIP top: `71T7550`, `79T8500`, `70T7553.09`, `173H7100`, `173H7130`.
- MOVENTO: `760H4000S`, `760H5000S`, `T51.7600`, `T51.7601`.
- TANDEM: `560H4000B`, `560H5000B`, `T51.1901`.

A coluna `referencia_extraida` do índice aponta para o arquivo pronto para abrir/importar. O sufixo numérico é o identificador CAD preservado da Blum. Entradas com mesmo código e identificadores diferentes não devem ser tratadas como intercambiáveis sem conferir a geometria e a aplicação.

## Cobertura do apartamento

| Ambiente/módulo | Dados disponíveis agora | O que segue pendente |
|---|---|---|
| Cozinha — gabinete da pia e aéreos A/B/C/D | Famílias CLIP top BLUMOTION e calços | Recobrimento, calço exato, peso e quantidade de dobradiças; ventilação e hidráulica |
| Cozinha — G1/G2/G3 | MOVENTO e TANDEM; referências nominais de 500 mm presentes | Escolher modelo/carga e recalcular construção das caixas; abertura total/amortecimento são funções aprovadas, marca não |
| Quarto — quatro gavetas inferiores | MOVENTO e TANDEM; referências nominais de 500 mm presentes | Carga, acoplamentos, caixa e interferência com portas de correr |
| Quarto — canto em L | CLIP top, 71T7550, 79T8500 e limitador 70T7553.09 | Calços, recobrimentos, movimento real e faixa proposta; biblioteca nativa anterior preservada |
| Quarto — aéreo lateral da cabeceira | CLIP top BLUMOTION e calços | Aplicação e interferência com o canto; quantidade e peso |
| Escritório — duas gavetas | MOVENTO e TANDEM; referências de 400 mm presentes | Modelo/carga e caixa. Comprimento nominal de 400 mm e abertura total aceitos; amortecimento ainda não escolhido |
| Escritório — aéreo | CLIP top BLUMOTION e calços | Divisão de portas, quantidade, recobrimento e fixações |
| Lavanderia — aéreo e eventuais portas convencionais | CLIP top BLUMOTION e calços | Aplicação exata; não estender ao basculante |
| Banheiro — gabinete/armário espelhado | Famílias de dobradiças disponíveis como referência | Definir frentes, substrato do espelho, fixação, tipo de abertura e possível gaveta antes de escolher ferragem |

Os apoios abertos do micro, a estrutura do forno e as prateleiras fixas não requerem corrediça/dobradiça comum apenas por serem peças de marcenaria. Banco baú tem tampas independentes/removíveis no estudo atual; não foi acrescentado mecanismo de elevação.

## Sistemas especiais sem referência comercial definida

O lote cobre as famílias Blum úteis às portas convencionais, canto e gavetas estudados. Permanecem sem STEP específico para a aplicação:

- Portas de correr inferiores do guarda-roupa e portas de correr do maleiro: trilhos, carros/guias, amortecimento e perfil ainda sem sistema comercial escolhido.
- Cesto basculante da lavanderia: pivôs, retenção e limite a 55° ainda sem conjunto escolhido; dobradiça comum não o substitui.
- Gaveta baixa de limpeza sobre rodas de silicone: diâmetro, carga, quantidade, guias e batentes pendentes; não recebe corrediça convencional por inferência.
- Varal: mecanismo próprio de extração/descida/travas e estrutura; corrediça de gaveta isolada não valida o conjunto.
- Puxadores em perfil preto fosco, suportes estruturais e demais fixações: seção e referência comercial exatas ainda não definidas.

Nenhum modelo ou compra foi aprovado pelo download. Os STEP são geometrias estáticas; não incluem automaticamente juntas, cinemática, carga ou furação executiva. Não transformar dimensões da caixa atual em lista de corte sem conferir as regras da ferragem selecionada.

Fonte local do levantamento: `../../05_Ferramentas_e_registros/gerar_modelo.py`, `../README.md`, `../../../Cozinha/README.md`, `../../../Escritorio/README.md`, `../../../Lavanderia/README.md`, `../../../Portas_e_quarto/README.md` e `../../../Banheiro/README.md`.
