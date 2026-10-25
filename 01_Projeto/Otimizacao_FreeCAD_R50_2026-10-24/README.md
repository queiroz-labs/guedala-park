# FreeCAD R50 completo otimizado

25/10/2026. **[Abrir o projeto completo R50](Guedala_Park_R50_Completo_Otimizado.FCStd)**. Geometria e movimentos da R49 preservados. A R50 muda a serialização do arquivo e vem acompanhada da correção de desempenho da integração local.

## Resultado medido

| Condição | Abertura até a cena pronta |
|---|---:|
| R49 com integração anterior | 314.64 s |
| R49 com integração corrigida | 17.28 s, mediana de 2 |
| R50 com integração corrigida | **14.68 s**, mediana de 3 |

Redução combinada de **95.3%**. Comparando somente os arquivos com a integração já corrigida, a redução foi **15.0%**.

Tamanho: **23.64 → 20.51 MB**, redução de 13.2%.

As medições foram feitas no mesmo computador e processo FreeCAD 1.1.4, sem perfilador, com arquivos já em cache. Incluem leitura/restauração, câmera axonométrica, enquadramento, atualização da interface e redesenho. Não incluem iniciar o aplicativo nem fechar o documento anterior. A condição anterior tem uma medição; as amostras posteriores estão no [JSON da comparação](Comparacao_final.json). Não é um ensaio de computador básico nem de disco frio.

## O que foi corrigido

O perfil diagnóstico da R49 registrou 78.002 consultas da integração à câmera durante a abertura: cerca de 341 s em um total instrumentado de 361 s. A integração passou a ignorar criação/alteração de objetos durante a restauração em massa, mantendo o registro das edições interativas. O arquivo do projeto não precisa registrar novamente cada propriedade ao ser lido.

Essa correção já foi aplicada à instalação local, com [backup dos bytes originais](event_observer.original_bytes.py), [registro da aplicação](Integracao_aplicada.json) e [testes das guardas](Verificacao_guardas.json). O socket de integração e os controles do modelo foram mantidos. Em outro computador sem esse complemento, esse gargalo específico pode não existir.

A geometria foi salva no formato BREP binário nativo do FreeCAD. Não foram substituídos sólidos por malhas, removidos objetos, achatados mecanismos ou alterados os parâmetros de exibição. Formas vazias de supressão continuam em ASCII para contornar uma falha do leitor binário desta versão; as formas não vazias usam o formato binário.

Referência de implementação: [gravação nativa no FreeCAD](https://github.com/FreeCAD/FreeCAD/blob/main/src/App/Document.cpp), [serialização de formas](https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/Part/App/PropertyTopoShape.cpp). A fonte instalada do complemento e o perfil local sustentam o diagnóstico da integração.

## Conferência de preservação

- **5,893 objetos**, com os mesmos nomes, tipos, hierarquias, referências e controles. Oito estados de visibilidade foram corrigidos no banheiro, conforme descrito abaixo; as demais propriedades foram preservadas.
- **1,546 geometrias** comparadas: topologia, vértices, volume, área, posição e caixa envolvente, sem diferenças acima da tolerância de 1e-7 usada na verificação.
- **7,702 expressões** preservadas; propriedades comparadas integralmente, exceto o nome interno do arquivo de representação geométrica, que muda de BREP textual para binário.
- Antes da correção adicional do banheiro, XML de aparência idêntico ao da R49 e 7,881 arquivos de recursos visuais transferidos com os mesmos bytes.
- Nessa etapa, aparência efetivamente carregada conferida em 5,893 objetos, sem diferenças nas propriedades comparadas. Imagens com a mesma câmera: 99.99569% dos pixels idênticos. [R49](Vista_R49.png) · [R50 antes do ajuste do banheiro](Vista_R50.png).
- **18 cenários de movimento** recomputados nos dois arquivos, comparando posições de todos os objetos e caixas envolventes das formas: portas, canto, cesto, duas tampas, gavetas, correr, varal, forno, grelhas e manutenção. Todos retornaram ao estado inicial; nenhum arquivo foi salvo durante esses testes.
- R49 original com SHA256 inalterado e ZIP da R50 verificado.

Evidências: [geometria e propriedades](Verificacao_binario.json), [diferenças geométricas](Diferencas_geometria.json), [diferenças de propriedades finais](Diferencas_propriedades_finais.json) e [movimentos](Verificacao_movimentos.json). O teste garante equivalência ao modelo anterior nos casos comparados; as condições técnicas de fabricação já registradas continuam nas fichas.

## Correção da visualização do banheiro

Na conferência, Elias identificou volumes estranhos sobre o gabinete. Eram referências de acesso/desmontagem e hidráulica que deveriam estar ocultas, mas estavam visíveis também na R49. Foram ocultados apenas oito objetos do grupo BC43_Referencias. O fundo original, caixa, ferragens, portas de correr e seus controles continuam presentes; nenhuma geometria foi removida. [Ver o banheiro corrigido](Banheiro_sem_referencias.png) · [Registro da correção](Banheiro_referencias_ocultas.json) · [oito diferenças de visibilidade](Diferencas_visuais_finais.json).

A comparação de imagem e aparência integral acima corresponde à otimização antes dessa correção intencional. Depois dela, a aparência efetiva dos 5.893 objetos foi comparada novamente: apenas essas oito visibilidades mudaram. As duas folhas de correr do banheiro também foram incluídas no teste de recomputação de movimentos.

## Abrir e continuar editando

Abra **Guedala_Park_R50_Completo_Otimizado.FCStd** no FreeCAD. O arquivo continua completo e editável. A R49 permanece na pasta original como base preservada.

Após editar, use **[Salvar_otimizado.FCMacro](Salvar_otimizado.FCMacro)** pelo menu Macro → Macros → Executar e escolha o destino. Mantenha **[serializacao_binaria.py](serializacao_binaria.py)** ao lado da macro. Ela grava o documento completo, trata as formas vazias e restaura a preferência global anterior. O salvamento comum do FreeCAD continua funcionando, mas pode voltar a gravar o BREP textual e perder parte do ganho de leitura do arquivo. A correção da integração continua válida.

A geometria do site e das fichas permanece a da R49; esta otimização local não publicou nem substituiu o pacote compartilhável R16. Para encaminhar a versão otimizada, use o arquivo R50 e os auxiliares de salvamento desta pasta.

## Reproduzir ou reverter

`criar_binario.py` e `verificar_movimentos.py` são executados pelo `freecadcmd.exe`; a primeira salva/confronta a candidata e a segunda compara recomputações sem salvar alterações. `medir_abertura.py` roda na GUI, após configurar `job.json`; `medir_serie.py` executa a série alternada de arquivos. `consolidar_resultados.py` gera esta página e o resumo.

Para voltar à versão anterior, abra a R49 preservada. A correção do complemento pode ser revertida restaurando os bytes do backup ao caminho exato registrado em `Integracao_aplicada.json`, com o FreeCAD fechado. Nenhum modelo anterior foi sobrescrito.
