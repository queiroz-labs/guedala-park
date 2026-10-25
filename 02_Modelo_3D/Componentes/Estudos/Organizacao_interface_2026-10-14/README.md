# FreeCAD — sessão organizada, R28 preservada

Elias pediu continuar resolvendo pendências e deixar o FreeCAD organizado. Nenhuma nova revisão CAD foi criada nesta etapa; arquivo vigente continua R28.

## Abas e memória

Havia dez revisões completas abertas, R18/R20–R28. Algumas janelas estavam marcadas como modificadas mesmo com`isTouched=False`; por isso não se inferiu ausência de alterações a partir desse sinal. A R28 não possui referências a documentos dessas outras abas.

Antes de fechar, foram gravadas **dez cópias de recuperação** emRecuperacao_abas: estado atual R28 e nove abas históricas. `saveCopy` manteve os nomes/caminhos dos documentos em memória e não sobrescreveu os arquivos originais. Os hashes originais foram conferidos em cada fechamento. [Registro](Abas_preservadas.json) · [CRC/XML e hashes das dez cópias](Integridade_recuperacao_abas.json).

As nove abas antigas foram fechadas reversivelmente; sóR28 ficou aberta. Coleta normal de objetosPython e eventos de descarteQt concluída, sem reiniciar FreeCAD/servidor/observador. Memória residente medida no mesmo processo: **16.055 MB →7.028 MB**, em unidades decimais, aproximadamente56% de redução. Memória privada também registrada. São medidas pontuais; não constituem diagnóstico definitivo do congelamento anterior ou garantia de desempenho futuro.

## Árvore e console

[Árvore](Arvore_navegacao.json):ordenação visual dos filhos da raiz, com00dados,01controles e02apartamento no início. Fontes/grupos históricos permaneceram presentes, sem ocultação, reparentamento, alterações de visibilidade geométrica ou parâmetros. Controles atuais expandidos, fontes recolhidas; câmera e enquadramento ajustados na interface, sem salvar nova geometria.

Console anterior preservado emConsole_antes_organizacao.json; as únicas linhas de erro eram a sondagem antiga de`getGlobalPlacement` no controleFeaturePython, já corrigida/documentada. Histórico arquivado e painel limpo; logs/notificações/configurações futuros continuam ativos. [Estado final](Estado_final_interface.json):R28 única aberta,5.899 objetos, nenhumInvalid, quatro portas do escritório em0°, lixeira em0, nenhuma nova linha de erro no painel. Não tratou limpeza do console como correção geométrica.

Arquivo canônico R28 manteve SHA256`2b623c09beddb4d01b581f474468ed707b9b41d8b9dc7cddc1312474fd5ecc99`. As cópias de memória podem diferir do arquivo salvo, preservando estados de sessão/visualização; não substituem automaticamente a versão canônica.

## Complemento do trecho afetado

Depois da descida20 mm do aéreo, foi conferido somente o encontro externo das quatro portas do escritório, incluindo frente, corpos de dobradiças e calços:30/60/86°, individualmente, outras portas fechadas. [ComplementoR28](../Folga_teto_R28_2026-10-14/Complemento_aberturas_R28.json):12situações/140.400 pares contra900 obstáculos estacionários, todos separados peloBBox conservador, nenhum candidato booleano, contato ou erro;52,36s em processo isolado. Não repetiu173poses antigas, apartamento inteiro, bandejas ou contatos internos. R28 e controles salvos não mudaram.

Essas doze poses não provam continuidade, tolerâncias, pessoas, todas as aberturas simultâneas ou batentes reais. Fixação/carga/teto físico e demais pendências permanecem. Revisão final Astra reservada para18h30 nesta mesma conversa; sem corte, furação, compra ou fabricação.
