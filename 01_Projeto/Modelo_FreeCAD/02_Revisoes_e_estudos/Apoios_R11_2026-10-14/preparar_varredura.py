from pathlib import Path
import ast
root=(Path(__file__).resolve().parent / '.').resolve()
code=((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/varrer_frentes.py').resolve()).read_text(encoding='utf-8').replace('R10','R11')
code=code.replace(" assert row['module_rotation']==[0.0,0.0,0.0,1.0],row['module_rotation']", " yaw=math.radians(row['module_yaw_deg']);cw,sw=math.cos(yaw),math.sin(yaw);module_rotation=np.array([[cw,-sw],[sw,cw]])")
code=code.replace(" mx=18 if row['side']=='left' else row['W']-18;", " mx=row['hinge_inner_x_mm'];")
code=code.replace('items.append((rect@rot.T)+base+mb)', 'items.append(((rect@rot.T)+base)@module_rotation.T+mb)')
ast.parse(code);((Path(__file__).resolve().parent / 'varrer_frentes.py').resolve()).write_text(code,encoding='utf-8')
print('Varredura preparada para sete novas folhas, orientação global incluída')
