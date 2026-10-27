# R20 — apartamento espelhado e portas opostas

Arquivo atual: Guedala_Park_R20_Apartamento_Espelhado.FCStd. Incorpora R18/R17 e todas as revisões anteriores. Plano até19h.

O apartamento foi refletido integralmente por Xnovo=7400−Xbase; Y/Z e dimensões preservados. Não é alteração da câmera. Na arquitetura de referência, a abertura externa fica entre as paredes Peca035/Peca037: antes X7400/Y6150–6900, agora X0/Y6150–6900. Entrando no sentido +X, a parede posterior da cozinha emY7000 fica à esquerda (+Y). Essa identificação usa o vão do modelo; não constitui levantamento físico da folha/maçaneta da entrada.

A composição usa vínculos nativos App::Link aos sólidos e módulos existentes, ScaleVector=(-1,1,1), LinkTransform=True, organizados por ambiente. Foram mantidos os pais, as matrizes de base e os tipos das propriedades de parâmetros. As fontes permanecem no mesmo documento e alimentam os vínculos espelhados.237 vínculos geométricos,209 visíveis na vista geral; paredes inteiras visíveis, paredes em corte e referências de equipamentos ocultas. As quatro raízes de referências de ferragens permanecem preservadas na base, fora da exibição atual. Solução articulada R03 e históricos do canto ocultos; R04 vigente preservada.

[Espelhamento_R20.json](Espelhamento_R20.json) registra coordenadas, vínculos e sentidos. Cinco amostras — micro, purificador, geladeira e duas frentes — preservaram dimensões/coordenadas transformadas. Duas frentes acompanhadas com abertura30° na composição espelhada, resíduo máximo2,28e−13mm. [Reabertura_R20.json](Reabertura_R20.json): reabertura da versão salva confirmou as cinco amostras, oito controles finais0°, LinkTransform persistente e nenhuma expressão inválida.

Portas vizinhas do escritório/cabeceira alternam os sentidos. A reflexão inverte sentido e ordem visual, mantendo alternância. Os controles atuais têm rótulos para a orientação espelhada; **editar Abertura nos controles externos**, não a propriedade vinculada da folha. Nomes em [Montagem_R18](../Portas/Montagem_R18.json); pares cozinha/lavanderia emMontagem_R10, banheiro emMontagem_R12, demais em suas revisões. Cotas/formulações da base seguem no referencial anterior: usar os vínculos da composição atual para ler coordenadas globais do apartamento.

[R18 e conferência das quatro portas alteradas](../Portas/Portas_opostas_R18_README.md):173 posições por frente,30 pares afetados sem sobreposição amostrada,230 obstáculos estacionários separados; inclui cantoR04. Não prova continuidade, tolerância, fixação ou carga. A reflexão preserva as distâncias e colisões ideais; não repete testes antigos nem resolve incompatibilidades físicas/comerciais já registradas.

Vistas inspecionadas: [axonometric](Apartamento_Axonometrico_R20.png) e [planta superior](Apartamento_Planta_R20.png). Representam gabaritos e ferragens/fontes CAD; polimento de árvore, vistas de acesso e documentação prossegue até19h. Não são desenhos executivos.

## Falha anterior e recuperação

A R19 não foi adotada: falhou ao consultar um grupo como sólido, produzindo o traceback mostrado pelo usuário. Sua construção em memória foi encerrada sem salvar; arquivo de base e scripts preservados. A conversão em massa PropertyLink→PropertyLinkGlobal foi bloqueada pela revisão automática e **não executada**. A R20 evita essa alteração e o reparentamento geométrico; os vínculos de parâmetros originais permanecem.

Os12 arquivos verificados após a janela de recuperação estavam íntegros emCRC/XML; cópias de recuperação preservadas. [Relatório](../Equipamentos/Integridade_apos_aviso_recuperacao.json). Isso não determina a causa do aviso nem homologa todos os conteúdos CAD. O usuário fechou o FreeCAD sem responder; operações extensas agora são calculadas fora da interface quando possível.

## Pendências para revisão até19h

Consultar [pendências consolidadas](Pendencias_apartamento_R20.md). Batentes físicos, cargas/fixações, tolerâncias, ferragens-gabarito e incompatibilidades documentais dos equipamentos continuam abertos. Fontes STEP originais preservadas; não cortar/deslocar peças para apagar contatos internos desconhecidos. Sem liberação de corte/furação/compra.

Scripts nesta pasta registram etapas já executadas. Não reconstruir a R20 nem executar de novo a tentativa R19. Visibilidade foi finalizada por finalizar_visibilidade.py após corrigir LinkTransform; visibilidade_atual.py não é procedimento de instalação idempotente.
