from pathlib import Path
import collections,json,re
root=Path(__file__).resolve().parent
r=json.loads((root/'Erros_interface.json').read_text(encoding='utf-8'))
lines=next(x['text'] for x in r['editors'] if x['is_report']).splitlines()
patterns=['App::Part:','Code execution failed:','Event observer error:','Original project file is corrupted:','Error reading from file']
events=[]
for line in lines:
    if re.match(r'^\d{2}:\d{2}:\d{2}\s+',line) and any(p in line for p in patterns):
        events.append({'time':line[:8],'message':re.sub(r'^\d{2}:\d{2}:\d{2}\s+','',line)})
counts=collections.Counter(x['message'] for x in events)
summary={'events':events,'unique':[{'count':v,'message':k} for k,v in counts.items()],
         'current_documents':r['documents'],'notes':'Console includes earlier failed trials. Reproduction in the current canonical document required before changing geometry/parameters.'}
(root/'Resumo_erros.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'events':len(events),'unique':len(counts),'last_error_times':sorted({x['time'] for x in events})[-8:]},ensure_ascii=False))
