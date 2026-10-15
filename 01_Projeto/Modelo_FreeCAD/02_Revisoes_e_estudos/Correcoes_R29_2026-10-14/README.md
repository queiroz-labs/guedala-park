# R29 — correções da auditoria independente

[Apartamento com as correções](Guedala_Park_R29_Correcoes_Auditoria.FCStd). Base: R28 inteira, arquivo R28 preservado (SHA256 igual antes e depois). Proposta de estudo, sem liberação de corte, furação, compra ou fabricação.

A auditoria de 14/10 (leitura do R28 pelo FreeCAD, 774 peças visíveis, 1.006 pares booleanos, armários contra paredes/equipamentos) apontou cinco inconsistências físicas fora dos doze achados da R28. A R29 corrige essas cinco; os itens 6–8 da auditoria (juntas, folgas do forno, rótulos/resíduos) ficaram fora desta revisão.

## O que mudou

| # | Onde | Problema na R28 | Correção R29 |
|---|---|---|---|
| 1 | Roupeiro, 4 gavetas | Frentes encostadas (0 mm) na face traseira da porta de correr de trás | Gaveta + guias recuadas 10 mm (`Placement.y = 72 mm − Extensao`, guias y 72). Folga porta × frente: **10 mm**. Frentes superiores 142 → **130 mm** (topo 1080), 2 mm sob a prateleira curta de 1082 |
| 2 | Roupeiro, 4 gavetas | `CursoNominal` 400 com guia MOVENTO NL500, que é de extração total | `CursoNominal` **500**. Aberta, a frente fica a **62 mm** da cama (cenário 2800). Alternativa não adotada: NL400 com caixa 390 (~162 mm) |
| 3 | Gabinete tanque/cesto | Rodapé 0–110 sobreposto à base 80–98 e aos apoios do pivô | Rodapé **0–80**, sob a base; recuo 50 da face mantido |
| 4 | Gabinete tanque/cesto | Fundo 18 mm inteiro atravessando as reservas hidráulicas (4,3 L + 0,57 L) | `FundoTanqueR29`: fundo com **abertura 450 × 602** (x 70–520, z 98–700 locais). Fica em U: faixas laterais 52 mm + faixa superior 700–900 |
| 5 | Aéreo C · uso diário | Portas 270 × 1016 com 2 dobradiças | **3ª dobradiça** 71B3550 + calço 173H7100 em cada porta, a z509 (meia altura entre z80 e z938), caneco furado na folha. Lista de dobradiças/calços passa de **54 para 56** |

## Conferência

[Verificacao_R29.json](Verificacao_R29.json):

- 6.041 objetos (R28: 5.899; +142 das duas dobradiças copiadas com suas origens, dois canecos e o corte do fundo); nenhum objeto inválido.
- Os cinco conflitos reais da R28 desapareceram do teste booleano. Os únicos contatos novos são internos às duas dobradiças novas, com os mesmos volumes das 54 existentes (fontes STEP Blum).
- Terceira dobradiça acompanha a porta: conferida fechada e aberta a 90°, mesma posição relativa das outras duas. Volume removido da frente confirma 3 canecos.
- Gaveta001 aberta a 500: frente em y 2862, cama em 2800.
- Vínculo espelhado (apartamento atual) segue válido; as mudanças aparecem por ele.

## Limites e pendências

- Com o recuo, as frentes de gaveta ficam 8 mm dentro do corpo e continuam com 1 mm de folga lateral no vão (já era assim na R28). Conferir com a regulagem real.
- 10 mm à porta de correr não comporta puxador saliente; pressupõe cava/perfil ou toque. Puxadores seguem pendentes (F15).
- Curso 500 deixa 62 mm até a cama com a gaveta toda aberta: decisão de uso de Elias; trocar por NL400 é a alternativa.
- O rodapé de 80 deixa a base (80–98) aparente entre 80 e a frente inferior a 150, recuada 50; conferir acabamento.
- Fundo em U precisa de verificação de rigidez/esquadro do gabinete e da passagem hidráulica real.
- 56 dobradiças é cenário de estudo; a tabela/peso reais do fabricante decidem. As listas da R28 (`Ferragens_consolidadas_R28.csv`) não foram alteradas.
- Não refeitas as varreduras de movimento das portas de correr, nem as 173 poses antigas.
