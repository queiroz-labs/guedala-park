import urllib.request,urllib.parse,re,json,pathlib
p=pathlib.Path(r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Pesquisa_comparativa_Cury\Unidades_entregues_2026-10-23\fontes')
def walk(o):
 if isinstance(o,dict):
  if 'videoRenderer' in o:yield o['videoRenderer']
  for v in o.values():yield from walk(v)
 elif isinstance(o,list):
  for v in o:yield from walk(v)
def txt(o):return o.get('simpleText') or ''.join(x.get('text','') for x in o.get('runs',[]))
all=[]
for q in ['Guedala Park apartamento vazio vistoria','Cury Vila das Belezas tour apartamento','Cury Joao Dias apartamento entregue','Cury apartamento ponta vazio tour']:
 try:
  url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
  h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode()
  m=re.search(r'var ytInitialData\s*=\s*',h);obj=json.JSONDecoder().raw_decode(h[m.end():])[0]
  rows=[{'id':v['videoId'],'title':txt(v.get('title',{})),'author':txt(v.get('ownerText',{})),'published_relative':txt(v.get('publishedTimeText',{})),'duration':txt(v.get('lengthText',{})),'url':'https://www.youtube.com/watch?v='+v['videoId']} for v in walk(obj)][:14]
  all.append({'query':q,'source':url,'results':rows});print(json.dumps(all[-1],ensure_ascii=True))
 except Exception as e:all.append({'query':q,'error':str(e)});print(q,str(e))
(p/'buscas_youtube.json').write_text(json.dumps(all,ensure_ascii=False,indent=2),encoding='utf8')
