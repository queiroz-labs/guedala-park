"""Importa JSON do celular para o índice de campo; só CSV e relatório mudam.

Não abre CAD, não regenera fichas/pranchas nem altera orçamento. Datas/códigos
e cotas são validados antes de escrever. Fixture não pode preencher o CSV real.
"""
import argparse
import csv
from datetime import datetime
import hashlib
import html
import io
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_CSV=ROOT/'07_Imovel/Medidas_e_impactos.csv'
sys.path.insert(0,str(ROOT/'ferramentas/site'))
from build_field_data import rows_from_csv,nominal_parts,chain_codes

STATUSES={'pendente','ok','fora_do_esperado'}


def external(path):
    path=Path(path).resolve()
    if path==ROOT or ROOT in path.parents:
        raise ValueError('Saída da cadeia deve ficar fora do repositório')
    return path


def field_csv(rows):
    """Somente entradas numéricas consumidas pela cadeia; vazio não é zero."""
    allowed=chain_codes();output=io.StringIO(newline='')
    writer=csv.DictWriter(output,fieldnames=['codigo_medida','valor_medido','evidencia_campo'])
    writer.writeheader();count=0
    for row in rows:
        code=row['codigo_medida'];value=row['valor_medido'].strip()
        if code not in allowed or not value:continue
        if code.startswith('PR-') and not row['evidencia_campo'].startswith('DATUM_CONFIRMADO:SIM; '):continue
        scalar=r'-?\d+(?:[.,]\d+)?\s*(?:mm|cm|m)'
        pattern='(?:'+scalar+r'|-?\d+(?:[.,]\d+)?\s*(?:mm|cm|m)?\s*[×x;]\s*'+scalar+')' if code.startswith('DIM-') else scalar
        if not re.fullmatch(pattern,value):raise ValueError('Cota inválida ou sem unidade explícita: '+code)
        parts=nominal_parts(code,value)
        if any(p['nominal_mm'] is None for p in parts):raise ValueError('Cota sem unidade explícita: '+code)
        if code.startswith('DIM-'):
            nominal=nominal_parts(code,row['valor_nominal_atual'])
            if len(parts)!=len(nominal):raise ValueError('DIM exige todos os eixos: '+code)
        writer.writerow({k:row[k] for k in writer.fieldnames});count+=1
    return output.getvalue().encode('utf-8'),count


