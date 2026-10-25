"""Snapshot de integridade das entregas, sem recalcular ou abrirCAD."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
folders=['Revisao_sem_tubos_R51_2026-10-25','Cargas_e_ligacoes_R50_2026-10-25','Solucoes_marcenaria_sem_tubos_2026-10-25',
 'P11_ligacoes_sem_tubos_2026-10-24','P01_apoios_ao_piso_2026-10-25','Bancada_marcenaria_2026-10-25',
 'P20_assento_fechado_2026-10-25','P14_reacoes_e_operacao_2026-10-25','P16_gavetas_estabilidade_2026-10-25',
 'P04_P15_suspensao_2026-10-25','Cinematica_offline_2026-10-25','Aereos_suspensao_P09_P11_P12_P17_2026-10-25',
 'P17_base_fundo_ligacoes_2026-10-25','P01_massas_equilibrio_2026-10-25','P01_P03_caminho_superior_2026-10-25',
 'P15_composicao_parcial_2026-10-25','P16_interface_guia_fundo_2026-10-25','Quantitativos_estudos_2026-10-25']
suffixes={'.md','.py','.json','.fcstd','.csv','.png','.html','.txt'}
paths=set()
for f in folders:
 folder=ROOT/f;assert folder.is_dir(),f
 for p in folder.iterdir():
  if p.is_file()and p.suffix.lower()in suffixes:paths.add(p)
for n in ['Estado_atual.md','Plano_execucao_ate_31_10_2026.md','Execucao_ate_07h_2026-10-25.md','Retomada_25_10_2026.md','Verificacao_consistencia.md',
 '../README.md','Otimizacao_FreeCAD_R50_2026-10-24/Guedala_Park_R50_Completo_Otimizado.FCStd',
 'Otimizacao_FreeCAD_R50_2026-10-24/serializacao_binaria.py','Otimizacao_FreeCAD_R50_2026-10-24/README.md',
 '../02_Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf',
 'Modelo_FreeCAD/02_Revisoes_e_estudos/Montagem_R07_2026-10-14/Fabricacao_corrigida/productionDrawings/MOVENTO-Gaveta-Sem-reling-40-kg-Comprimen.PDF']:
 p=(ROOT/n).resolve();assert p.exists(),n;paths.add(p)
for n in ['README.md','montar_manifesto.py','verificar_entrada.py','registrar_automacao.py','criar_copia.py','Conferencia_sessao_R51.json',
 'Automacao_configuracao_lida.json','Automacao_pausa_confirmada.json']:
 p=HERE/n
 if p.exists():paths.add(p)
now=datetime.now(timezone.utc);deadline=datetime(2026,10,25,10,tzinfo=timezone.utc)
closed='--encerrado'in sys.argv
if closed:assert now>=deadline,'Nao encerrar antes das07:00SP/10:00UTC'
rows=[]
for p in sorted(paths,key=lambda p:str(p)):
 p=p.resolve();rows.append(dict(path=Path(os.path.relpath(p,ROOT)).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
out=dict(created_UTC=now.isoformat(),window_deadline_UTC=deadline.isoformat(),phase='encerramento'if closed else 'preparacao_antes_do_prazo',files=rows,
 source_R51_sha256='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16',
 historical_R50_sha256='1eda9a56e7346f5e08d5b4a391a57b4407132f14a142efdef1e2e5699c4dfd69',
 physical_tests=0,scope='Snapshot de arquivos, nao recertificacao dos modelos fisicos ou incorporacao de estudos. Manifesto e seu resultado sao excluidos do proprio hash.')
(HERE/'Manifesto.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(dict(files=len(rows),phase=out['phase'])))
