from pathlib import Path
import ast
root=(Path(__file__).resolve().parent / '.').resolve()
code=((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/auditar_dobradicas.py').resolve()).read_text(encoding='utf-8').replace('R10','R11').replace('Guedala_Park_R11_Dobradicas_Comuns','Guedala_Park_R11_Apoios_Simples')
code=code.replace("wood=[o for o in module.Group if o.TypeId=='Part::Box']+[front]", "wood=[o for o in module.Group if o.TypeId=='Part::Box']+([doc.getObject('DivisorApoioVizinhaR03')] if module.Name=='Modulo003' else [])+[front]\n adjacent=[doc.getObject(x['front']) for x in data['doors'] if x['door']!=r['door'] and x['module']==r['module']]+([doc.getObject('VizinhaComCanecosR03')] if module.Name=='Modulo003' else [])")
code=code.replace('for q in wood:\n', 'for q in wood+adjacent:\n')
code=code.replace('for q in wood[:-1]:', 'for q in wood[:-1]+adjacent:')
code=code.replace('48 posições individuais','28 posições individuais')
code=code.replace("report={'cases':", "\n# Changed third leaf against existing neighbor in its proposed study opening.\nneighbour=[]\ns=doc.getObject('ControleCanto');s.set('B4','86 deg');doc.recompute()\nr=next(x for x in data['doors'] if x['door']=='Folha002');control=doc.getObject(r['control']);nf=doc.getObject('VizinhaComCanecosR03')\nfor angle in [0,30,60,86]:\n control.Abertura=angle;doc.recompute();neighbour.append({'new_door_angle':angle,'neighbor_input_deg':86,'front_intersection_mm3':common(shape(doc.getObject(r['front'])),shape(nf))})\ncontrol.Abertura=0;s.set('B4','0 deg');doc.recompute();doc.save()\nreport={'neighbor_changed_leaf':neighbour,'cases':")
code=code.replace("'simultaneous':simultaneous},ensure_ascii=False)", "'simultaneous':simultaneous,'neighbor':neighbour},ensure_ascii=False)")
ast.parse(code);((Path(__file__).resolve().parent / 'auditar_apoios.py').resolve()).write_text(code,encoding='utf-8')
print('Auditoria preparada, somente folhas alteradas R11')
