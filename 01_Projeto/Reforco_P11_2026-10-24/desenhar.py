"""Esquema vetorial do dimensionamento, sem executar cortes no CAD."""
from pathlib import Path
import json

P=Path(__file__).resolve().parent
r=json.loads((P/'Resultados.json').read_text(encoding='utf-8'))
out=['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1020" viewBox="0 0 1200 1020" role="img" aria-labelledby="title desc">
<title id="title">P11: reforço dimensionado para estudo de20kg</title>
<desc id="desc">Três tubos35por15parede2 sobMDF18; centros30,156,282. Seis bolsosinternos43por18profundidade6 e calçosanti-giro. Dimensionamento condicionado à prova da ligação no MDF.</desc>
<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#304856"/></marker></defs>
<rect width="1200" height="1020" fill="white"/>
<g font-family="Arial,sans-serif" fill="#253d4b">
<text x="45" y="44" font-size="26" font-weight="bold">P11 · reforço mantendo o MDF de 18 mm</text>
<text x="45" y="74" font-size="16">3 tubos de aço 35 × 15 × 2 mm · 15 mm na vertical · estudo R00 de24/10/2026</text>
<text x="45" y="104" font-size="14" fill="#8b542d">20 kg: cálculo condicional. Provar encaixes/calços no MDF e dimensionar a suspensão antes de liberar uso.</text>
<text x="45" y="143" font-size="18" font-weight="bold">Planta · prateleira transparente para mostrar os tubos abaixo</text>
<rect x="80" y="180" width="850" height="270" fill="#f5f6f3" stroke="#596b6d" stroke-width="2"/>
<rect x="57" y="180" width="23" height="270" fill="#d8dfd6" stroke="#596b6d"/>
<rect x="930" y="180" width="23" height="270" fill="#d8dfd6" stroke="#596b6d"/>
<text x="505" y="172" text-anchor="middle" font-size="14">FUNDO · y = 312</text>''']
for cy in r['settings']['perfil']['centros_y_mm']:
    y=450-cy/312*270
    out.append(f'<rect x="73" y="{y-15.14:.2f}" width="864" height="30.29" fill="#a9c4cf" stroke="#34596b" stroke-width="1.5"/>')
    for x in [73,911.36]:
        out.append(f'<rect x="{x:.2f}" y="{y-15.14:.2f}" width="25.72" height="30.29" fill="#c18b58" stroke="#8c582c"/>')
    out.append(f'<text x="980" y="{y+5:.2f}" font-size="16">y = {cy} mm</text>')
for x in [80+34/661*850,80+(661-34)/661*850]:
    for cy in [60,252]:
        y=450-cy/312*270
        out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7" fill="white" stroke="#5b705f" stroke-width="2"/>')
out.append('''<path d="M80 480h850" stroke="#304856" marker-start="url(#arr)" marker-end="url(#arr)"/>
<text x="505" y="504" text-anchor="middle" font-size="17">661 de vão livre · tubos com672 nominais, entrando5,5 de cada lado</text>
<text x="505" y="470" text-anchor="middle" font-size="14">FRENTE · y = 0</text>
<rect x="70" y="533" width="22" height="14" fill="#a9c4cf" stroke="#34596b"/><text x="103" y="546" font-size="14">Tubo</text>
<rect x="200" y="533" width="22" height="14" fill="#c18b58" stroke="#8c582c"/><text x="233" y="546" font-size="14">Sapata / bolso na ponta</text>
<circle cx="488" cy="540" r="7" fill="white" stroke="#5b705f" stroke-width="2"/><text x="505" y="546" font-size="14">Minifix nominal existente · acesso inferior preservado na triagem</text>
<path d="M45 573h1110" stroke="#d7dede"/>
<text x="45" y="610" font-size="18" font-weight="bold">Espaço e encaixe das pontas</text>
<text x="50" y="652" font-size="19" font-weight="bold">Sem divisória no vão</text>
<text x="50" y="685" font-size="17">Sob os tubos: 258 → 243 mm livres</text>
<text x="50" y="715" font-size="17">Nas pequenas pontas: cerca de240,5 mm</text>
<text x="50" y="745" font-size="17">Envelope dos tubos: cerca de1,04 litro</text>
<text x="50" y="775" font-size="17">Tubos: cerca de2,86 kg; cálculo reserva4 kg</text>
<text x="50" y="812" font-size="15">Comprimento de corte = vão real + 11 mm.</text>
<text x="50" y="838" font-size="15">Inserto maciço de20 mm dentro de cada ponta.</text>
<text x="50" y="864" font-size="15">Fechar a caixa somente após encaixar os tubos.</text>
<text x="690" y="637" font-size="16" font-weight="bold">Corte pela ponta, dentro da lateral</text>
<rect x="703" y="663" width="301" height="126" rx="21" fill="#e7ddc9" stroke="#8c6b48" stroke-width="2"/>
<rect x="731" y="666.5" width="245" height="105" rx="28" fill="#aac3cd" stroke="#34596b" stroke-width="2"/>
<rect x="750" y="684" width="207" height="70" rx="14" fill="#6d8995"/>
<rect x="731" y="771.5" width="245" height="14" fill="#c18b58" stroke="#8c582c"/>
<rect x="731" y="785.5" width="245" height="3.5" fill="#6e7375"/>
<rect x="731" y="663" width="245" height="3.5" fill="#6e7375"/>
<text x="1018" y="719" font-size="14">15 tubo</text>
<text x="1018" y="780" font-size="14">2 sapata</text>
<text x="853" y="818" text-anchor="middle" font-size="15">Bolso43 × 18 · R3 · profundidade6</text>
<text x="853" y="845" text-anchor="middle" font-size="14">Calços inferior e superior:0,5 nominais</text>
<text x="853" y="871" text-anchor="middle" font-size="14">Sem folga sob apoio; superior impede giro</text>
<rect x="45" y="910" width="1110" height="67" rx="4" fill="#eff4f4"/>
<text x="62" y="936" font-size="16">Deformação calculada:2,118 mm ≤ critério2,203 mm · 20 kg de conteúdo total, contato mínimo50 × 60 mm.</text>
<text x="62" y="961" font-size="14">Esquema nominal, sem escala de usinagem. Raios, folgas, apoios no MDF e interferências precisam de prova/compatibilização.</text>
</g></svg>''')
svg='\n'.join(out)
for before,after in [('de24','de 24'),('com672','com 672'),('entrando5','entrando 5'),('de240','de 240'),('de1,04','de 1,04'),('de2,86','de 2,86'),('reserva4','reserva 4'),('de20','de 20'),('Bolso43','Bolso 43'),('profundidade6','profundidade 6'),('superior:0,5','superior: 0,5'),('calculada:2','calculada: 2'),('critério2','critério 2'),('mínimo50','mínimo 50')]:
    svg=svg.replace(before,after)
(P/'Esquema_P11.svg').write_text(svg,encoding='utf-8')
print('Esquema_P11.svg')
