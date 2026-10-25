"""Consolida somente evidencias concluidas; nao estima tempos ausentes."""
from pathlib import Path
import json
import statistics
import zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent

def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))

geometry=read('Verificacao_binario.json')
motions=read('Verificacao_movimentos.json')
guard=read('Verificacao_guardas.json')
saver=read('Verificacao_salvamento.json')
appearance49=read('Aparencia_R49.json');appearance50=read('Aparencia_R50.json')
appearance_diff=[n for n in set(appearance49)|set(appearance50) if appearance49.get(n)!=appearance50.get(n)]
assert not appearance_diff, 'Diferencas visuais ainda abertas'
final_appearance=read('Aparencia_R50_final.json')
intentional=set(read('Banheiro_referencias_ocultas.json')['hidden_references'])
final_diff=[(n,key) for n in appearance49 for key in set(appearance49[n])|set(final_appearance[n])
            if appearance49[n].get(key)!=final_appearance[n].get(key)]
assert set(final_diff)=={(n,'Visibility') for n in intentional}
visual=read('Comparacao_visual.json')
old=read('Tempo_antes_sem_perfil.json')
r49=[read(f'Tempo_r49_corrigida_0{i}.json') for i in [1,2]]
r50=[read(f'Tempo_r50_final_0{i}.json') for i in [1,2,3]]
assert not old['profile_enabled'] and all(not x['profile_enabled'] for x in r49+r50)
assert geometry['geometry_differences']==0 and geometry.get('unexpected_final_property_differences',0)==0
assert motions['all_equal'] and saver['passed']
a=old['total_s'];b=statistics.median(x['total_s'] for x in r49);c=statistics.median(x['total_s'] for x in r50)
with zipfile.ZipFile(HERE/'Guedala_Park_R50_Completo_Otimizado.FCStd') as z:
    assert z.testzip() is None
    xml=ET.fromstring(z.read('Document.xml'))
    expressions=sum(len(p[0]) for p in xml.findall("./ObjectData/Object/Properties/Property[@name='ExpressionEngine']") if len(p))
summary={'date':'2026-10-25','timings_gui_unprofiled_s':{'original_integration_R49':[a],
    'corrected_integration_R49':[x['total_s'] for x in r49], 'corrected_integration_R50':[x['total_s'] for x in r50]},
    'original_s':a,'R49_corrected_median_s':b,'R50_corrected_median_s':c,
    'combined_reduction_percent':100*(1-c/a),'file_only_reduction_percent':100*(1-c/b),
    'size_reduction_percent':100*(1-geometry['target_bytes']/geometry['source_bytes']),
    'objects':geometry['objects'],'geometries_checked':geometry['geometries_checked'],
    'expressions_preserved':expressions,'movement_cases':motions['count'],
    'appearance_objects_checked':len(appearance49),'appearance_differences':appearance_diff,
    'intentional_bathroom_visibility_corrections':sorted(intentional),
    'image_same_pixels_percent':visual['same_pixels_percent'],
    'source_sha256':geometry['source_sha256_after'],'target_sha256':geometry['target_sha256'],
    'method':'Same FreeCAD 1.1.4 GUI process; warmed cache; document restore + camera + fitAll + redraw; no profiler. Original has one observation. Corrected R49 median of two; R50 median of three. Excludes application startup and closing previous document.'}
(HERE/'Comparacao_final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text=f'''# FreeCAD R50 completo otimizado

25/10/2026. **[Abrir o projeto completo R50](Guedala_Park_R50_Completo_Otimizado.FCStd)**. Geometria e movimentos da R49 preservados. A R50 muda a serialização do arquivo e vem acompanhada da correção de desempenho da integração local.

## Resultado medido

| Condição | Abertura até a cena pronta |
|---|---:|
| R49 com integração anterior | {a:.2f} s |
| R49 com integração corrigida | {b:.2f} s, mediana de 2 |
| R50 com integração corrigida | **{c:.2f} s**, mediana de 3 |

Redução combinada de **{summary['combined_reduction_percent']:.1f}%**. Comparando somente os arquivos com a integração já corrigida, a redução foi **{summary['file_only_reduction_percent']:.1f}%**.

Tamanho: **{geometry['source_bytes']/1e6:.2f} → {geometry['target_bytes']/1e6:.2f} MB**, redução de {summary['size_reduction_percent']:.1f}%.

As medições foram feitas no mesmo computador e processo FreeCAD 1.1.4, sem perfilador, com arquivos já em cache. Incluem leitura/restauração, câmera axonométrica, enquadramento, atualização da interface e redesenho. Não incluem iniciar o aplicativo nem fechar o documento anterior. A condição anterior tem uma medição; as amostras posteriores estão no [JSON da comparação](Comparacao_final.json). Não é um ensaio de computador básico nem de disco frio.

## O que foi corrigido

O perfil diagnóstico da R49 registrou 78.002 consultas da integração à câmera durante a abertura: cerca de 341 s em um total instrumentado de 361 s. A integração passou a ignorar criação/alteração de objetos durante a restauração em massa, mantendo o registro das edições interativas. O arquivo do projeto não precisa registrar novamente cada propriedade ao ser lido.

Essa correção já foi aplicada à instalação local, com [backup dos bytes originais](event_observer.original_bytes.py), [registro da aplicação](Integracao_aplicada.json) e [testes das guardas](Verificacao_guardas.json). O socket de integração e os controles do modelo foram mantidos. Em outro computador sem esse complemento, esse gargalo específico pode não existir.

A geometria foi salva no formato BREP binário nativo do FreeCAD. Não foram substituídos sólidos por malhas, removidos objetos, achatados mecanismos ou alterados os parâmetros de exibição. Formas vazias de supressão continuam em ASCII para contornar uma falha do leitor binário desta versão; as formas não vazias usam o formato binário.

Referência de implementação: [gravação nativa no FreeCAD](https://github.com/FreeCAD/FreeCAD/blob/main/src/App/Document.cpp), [serialização de formas](https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/Part/App/PropertyTopoShape.cpp). A fonte instalada do complemento e o perfil local sustentam o diagnóstico da integração.

## Conferência de preservação

- **{geometry['objects']:,} objetos**, com os mesmos nomes, tipos, hierarquias, referências e controles. Oito estados de visibilidade foram corrigidos no banheiro, conforme descrito abaixo; as demais propriedades foram preservadas.
- **{geometry['geometries_checked']:,} geometrias** comparadas: topologia, vértices, volume, área, posição e caixa envolvente, sem diferenças acima da tolerância de 1e-7 usada na verificação.
- **{expressions:,} expressões** preservadas; propriedades comparadas integralmente, exceto o nome interno do arquivo de representação geométrica, que muda de BREP textual para binário.
- Antes da correção adicional do banheiro, XML de aparência idêntico ao da R49 e {geometry['gui_resource_files_identical']:,} arquivos de recursos visuais transferidos com os mesmos bytes.
- Nessa etapa, aparência efetivamente carregada conferida em {len(appearance49):,} objetos, sem diferenças nas propriedades comparadas. Imagens com a mesma câmera: {visual['same_pixels_percent']:.5f}% dos pixels idênticos. [R49](Vista_R49.png) · [R50 antes do ajuste do banheiro](Vista_R50.png).
- **{motions['count']} cenários de movimento** recomputados nos dois arquivos, comparando posições de todos os objetos e caixas envolventes das formas: portas, canto, cesto, duas tampas, gavetas, correr, varal, forno, grelhas e manutenção. Todos retornaram ao estado inicial; nenhum arquivo foi salvo durante esses testes.
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
'''
(HERE/'README.md').write_text(text,encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
