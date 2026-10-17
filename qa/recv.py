import http.server, os, urllib.parse
OUT=os.path.expanduser('~/Desktop/AI Governance Clone/capture')
class H(http.server.BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','*'); self.send_header('Access-Control-Allow-Private-Network','true')
    def do_OPTIONS(self): self.send_response(204); self.cors(); self.end_headers()
    def do_POST(self):
        name=urllib.parse.unquote(self.path.lstrip('/')).replace('..','')
        data=self.rfile.read(int(self.headers.get('Content-Length',0)))
        p=os.path.join(OUT,name); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'wb').write(data)
        self.send_response(200); self.cors(); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
