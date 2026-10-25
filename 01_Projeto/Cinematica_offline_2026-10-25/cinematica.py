"""Avalia as expressoes numericas extraidas do FreeCAD sem abrir o projeto.
Lista fechada de operacoes AST: nao usa eval/exec nem resolve objetos Python.
Trigonometricas recebem/retornam graus conforme as formulas desta fotografia.
"""
from pathlib import Path
import ast,math,re,json,functools
import numpy as np
HERE=Path(__file__).resolve().parent
FUNCTIONS=dict(sin=lambda x:math.sin(math.radians(x)),cos=lambda x:math.cos(math.radians(x)),
 atan2=lambda y,x:math.degrees(math.atan2(y,x)),sqrt=math.sqrt,min=min,max=max)
@functools.lru_cache(maxsize=4096)
def parse(text):
 s=text.strip()
 if s.startswith('='):s=s[1:]
 s=s.replace(';',',').replace('^','**')
 s=re.sub(r'(?<=\d)\s*(?:mm|deg)\b','',s)
 return ast.parse(s.strip(),mode='eval').body

class Context:
 def __init__(self,engine,overrides):self.engine=engine;self.overrides=overrides;self.cache={};self.pending=set()
 def memo(self,key,calculate):
  if key in self.cache:return self.cache[key]
  if key in self.pending:raise ValueError('Dependencia circular: '+str(key))
  self.pending.add(key)
  try:value=float(calculate())
  finally:self.pending.remove(key)
  if not math.isfinite(value):raise ValueError('Valor nao finito: '+str(key))
  self.cache[key]=value;return value
 def cell(self,sheet,name):
  addr=self.engine.aliases[sheet].get(name,name)
  if addr not in self.engine.data['sheets'][sheet]:raise ValueError('Celula desconhecida: '+sheet+'.'+name)
  text=self.engine.data['sheets'][sheet][addr]['content']
  return self.memo(('cell',sheet,addr),lambda:self.expression(text,sheet=sheet))
 def prop(self,leaf,name):
  d=self.engine.data['leaves'][leaf]
  if name in d['expressions']:
   return self.memo(('prop',leaf,name),lambda:self.expression(d['expressions'][name],leaf=leaf))
  if name in d['props']:return float(d['props'][name])
  raise ValueError('Propriedade desconhecida: '+leaf+'.'+name)
 def attribute(self,owner,name):
  if owner in self.engine.data['controls']:
   if (owner,name) in self.overrides:return self.overrides[owner,name]
   if name in self.engine.data['controls'][owner]:return self.engine.data['controls'][owner][name]
  if owner in self.engine.data['sheets']:return self.cell(owner,name)
  raise ValueError('Referencia fora da fotografia: '+owner+'.'+name)
 def expression(self,text,sheet=None,leaf=None):
  def visit(n):
   if isinstance(n,ast.Constant) and type(n.value) in (int,float):return n.value
   if isinstance(n,ast.UnaryOp):
    v=visit(n.operand)
    if isinstance(n.op,ast.USub):return -v
    if isinstance(n.op,ast.UAdd):return v
   if isinstance(n,ast.BinOp):
    a,b=visit(n.left),visit(n.right)
    if isinstance(n.op,ast.Add):return a+b
    if isinstance(n.op,ast.Sub):return a-b
    if isinstance(n.op,ast.Mult):return a*b
    if isinstance(n.op,ast.Div):return a/b
    if isinstance(n.op,ast.Pow):
     if abs(b)>16:raise ValueError('Expoente fora do escopo')
     return a**b
   if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in FUNCTIONS and not n.keywords:
    return FUNCTIONS[n.func.id](*[visit(x) for x in n.args])
   if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name):return self.attribute(n.value.id,n.attr)
   if isinstance(n,ast.Name):
    if sheet is not None:return self.cell(sheet,n.id)
    if leaf is not None:return self.prop(leaf,n.id)
   raise ValueError('Operacao nao permitida: '+ast.dump(n))
  return float(visit(parse(text)))

class Engine:
 def __init__(self,path=HERE/'Snapshot_R51.json'):
  self.data=json.loads(Path(path).read_text(encoding='utf8'))
  self.aliases={s:{r['alias']:a for a,r in cells.items() if r['alias']} for s,cells in self.data['sheets'].items()}
  if any(abs(v['props']['Abertura'])>1e-8 for v in self.data['leaves'].values()):
   raise ValueError('Fotografia requer folhas fechadas para conservar o eixo de referencia')
 def leaf_names(self,include_hidden=False):return [n for n,v in self.data['leaves'].items() if include_hidden or v['visible_effective']]
 def placement(self,leaf,angle,include_hidden=False):
  d=self.data['leaves'][leaf]
  if not include_hidden and not d['visible_effective']:raise ValueError('Folha oculta/historica: '+leaf)
  if not math.isfinite(angle):raise ValueError('Angulo nao finito')
  if not 0<=angle<=86:raise ValueError('Intervalo validado desta fotografia:0..86graus')
  expr=d['expressions']['Abertura'];match=re.fullmatch(r'(\w+)\.(\w+)',expr)
  if not match:raise ValueError('Controlador direto nao reconhecido: '+expr)
  ctx=Context(self,{match.groups():float(angle)})
  x,y,z=(-ctx.prop(leaf,'LocalX'),ctx.prop(leaf,'LocalY'),ctx.prop(leaf,'LocalZ'))
  theta=math.radians(ctx.prop(leaf,'GiroLocal'))
  # O eixo nativo desta fotografia e-Z. Nao o substituir por+Z.
  axis=np.asarray(d['source_axis'],float);axis/=np.linalg.norm(axis);a,b,c=axis
  K=np.array([[0,-c,b],[c,0,-a],[-b,a,0]],float)
  R=np.eye(3)*math.cos(theta)+(1-math.cos(theta))*np.outer(axis,axis)+math.sin(theta)*K
  local=np.eye(4);local[:3,:3]=R;local[:3,3]=[x,y,z]
  return np.asarray(d['parent_matrix'],float).reshape(4,4)@local
 def centers(self,leaf,angle,include_hidden=False):
  transform=self.placement(leaf,angle,include_hidden=include_hidden)
  return {p['name']:(transform@np.r_[p['leaf_local_center_mm'],1.])[:3].tolist() for p in self.data['leaves'][leaf]['fronts']}