def iso(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?(?:Z|[+-]\d\d:\d\d)',value):
        raise ValueError('Data/hora ISO com fuso obrigatória')
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def validate(payload,catalog):
    if not isinstance(payload,dict) or type(payload.get('versao')) is not int or payload.get('versao')!=1 or payload.get('projeto')!='guedala-park' or not isinstance(payload.get('medidas'),list):
        raise ValueError('Formato de exportação incompatível')
    iso(payload.get('exportado_em'));allowed={p['codigo'] for row in catalog for p in row['partes']}
    seen=set();result=[]
    for r in payload['medidas']:
        if not isinstance(r,dict) or not isinstance(r.get('codigo'),str) or r.get('codigo') not in allowed:raise ValueError('Código desconhecido ou composto incompleto: '+str(r.get('codigo') if isinstance(r,dict) else r))
        code=r['codigo']
        if code in seen:raise ValueError('Código repetido: '+code)
        seen.add(code);value=r.get('valor_mm')
        if 'valor_mm' not in r or value is not None and (type(value) not in (int,float) or not math.isfinite(value)):raise ValueError('Valor numérico inválido: '+code)
        if value is not None and code.startswith(('PD-','DIM-')) and value<=0:raise ValueError('Dimensão deve ser positiva: '+code)
        if not isinstance(r.get('status'),str) or r.get('status') not in STATUSES or not isinstance(r.get('observacao'),str):raise ValueError('Status/observação inválidos: '+code)
        iso(r.get('data_hora'));result.append(r)
        if 'datum_confirmado' in r and type(r['datum_confirmado']) is not bool:
            raise ValueError('datum_confirmado deve ser booleano: '+code)
    return result


def fmt(value):return format(float(value),'.12g')


def md(value):return html.escape(str(value)).replace('|','\\|').replace('\n','<br>')


def referenced_files(row):
    columns=('arquivos_ficha','arquivos_prancha','arquivos_readme','arquivos_orcamento','outras_fontes_ou_arquivos')
    return sorted({p.strip() for k in columns for p in row.get(k,'').split('|') if p.strip() and p.strip().lower() not in ('não se aplica','a definir')})


def evidence(records,input_name,sha):
    values=[]
    for r in sorted(records,key=lambda v:v['codigo']):
        value='sem cota' if r['valor_mm'] is None else fmt(r['valor_mm'])+' mm'
        values.append(f"{r['codigo']}={value}; {r['data_hora']}; status={r['status']}; obs={r['observacao']}")
    confirmed=all(r.get('datum_confirmado') is True for r in records)
    prefix=('DATUM_CONFIRMADO:SIM; ' if confirmed else 'DATUM_CONFIRMADO:NAO; ') if records[0]['codigo'].startswith('PR-') else ''
    return prefix+f'JSON {input_name}; SHA256 {sha}; '+' | '.join(values)


def atomic_write(path,content):
    """Troca atômica do arquivo; temporário da mesma unidade sempre removido."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.medidas_',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(content)
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)


def import_file(input_path,csv_path=DEFAULT_CSV,report_path=None,field_path=None):
    input_path=Path(input_path);csv_path=Path(csv_path)
    report_path=Path(report_path) if report_path else ROOT/'07_Imovel/Relatorio_medidas_reais.md'
    if csv_path.resolve()==report_path.resolve():raise ValueError('CSV e relatório precisam de caminhos distintos')
    if input_path.resolve() in (csv_path.resolve(),report_path.resolve()):raise ValueError('Preservar o JSON de entrada em caminho separado')
    if field_path is not None:
        field_path=external(field_path)
        if field_path in {input_path.resolve(),csv_path.resolve(),report_path.resolve()}:
            raise ValueError('campo.csv precisa de caminho distinto das fontes e relatório')
    raw_input=input_path.read_bytes();payload=json.loads(raw_input.decode('utf-8-sig'))
    if not isinstance(payload,dict):raise ValueError('Formato de exportação incompatível')
    if (str(payload.get('uso','')).lower().startswith('teste') or 'ficticio' in input_path.name.lower()) and csv_path.resolve()==DEFAULT_CSV.resolve():
        raise ValueError('Fixture fictícia só pode preencher cópia de teste fora do projeto')
    raw=csv_path.read_bytes();catalog=rows_from_csv(csv_path);records=validate(payload,catalog)
    stream=io.StringIO(raw.decode('utf-8-sig'),newline='');reader=csv.DictReader(stream);fields=reader.fieldnames
    rows=list(reader);by_code={r['codigo_medida']:r for r in rows}
    if len(by_code)!=len(rows):raise ValueError('Fonte CSV tem códigos repetidos')
    for field in ('valor_medido','evidencia_campo'):
        if field not in fields:raise ValueError('Coluna ausente: '+field)
    groups={}
    for r in records:groups.setdefault(r['codigo'].split('/')[0],[]).append(r)
    changes=[];pending=[];unchanged=[];stale=[];blocked=[];source_sha=hashlib.sha256(raw_input).hexdigest()
    for item in catalog:
        code=item['codigo']
        if code not in groups:continue
        captured=groups[code];row=by_code[code];by_part={r['codigo']:r for r in captured}
        old_dates=re.findall(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?(?:Z|[+-]\d\d:\d\d)',row['evidencia_campo'])
        if old_dates and max(iso(v) for v in old_dates)>max(iso(r['data_hora']) for r in captured):
            stale.append(code);continue
        # Uma cota composta só é real se todos os seus componentes forem reais.
        complete=all(p['codigo'] in by_part and by_part[p['codigo']]['valor_mm'] is not None for p in item['partes'])
        proof=evidence(captured,input_path.name,source_sha)
        if code.startswith('PR-') and not all(r.get('datum_confirmado') is True for r in captured):
            row['valor_medido']='';row['evidencia_campo']=proof;blocked.append(code)
            continue
        if not complete:
            missing=[p['codigo'] for p in item['partes'] if p['codigo'] not in by_part or by_part[p['codigo']]['valor_mm'] is None]
            if row['evidencia_campo'] and proof not in row['evidencia_campo']:proof+=' | Evidência anterior preservada: '+row['evidencia_campo']
            row['evidencia_campo']=proof
            pending.append((code,', '.join(missing),'Cota anterior preservada; sem preenchimento numérico parcial.'))
            continue
        values=[by_part[p['codigo']]['valor_mm'] for p in item['partes']]
        differences=[None if p['nominal_mm'] is None else v-p['nominal_mm'] for p,v in zip(item['partes'],values)]
        measured=' × '.join(fmt(v) for v in values)+' mm'
        row['valor_medido']=measured;row['evidencia_campo']=proof
        entry=dict(codigo=code,nominal=row['valor_nominal_atual'],medido=measured,
                   delta=' × '.join('sem nominal' if d is None else ('+' if d>0 else '')+fmt(d)+' mm' for d in differences),
                   moveis=row['moveis_afetados'],files=referenced_files(row),status=' | '.join(sorted({r['status'] for r in captured})))
        if any(d is None or abs(d)>1e-9 for d in differences):changes.append(entry)
        else:unchanged.append(entry)
    lines=['# Medidas reais importadas do site','',
           f"Exportação: {md(payload['exportado_em'])}. Fonte: {md(input_path.name)}; SHA256 `{source_sha}`.",'',
           'Relatório de diferença, sem tolerância presumida. Status OK/fora do esperado é anotação do usuário, não aceitação técnica. CAD, fichas e orçamento não foram alterados.','',
           f'{len(records)} registros recebidos; {len(changes)+len(unchanged)} linhas numéricas preenchidas; {len(pending)} linhas sem todas as cotas.','',
           '## Diferenças e dados sem nominal','',
           '| Código | Nominal | Medido | Diferença | Móveis |','|---|---|---|---|---|']
    if not changes:lines.append('| — | — | — | Nenhuma diferença numérica nesta entrada | — |')
    for item in changes:
        lines.append('| '+' | '.join(md(item[k]) for k in ('codigo','nominal','medido','delta','moveis'))+' |')
    lines+=['','## Arquivos que precisam de revisão','']
    for item in changes:
        lines.append(f"- **{md(item['codigo'])} — {md(item['moveis'])}:** "+('; '.join('`'+p+'`' for p in item['files']) if item['files'] else 'vínculos ausentes; conferir com projeto/RT/oficina.'))
    if not changes:lines.append('Nenhum arquivo apontado por diferença; isto não valida encaixe ou instalação.')
    lines+=['','## Registros incompletos ou qualitativos','']
    for code,missing,reason in pending:lines.append(f'- **{md(code)}:** faltam {md(missing)}. {reason} Evidência no CSV.')
    if not pending:lines.append('Nenhuma cota parcial recebida.')
    lines+=['','## Registros anteriores ignorados','',', '.join(stale) or 'Nenhum nesta entrada.']
    lines+=['','## Coordenadas sem datum','']
    for code in blocked:lines.append(f'- **{code}:** coordenada de campo sem vínculo ao datum — não aplicar. Valor apenas na evidência; não enviado à cadeia.')
    if not blocked:lines.append('Nenhuma coordenada bloqueada nesta entrada.')
    lines+=['','## Valores iguais ao nominal','',', '.join(r['codigo'] for r in unchanged) or 'Nenhum nesta entrada.','',
            '## Conferência seguinte','',
            'Conferir pontos/face acabada e evidências com RT/oficina. Atualizar os derivados somente em etapa posterior, após revisão; nenhuma regeneração foi executada.','']
    report='\n'.join(lines).encode('utf-8')
    output=io.StringIO(newline='');writer=csv.DictWriter(output,fieldnames=fields,lineterminator='\r\n' if b'\r\n' in raw else '\n')
    writer.writeheader();writer.writerows(rows);data=output.getvalue().encode('utf-8')
    if raw.startswith(b'\xef\xbb\xbf'):data=b'\xef\xbb\xbf'+data
    if csv_path.read_bytes()!=raw:raise ValueError('O CSV mudou durante a importação; repetir com a fonte atual')
    writes=[(report_path,report)]
    field_count=0
    if field_path is not None:
        field_data,field_count=field_csv(rows);writes.append((field_path,field_data))
    if data!=raw:writes.append((csv_path,data))
    applied=[]
    try:
        for path,content in writes:
            previous=path.read_bytes() if path.exists() else None
            atomic_write(path,content);applied.append((path,previous))
    except OSError:
        for path,previous in reversed(applied):
            if previous is None:path.unlink()
            else:atomic_write(path,previous)
        raise
    return dict(recebidos=len(records),preenchidos=len(changes)+len(unchanged),divergencias=len(changes),incompletos=len(pending),antigos_ignorados=len(stale),
                csv=str(csv_path),relatorio=str(report_path),campo=str(field_path) if field_path else None,entradas_cadeia=field_count,sem_datum=len(blocked))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--entrada',type=Path,required=True)
    parser.add_argument('--csv',type=Path,default=DEFAULT_CSV);parser.add_argument('--relatorio',type=Path,default=ROOT/'07_Imovel/Relatorio_medidas_reais.md')
    parser.add_argument('--campo',type=Path,help='CSV numérico para cadeia, fora do repositório')
    args=parser.parse_args()
    try:print(json.dumps(import_file(args.entrada,args.csv,args.relatorio,args.campo),ensure_ascii=False))
    except (ValueError,KeyError,OSError) as exc:parser.exit(1,'Importação não aplicada: '+str(exc)+'\n')


if __name__=='__main__':main()
