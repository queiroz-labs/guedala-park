"""Hashes portaveis de fontes: Git pode converter LF/CRLF no checkout."""
import hashlib

TEXT_SUFFIXES={'.py','.json','.csv','.md','.txt'}
HASH_RULE='SHA256: texto .py/.json/.csv/.md/.txt com CRLF convertido em LF;demais bytes preservados. Binarios sem normalizacao.'

def sha(path):
    data=path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()
