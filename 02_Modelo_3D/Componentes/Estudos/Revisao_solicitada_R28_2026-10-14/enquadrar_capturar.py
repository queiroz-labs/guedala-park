from pivy import coin
import FreeCAD as App, FreeCADGui as Gui
from pathlib import Path
root=(Path(__file__).resolve().parent / '.').resolve()
d=App.ActiveDocument;assert d.Name=='RevisaoVisualR28'
scene=globals()['scene']
cameras={'cozinha':[.12,-1,.3],'lavanderia':[.12,-1,.3],'quarto':[-1,-.8,.45],'escritorio':[-1,-.2,.35],'banheiro':[.12,-1,.3],'banco':[1,-.4,.6]}
files={'cozinha':'03_cozinha.png','lavanderia':'04_lavanderia.png','quarto':'05_quarto.png','escritorio':'06_escritorio.png','banheiro':'07_banheiro.png','banco':'08_banco.png'}
Gui.updateGui();cfg={'camera':cameras[scene]}
fragment=((Path(__file__).resolve().parent / 'vista_detalhe.py').resolve()).read_text(encoding='utf-8').split('d.recompute();v=')[1].split('(root/')[0]
exec('v='+fragment)
Gui.updateGui();v.saveImage(str(root/files[scene]),1700,1100,'Current')
result={'scene':scene,'image':str(root/files[scene])}
