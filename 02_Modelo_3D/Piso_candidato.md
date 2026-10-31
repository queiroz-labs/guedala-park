# Piso por tipo — macro e aceite do candidato

**Candidato; aprovação PENDENTE.** Escopo reduzido por Elias, 30/10/2026, nesta conversa: terminar somente a macro independente do rodapé e o teste da grade; notas neste arquivo, sem editar os READMEs compartilhados, o estado atual ou o relatório de outra sessão.

Fonte padrão: `Guedala_Park_R54_Berlin.FCStd`, SHA256 `4a2996ee63dd6f2f3dc302025a73fb65011b3339bae510130732859706049528`. A macro copia essa fonte para fora do repositório e salva somente a cópia pela GUI. Não altera o vigente, a base, os cenários ou candidatos de outras sessões. Sem número novo: R55 identifica o candidato paralelo do box verde; a integração ficará para a terceira sessão.

## Peças e limites

| Grupo novo | Peça | Área nativa (m²) | Regra |
|---|---|---:|---|
| `Piso_vinilico` | `Vinilico_continuo` | 30,9751 | Um sólido, Olmo claro; sala, cozinha, circulação, escritório e quarto, com as passagens |
| `Piso_lavanderia` | `Lavanderia_Iseo_Marfim` | 2,0769 | Eliane Iseo Marfim, ivory, área molhada independente |
| `Piso_lavanderia` | `Soleira_cozinha_lavanderia` | 0,0644 | Faixa de encontro de 40 mm; produto/perfil/junta nominais e pendentes |
| `Piso_banheiro` | `Banheiro_Travertino_Reale_Greige` | 2,5916 | Porcelanato greige, separado do vinílico |
| `Piso_banheiro` | `Soleira_banheiro` | 0,0700 | Vão 700 × 100 mm; vinílico somente como hipótese visual sob a folha |

Os cinco sólidos ocupam Z −50..0 mm, com topo a zero. Os nove antigos `Peca` a `Peca008` conservam nome, forma e posição, mas ficam ocultos: a regra oficial de objetos removidos impede apagá-los. Não são piso ativo duplicado.

Contorno definido pelas faces internas externas nativas e pelas paredes `ParedesInteiras`, sem mover paredes ou outros objetos. Recorta a projeção das paredes térreas para evitar piso dentro delas. A lavanderia nativa começa em Y=5390 mm, enquanto a planta gráfica usa 5460 mm; a soleira acompanha o contorno nativo. Matriz `floors` do site e quantitativos de 30,8101 m² preservados; a geometria nativa não redefine a compra.

## Reprodução e integração posterior

- [Macro GUI](../ferramentas/estudos/modelar_pisos.FCMacro): definir `GP_REPO` e `GP_PISOS_DIR` externos; executar no FreeCAD GUI. Saída `Guedala_Park_Piso_candidato.FCStd`; recusa sobrescrever arquivo existente.
- [Teste somente leitura](../ferramentas/estudos/test_pisos_freecad.py): com as mesmas variáveis, executar no FreeCADCmd. Reabre a cópia salva, confere cinco sólidos válidos, antigos ocultos e contatos das soleiras; grava `Aceite_pisos.json` na saída externa.
- A fonte padrão é exclusivamente o R54 original, sem depender de rodapé ou verde. Na integração posterior, `GP_PISOS_FONTE` pode apontar a uma cópia externa já tratada por outra macro; a fonte continua somente leitura. Repetir os testes e a inspeção completa do conjunto.

## Aceite

Execução GUI sobre R54 original e reconferência do arquivo salvo no FreeCADCmd: **59.104 células interiores; zero células sem piso e sem parede; zero sobreposições de volumes dos cinco pisos; zero área de piso sob parede**. Os cinco sólidos são fechados e válidos; o vinílico é um único sólido. Resultado do teste: **OK**.

Contatos exatos em ambas as faces de cada soleira: cozinha/lavanderia **80.500 mm² por face**; banheiro **35.000 mm² por face**, todos com interseção volumétrica zero.

Controle anterior: **569 células com falta parcial/total de cobertura, 0,2866 m² sem piso nem parede**. Os pisos sala/cozinha se sobrepunham em **0,49 m² / 24.500.000 mm³**; havia também 0,1356 m² de piso sob paredes. A prova detectou a fresta artificial de 1 mm × 100 mm (0,0001 m²) e a penetração artificial de 1 mm (5.000 mm³).

As **1.489 geometrias próprias anteriores** conservam suas assinaturas, posições e expressões. Aparência anterior preservada, exceto a visibilidade dos nove pisos antigos. Rodapé e verde não estão neste candidato independente.

Candidato externo: `../outputs/Pisos_candidato/Guedala_Park_Piso_candidato.FCStd`, salvo pela GUI. SHA256 `cd8ace566d57475c52e14cbe58827c248a316c752cca9bd145bc85a4f9493c0d`. Evidências completas ao lado: `Pisos.json` (inclui a lista das células antigas), `Assinaturas_geometricas.json` e `Aceite_pisos.json`. Assinaturas: SHA256 `c059ee2777ab393a6531875f3b42ddc63e5515a24b0d85ec389af098a72563a6`.

A grade de 25 mm é subdividida nas arestas ortogonais do BRep. Cada subcélula interior precisa de piso ou parede; assim uma fresta menor que o passo também é detectada. O contorno de teste é fixo, independente das peças novas. Interseções de volume são verificadas por booleanas exatas entre cada par de pisos. Controles negativos: nove pisos antigos, fresta de 1 mm e penetração de 1 mm.

## Pendências para a integração

1. Qual material ficará sob a folha da porta do banheiro?
2. Qual produto/perfil e espessura de junta serão usados nas duas transições?
3. A terceira sessão precisa compatibilizar o conjunto com rodapé e verde, repetir a inspeção completa e apresentar o relatório antes de qualquer decisão sobre a base.

Verificação geral `python ferramentas/verificar_tudo.py`: **OK**, usando TEMP/TMP externos ao repositório. A primeira tentativa falhou por permissão na pasta temporária do sandbox; a execução com diretório externo passou, sem mudar testes ou regras.

Não houve exportação CAD_DATA, alteração do site, promoção a vigente, atualização de base ou push neste escopo reduzido. A inspeção completa com movimentos fica para a integração solicitada; este aceite se limita aos pisos e à preservação registrada acima.
