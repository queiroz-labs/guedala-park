from pathlib import Path
import json

P=Path(__file__).resolve().parent
r=json.loads((P/'Resultados.json').read_text(encoding='utf-8'))
out=['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="930" viewBox="0 0 1200 930" role="img" aria-labelledby="title desc">
<title id="title">P11 sem tubos: ligações nominais e cálculo condicional</title>
<desc id="desc">Quatro Minifix nas laterais, quatro Confirmat na traseira e três cavilhas. Fundo18 preso às laterais por três Confirmat em cada lado. Proposta10kg distribuídos depende de rigidez e resistência das juntas.</desc>
<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#344d57"/></marker></defs>
<rect width="1200" height="930" fill="white"/>
<g font-family="Arial,sans-serif" fill="#243e4b">
<text x="45" y="43" font-size="27" font-weight="bold">P11 · prateleira de 18 mm, sem tubos</text>
<text x="45" y="74" font-size="16">Ligações às laterais e ao fundo de 18 mm · estudo R00 · 24/10/2026</text>
<text x="45" y="104" font-size="14" fill="#945425">Carga de uso proposta:10 kg bem distribuídos. Junta real e suspensão ainda precisam de comprovação.</text>
<text x="45" y="141" font-size="18" font-weight="bold">Planta · posições nominais, em mm</text>
<rect x="80" y="200" width="850" height="270" fill="#f4f6f3" stroke="#596f64" stroke-width="2"/>
<rect x="57" y="184" width="23" height="286" fill="#dbe4d5" stroke="#596f64"/>
<rect x="930" y="184" width="23" height="286" fill="#dbe4d5" stroke="#596f64"/>
<rect x="80" y="184" width="850" height="16" fill="#dbe4d5" stroke="#596f64"/>
<text x="1000" y="196" font-size="15">FUNDO 18</text>
<text x="1000" y="222" font-size="14">y = 312</text>''']
for x in [72,244,417,589]:
    xx=80+x/661*850
    out.append(f'<path d="M{xx:.2f} 179v49" stroke="#9e6036" stroke-width="4"/><path d="M{xx-6:.2f} 179h12" stroke="#9e6036" stroke-width="3"/><text x="{xx:.2f}" y="168" text-anchor="middle" font-size="14">{x}</text>')
for x in [158,330.5,503]:
    xx=80+x/661*850
    out.append(f'<path d="M{xx:.2f} 192v24" stroke="#58836b" stroke-width="6"/>')
for x in [80,930]:
    for y in [60,252]:
        yy=470-y/312*270
        xc=x+34/661*850 if x==80 else x-34/661*850
        out.append(f'<path d="M{x} {yy:.2f}H{xc:.2f}" stroke="#386f89" stroke-width="3"/><circle cx="{xc:.2f}" cy="{yy:.2f}" r="8" fill="white" stroke="#386f89" stroke-width="2"/>')
for y in [60,252]:
    yy=470-y/312*270
    out.append(f'<text x="989" y="{yy+5:.2f}" font-size="15">y = {y}</text>')
out.append('''<text x="505" y="493" text-anchor="middle" font-size="15">FRENTE · y = 0 · borda mais sensível à carga concentrada</text>
<path d="M80 516h850" stroke="#344d57" marker-start="url(#arr)" marker-end="url(#arr)"/>
<text x="505" y="540" text-anchor="middle" font-size="17">Vão661 × profundidade312 · manter chapa18 e alturas livres</text>
<circle cx="70" cy="566" r="7" fill="white" stroke="#386f89" stroke-width="2"/><text x="85" y="571" font-size="14">4 Minifix existentes</text>
<path d="M300 555v18" stroke="#9e6036" stroke-width="4"/><text x="314" y="571" font-size="14">4 Confirmat traseiros</text>
<path d="M550 555v18" stroke="#58836b" stroke-width="6"/><text x="564" y="571" font-size="14">3 cavilhas · sem crédito extra de capacidade</text>
<path d="M45 591h1110" stroke="#d5ddda"/>
<text x="45" y="624" font-size="18" font-weight="bold">Caminho da carga no fundo</text>
<rect x="105" y="654" width="300" height="230" fill="#eff3ed" stroke="#596f64" stroke-width="2"/>
<text x="255" y="647" text-anchor="middle" font-size="14">Vista posterior esquemática</text>''')
for z in [72,287,502]:
    yy=654+(574-z)/574*230
    for x in [105,405]:
        out.append(f'<circle cx="{x}" cy="{yy:.2f}" r="5" fill="#9e6036"/>')
out.append('''<text x="425" y="691" font-size="14">3 Confirmat por lateral</text>
<text x="425" y="717" font-size="14">Alturas90 / 305 / 520</text>
<text x="425" y="740" font-size="14">desde a base do módulo</text>
<text x="425" y="773" font-size="14">Fundo pesa cerca de5,55 kg</text>
<text x="425" y="799" font-size="14">Suas ligações também cedem;</text>
<text x="425" y="822" font-size="14">não foi tratado como apoio imóvel.</text>
<rect x="765" y="646" width="385" height="220" rx="5" fill="#eef4f4"/>
<text x="786" y="679" font-size="18" font-weight="bold">10 kg distribuídos</text>
<text x="786" y="711" font-size="16">Imediata:0,954 mm</text>
<text x="786" y="742" font-size="16">Cenário diferido:1,908 mm</text>
<text x="786" y="773" font-size="16">Com reserva:2,108 mm</text>
<text x="786" y="804" font-size="16">Critério escolhido:2,203 mm</text>
<text x="786" y="839" font-size="13" fill="#945425">Resultado condicional; capacidade não liberada.</text>
<text x="45" y="915" font-size="14">Sem escala de usinagem. Não representa todos os volumes de ferragens/furos ou uma verificação de colisão no CAD.</text>
</g></svg>''')
svg='\n'.join(out)
for a,b in [('proposta:10','proposta: 10'),('Vão661','Vão 661'),('profundidade312','profundidade 312'),('chapa18','chapa 18'),('Alturas90','Alturas 90'),('de5,55','de 5,55'),('Imediata:0','Imediata: 0'),('diferido:1','diferido: 1'),('reserva:2','reserva: 2'),('escolhido:2','escolhido: 2')]:svg=svg.replace(a,b)
(P/'Mapa_P11.svg').write_text(svg,encoding='utf-8')
print('Mapa_P11.svg')
