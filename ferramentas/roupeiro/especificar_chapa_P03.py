"""Base de especificacao MDF18/P03 e massas por area publicada.

Sem abrir CAD. Nao transforma peso medio de chapa em capacidade de parafuso.
Cada chapa tem um unico padrao. Conjuntos18+15 so com duas pecas identificadas; nao adotados neste estudo.
"""
import hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P03'
reference=json.loads((OUT/'Dobradicas_A.json').read_text(encoding='utf-8'))
cad=ROOT/'02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd'
assert hashlib.sha256(cad.read_bytes()).hexdigest()==reference['source_sha256']
sheet_area=2.750*1.850
leaf_area=.672*.306
catalog=[dict(product='Arenza Colore Lizze',thickness_mm=t,sheet_mass_kg=m,
              sheet_area_m2=sheet_area,areal_mass_kg_m2=m/sheet_area,
              gross_leaf_area_mass_kg=leaf_area*m/sheet_area)
         for t,m in [(15,52.7),(18,63.2),(25,86.5)]]
catalog.append(dict(product='Arenza MDF Green HR Matte Acetinado',thickness_mm=18,
                    sheet_mass_kg=66.9,sheet_area_m2=sheet_area,areal_mass_kg_m2=66.9/sheet_area,
                    gross_leaf_area_mass_kg=leaf_area*66.9/sheet_area))
