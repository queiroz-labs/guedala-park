"""Diagramas nominais: eixos e face explícitos, nunca gabarito de impressão 1:1."""
from html import escape

def label(value):return escape(str(value))

def render(drawings, code):
    height=440*len(drawings)+60
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" style="max-width:100%;height:auto" viewBox="0 0 1000 {height}" role="img" aria-label="{code}: mapas nominais de furação"><rect width="1000" height="{height}" fill="#fffefa"/><g font-family="Arial" fill="#263f3b"><text x="30" y="28" font-size="16">{code} · MAPAS NOMINAIS · mm · SEM ESCALA DE IMPRESSÃO</text>']
    for n,d in enumerate(drawings):
        y0=55+n*440;w=d['width'];h=d['height'];scale=min(380/w,300/h)
        x=50+(380-w*scale)/2;y=y0+57+(300-h*scale)/2
        out.append(f'<text x="30" y="{y0+18}" font-size="17">{label(d["partId"])} · {label(d["title"])}</text>')
        out.append(f'<rect x="{x}" y="{y}" width="{w*scale}" height="{h*scale}" fill="#e9eee3" stroke="#263f3b"/>')
        for i,p in enumerate(d['holes'],1):
            px=x+p['x']*scale;py=y+(h-p['y'])*scale
            radius=max(p['diameter']*scale/2,2)
            out.append(f'<circle cx="{px}" cy="{py}" r="{radius}" fill="#fffefa" stroke="#a16b25" stroke-width="1.4"/><path d="M{px-4},{py}h8 M{px},{py-4}v8" stroke="#a16b25" stroke-width=".6"/><text x="{px+radius+4}" y="{py-4}" font-size="11">{i}</text>')
        out.append(f'<text x="{x+w*scale/2}" y="{y+h*scale+22}" text-anchor="middle" font-size="13">U: {w:g}</text><text transform="translate({x-14},{y+h*scale/2}) rotate(-90)" text-anchor="middle" font-size="13">V: {h:g}</text>')
        out.append(f'<circle cx="{x}" cy="{y+h*scale}" r="3" fill="#263f3b"/><text x="{x-9}" y="{y+h*scale+17}" text-anchor="end" font-size="11">0,0</text>')
        lines=[d.get('face',''),d.get('origin',''),d.get('orientation',''),'']
        # Text is authored as short labeled lines; wrap without losing numerical strings.
        import textwrap
        lines=[part for s in lines for part in (textwrap.wrap(s,64) or [''])]
        ty=y0+50
        for line in lines:
            out.append(f'<text x="470" y="{ty}" font-size="12">{label(line)}</text>');ty+=17
        out.append(f'<text x="470" y="{ty+10}" font-size="12" font-weight="bold">Furo · U · V · Ø · profundidade</text>');ty+=34
        for i,p in enumerate(d['holes'],1):
            out.append(f'<text x="470" y="{ty}" font-size="12">{i} · {p["x"]:g} · {p["y"]:g} · {p["diameter"]:g} · {label(p.get("depth","ver ficha"))}</text>');ty+=18
        ty+=15
        for line in textwrap.wrap(d.get('status','Mapa nominal; conferir ferragem e prova em retalho.'),64):
            out.append(f'<text x="470" y="{ty}" font-size="11" fill="#806333">{label(line)}</text>');ty+=16
        out.append(f'<text x="30" y="{y0+415}" font-size="11" fill="#617269">Eixos locais de leitura conforme descritos. Não espelhar pela aparência do desenho; seguir a face e o sentido informados.</text>')
    out.append('</g></svg>')
    return ''.join(out)
