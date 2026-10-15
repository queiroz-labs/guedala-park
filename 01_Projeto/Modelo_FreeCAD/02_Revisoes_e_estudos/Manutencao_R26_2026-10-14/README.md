# R26 — manutenção simples do cesto

[Apartamento atual](Guedala_Park_R26_Manutencao_Simples.FCStd). Incorpora a R25 e preserva todas as revisões anteriores. Elias autorizou resolver autonomamente pendências com soluções simples.

## Pendência avançada

Foi definido um **endereço temporário proposto para a lixeira Loop 20 L**, sem alterar seu lugar habitual. Antes da manutenção do cesto, afastar a lixeira **650 mm lateralmente para o centro da cozinha**. No apartamento espelhado, isso corresponde a diminuir X em650 mm; Y e Z permanecem iguais. O corpo/tampa/pedal continuam os três gabaritos existentes, não uma nova lixeira ou ferragem.

| Estado | Envelope completo no apartamento atual, em mm |
|---|---|
| Habitual, salvo | X4540–4830 / Y5410–5730 / Z0–437 |
| Temporário proposto | X3890–4180 / Y5410–5730 / Z0–437 |

O envelope completo inclui o pedal, mais profundo que o corpo. A posição temporária fica inteiramente sobre o piso ideal da lavanderia. A translação lateral completa, inclusive a volta pelo mesmo trajeto, ficou separada dos obstáculos atuais no escopo documentado. A retirada da armação de0 a400 mm, com cesto55°, ficou **100 mm afastada lateralmente** da lixeira estacionada. São distâncias nominais CAD, não tolerâncias ou espaço para uma pessoa comprovados.

## Controle e sequência

Em **01 — CONTROLES ATUAIS → Lavanderia — aéreo, cesto e manutenção da lixeira**, selecionar `ControleLoopManutencaoR26` e editar **Afastamento**:

1. `0 mm`: posição habitual. É o valor salvo; uso diário anterior preservado.
2. Para manutenção, primeiro desocupar a lixeira e mantê-la fechada; `650 mm`: posição temporária proposta.
3. Só então usar a sequência do cesto:55°, saco445/endireitar55; conjunto sustentado e retenções reais liberadas, painel200 e retirada da armação até400 como estudos.
4. Repor armação/painel, fechar o cesto e retornar **Afastamento0** antes do uso diário.

Esta sequência não possui intertravamento. O controle é de visualização geométrica, não rodízio, trilho ou método físico de movimentação. Não recomenda arrastar a lixeira nem garante pega, levantamento, peso, piso ou postura. Enquanto estacionada, a lixeira ocupa espaço de passagem; não foi aprovada circulação, uso simultâneo de outros equipamentos ou outras portas/gavetas abertas.

## Evidência e preservação

[Conferência do estacionamento](Estacionamento_Loop_R26.json):2.928 pares separados por envoltórias conservadoras, nenhum candidato que exigisse booleano, contato ou erro. Inclui o trajeto das três peças da lixeira contra958 obstáculos selecionados da composição vigente e o encontro afetado da manutenção com a lixeira estacionada. Não repetiu a auditoria geral, as antigas poses diárias do cesto ou os demais armários. A cabeça antiga de um painel foi substituída na seleção pelos dois painéis atuais; sofá/históricos seguem as correções R24/R25.

[Incorporação](Incorporacao_R26.json):5.898 objetos anteriores comparados. Todas as posições salvas, geometrias, visibilidades, pais geométricos e alvos dos vínculos foram preservados. Três peças da lixeira receberam expressões X vinculadas ao novo controle; o grupo de navegação ganhou esse controle independente. A instrução do cesto e o rótulo do grupo foram atualizados. **5.899 objetos,46 acessos de navegação,20 módulos**, nenhum objeto inválido. Nenhuma peça foi reparentada.

[Controle salvo](Verificacao_controle_R26.json):R26 aberta em processo separado e controle0→650→0 conferido; os três vínculos espelhados acompanham os corpos/tampa/pedal e o cesto permanece com os cinco controles0. Arquivo não foi alterado durante a conferência; R25 preservada.

Os processos isolados emitiram avisos de criação de cache temporário no ambiente restrito; abriram os documentos, produziram os relatórios e preservaram os arquivos. Isso não foi classificado como erro geométrico resolvido nem ocultado. Uma sondagem inicial na interface consultou Placement de um controle sem geometria; o script foi corrigido com verificação de tipo, sem alterar o projeto na chamada que falhou. Histórico emConsole_R26.json.

## Limites que continuam

O endereço e percurso CAD foram definidos como proposta. **Manuseio físico, pega/peso, piso real, sustentação da armação, ferragem comum, retenção55°, carga, hidráulica e Telca continuam pendentes.** A colisão de manutenção com a lixeira no lugar habitual permanece documentada na R15; não foi apagada para declarar solução pronta. As demais pendências R25 permanecem, sem corte, furação, compra ou fabricação liberados.

Scripts desta pasta registram etapas já executadas. Não reconstruir R26 nem repetir os testes sem mudança relevante.
