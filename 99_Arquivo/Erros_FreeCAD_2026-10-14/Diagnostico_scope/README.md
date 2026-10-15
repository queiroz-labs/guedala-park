# Avisos App::Part de escopo — histórico e reprodução R25

**Os avisos capturados não reproduziram no arquivo R25 canônico.** O teste separado abriu a R25, marcou somente os20 módulos principais com `touch()` e executou um recálculo. O log dessa abertura/recálculo não contém `out of the allowed scope`, nenhuma expressão ficou inválida e o SHA do CAD permaneceu idêntico. Não há evidência que justifique alterar os tipos de vínculos ou hierarquias da R25 para corrigir esses avisos históricos.

## Evidência de execução atual

`Probe_scope_R25.json` registra arquivo exato, hash antes/depois,5.898 objetos, os20 módulos, tipos dos parâmetros, alvos, pais geométricos e grupos não geométricos. O processo foi `FreeCADCmd.exe`1.1.4 em modo seguro, `GuiUp=False`; duração3,406 s. `recompute()` retornou53, sem módulos ainda marcados `Touched` ou objetos `Invalid`.

`Probe_console_R25.log` tem marcadores separados de antes/depois da abertura, touch dos20 e antes/depois do recálculo. **Zero avisos de escopo nessas fases.** Essa evidência é mais específica que apenas observar ausência de `Invalid`: a emissão real do console foi capturada. Os avisos de criação de cache temporário do sandbox presentes no console são distintos dos avisos App::Part e não foram atribuídos ao modelo.

Os20 campos `PlanilhaDimensoes` continuam `App::PropertyLink`, apontando para `Dimensoes`/`DimensoesNNN`. Os módulos atuais têm **pai geométrico nenhum**, agrupados pelos ambientes não geométricos. As planilhas também têm pai geométrico nenhum e pertencem ao grupo `Documentacao`. O invólucro geométrico `FonteApartamentoR19` e os `FonteAmbienteR...` da tentativa abortada não existem naR25. Nenhum tipo, status, valor, transformação ou pai foi modificado pelo teste.

## O que o histórico mostra

O texto de `Erros_interface.json` foi capturado em dois editores que duplicam as mesmas mensagens. Após deduplicação, existem **28 avisos App::Part** e **um App::DocumentObjectGroup**:

| Horário registrado | Mensagens distintas | Contexto |
|---|---:|---|
| 08:23:15 | 15 App::Part | Construção abortada R19 |
| 08:23:18 | 3 App::Part | Construção abortada R19 |
| 08:27:05 | 10 App::Part | Tentativa de continuação R19 |
| 09:11:14 | 1 App::DocumentObjectGroup | Inserção direta da gaveta no grupo de navegação R21, interrompida e corrigida |

Não há nova mensagem de escopo posterior a09:11:14 no histórico capturado. O teste atual R25 foi uma captura independente, sem limpar ou suprimir mensagens. `Ligacoes_e_historico_R25.json` guarda as linhas deduplicadas e os horários.

## Causa da tentativa R19

O script preservado `Apartamento_espelhado_R19_2026-10-14/espelhar_apartamento.py` criava `FonteApartamentoR19` e grupos de ambiente **App::Part**, retirando raízes dos antigos grupos não geométricos e inserindo módulos/geometrias nesses novos pais geométricos. As planilhas de dimensões e o controle do canto permaneciam fora desses invólucros. Esse desenho introduzia fronteiras de escopo novas para dependências que anteriormente compartilhavam o nível de documento. O texto dos avisos cita precisamente essas dependências `DimensoesNNN`/`ControleCanto` e seus destinos fora da fronteira permitida.

A R20 adotou vínculos espelhados aos resultados/raízes existentes e organização por grupos não geométricos; a R25 mantém essa solução. A causalidade é sustentada pelo código/histórico, pela ausência dos invólucros naR25, pela preservação dos vínculos e pela reprodução atual sem avisos. Não se executou de novo a R19 ou um reparentamento experimental para repetir seu defeito.

NaR25, a pesquisa XML **não encontrou propriedade chamada `FonteControle`**. O registro traz separadamente83 expressões que referenciam `ControleCanto`, preservadas em diferentes objetos do canto, incluindo históricos. A menção antiga a esse controle não deve ser usada como justificativa para criar ou converter um campo inexistente.

## Reparo mínimo indicado

Para este grupo específico de mensagens, o reparo estrutural já está incorporado na composição R20/R25: **não acrescentar o invólucro App::Part da R19**. Manter pais e parâmetros atuais. O responsável pode preservar este relatório e o console antigo, identificar os erros como históricos e apresentar uma sessão limpa após corrigir outros erros atuais. Limpar a apresentação do histórico por si só não foi tratado como prova de correção; a captura/reprodução atual acima fornece a evidência.

Não há recomendação de conversão em massa `PropertyLink`→`PropertyLinkGlobal`, anteriormente rejeitada pela revisão automática. Também não é necessário mover planilhas para dentro de módulos, remover controles históricos, apagar parâmetros, alterar status ou reparentar geometria: essas ações mudariam escopos/dependências desnecessariamente e poderiam afetar o funcionamento/organização.

O limite da prova é a abertura e o recálculo explícito dos20 módulos principais daR25. Não reproduz toda interação futura ou todo objeto de arquivo histórico. Se nova mensagem surgir durante uma ação específica, registrar documento/nome/etapa atuais e revisar somente a fronteira afetada. Não concluir que todo erro da interface pertence a este grupo; PySide2/Qt, tracebacks de scripts antigos e mensagens de recuperação são investigações separadas.

## Arquivos

- `probe_scope.py`: teste somente em memória; não chama `save()`/`saveAs()`.
- `Probe_scope_R25.json`: estado/links/pais/hashes.
- `Probe_console_R25.log`: console completo e fases.
- `Ligacoes_e_historico_R25.json`: tipos/alvos/grupos do XML e contexto do histórico deduplicado.

Sem uso da interface, salvamento CAD, alterações de tipos/propriedades/pais, testes booleanos ou mudanças de scripts obsoletos.
