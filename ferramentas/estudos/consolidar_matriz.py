"""Consolida somente a matriz vigente; nao abre CAD nem gera mapas de furacao."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / '04_Moveis/Cargas_e_ligacoes'
UPDATES = {
 'P08': ('336 cenarios de equilibrio; 1292 distribuicoes extremas; 26 casos inviaveis ao excluir uma roda de canto; seis contatos admitem os 48 casos de carga; R52 preservada',
         'Medir massa acabada e seis contatos; verificar flexao do fundo, juntas, fixacao real, guias e batente; 0/5/10/20 kg sao sensibilidades, nao carga de uso'),
 'P20': ('Kit de oficina para agenda 27/10: desenho nominal, lista com precos/fontes e formulario conjunto de 12 ensaios vazios; nenhum novo calculo ou ensaio fisico',
         'Identificar piano e par D/E; fechar apoio fixo, terminais 22/30 mm, trava/liberacao e juntas; cotar itens sem preco e executar protocolo preenchido por responsavel'),
 'P14': ('Desenho de preparacao com corte axial a completar, lista e formulario conjunto P20/P14 prontos; 8 registros dimensionais proprios preservados; zero ensaios',
         'Produto/oficina: completar bucha, pilha axial, rosca, retencao contra levantamento e acesso SW5; conferir trava a 55 graus, retirada do saco e plano de prova'),
 'P02': ('Elias27/10/2026: U1:A/U2:A/U3:A/U4:A; leves ocasionais, requisito10kg total, peso na regiao apoiada, preservar vaos/aparencia; capacidade nao demonstrada',
         'Uso definido; produto completo C01, ensaio MDF, curvas de juntas e montagem continuam pendentes. Nao repetir varredura sem dados novos'),
 'P13': ('Peca350 697x470x18 preservada; pergunta F13 Arenza ou Branco TX nas duas faces preparada; continua excluida do corte',
         'Elias: responder F13; fornecedor: produto/substrato18 e bordas. Depois atualizar auditoria por ID; apoio/juntas e ventilacao do micro seguem condicionados'),
 'P04': ('Meta10kg; fundo308/base limpa; quatro acessosSW4 nominais e pacoteT0 reconferido26/10:5retalhos,8Minifix,15registros vazios',
         'Oficina ainda indisponivel conforme Elias26/10; roteiro pronto. ExecutarT0 sem carga quando houver material/oficina;T1juntas,T2Bigfer eT3caixa continuam pendentes;parede/contatos reais depois'),
 'P12': ('Meta10kg; fundo548;9grupos/21posicoes candidatas e30cortes de carga,210pares de envelopes conferidos;12Minifix/9Confirmat,sem ligacao direta base-fundo;R52 preservada',
         'Qualificar juntas axial/cortante e caixa completa;pilotos/cabecas/torque/ferramenta reais e Bigfer com auxiliar12 pendentes;rigidez/flechaP12 nao herdadas doP17;contato inferior e parede reais'),
 'P17': ('Meta20kg; fundo550;21grupos/70posicoes candidatas e30cortes de carga,2415pares de envelopes conferidos;24Minifix/42Confirmat/4faceaface;24apoios reconciliados porv=330-y;R52 preservada',
         'Caracterizar rigidez/retencao das juntas e deformacao da caixa/referencia superior;confirmar fixadores/cabecas/pilotos/torque e ferramentaBigfer. Sem credito monolitico36;contato inferior,parede e ensaio pendentes'),
}
EVIDENCE = {
 'P04':'Aereos_suspensao/README.md', 'P12':'P12/README.md', 'P17':'P17/Base_fundo_ligacoes/README.md',
 'P05':'Cargas_e_ligacoes/README.md','P07':'Cargas_e_ligacoes/README.md','P10':'Cargas_e_ligacoes/README.md',
 'P18':'Cargas_e_ligacoes/README.md','P19':'Cargas_e_ligacoes/README.md',
 'P06':'../02_Modelo_3D/Componentes/Estudos/Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html',
 'P08':'P08/README.md',
 'P14':'P14/Reacoes_e_operacao/README.md','P16':'P16/Interface_guia_fundo/README.md','P20':'P20/Assento_fechado/README.md',
}

def main():
 with (HERE/'Andamento_20_moveis.csv').open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f,delimiter=';');fields=reader.fieldnames;rows=list(reader)
 assert sorted(r['module'] for r in rows)==[f'P{i:02}' for i in range(1,21)]
 for r in rows:
  code=r['module']
  if code in UPDATES:r['status'],r['next_action']=UPDATES[code]
  r['evidence']=EVIDENCE.get(code,r['evidence'])
  assert (HERE.parent/r['evidence']).is_file(),r['evidence']
  assert all(r[k].strip() for k in fields),code
  if code=='P13':r['proposed_owner']='Elias; projeto; produto/oficina'
  if code=='P02':r['proposed_owner']='projeto; produto/oficina'
  if code=='P03':r['name']='Maleiro reto: correr na R52; abertura A672 em estudo'
 lines=['# Matriz dos 20 moveis — consolidacao em 27/10/2026','',
 'Fechamento documental de 25/10, atualizado com preparacao P04 e kit P20/P14, uso P02 definido em27/10 e pergunta P13. 20/20 linhas revisadas; nenhuma representa capacidade fisica demonstrada ou incorporacao das propostas na R52. Numeros de formas/contatos sao o inventario historico R50, nao lista de corte atual.',
 '', 'T01: revisao da matriz concluida. T02/T03: estudos condicionados, mapas e comprovacoes ainda parciais. T04: kit documental pronto, montagem e ensaio bloqueados em produto/oficina; T05: interfaces em andamento. T06/T07: acabamentos, quantitativos e custos pendentes. T08/T09: integracao e entrega permanecem na agenda.',
 '', '| Movel | Estado comprovado | Proxima acao | Responsavel proposto / bloco planejado | Evidencia |','|---|---|---|---|---|']
 for r in rows:
  clean=lambda s:str(s).replace('|','/')
  lines.append('| '+clean(r['module']+' '+r['name'])+' | '+clean(r['status'])+' | '+clean(r['next_action'])+' | '+clean(r['proposed_owner']+' / '+r['planned_work_block_2026'])+' | [Relatorio](../'+r['evidence']+') |')
 lines += ['', 'Pendencias por tipo: projeto agora = caminhos resistentes, mapas e rigidez; produto/oficina = ferragens, materiais, juntas e ensaios; Elias = aparencia do soco62 e acabamentos ainda abertos (incluindo P13); apartamento/RT = medidas, parede, piso e ancoragens reais. Nao converter trabalho de projeto em espera generica pelas chaves.',
 '', 'Datas sao blocos planejados, nao datas de aprovacao. Consultas prontas nao foram enviadas; nenhum ensaio fisico executado. No P04, as15 linhas do formulario continuam NAO_EXECUTADO; no kit P20/P14,12 registros de ensaio vazios, alem dos8 dimensionais P14. Responsaveis sao propostos, nao contratados.',
 '', 'Fonte vigente: este CSV para as linhas preservadas e atualizacoes em [consolidar_matriz.py](../../ferramentas/estudos/consolidar_matriz.py). Regerar: `python -B ferramentas/estudos/consolidar_matriz.py` (tambem disponivel em `organizar_entregas.py --consolidar`). [Retomada](../../ESTADO_ATUAL.md).', '']
 with (HERE/'Andamento_20_moveis.csv').open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields,delimiter=';');writer.writeheader();writer.writerows(rows)
 (HERE/'Andamento_20_moveis.md').write_text('\n'.join(lines),encoding='utf-8')
 print('20/20 moveis; campos e caminhos conferidos; somente matriz CSV/Markdown atualizada.')

if __name__=='__main__':main()
