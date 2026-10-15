from pathlib import Path
import json
import FreeCAD as App

out = (Path(__file__).resolve().parent / 'Estado_interface.json').resolve()
rows = []
for d in App.listDocuments().values():
    rows.append({'name': d.Name, 'label': d.Label, 'file': d.FileName,
                 'objects': len(d.Objects),
                 'invalid': [o.Name for o in d.Objects if 'Invalid' in o.State]})
out.write_text(json.dumps({'documents': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
