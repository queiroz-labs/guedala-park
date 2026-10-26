"""Consolida somente a matriz vigente; nao abre CAD nem gera mapas de furacao."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / '04_Moveis/Cargas_e_ligacoes'
UPDATES = {
 'P04': ('Meta de conteudo10kg; fundo308/base limpa,24Minifix/36Confirmat candidatos; quatro acessosSW4 nominais,765equilibrios/1530vetores; pacote de laboratorio preparado',
         'Executar T0 dos quatro acessos; caracterizar juntas T1, seis casos simultaneos V/T T2 e caixa inteira T3; Bigfer no divisor18/fundo e lateral direita sem capacidade demonstrada; conferir contato e parede real'),
 'P12': ('Meta10kg; fundo548 atual/base limpa; suspensao candidatau40.5/724.5 Z548;225equilibrios/450vetores,seis casos;4calcos e12acessosMinifix conferidos;R52 preservada',
         'QualificarBigfer/MDF18 e ferramenta12 no auxiliar;comprovar base/divisor,juntas e caixa com12Minifix/9Confirmat candidatos,sem apoio traseiro continuo;contato inferior/ferragens reais e parede pendentes'),
 'P17': ('Meta20kg; fundo550/base limpa; suspensao candidatau40.5/1923.5 Z514;765equilibrios/1530vetores,seis casos;8calcos e24acessosMinifix conferidos;R52 preservada',
         'QualificarBigfer/MDF18 e ferramenta:auxiliar exige reserva12;provar juntas/rigidez da caixa e referencia superior,incluir ferragens reais e medir contato inferior;parede/ancoragens apos chaves'),
}
EVIDENCE = {
 'P04':'Aereos_suspensao/README.md', 'P12':'P12/README.md', 'P17':'P17/Base_fundo_ligacoes/README.md',
 'P05':'Cargas_e_ligacoes/README.md','P07':'Cargas_e_ligacoes/README.md','P10':'Cargas_e_ligacoes/README.md',
 'P18':'Cargas_e_ligacoes/README.md','P19':'Cargas_e_ligacoes/README.md',
 'P06':'../02_Modelo_3D/Componentes/Estudos/Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html',
 'P08':'../03_Ambientes/Cozinha/Rodizios_gaveta/Selecao.md',
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
  if code=='P03':r['name']='Maleiro reto: correr na R52; abertura A672 em estudo'
 lines=['# Matriz dos 20 moveis — consolidacao em 26/10/2026','',
 'Fechamento documental de 25/10, atualizado com a preparacao P04 para laboratorio. 20/20 linhas revisadas; nenhuma representa capacidade fisica demonstrada ou incorporacao das propostas na R52. Numeros de formas/contatos sao o inventario historico R50, nao lista de corte atual.',
 '', 'T01: revisao da matriz concluida. T02/T03: estudos condicionados, mapas e comprovacoes ainda parciais. T04/T05: montagem/prototipos e interfaces em andamento. T06/T07: acabamentos, quantitativos e custos pendentes. T08/T09: integracao e entrega permanecem na agenda.',
 '', '| Movel | Estado comprovado | Proxima acao | Responsavel proposto / bloco planejado | Evidencia |','|---|---|---|---|---|']
 for r in rows:
  clean=lambda s:str(s).replace('|','/')
  lines.append('| '+clean(r['module']+' '+r['name'])+' | '+clean(r['status'])+' | '+clean(r['next_action'])+' | '+clean(r['proposed_owner']+' / '+r['planned_work_block_2026'])+' | [Relatorio](../'+r['evidence']+') |')
 lines += ['', 'Pendencias por tipo: projeto agora = caminhos resistentes, mapas e rigidez; produto/oficina = ferragens, materiais, juntas e ensaios; Elias = carga P02, aparencia do soco62 e acabamentos ainda abertos (incluindo P13); apartamento/RT = medidas, parede, piso e ancoragens reais. Nao converter trabalho de projeto em espera generica pelas chaves.',
 '', 'Datas sao blocos planejados, nao datas de aprovacao. Consultas prontas nao foram enviadas; nenhum ensaio fisico executado. No P04, as15 linhas do formulario continuam NAO_EXECUTADO. Responsaveis sao propostos, nao contratados.',
 '', 'Fonte vigente: este CSV para as linhas preservadas e atualizacoes em [consolidar_matriz.py](../../ferramentas/consolidar_matriz.py). Regerar: `python -B ferramentas/consolidar_matriz.py` (tambem disponivel em `organizar_entregas.py --consolidar`). [Retomada](../../ESTADO_ATUAL.md).', '']
 with (HERE/'Andamento_20_moveis.csv').open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields,delimiter=';');writer.writeheader();writer.writerows(rows)
 (HERE/'Andamento_20_moveis.md').write_text('\n'.join(lines),encoding='utf-8')
 print('20/20 moveis; campos e caminhos conferidos; somente matriz CSV/Markdown atualizada.')

if __name__=='__main__':main()
