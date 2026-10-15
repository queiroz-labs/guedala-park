from pathlib import Path
import json,math,ast
root=(Path(__file__).resolve().parent / '.').resolve()
# Refine ONLY the new whole-seat70 bound that was inconclusive with5-degree spacing.
# Reuse pure polygon helpers without executing any FreeCAD mutations/tests from that file.
tree=ast.parse(((Path(__file__).resolve().parent / 'complementar_acessos.py').resolve()).read_text(encoding='utf-8'))
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['intersects','segment','distance']]
exec(compile(ast.Module(body=funcs,type_ignores=[]),'<polygon_helpers>','exec'))
table=[(-700,720),(50,720),(50,750),(-700,750)];samples=[]
for deg in range(91):
 t=math.radians(deg);c,s=math.cos(t),math.sin(t)
 poly=[(448+u*c+z*s,470-u*s+z*c) for u,z in [(-448,-70),(0,-70),(0,0),(-448,0)]]
 samples.append({'angle_deg':deg,'distance_mm':distance(poly,table)})
minimum=min(samples,key=lambda x:x['distance_mm']);bound=math.hypot(448,70)*math.radians(.5)
out={'reason':'Novo envelope70 do primeiro assento: limite anterior5graus=-2,20mm não confirmava separação contínua. Refinar1grau, sem repetir901 do modelo antigo ou28 poses CAD.','samples':len(samples),'minimum':minimum,'half_step_vertex_displacement_bound_mm':bound,'continuous_ideal_gap_lower_bound_mm':minimum['distance_mm']-bound,'proof_scope':'A distância entre polígonos é Lipschitz no maior deslocamento de vértice. Cada ângulo está até0,5grau de uma amostra; movimento máximo limitado porR*delta, R=hypot448,70. Primeiro assento conservador70/448 em eixo448/470 e tampo no corteu[-700,50]/Z[720,750]. Almofada extra2 posterior permaneceu>=398, fora da projeção da mesa. Não prova ferragem/carga/tolerância/mãos/deformação/objetos no tampo ou entorno completo.'}
assert out['continuous_ideal_gap_lower_bound_mm']>0
((Path(__file__).resolve().parent / 'Margem_assento_R16.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
