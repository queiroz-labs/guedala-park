import json,pathlib,urllib.request,math,sys
from PIL import Image,ImageDraw
p=pathlib.Path(r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Pesquisa_comparativa_Cury\Unidades_entregues_2026-10-23\fontes')
for vid in (sys.argv[1:] or ['_3VZ7y1rVkI','SbHNt25EPzk']):
 d=json.loads((p/(vid+'_metadados.json')).read_text(encoding='utf8'))
 tracks=(d.get('captions') or {}).get('playerCaptionsTracklistRenderer',{}).get('captionTracks',[])
 for tr in (tracks[:1] if not sys.argv[1:] else []):
  try:
   raw=urllib.request.urlopen(tr['baseUrl']+'&fmt=json3',timeout=25).read()
   (p/(vid+'_legenda_resposta.txt')).write_bytes(raw)
   print(vid,'caption_bytes',len(raw))
  except Exception as e:print(vid,'caption_error',str(e))
 parts=d['storyboards']['playerStoryboardSpecRenderer']['spec'].split('|');level=len(parts)-2
 w,h,n,c,r,dt,name,sig=parts[level+1].split('#');w,h,n,c,r,dt=map(int,[w,h,n,c,r,dt]);sheets=[]
 for i in range(math.ceil(n/(c*r))):
  url=parts[0].replace('$L',str(level)).replace('$N',name.replace('$M',str(i)))+'&sigh='+sig
  path=p/(vid+'_storyboard_'+str(i)+'.jpg')
  try:urllib.request.urlretrieve(url,path);sheets.append(Image.open(path))
  except Exception as e: print(vid,'sheet_error',i,str(e));break
 manifest={'video':vid,'level':level,'width':w,'height':h,'count':n,'columns':c,'rows':r,'interval_ms':dt,'sheets_downloaded':len(sheets),'time_note':'Tempos aproximados derivados do intervalo do storyboard; não frames exatos de reprodução.'}
 (p/(vid+'_storyboard_manifesto.json')).write_text(json.dumps(manifest,indent=2),encoding='utf8')
 # Uma amostra a cada 30 segundos para navegação; originais preservados.
 indices=list(range(0,n,max(1,30000//dt)))
 for page in range(math.ceil(len(indices)/30)):
  subset=indices[page*30:(page+1)*30];canvas=Image.new('RGB',(960,math.ceil(len(subset)/4)*160),'white');draw=ImageDraw.Draw(canvas)
  for j,k in enumerate(subset):
   si=k//(c*r);cell=k%(c*r)
   if si>=len(sheets):continue
   frame=sheets[si].crop(((cell%c)*w,(cell//c)*h,(cell%c+1)*w,(cell//c+1)*h));frame.thumbnail((232,132))
   x=(j%4)*240;y=(j//4)*160;canvas.paste(frame,(x,y+22));t=k*dt//1000
   draw.text((x+4,y+4),f'{t//60:02}:{t%60:02} (aprox.)',fill='black')
  canvas.save(p/(vid+'_contato_'+str(page)+'.jpg'))
 print(vid,manifest)
