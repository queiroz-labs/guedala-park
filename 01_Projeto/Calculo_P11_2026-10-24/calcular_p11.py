"""Memoria P11 reproduzivel em N, mm, MPa e kg. Nao modifica o CAD.

Executar: python calcular_p11.py
Verificacao independente (requer numpy): python verificar_p11.py
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def extract_geometry(settings):
    """Leitura do XML persistido, sem recomputar ou executar codigo do FCStd."""
    file = ROOT / settings['cad']
    sha = hashlib.sha256(file.read_bytes()).hexdigest()
    if sha != settings['sha256_cad_esperado']:
        raise ValueError('CAD diferente da base auditada: reconciliar antes de calcular')
    with zipfile.ZipFile(file) as archive:
        doc = ET.fromstring(archive.read('Document.xml'))
        parts = {}
        for name in ['Modulo010', 'Peca334', 'Peca335', 'Peca336', 'Peca337', 'Peca338', 'Peca339']:
            obj = doc.find(f"./ObjectData/Object[@name='{name}']")
            typ = doc.find(f"./Objects/Object[@name='{name}']")
            props = {}
            for prop in obj.findall('./Properties/Property'):
                if len(prop) and prop.get('name') in ['Label', 'Length', 'Width', 'Height', 'Placement', 'EspecificacaoR14', 'MaterialReferencia']:
                    props[prop.get('name')] = dict(prop[0].attrib)
            parts[name] = dict(type=typ.get('type'), properties=props)
        # Todos os corpos relevantes sao caixas sem rotacao na base persistida.
        for name, row in parts.items():
            pos = row['properties']['Placement']
            assert abs(float(pos['A'])) < 1e-10
            if name == 'Modulo010':
                continue
            p = row['properties']
            assert row['type'] == 'Part::Box'
            low = [float(pos[k]) for k in ['Px', 'Py', 'Pz']]
            size = [float(p[k]['value']) for k in ['Length', 'Width', 'Height']]
            row['bbox_local_modulo_mm'] = low + [low[i]+size[i] for i in range(3)]
        shelf = parts[settings['peca']]
        size = [float(shelf['properties'][k]['value']) for k in ['Length', 'Width', 'Height']]
        assert size == settings['dimensoes_nominais_mm']
        bb = shelf['bbox_local_modulo_mm']
        # Contatos nominais constatados no XML de caixas. Nao e teste BREP.
        left = parts['Peca335']['bbox_local_modulo_mm']
        right = parts['Peca334']['bbox_local_modulo_mm']
        back = parts['Peca336']['bbox_local_modulo_mm']
        assert math.isclose(left[3], bb[0]) and math.isclose(right[0], bb[3])
        assert math.isclose(bb[4], back[1])
        assert math.isclose(left[3], back[0]) and math.isclose(right[0], back[3])
        assert min(left[4],back[4])-max(left[1],back[1]) == 18
        assert min(right[4],back[4])-max(right[1],back[1]) == 18
        markers = []
        for obj in doc.findall('./ObjectData/Object'):
            label = obj.find("./Properties/Property[@name='Label']/String")
            if label is not None and 'P11' in label.get('value', '') and 'Peca339' in label.get('value', ''):
                markers.append(dict(id=obj.get('name'), label=label.get('value')))
        assert len(markers) == 4
        source_joinery = ROOT / '01_Projeto/Estudo_interativo/fabrication/r14/joinery.json'
        joinery = json.loads(source_joinery.read_text(encoding='utf-8'))['modules']['P11']
        positions = [r for r in joinery['nominalPositions'] if r['board'] == settings['peca']]
        assert len(positions) == 4
        depths = sorted({r['offset_from_Ymin_mm'] for r in positions})
        assert depths == settings['ligacoes']['profundidades_relativas_a_frente_mm']
    result = dict(cad=settings['cad'], sha256=sha, method='Document.xml persistido: parametros e caixas com rotacao zero; sem sessao FreeCAD ou analise BREP nesta rodada',
                  module=settings['modulo'], parts=parts, nominal_markers=markers,
                  nominal_positions_documental=positions, rear_joint_unmapped=joinery['unmappedInterfaces'],
                  shelf_span_mm=size[0], shelf_depth_mm=size[1], shelf_thickness_nominal_mm=size[2],
                  shelf_nominal_volume_mm3=math.prod(size),
                  status='Geometria nominal conferida; nenhuma ligacao resistente validada')
    assert hashlib.sha256(file.read_bytes()).hexdigest() == sha
    return result


def beam_case(L, b, t, E, rho, mass, kind, g=9.80665, a_ratio=0.5, mass_thickness_mm=None, additional_distributed_kg=0):
    """Euler-Bernoulli, apoios simples; ponto no vao usa toda largura b."""
    I = b*t**3/12
    Z = b*t**2/6
    mass_thickness_mm = t if mass_thickness_mm is None else mass_thickness_mm
    own = L*b*mass_thickness_mm*rho/1e9
    G, P = own*g, mass*g
    a = L*a_ratio
    distributed = kind == 'distribuida'
    assert additional_distributed_kg >= 0 and not (distributed and additional_distributed_kg)
    q = (G + P)/L if distributed else (G+additional_distributed_kg*g)/L
    point = 0 if distributed else P
    RA = q*L/2 + point*(L-a)/L
    RB = q*L/2 + point*a/L

    def deflection(x):
        uniform = q*x*(L**3 - 2*L*x*x + x**3)/(24*E*I)
        if x <= a:
            local = point*(L-a)*x*(L*L-(L-a)**2-x*x)/(6*L*E*I)
        else:
            local = point*a*(L-x)*(L*L-a*a-(L-x)**2)/(6*L*E*I)
        return uniform+local

    def slope(x):
        uniform = q*(L**3-6*L*x*x+4*x**3)/(24*E*I)
        if x <= a:
            local = point*(L-a)*(L*L-(L-a)**2-3*x*x)/(6*L*E*I)
        else:
            local = -point*a*(L*L-a*a-3*(L-x)**2)/(6*L*E*I)
        return uniform+local

    lo, hi = 0., L
    for _ in range(80):
        mid = (lo+hi)/2
        if slope(mid)>0:
            lo = mid
        else:
            hi = mid
    xmax = (lo+hi)/2
    candidates = [0., L, a]
    if q:
        if 0 <= RA/q <= a:
            candidates.append(RA/q)
        if a <= (RA-point)/q <= L:
            candidates.append((RA-point)/q)
    moment = max(RA*x-q*x*x/2-point*max(0, x-a) for x in candidates)
    return dict(span_mm=L, depth_mm=b, structural_thickness_mm=t, E_MPa=E, density_kg_m3=rho,
                thickness_for_mass_mm=mass_thickness_mm,
                content_kg=mass+additional_distributed_kg, type=kind, point_x_mm=None if distributed else a,
                distributed_content_kg=mass if distributed else additional_distributed_kg,
                localized_content_kg=0 if distributed else mass,
                self_mass_kg=own, I_mm4=I, Z_mm3=Z, total_force_N=G+P+additional_distributed_kg*g,
                max_deflection_mm=deflection(xmax), deflection_at_midspan_mm=deflection(L/2),
                x_max_deflection_mm=xmax, max_moment_Nmm=moment, gross_bending_stress_MPa=moment/Z,
                max_shear_stress_rectangular_MPa=1.5*max(RA, RB)/(b*t),
                reaction_left_N=RA, reaction_right_N=RB)


def limit_by_deflection(L, b, t, E, rho, multiplier, divisor, kind, mass_thickness_mm=None):
    zero = beam_case(L,b,t,E,rho,0,kind,mass_thickness_mm=mass_thickness_mm)['max_deflection_mm']
    one = beam_case(L,b,t,E,rho,1,kind,mass_thickness_mm=mass_thickness_mm)['max_deflection_mm']
    return max(0., (L/divisor/multiplier-zero)/(one-zero))


def build():
    s = json.loads((HERE/'Premissas.json').read_text(encoding='utf-8'))
    geometry = extract_geometry(s)
    L,b,_ = s['dimensoes_nominais_mm']
    divisor = s['criterio_flecha']['divisor_vao']
    rows, limits = [], []
    for c in s['cenarios']:
        for m in s['conteudo_kg']:
            for kind in s['tipos_carga']:
                row = beam_case(L,b,c['espessura_resistente_mm'],c['E_MPa'],c['densidade_kg_m3'],m,kind,
                                s['gravidade_m_s2'],s['posicoes_relativas_no_vao'].get(kind,0.5),c['espessura_para_massa_mm'])
                row['scenario'] = c['id']
                row['reference_deflection_mm'] = L/divisor
                for f in s['multiplicadores_flecha_sustentada']:
                    row[f'deflection_multiplier_{f:g}_mm'] = f*row['max_deflection_mm']
                rows.append(row)
        for kind in ['distribuida','localizada_central']:
            for f in s['multiplicadores_flecha_sustentada']:
                limits.append(dict(scenario=c['id'],type=kind,multiplier=f,
                                   content_limit_deflection_only_kg=limit_by_deflection(L,b,c['espessura_resistente_mm'],c['E_MPa'],c['densidade_kg_m3'],f,divisor,kind,c['espessura_para_massa_mm']),
                                   status='Limite da hipotese de flecha; nao capacidade liberada'))
    ref = next(c for c in s['cenarios'] if c['id']=='referencia_fabricante_condicional')
    reference = [r for r in rows if r['scenario']==ref['id']]
    mixed = []
    for distributed,central in [(2,3),(3,2)]:
        row = beam_case(L,b,ref['espessura_resistente_mm'],ref['E_MPa'],ref['densidade_kg_m3'],central,'mista',
                        mass_thickness_mm=ref['espessura_para_massa_mm'],additional_distributed_kg=distributed)
        row['deflection_multiplier_2_mm']=2*row['max_deflection_mm']
        row['reference_deflection_mm']=L/divisor
        row['scenario']=ref['id']
        mixed.append(row)
    requirements = []
    for m in [10,20]:
        for kind in ['distribuida','localizada_central']:
            row = next(r for r in reference if r['content_kg']==m and r['type']==kind)
            ratio = 2*row['max_deflection_mm']/(L/divisor)
            requirements.append(dict(content_kg=m,type=kind,required_E_if_section_unchanged_MPa=ratio*ref['E_MPa'],
                                     required_EI_Nmm2=ratio*ref['E_MPa']*row['I_mm4'],
                                     ratio_to_reference_EI=ratio,extra_reinforcement_weight_included=False))
    alternatives = []
    for t in [24.7,29.7]:
        for kind in ['distribuida','localizada_central']:
            # E2100 e apenas sensibilidade. Nao atribuir E2200 a painel de25.
            row = beam_case(L,b,t,2100,800,20,kind,mass_thickness_mm=t+0.6)
            alternatives.append(dict(option=f'Espessura resistente hipotetica {t:g} mm',**row,
                                     deflection_multiplier_2_mm=2*row['max_deflection_mm'],status='Nao selecionado; exige nova geometria, produto e ligacoes'))
    for kind in ['distribuida','localizada_central']:
        row = beam_case(L/2,b,17.7,2200,800,20,kind,mass_thickness_mm=18.3)
        alternatives.append(dict(option='Linha de apoio intermediaria ideal; toda carga em uma metade',**row,
                                 deflection_multiplier_2_mm=2*row['max_deflection_mm'],reference_deflection_mm=(L/2)/divisor,
                                 status='Comparacao de vao, nao dimensionamento do apoio; precisa sustentar profundidade e descarregar em estrutura resistente'))
    own = next(r for r in reference if r['type']=='distribuida')['self_mass_kg']
    G, P = own*s['gravidade_m_s2'],20*s['gravidade_m_s2']
    y1,y2 = s['ligacoes']['profundidades_relativas_a_frente_mm']
    demand = dict(content_kg=20,content_x_mm=L/2,content_y_from_front_mm=0,
                  front_connector_per_side_N=(P/2)*(y2/(y2-y1))+G/4,
                  rear_connector_per_side_N=-(P/2)*(y1/(y2-y1))+G/4,
                  status='Equilibrio ideal com reparto simetrico entre laterais; negativo e tracao/retencao. Nao comprova reparto elastico ou resistencia de Minifix')
    # Triagem explicita, nao tensao admissivel normativa.
    stress_screen = dict(MOR_catalog_reference_MPa=20,selected_study_fraction=0.25,
                         stress_screen_MPa=5,status='Comparacao historica CPA escolhida para triagem da secao bruta; nao fator normativo nem liberacao de furos, ligacoes ou ancoragem')
    result = dict(revision='R00',scope='P11/Peca339 - calculo global condicional, sem mudanca no CAD',
                  source_sha256=geometry['sha256'],units='N, mm, MPa, kg',
                  assumptions=s,geometry=geometry,cases=rows,deflection_limits=limits,
                  mixed_load_cases=mixed,
                  stiffness_requirements=requirements,alternatives=alternatives,
                  front_edge_connector_equilibrium=demand,gross_stress_screen=stress_screen,
                  conclusion=dict(reference_limit_factor2_distributed_kg=next(r['content_limit_deflection_only_kg'] for r in limits if r['scenario']==ref['id'] and r['type']=='distribuida' and r['multiplier']==2),
                                  reference_limit_factor2_central_kg=next(r['content_limit_deflection_only_kg'] for r in limits if r['scenario']==ref['id'] and r['type']=='localizada_central' and r['multiplier']==2),
                                  preliminary_study_target_distributed_kg=5,
                                  preliminary_study_target_central_kg=3,
                                  targets_are_alternative_not_cumulative=True,
                                  release_status='Nao liberado: confirmar chapa/resistencia efetiva, detalhar ligacoes e suspensao; cargas localizadas exigem placa/local/torcao e prova de oficina',
                                  decision='Para10-20kg sustentados, desenvolver reforco/apoio mantendo18mm como preferencia; nao contar apenas com Minifix ou contato no fundo'))
    write_json(HERE/'Geometria_R49.json',geometry)
    write_json(HERE/'Resultados.json',result)
    with (HERE/'Casos.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter=';')
        writer.writeheader();writer.writerows(rows)
    return result


if __name__=='__main__':
    r=build()
    print(json.dumps({'cases':len(r['cases']),'geometry':r['source_sha256'],'limits':r['conclusion']},ensure_ascii=True))
