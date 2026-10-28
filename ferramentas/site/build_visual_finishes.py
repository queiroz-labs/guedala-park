"""Presentation finishes from the documented decisions; never alters CAD or cut data."""
from pathlib import Path
import json, re, hashlib

STUDY=Path(__file__).resolve().parent

def build():
    cad=json.loads(re.search(r'const CAD_DATA\s*=\s*(\{.*\});',(STUDY/'src/cad-data.js').read_text(encoding='utf-8'),re.S)[1])
    audit=json.loads((STUDY/'fabrication/finish-audit.json').read_text(encoding='utf-8'))
    parts={p['source']:p for p in cad['parts']}
    bounds={}
    for p in parts.values():
        if not p.get('module') or not p.get('piece'):continue
        low=[p['x'],p['y'],p['z']]; high=[p['x']+p['w'],p['y']+p['h'],p['z']+p['d']]
        lo,hi=bounds.setdefault(p['module'],[low[:],high[:]])
        for i in range(3):lo[i]=min(lo[i],low[i]);hi[i]=max(hi[i],high[i])

    def palette(text):
        if not text:return 'whiteTX'
        if text=='Branco TX':return 'whiteTX'
        if 'Espelho' in text:return 'whiteTX' # mirror is a separate applied layer
        if 'Arenza' in text:return 'wood'
        if 'Petróleo' in text:return 'petrol'
        if 'Off-white' in text:return 'offwhite'
        if 'Bege' in text or 'Beige Matt' in text:return 'bathbeige'
        if 'Madeira clara' in text or 'Louro Freijó Poro' in text:return 'lightwood'
        raise ValueError(text)

    finishes={}
    for spec in audit['overrides']:
        p=parts[spec['source']]
        if spec.get('finishAssignmentMode','').startswith('whole_piece'):
            whole=spec.get('wholeBoardMaterial')
            finishes[spec['source']]={'material':palette(whole) if whole else (p['mat'] or 'finishPending'),
                                     'evidence':spec['evidence'],'sameFinishBothFaces':True}
            if not whole:finishes[spec['source']]['finishStatus']='Um padrão único ainda a definir para a peça inteira'
            continue
        row={'material':palette(spec.get('exposedMaterial')),'evidence':spec['evidence']}
        one_side=spec['sourceRole'].startswith(('Face interna do fundo','Face voltada ao compartimento','Base do espelheiro','Laterais do gaveteiro','Quadro frontal desmontável'))
        if one_side and not spec.get('exposedMaterial'):
            row.update(material=p['mat'] or 'finishPending',outerStatus='Existing illustrative CAD color; hidden/reverse finish not specified')
        if (spec.get('exposedMaterial') and row['material']!='whiteTX') or one_side:
            axis=min(range(3),key=lambda i:[p['w'],p['h'],p['d']][i])
            lo,hi=bounds[p['module']]
            mid=[p['x']+p['w']/2,p['y']+p['h']/2,p['z']+p['d']/2][axis]
            row.update(inner='whiteTX',axis=axis,outward=1 if mid>(lo[axis]+hi[axis])/2 else -1)
        # Upper surfaces hidden beneath cushions have no specified finish.
        # Only their downward, interior face has been selected as TX.
        if p['source'] in ['BancoR43_Painel1','BancoR43_Painel2']:
            row.update(material='finishPending',inner='whiteTX',axis=1,outward=1)
        finishes[p['source']]=row

    explicit={
        'Fechada_110Tampo':'wood','Fechada_110Sapata':'black',
        'CabeceiraDoisPaineisR25':'head',
        'EspelhoAplicadoR12':'mirror','EspelhoAplicadoR001':'mirror',
        'FischerFrenteR31':'black','FischerCorpoConservadorR31':'black',
    }
    for source,material in explicit.items():
        assert source in parts
        finishes[source]={'material':material,'evidence':'R43 LEIA-ME:7; decisões de acabamento R13; Fischer escolhido preto em src/data.js'}
    for source in ('Fechada_110Pedestal','Aberta_cadeira_lateralPedestal'):
        assert parts[source]['mat']=='black'
        finishes[source]={'material':'black','evidence':'Elias, 27/10/2026: pedestal preto aproximado, conforme Mesa_e_varal.md'}
    # Documented module appearance used by the lightweight orbit envelopes.
    module_material={f'P{i:02d}':'wood' for i in range(1,21)}
    module_material.update({f'P{i:02d}':'petrol' for i in range(9,13)})
    module_material.update(P17='offwhite',P18='bathbeige',P19='mirror')
    data={'revision':'R15','scope':'Visual approximation only. No manufacturing or CAD changes.',
          'parts':finishes,'modules':module_material}
    chair_path=STUDY/'fabrication/chair-visual-faces.json'
    for source,row in json.loads(chair_path.read_text(encoding='utf-8')).items():
        part=parts[source]
        assert len(row['triangles'])==len(part['t'])
        geometry=json.dumps({'v':part['v'],'t':part['t']},separators=(',',':')).encode('utf-8')
        assert hashlib.sha256(geometry).hexdigest()==row['geometrySHA256'],f'Review chair face mapping: {source}'
        finishes[source]=row
    (STUDY/'src/visual-finishes.js').write_text('// Generated from documented finishes; CAD source remains untouched.\nconst VISUAL_FINISHES = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    print(f'Visual finishes R15: {len(finishes)} components; 20 module palettes.')

if __name__=='__main__':build()
