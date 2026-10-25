# FreeCAD R48 — depurador sem canal de duto

24/10/2026. **[Guedala_Park_R48_Depurador_sem_canal.FCStd](Guedala_Park_R48_Depurador_sem_canal.FCStd)** parte da [R46](../Fichas_no_CAD/README.md), preservada. (R47 já nomeia o estudo Southco do banco; por isso esta revisão é R48.)

**Continuação técnica25/10, sem alterar a R51:** [carga e interface de montagemP09](../../../04_Moveis/Aereos_suspensao/README.md). ManualREV.0025 informa6,00 kg para60 cm e fixação à parede+gabinete. Entre o gabaritoPeca139 e a base há42 mm nominais; abas/adaptação e transferência de esforços ainda não estão demonstradas. Retorno de ar20 mm e ausência do canal permanecem; posições preservadas.

## O que mudou

Elias observou que o Suggar DE61IX em modo depurador não tem duto: um cano subindo pelo aéreo seria de coifa. Removida a **Reserva canal técnico · sem armazenamento** (`Peca321`, 196 × 178 × 556 mm, laranja) do aéreo D (`Modulo008`, P09). O registro de 03/10 já a tratava como reserva ilustrativa, não aprovada; o manual DE61IX REV.0025 pede só **abertura de retorno de 20 mm na largura do armário**, que continua obrigatória junto com filtros e acesso.

- **Divisor até o fundo:** a divisória `Peca320` (18 mm) passa de 118 para 312 mm de profundidade, de Y20 até a face do fundo em Y332. O aéreo D fica com dois nichos de 298 × 312 × 556 mm.
- **Prateleiras:** o P09 não tem prateleiras no CAD. Os dois níveis acima do aparelho (apoios a 197,6 e 225,4 cm, no [estudo Aéreos R00](../../../03_Ambientes/Cozinha/Aereos.md)) nunca foram aprovados nem modelados, e continuam fora do modelo.
- `Modulo008.ResumoR14` e a linha P09 da tabela `FichasR14` deixam de citar o canal; nova propriedade `StatusR48`.
- **Visualizador:** `Estudo_interativo/src/cad-data.js` sem o canal (P09 com 8 peças) e com o divisor de 31,2 cm; HTML reconstruído.
- **Fichas R14 do P09:** medidas internas, montagem, ligações, conferências de campo e resumo reescritos (sem duto, divisor de profundidade total). Ligações do divisor: base e tampo com 18 × 312 e novo encontro com o fundo, 18 × 556. Editados os dados de origem (`fabrication/*.json`, `r14/*.json`, `compile_technical_revision.py`, `Matriz_20_modulos.md`) e as fichas regeneradas. A geração foi feita numa cópia limpa do commit `4d01833`, porque os scripts geradores tinham alterações em andamento de outra sessão. Só arquivos do P09 e os índices (`Levantamento`, `Pendencias`, `Tecnica_R14.json`) mudaram.
- **Reservas ocultas sem decisão (revisão de 24/10):** a pedido de Elias, removidas do CAD a proteção lateral de 10 mm do quarto (`Peca250`), a faixa de cadeira 800 × 500 × 720 do estudo da bancada do escritório (`R45_Ref_Faixa_cadeira`) e o grupo `ReservasTecnicasR31` da cocção com seus 7 volumes de diagnóstico (cooktop 131, recorte, ar traseiro 45, entrada, inferiores e saída de ar). Nenhuma tinha dependentes nem aparecia no visualizador ou nas fichas. Tanque externo e reservas hidráulicas do cesto (P14) mantidos até a medição.
- O rodapé das fichas continua citando o CAD R45 como base; o `source_sha256` não foi trocado porque os quadros de módulo (`module-frames.json`) estão amarrados a ele.

## Verificação

[Verificacao_R48.json](Verificacao_R48.json): divisor com caixa envolvente conferida (−334, 20, 18 → −316, 332, 574) encostando no fundo; 10 objetos de reserva removidos (5.903 → 5.893); os outros 5.892 objetos com geometria e posição idênticas (1e-9 mm, [Diferencas_CAD.json](Diferencas_CAD.json) vazio), aparência idêntica, arquivo reaberto e R46 com SHA256 inalterado. Reproduzir: abrir [Remover_canal_R48.FCMacro](Remover_canal_R48.FCMacro) no FreeCAD 1.1 com interface.
