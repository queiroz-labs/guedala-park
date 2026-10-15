"""Correct the upstream Windows connection check and partial socket responses."""
import os
from pathlib import Path
bridge=Path(os.environ['LOCALAPPDATA'])/'Programs'/'FreeCAD-MCP'/'working_bridge.py'
code=bridge.read_text(encoding='utf-8')
old='''        if name == "check_freecad_connection":
            status = {'''
new='''        if name == "check_freecad_connection":
            # Test the endpoint, rather than assuming Windows means connected.
            connected = False
            try:
                if platform.system() == "Windows":
                    probe = socket.create_connection(('127.0.0.1', 23456), timeout=2)
                else:
                    probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    probe.settimeout(2)
                    probe.connect(socket_path)
                probe.close()
                connected = True
            except OSError:
                pass
            status = {'''
if old in code:
    code=code.replace(old,new)
    code=code.replace('"freecad_socket_exists": freecad_available,','"freecad_socket_exists": connected,')
    code=code.replace('"status": "FreeCAD running with AI Copilot workbench" if freecad_available',
                      '"status": "FreeCAD running with AI Copilot workbench" if connected')
    code=code.replace("sock.send(command.encode('utf-8'))","sock.sendall(command.encode('utf-8'))")
    code=code.replace("            response = sock.recv(8192).decode('utf-8')",'''            response_bytes = bytearray()
            while True:
                chunk = sock.recv(8192)
                if not chunk:
                    raise ConnectionError("FreeCAD closed an incomplete response")
                response_bytes.extend(chunk)
                try:
                    response = response_bytes.decode('utf-8')
                    json.loads(response)
                    break
                except (UnicodeDecodeError, json.JSONDecodeError):
                    if len(response_bytes) > 16 * 1024 * 1024:
                        raise ValueError("FreeCAD response exceeds 16 MiB")''')
    compile(code,str(bridge),'exec')
    bridge.write_text(code,encoding='utf-8')
    print('Ponte corrigida: conexão real e leitura completa de respostas JSON.')
else:
    print('Correções da ponte já aplicadas ou upstream diferente; nenhuma substituição.')
