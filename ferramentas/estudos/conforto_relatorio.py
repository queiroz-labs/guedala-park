"""Síntese compacta dos resultados, sem alterar decisões ou o pipeline real."""
import json
from pathlib import Path
import numpy as np
from conforto_clima import read_csv,write_csv,sha,dump


def supplemental(config,out,external,root):
    premises=[]
    def flatten(obj,prefix=''):
        for key,value in obj.items():
            path=prefix+'.'+key if prefix else key
            if isinstance(value,dict):flatten(value,path)
            else:premises.append(dict(parametro=path,valor=json.dumps(value,ensure_ascii=False),
                      natureza='dado/fonte/hipótese conforme Conforto_hipoteses.json; não medição de campo'))
    flatten(config);write_csv(out/'Premissas.csv',premises)
    manifest=json.loads((external/'Fontes_brutas.json').read_text(encoding='utf-8'))
    manifest.append(dict(arquivo=config['clima']['era5_arquivo'],url='https://open-meteo.com/en/docs/historical-weather-api',acesso='2026-10-30',
                   sha256=sha(external/config['clima']['era5_arquivo']),bytes=(external/config['clima']['era5_arquivo']).stat().st_size,
                   nota='Arquivo fornecido por Elias; URL da documentação; requisição original não arquivada. ERA5 conforme proveniência fornecida.'))
    write_csv(out/'Fontes.csv',[dict(arquivo=r['arquivo'],url=r['url'],acesso=r['acesso'],sha256=r.get('sha256',''),
                  bytes=r.get('bytes',''),situacao='ok' if 'sha256' in r else r.get('erro','não disponível'),nota=r.get('nota','')) for r in manifest])
    # Não atribuir ao fundo o contato que é apenas da lateral do módulo.
    contacts=[('P04','quarto','SSE','fundo/lateral estreita junto a x0,01; confirmar montagem e parede exterior','prioridade para medir'),
              ('P01|P02','quarto','SSE_lateral','lateral x0,01; fundos principais junto a y3,94 são internos','não aplicar risco SSE a todo o roupeiro'),
              ('P03','quarto','interna','maleiro y3,29–3,94 afastado da janela SW; não é fundo SW','umidade ambiente e acesso ao teto'),
              ('P14','lavanderia','SSE_lateral','borda x2,55 junto à fachada; fundo y7 em outra face','conferir contato lateral e circulação de ar'),
              ('P15','lavanderia','outra_face','fundo y7; não é fachada SSE da janela x2,55','roupa/dutos e umidade local, não inferir parede exterior'),
              ('P18|P19','banho','interna','x4,04–4,64; opostos à fachada SSE x2,55; fundo y5,29','risco de banho/água, não classificar como fundo SSE'),
              ('P09|P10|P11|P12','cozinha','outra_face','fundos y7; cozinha sem janela própria; adjacência exterior não comprovada','confirmar parede/shafts e vapor de cocção'),
              ('P17','escritorio','adiado','D06 E06 adiada; não usado como oclusor existente','não reinstalar por hipótese do estudo'),
              ('P16','escritorio','SW_proximidade','janela y0; módulo inicia y0,25; bancada Peca110 junto à janela','luz e calor no posto, não fundo encostado SW'),
              ('sofa|TV','sala','SW_proximidade','sofá Peca077–083 junto y1,85; TV Peca088 no painel Peca084 em x4,95','UV/ofuscamento/temperatura e cortina, sem índices DGP/UGR'),
              ('tapete','sala','implantacao_pendente','140x200 nominal; localização exata não confirmada no projeto','não inventar interseção da mancha de sol')]
    write_csv(out/'Moveis_contatos.csv',[dict(moveis=a,ambiente=b,face=c,evidencia_geometrica=d,tratamento=e) for a,b,c,d,e in contacts])
    raw=read_csv(out/'Conforto_ERA5.csv');rows=[]
    # Contagem de desconforto é por zona/hora, sem somar cômodos como pessoas.
    for room in ('sala','quarto','escritorio'):
        names=sorted({r['cenario'] for r in raw});totals={}
        for name in names:
            selected=[r for r in raw if r['ambiente']==room and r['cenario']==name]
            totals[name]={k:sum(float(r[k]) for r in selected) for k in ('h_ano_abaixo18','h_ano_abaixo20','h_ano_acima28','h_ocupadas_acima_adapt','h_ocupadas_acima_adapt_com_alivio')}
        for name,t in totals.items():
            base=totals['base'];rows.append(dict(ambiente=room,cenario=name,
                h_ano_frio18=t['h_ano_abaixo18'],h_ano_calor28=t['h_ano_acima28'],
                h_calor28_evitadas_vs_base=round(base['h_ano_acima28']-t['h_ano_acima28'],1),
                h_frio18_evitadas_vs_base=round(base['h_ano_abaixo18']-t['h_ano_abaixo18'],1),
                h_ocupadas_calor_adapt_evitadas_com_alivio=round(base['h_ocupadas_acima_adapt']-t['h_ocupadas_acima_adapt_com_alivio'],1)))
    write_csv(out/'Efeito_anual.csv',rows)
    proposals=[
      (1,'usar persiana existente de forma sazonal','baixo/sem compra se entregue','persiana_13_18','cortina da sala; confirmar persiana na sala','PQ-001|PQ-007','verão13–18h; inverno abrir à tarde/fechar ao anoitecer; escurece e pode restringir ventilação'),
      (2,'ventilação noturna com portas abertas','baixo','persiana_vent_noite','varal, acesso e móveis altos','PQ-001|PQ-017','abrir quando fora mais fresco; chuva, ruído e segurança reais condicionam operação'),
      (3,'ventilador de teto','médio; R$300–1200 instalado hipótese','ventilador','iluminação e teto;127V','PQ-012|PQ-017','30W referência anterior;0,5m/s≈2°C alívio hipotético, não queda da temperatura do ar'),
      (4,'vedar frestas com controle de vapor','baixo; R$100–500 hipótese','sazonal_vedada','caixa de persiana/manutenção','PQ-007|PQ-018','não bloquear admissão necessária a gás/exaustão; ventilar por eventos no inverno'),
      (5,'cortina/blackout claro ou tecido','médio; cotar conforme C2 Areia','blackout_claro','cortina sala, C2 preservada','PQ-028|PQ-029','avaliar cor externa, trilho, vãos e acesso à janela; interna pode reter calor'),
      (6,'película compatível','médio; R$150–400/m² hipótese','pelicula_refletiva','vidro e fachada/garantia','PQ-007|PQ-017','condomínio/fabricante; reduz luz útil também no inverno; não prescrever SKU'),
      (7,'manta pessoal e tapete sobre piso','baixo/médio; tapete histórico R$269 não recotado','nao_modelado_Top','Olmo/tapete escolhido','PQ-019','alívio de contato; não atribuir horas de Top evitadas; manta sob vinílico/adesivo exige sistema aprovado pelo fabricante'),
      (8,'aquecedor portátil no quarto','R$200–800 hipótese','portatil1500_quarto','elétrica127V, circulação junto à cama','PQ-012','1500W referência=11,81A equivalente; termostato/noite; tomadas/circuito/proteções com RT'),
      (9,'split quente/frio','alto; R$3000–7000/zona hipótese','AC_ideal26','climatização e fachada','PQ-017|PQ-012','memorial§5.9 x convençãoart58; sem viabilidade/capacidade definida, sem compra'),
      (10,'isolamento interno40mm+gesso12,5mm','alto; R$150–350/m² hipótese','isolamento','área útil, marcenaria e acústica','PQ-008|PQ-026','pode reter calor; Glaser/chuva/ponte2D e acústica sem desempenho certificado'),
      (11,'piso radiante elétrico','alto; R$250–600/m² hipótese','ideal20','Olmo, contrapiso e elétrica','PQ-019|PQ-012|PQ-034','referência100W/m²; base/sistema<=27°C; sem prova de potência útil suficiente ou de compatibilidade do SKU')]
    write_csv(out/'Prioridades.csv',[dict(ordem=a,solucao=b,custo_qualitativo=c,cenario=d,decisao_afetada=e,PQ=f,condicoes=g) for a,b,c,d,e,f,g in proposals])
    # Áreas/potências da opção de piso e perda de pé-direito são condicionais.
    zones=read_csv(out/'Zonas_termicas.csv');floors=[]
    for zone in zones:
        if zone['ambiente'] in ('banho','lavanderia'):continue
        a=float(zone['area_m2']);power=a*100
        floors.append(dict(ambiente=zone['ambiente'],area_bruta_m2=a,fracao_aquecivel_hipotese=.70,potencia_eletrica100W_m2_W=round(power*.7,1),
            corrente_equivalente127V_A=round(power*.7/127,2),potencia_termica_teto27C_Ti20_h8_W=round(a*.7*8*(27-20),1),
            acrescimo_piso_hipotese_mm='10–30',pe_direito_depois_m='2,57–2,59; banho2,47–2,49 se aplicável',
            restricao='área livre sem armários; potência100W/m² não é entrega contínua; sensor/adesivo/SKU/RT pendentes, não alterar piso'))
    write_csv(out/'Piso_radiante_hipoteses.csv',floors)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[2];out=root/'03_Ambientes/Conforto_ambiental';external=root.parent/'outputs/Codex_sol_e_umidade'
    config=json.loads((root/'ferramentas/estudos/modelos/Conforto_hipoteses.json').read_text(encoding='utf-8'))
    supplemental(config,out,external,root)
