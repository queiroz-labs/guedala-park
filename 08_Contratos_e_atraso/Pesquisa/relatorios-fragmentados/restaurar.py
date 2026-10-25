from pathlib import Path
import argparse,json,hashlib
ap=argparse.ArgumentParser(description="Reconstrói os originais públicos do IPHAN sem alteração dos bytes.")
ap.add_argument("destino",type=Path)
a=ap.parse_args();a.destino.mkdir(parents=True,exist_ok=True)
base=Path(__file__).resolve().parent
for doc in json.loads((base/"indice.json").read_text(encoding="utf8")):
 target=a.destino/doc["nome"]
 if target.exists():
  if hashlib.file_digest(target.open("rb"),"sha256").hexdigest()==doc["sha256"]:
   print("Já verificado:",target);continue
  raise RuntimeError("Destino existente divergente: "+str(target))
 with target.open("wb") as out:
  for part in doc["partes"]:
   with (base/part).open("rb") as inp:
    while data:=inp.read(1024*1024):out.write(data)
 assert target.stat().st_size==doc["bytes"]
 assert hashlib.file_digest(target.open("rb"),"sha256").hexdigest()==doc["sha256"]
 print("Restaurado e verificado:",target)
