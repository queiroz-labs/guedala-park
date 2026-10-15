import FreeCAD as App
EXCLUDED={'FolhaAReal','FolhaBReal','PrincipalBlumR03','PrincipalBlumR001','DivisorApoioVizinhaR03','Peca251','Peca252','Peca253','Peca254'}
BOOLEAN_TYPES={'Part::Cut','Part::Fuse','Part::MultiFuse','Part::Common','Part::MultiCommon','Part::Compound'}
def show_current(doc,module_names):
 changed=[];excluded=[];operands=[]
 def setvis(o,value,reason):
  if 'Visibility' in o.PropertiesList and o.Visibility!=value:
   changed.append({'object':o.Name,'before':o.Visibility,'after':value,'reason':reason});o.Visibility=value
 def hide(o,reason):
  setvis(o,False,reason)
  if 'Group' in o.PropertiesList:
   for c in o.Group:hide(c,reason)
 def walk(o,root=False):
  if o.Name.startswith('Historico') or o.Name in EXCLUDED:
   excluded.append(o.Name);hide(o,'historical/replaced geometry');return
  if any(p.TypeId in BOOLEAN_TYPES for p in o.InList):
   operands.append(o.Name);hide(o,'boolean operand, final result displayed instead');return
  if o.TypeId=='App::Part':
   if not root:setvis(o,True,'current assembly')
   for c in o.Group:walk(c)
  elif 'Shape' in o.PropertiesList:setvis(o,True,'current geometric result')
 for n in module_names:walk(doc.getObject(n),True)
 return {'changed':changed,'excluded':excluded,'boolean_operands_hidden':operands}