chosen=catalog[1]
parts=[
 dict(part='Peca259',name='Lateral direita',size_mm=[630,308,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze'),
 dict(part='Peca260',name='Lateral esquerda',size_mm=[630,308,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze'),
 dict(part='Peca261',name='Fundo',size_mm=[1314,272,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze'),
 dict(part='Peca262',name='Base',size_mm=[1314,612,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze'),
 dict(part='Peca263',name='Topo',size_mm=[1314,612,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze'),
 dict(part='A_esquerda',name='Porta esquerda',size_mm=[672,306,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze'),
 dict(part='A_direita',name='Porta direita',size_mm=[672,306,18],inside='Arenza liso Lizze',outside='Arenza liso Lizze')]
for p in parts:
    a,b,t=p['size_mm'];p['area_m2']=a*b/1e6
    p['equivalent_mass_if_same_areal_weight_as_Arenza18_kg']=p['area_m2']*chosen['areal_mass_kg_m2']
    p['conservative_wood_mass_hypothesis800_t18_3_kg']=p['area_m2']*.0183*800
    p['same_finish_both_faces']=True
    p['face_supply_confirmed']=None
budget=4.-chosen['gross_leaf_area_mass_kg']
loads=dict(finished_leaf_budget_hypothesis_kg=4.,published_sheet_reference_gross_leaf_kg=chosen['gross_leaf_area_mass_kg'],
           budget_remaining_for_hardware_edges_pull_finish_kg=budget,
           reference_bare_leaf_nominal_gravity_moment_Nm=chosen['gross_leaf_area_mass_kg']*9.80665*.336,
           maintained_finished4kg_moment_Nm=4*9.80665*.336,
           maintained_finished4kg_extreme_pair202_N=4*9.80665*.336/.202)
sources=[
 dict(url='https://greenplac.com.br/products/mdf-arenza-linha-colore',
      facts=['Arenza liso areia/fendi,Lizze,2750x1850,18mm e63.2kg/chapa;15=52.7kg,25=86.5kg.',
             'Nao publica SKU18 nem confirmacao do versoBrancoTX na pagina consultada.']),
 dict(url='https://greenplac.com.br/products/arenza-hr-2-750-x-1-850-mm-02-faces',
      facts=['ArenzaGreenHR18=66.9kg/chapa2750x1850;MatteAcetinado, outra textura.']),
 dict(url='https://greenplac.com.br/products/branco-tx-hr-2-750-x-1-850-mm-02-faces',
      facts=['DescreveBrancoTXconvencional eHR;valores66.9kg/18 apresentados na paginaHR,nao transferidos ao convencional.']),
 dict(url='https://download.greenplac.com.br/download/qualidade-requisitos-normativos-e-cuidados.pdf',
      facts=['MDFBP revestido emumaouduasfaces;formatos2750x1850;uso geral nao estrutural emcondicoessecas.',
             'ReferenciaE minimo2200MPa faixa>12a19,tolerancia±0.3;jaadotados na referencia mecanica do projeto.',
             'Documento nao fornece capacidade de arrancamento do609.1500 nem curva do grupo.',
             'Tabela extraida;renderizacao visual desta consulta indisponivel. Outros numeros de resistencia nao usados no calculo.'])]
report=dict(source_sha256=reference['source_sha256'],user_finish_confirmation='Elias confirmou manterArenza liso,25/10/2026',
            specification_basis=dict(core='MDF Greenplac convencional para ambiente interno seco',
                finish='BP melaminico industrial',nominal_thickness_mm=18,
                apparent_finish='Arenza LinhaColore, texturaLizze, liso areia/fendi',internal_finish='Arenza liso Lizze,mesmo padrao da peca unica',
                sheet_format_mm=[2750,1850],status='base_tecnica_Arenza_duas_faces;SKU,lote e fabricacao pendentes'),
            manufacturer_reference=dict(E_min_MPa=2200,nominal_thickness_tolerance_mm=.3,
                minimum_resistant_thickness_hypothesis_mm=17.7,maximum_thickness_for_mass_hypothesis_mm=18.3,
                long_term_effective_E_hypothesis_MPa=1100,
                note='2200 e referencia minima de modulo imediato,nao resistencia admissivel nemmodulo de longa duracao.1100 e hipotese de estudo anterior,nao dadoGreenplac. Revestimento sem credito estrutural.'),
            catalog_mass_comparison=catalog,door_mass_budget=loads,parts_and_requested_faces=parts,
            totals=dict(nominal_area_m2=sum(p['area_m2'] for p in parts),
                equivalent_all_panels_Arenza_areal_mass_kg=sum(p['equivalent_mass_if_same_areal_weight_as_Arenza18_kg'] for p in parts),
                conservative_wood800_t18_3_kg=sum(p['conservative_wood_mass_hypothesis800_t18_3_kg'] for p in parts),
                note='Estimativa por area de Arenza para todas as pecasP03;nao pesagem,nao inclui ferragens.Nao atualizar matriz global como se fosse medicao.'),
            rejected_shortcuts=[
                dict(option='15mm',reason='Nao adotar:caneco minimo13 deixa somente2mmnominais;e alterar caixa mudaria vaos/juntas. Para base com mesmoE,rigidezfora do plano15/18=(15/18)^3.',base_flexural_rigidity_ratio_sameE=(15/18)**3),
                dict(option='25mm',reason='Nao adotar como conserto automatico:porta maispesada e alteracao de folgas/recuo/volume interno;caixa exige estudo proprio.'),
                dict(option='HR',reason='Opcao para requisito de umidade confirmado;mais pesado e textura diferente. Nao comprovou maior capacidade do grupo de dobradicas.'),
                dict(option='MDP_generic',reason='Sem produtoArenza e dados de chapa confirmados neste levantamento;nao substituir MDF nem importar recomendacaoP2Blum automaticamente.')],
            unresolved=[
                'Confirmar SKU,lote e espessura final da chapa18ArenzaLizze nasduasfaces,semcoresopostas.',
                'P03 atual tem pecas unicas18;nenhum painel interno15 adicionado. Duaspecas18+15 podemtercoresdiferentes,masexigemIDs,vaos,ligacoes e cargas proprios.',
                'Codigo/SKU de18,amostra,lote,textura e massa real do produtoArenza.',
                'Fitas/selagem/adesivo e compensacoes nas dimensoes acabadas;nao executar usinagem pelas cotas de estudo.',
                'Pilotos,parafusos e capacidade do grupo de dobradicas para MDF18/672x306;ensaio e confirmacaoBlum pendentes.',
                'Caixa/base/juntas/caminhoP01 para20kg e eventual30kg:nao liberados por selecionar MDF18.'],
            sources=sources,cad_unchanged=True)
assert chosen['gross_leaf_area_mass_kg']<4 and budget>0
(OUT/'Chapa_P03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

im=Image.new('RGB',(1800,1190),'white');dr=ImageDraw.Draw(im)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
def tx(x,y,t,n=25,b=False,c='#29414d'):dr.text((x,y),t,font=font(n,b),fill=c)
tx(60,40,'Maleiro A — base de especificação da chapa',37,True)
tx(60,105,'MDF BP Greenplac 18 mm • Arenza liso / Linha Colore / Lizze nas duas faces de cada peça',25)
tx(60,180,'Peso de uma porta de 67,2 × 30,6 cm, por área publicada da chapa',29,True)
for row,yy in zip(catalog,[265,385,505,625]):
    label=f"{row['thickness_mm']} mm — "+('Arenza HR / Matte Acetinado' if 'HR' in row['product'] else 'Arenza Colore / Lizze')
    tx(60,yy,label,25,b=row['thickness_mm']==18 and 'HR' not in row['product'])
    mass=row['gross_leaf_area_mass_kg'];xx=790
    dr.rectangle([xx,yy,xx+mass*210,yy+42],fill='#b69a7f' if row is chosen else '#c7d2d0')
    tx(xx+mass*210+20,yy+3,f'{mass:.2f} kg'.replace('.',','),26,True)
tx(60,735,'18 mm: referência de 2,55 kg antes de ferragens/bordas; manter hipótese acabada de 4 kg.',26,True)
tx(60,785,'Massa estimada pela área da chapa Arenza; não há pesagem. Cada peça tem um único padrão.',24)
tx(60,855,'Espessura preservada: 18 mm. Referência de cálculo resistente: 17,7 mm; E imediato mínimo: 2.200 MPa.',24)
tx(60,900,'Não se atribuiu resistência de parafuso a partir da densidade ou do módulo de elasticidade.',24)
tx(60,970,'Confirmar SKU/lote, espessura final e fixação. Caixa interna 15 mm seria outro conjunto de peças.',25,True,c='#955238')
tx(60,1020,'15 mm deixa só 2 mm nominais atrás do caneco mínimo de 13; 25 mm altera peso e geometria.',24)
tx(60,1090,'Nenhuma mudança no CAD. Chapa selecionada para estudo não libera as dobradiças ou 20 kg de malas.',24)
im.save(OUT/'Chapa_P03.png')
print(json.dumps(dict(leaf18kg=chosen['gross_leaf_area_mass_kg'],budget_to4kg=budget,
    area_m2=report['totals']['nominal_area_m2'],equivalent_wood_mass_kg=report['totals']['equivalent_all_panels_Arenza_areal_mass_kg'],
    hr_extra_leaf_kg=catalog[3]['gross_leaf_area_mass_kg']-chosen['gross_leaf_area_mass_kg'],cad_unchanged=True),ensure_ascii=False))
