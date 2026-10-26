"""Regressao: formato de checkout nao e alteracao de fonte;binario continua exato."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
from fontes import sha

with TemporaryDirectory(prefix='gp_hash_') as tmp:
    base=Path(tmp)
    for suffix in ['.py','.json','.md','.txt','.csv']:
        a=base/('lf'+suffix);b=base/('crlf'+suffix)
        a.write_bytes(b'\xef\xbb\xbfA\nB\n');b.write_bytes(b'\xef\xbb\xbfA\r\nB\r\n')
        assert sha(a)==sha(b)
        b.write_bytes(b'\xef\xbb\xbfA\r\nC\r\n');assert sha(a)!=sha(b)
    for suffix in ['.pdf','.FCStd','.png']:
        a=base/('bin'+suffix);data=b'A\r\nB\n\x00';a.write_bytes(data)
        assert sha(a)==hashlib.sha256(data).hexdigest()
        a.write_bytes(data.replace(b'\r\n',b'\n'));assert sha(a)!=hashlib.sha256(data).hexdigest()
print('Hashes: LF/CRLF equivalentes em texto;mudanca de conteudo detectada;binarios exatos.')
