# Guedala Park — conjunto atual no FreeCAD

Abrir [Guedala_Park_R23_Rotulos_Consistentes.FCStd](../02_Revisoes_e_estudos/Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd). Versão consolidada de estudo em14/10/2026; continuidade agendada até19h em São Paulo. Todas as revisões anteriores foram preservadas.

O apartamento está espelhado, com a cozinha à esquerda ao entrar pelo vão do modelo. Portas vizinhas de giro alternam esquerda/direita. O canto usa duas portas independentes e faixas fixas; o mecanismo79T8500 permanece aposentado. Escritório, cabeceira e vizinha receberam os ajustes R18 com ferragens comuns e apoios propostos.

Para trabalhar no arquivo, usar **01 — CONTROLES ATUAIS**, escolher o ambiente e editar os campos originais descritos no [guia dos45 acessos](../02_Revisoes_e_estudos/Rotulos_R23_2026-10-14/Guia_controles_R23.md). Dez gavetas e a entrada do banheiro usam vínculos de acesso para preservar seus pais; selecionar o objeto vinculado, sem editar Placement do atalho. **02 — APARTAMENTO ATUAL** reúne a composição espelhada. Fontes e fórmulas de base continuam no referencial anterior; coordenadas globais atuais devem ser lidas nos vínculos espelhados.

Os corpos dos armários estão novamente visíveis;101 resultados antes ocultos foram expostos na R22. Rótulos de folhas/frentes/dobradiças e laterais agora correspondem à orientação física atual.152 ajustes de rótulo na R23 não mudaram geometrias ou movimentos.

## Resultados registrados

| Frente de trabalho | Registro concluído | Limite prático |
|---|---|---|
| Espelhamento | Cinco amostras, acompanhamento de dois controles e reabertura R20 | Preserva dimensões e distâncias ideais; não confirma levantamento físico |
| Portas alteradas |173 posições por frente,30 pares afetados e230 obstáculos estacionários selecionados; inclui canto atual | Amostras/envoltórias de frentes; não prova contínua, tolerância ou todos os corpos de ferragens |
| Ferragens externas das quatro folhas alteradas | Auditoria isolada concluída:256 booleanos, sem contato acima de0,1mm³; complemento168 combinações de ângulos diferentes entre folhas | Escopo amostrado de quatro folhas e seus encontros; não homologa contatos internos, continuidade, fixação, carga ou batente |
| Navegação |45 acessos por seis ambientes e11 vínculos; R21 salva/reaberta | Controles independentes, sem intertravamento ou batentes físicos |
| Exibição |101 peças/resultados atuais visíveis; R22 salva/reaberta | Mostrar corpo não calcula sua estrutura, fixação ou carga |
| Identificação |152 rótulos coerentes com controles e implantação; propriedades geométricas/fórmulas preservadas | Nomes internos e referências de fonte continuam iguais |
| Equipamentos | CorpoME23P corrigido352 e avanço70 propostoPE12G; fontes e divergências arquivadas | Não homologa instalação, ventilação ou conflitos conhecidos |

As conferências R04–R16 estão incorporadas, com seus próprios escopos e limites. Não somar todas as poses como se constituíssem uma aprovação única do apartamento. MOVENTO permanece referência estática; não há mecanismo telescópico real validado.

[Auditoria externa e limites](../02_Revisoes_e_estudos/Auditoria_externa_R23_2026-10-14/README.md): concluída fora da interface, sem salvar ou alterar a R23. Resolve a lacuna externa deixada pela chamada longa interrompida na R18 somente no escopo descrito. O complemento usa0/30/60/86 em ângulos diferentes; todos os24.192 pares metálicos ficaram separados pelo BBox conservador. Não houve repetição dos testes de frentes, bandejas ou gavetas.

## Vistas e programa

[Galeria local atual](Galeria_R28_2026-10-14.html) · [Oito acessos comentados](../02_Revisoes_e_estudos/Vistas_R21_2026-10-14/Galeria_acessos_R22.md) · [Cobertura dos vinte módulos](../02_Revisoes_e_estudos/Rotulos_R23_2026-10-14/Cobertura_modulos_R23.md).

As imagens mostram poses ilustrativas em cópia de trabalho. O arquivo atual mantém seus valores salvos; essas poses não foram aplicadas ao apartamento. Banco180×55cm/topo47cm, folha inteira800×350×70, nove gavetas comuns, bandejas455/nove gabaritos e cesto55°/saco removível preservados. A rotina de retirar também a almofada do setor da folha é proposta nova, distinta do aceite anterior para bebidas/balde.

## O que permanece aberto

Fixação, carga, tolerâncias e batentes; limitador70T3553 e contatos internos STEP desconhecidos; ferragens reais do correr/cesto/rodas, aplicação no maleiro baixo/largo e estrutura independente da gaveta baixa; vidro/adesivo/pinos/hidráulica do banheiro; materiais, apoios, retenção e manuseio do banco. A manutenção do cesto intercepta a Loop20L e depende da proposta de desobstrução temporária ainda sem endereço/manuseio comprovados.

Equipamentos mantêm as pendências documentadas: micro100mm acima versus manual300; E21 laterais70/50 versus200 recomendados e datums/conexões desconhecidos; Venax3/5 versus10cm, distância inferiorKE4GC, apoios/ventilação, isolamentoLG e retornoSuggar. Não alterar escolha expressa nem inventar instalação para eliminar essas pendências. Elias não dispõe de novas medidas da entrada do banheiro; não repetir o pedido.

[Revisão documental atual Venax/KE4GC](../02_Revisoes_e_estudos/Revisao_fontes_coccao_R23_2026-10-14/Revisao_documental.md): downloads oficiais iguais aos manuais arquivados, sem nova edição ou esclarecimento suficiente para mudar o CAD. As lacunas de cocção exigem documentação do fabricante e levantamento competente dos aparelhos/instalação; nenhuma nova decisão de preferência é necessária nesta etapa.

[Lista técnica consolidada](../02_Revisoes_e_estudos/Apartamento_espelhado_R20_2026-10-14/Pendencias_apartamento_R20.md). Novas cotas/ferragens são propostas; **sem liberação de corte, furação ou compra**. Quando a continuação depender apenas de dados indisponíveis, registrar a dependência e manter os resultados prontos, sem repetir testes ou criar revisões artificiais.
