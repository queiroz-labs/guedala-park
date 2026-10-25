# CAD oficial Blum — canto do quarto

Dados baixados diretamente do Blum E-SERVICES autenticado em 13/10/2026, pelo serviço **Produto único (3D)**. Seleção: todas as variantes de componentes, STEP, nível MEDIUM, PDF adicional. O nome automático dos ZIPs usa 14/10; a data local da consulta é 13/10, em São Paulo.

| Produto consultado | CAD oficial | Componentes sólidos |
|---|---|---:|
| CLIP top 155° 71T7550, recobrimento total, caneco para aparafusar | `71T7550/71T7550_40004143.step` | 7 |
| CLIP top 60° 79T8500, porta conjugada, niquelado, caneco para aparafusar | `79T8500/79T8500_46584366.step` | 4 |

Biblioteca nativa FreeCAD · [Prévia](Blum_Canto_CAD_Oficial.png) · [Inventário e hashes](Inventario_importacao.json).

A biblioteca mantém as geometrias internas dos STEP e apresenta os dois produtos lado a lado. Não posiciona as ferragens nas portas nem cria juntas mecânicas. Os sólidos foram importados sem erros de validade; o FCStd foi fechado e reaberto com 31 objetos e nenhum objeto inválido. Os conjuntos e seus filhos aparecem no inventário: não somar os sólidos do conjunto aos mesmos sólidos dos filhos.

Os PDFs adicionais contêm anotações 3D incorporadas. A renderização estática no Poppler mostra uma página em branco; não são fichas dimensionais 2D. Os STEP são a referência utilizável no FreeCAD.

## Limitação encontrada no configurador

No **Configurador de produtos > Sistemas de dobradiças**, a construção **Armário de canto — Porta conjugada** está disponível na configuração rápida. Ao mudar para **Detalhada**, o sistema informa conflito com a construção selecionada e remove a opção de canto. A configuração rápida não oferece dados CAD/CAM de instalação, segundo a tabela exibida pelo próprio serviço. A seleção de canto foi preservada, sem encomenda ou envio à revenda.

O acesso à conta resolveu a obtenção do CAD oficial. Permanece pendente reconstruir/verificar os movimentos internos, selecionar os calços e definir recobrimentos/furação para a aplicação do quarto. Esses arquivos não certificam a trajetória completa nem substituem a conferência das ferragens reais.

Fonte: [Blum E-SERVICES](https://e-services.blum.com/), CAD/CAM e configurador de produtos.
