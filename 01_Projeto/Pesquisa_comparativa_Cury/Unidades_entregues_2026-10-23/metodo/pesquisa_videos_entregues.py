import urllib.request,json,re,pathlib,sys
out=pathlib.Path(r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Pesquisa_comparativa_Cury\Unidades_entregues_2026-10-23\fontes')
for vid in (sys.argv[1:] or ['_3VZ7y1rVkI','SbHNt25EPzk']):
    result={'video_id':vid,'url':'https://www.youtube.com/watch?v='+vid}
    try:
        meta=json.load(urllib.request.urlopen('https://www.youtube.com/oembed?url='+result['url']+'&format=json',timeout=30))
        result['oembed']=meta
        urllib.request.urlretrieve(meta['thumbnail_url'],out/(vid+'_miniatura.jpg'))
        req=urllib.request.Request(result['url'],headers={'User-Agent':'Mozilla/5.0'})
        html=urllib.request.urlopen(req,timeout=30).read().decode('utf8')
        for variable in ['ytInitialPlayerResponse','ytInitialData']:
            m=re.search(r'(?:var\s+)?'+variable+r'\s*=\s*',html)
            if m:
                obj=json.JSONDecoder().raw_decode(html[m.end():])[0]
                (out/(vid+'_'+variable+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
                if variable=='ytInitialPlayerResponse':
                    result['videoDetails']=obj.get('videoDetails');result['microformat']=obj.get('microformat');result['playabilityStatus']=obj.get('playabilityStatus');result['captions']=obj.get('captions');result['storyboards']=obj.get('storyboards')
        result['html_bytes']=len(html)
    except Exception as e:result['error']=str(e)
    (out/(vid+'_metadados.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(vid, result.get('videoDetails',{}).get('title'), result.get('microformat',{}).get('playerMicroformatRenderer',{}).get('publishDate'),result.get('error','OK'))
