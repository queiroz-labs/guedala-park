from pathlib import Path
import ast
root=(Path(__file__).resolve().parent / '.').resolve()
code=((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/auditar_dobradicas.py').resolve()).read_text(encoding='utf-8').replace('R10','R12').replace('Guedala_Park_R12_Dobradicas_Comuns','Guedala_Park_R12_Banheiro_Simples')
code=code.replace("wood=[o for o in module.Group if o.TypeId=='Part::Box']+[front]", "wood=[o for o in module.Group if o.TypeId=='Part::Box']+([doc.getObject(r['mirror'])] if 'mirror' in r else [])+[front]\n adjacent=[doc.getObject(x['front']) for x in data['doors'] if x['door']!=r['door'] and x['module']==r['module']]+[doc.getObject(x['mirror']) for x in data['doors'] if x['door']!=r['door'] and x['module']==r['module'] and 'mirror' in x]")
code=code.replace('for q in wood:\n', 'for q in wood+adjacent:\n').replace('for q in wood[:-1]:','for q in wood[:-1]+adjacent:')
code=code.replace('v=common(fa,shape(q))', "if 'mirror' in r and q.Name==r['mirror']:continue\n   moving=[fa]+([shape(doc.getObject(r['mirror']))] if 'mirror' in r else [])\n   v=sum(common(fp,shape(q)) for fp in moving)")
code=code.replace("b=fa.optimalBoundingBox();closed.append", "b=fa.optimalBoundingBox()\n   if 'mirror' in r:b.add(shape(doc.getObject(r['mirror'])).optimalBoundingBox())\n   closed.append")
code=code.replace("front.Tool.Shapes[0 if h['level']==r['hinges'][0]['level'] else 1]", "front.Tool.Shapes[[x['level'] for x in r['hinges']].index(h['level'])]")
code=code.replace("a,b=shape(doc.getObject(r['front'])),shape(doc.getObject(q['front']));v=common(a,b)", "ra=[doc.getObject(r['front'])]+([doc.getObject(r['mirror'])] if 'mirror' in r else []);rb=[doc.getObject(q['front'])]+([doc.getObject(q['mirror'])] if 'mirror' in q else [])\n   v=sum(common(shape(a),shape(b)) for a in ra for b in rb)")
code=code.replace('48 posições individuais','16 posições individuais, madeira/espelho representados')
ast.parse(code);((Path(__file__).resolve().parent / 'auditar_banheiro.py').resolve()).write_text(code,encoding='utf-8')
print('Auditoria preparada: quatro folhas alteradas R12')
