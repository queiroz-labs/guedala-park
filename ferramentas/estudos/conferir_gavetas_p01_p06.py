"""Reconcilia sete caixas R52 com a folha FGVTN 500 arquivada. Sem CAD."""
from pathlib import Path
import gzip, hashlib, json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Inventario_dimensional/Gavetas'


def main():
    basepath=ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base=json.loads(gzip.decompress(basepath.read_bytes()));objects=base['objetos']
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/release['cadPath']).read_bytes()).hexdigest()==base['sha256']
    historical=ROOT/'04_Moveis/Avanco_pendencias/Gavetas/Medicoes_nove_gavetas.json'
    old=json.loads(historical.read_text(encoding='utf-8'))['drawers'][:7]
    pairs=[('GavetaComumR08','GavetaComumR001')]+[
        (f'GavetaComumR{i:03}',f'GavetaComumR{i+1:03}') for i in [12,24,36,48]]+[
        ('MontagemG2R017','MontagemG2R018'),('GavetaComumR060','GavetaComumR061')]
    rows=[]
    for row,names in zip(old,pairs):
        sides=sorted([objects[n]['caixa_global'] for n in names],key=lambda b:b[0])
        l,r=sides
        left,ln=row['limites_laterais']['esquerda'];right,rn=row['limites_laterais']['direita']
        assert abs(objects[ln]['caixa_global'][3]-left)<1e-6
        assert abs(objects[rn]['caixa_global'][0]-right)<1e-6
        backname=row['raios'][0]['obstacle']
        back=objects[backname]['caixa_global'][1]
        front=min(objects[ln]['caixa_global'][1],objects[rn]['caixa_global'][1])
        assert abs(back-row['fundo_interno_y_mm'])<1e-6
        assert abs(front-row['frente_carcaca_y_mm'])<1e-6
        A=right-left;inner=r[0]-l[3]
        assert abs((r[3]-l[0])-(inner+l[3]-l[0]+r[3]-r[0]))<1e-6
        children={n:o for n,o in objects.items() if o.get('pai')==row['gaveta']}
        locks=[n for n,o in children.items() if 'T51.7601' in o.get('rotulo','')]
        rows.append(dict(drawer=row['gaveta'],module='P01' if len(rows)<4 else 'P06',
            side_objects=list(names),carcass_front_y_mm=front,carcass_back_y_mm=back,
            carcass_width_A_mm=A,carcass_depth_mm=back-front,margin_to_P1_520_mm=back-front-520,
            side_depth_mm=l[4]-l[1],delta_to_catalogue_P500_mm=500-(l[4]-l[1]),
            side_thicknesses_mm=[l[3]-l[0],r[3]-r[0]],
            inner_width_mm=inner,nominal_inner_A_minus41_mm=A-41,
            catalogue_inner_interval_mm=[A-41-.5,A-41+1],
            shortfall_to_inner_lower_bound_mm=max(0,A-41-.5-inner),
            external_box_width_mm=r[3]-l[0],back_clearance_current_mm=back-l[4],
            back_clearance_if_depth_extended_10_mm=back-l[4]-10,
            lock_references_T51=list(locks),status='DIVERGENCIA_DIMENSIONAL_NAO_CORRIGIDA'))
    drawing=ROOT/'04_Moveis/Avanco_pendencias/Ferragens/FGVTN_Oculta_ET_montagem_Set24.png'
    result=dict(cad_sha256=base['sha256'],cad_opened=False,cad_changed=False,
        archived_drawing=drawing.relative_to(ROOT).as_posix(),
        drawing_sha256=hashlib.sha256(drawing.read_bytes()).hexdigest(),
        base_sha256=hashlib.sha256(basepath.read_bytes()).hexdigest(),
        catalogue_transcription=dict(reference_mm=500,P_mm=500,P1_min_mm=520,C_mm=475,
            C_tolerance_mm=3,inner_width='A-41 +1/-0.5',side_max_mm=16,
            vertical_adjustment_mm=3,release='Destrave simultaneo dos dois lados'),
        rows=rows,physical_tests_executed=0,
        limits=['Cotas da imagem arquivada conferidas visualmente; nao configuracao individual de compra.',
                'Raios historicos usados somente para identificar faces, reconferidas nas caixas R52.',
                'Caixas de 490 mm nao foram aumentadas; nao recalcula rasgos/engates nem parafusos.',
                'T51.7601 e referencia de geometria presente, nao prova de compatibilidade FGVTN.',
                'Folga de profundidade nao comprova interface vertical, recortes, furacao ou retirada.',
                '475 +/-3 do desenho nao autoriza alterar os controladores existentes.'])
    (OUT/'Conferencia_P01_P06.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rows,ensure_ascii=True))


if __name__=='__main__':main()
