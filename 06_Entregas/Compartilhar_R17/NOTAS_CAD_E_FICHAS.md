# Notas sobre o banco P20 e a R52

As fichas e os CSV atuais retiraram o resíduo textual “composição com receptor R47”. A direção operacional é dobradiça piano com articuladores/trava; composição real da tampa, fixação, eixo e capacidade continuam a detalhar.

A conferência direta de Document.xml da R52, SHA256 `941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`, mostrou que `BancoR43_Painel1` e `BancoR43_Painel2` têm `EspecificacaoR14` apenas como Branco TX nas faces internas, sem menção ao receptor R47 nesse campo. Portanto não é necessário alterar o CAD para retirar essa frase.

A R52 permanece preservada. O pacote não declara sincronização integral de todos os campos históricos do CAD com os estudos posteriores e não libera fabricação ou carga. Consulte as fichas operacionais e as verificações antes da execução.

Esta nota acompanha a pasta externa do pacote; não altera o ZIP imutável R17.
