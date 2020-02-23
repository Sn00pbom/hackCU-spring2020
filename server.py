from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
import random
import string
from urllib.parse import urlparse, parse_qs
import json

import temp_loader
import chatcrypto



class ScanHandler(BaseHTTPRequestHandler):
    CONVOS = {}

    def do_POST(self):
        """Serve POST Request"""
        datalen = int(self.headers['Content-Length'])
        wl_io = StringIO(self.rfile.read(datalen).decode('utf-8'))
        self.send_response(200)
        self.end_headers()

        dat = wl_io.read()
        print(dat)

    def do_GET(self):
        """Serve GET Request"""
        mimetype = 'text/plain'  # default case

        if self.path == '/':
            # index case
            self.path = '/index.html'
            mimetype = 'text/html'
            self.send_response(200)
            self.send_header('content-type', mimetype)
            self.end_headers()
            with open('./web' + self.path, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/create':
            # create group case
            mimetype = 'text/plain'
            self.send_response(200)
            self.send_header('content-type', mimetype)
            self.end_headers()
            sid = get_id()
            tch = temp_loader.TChatHistory(sid)
            self.CONVOS[sid] = tch
            tch.save()
            self.wfile.write(bytes(sid, 'utf-8'))
        elif self.path.startswith('/hash'):
            out = urlparse(self.path)
            qsp = parse_qs(out.query)
            mimetype = 'text/plain'
            self.send_response(200) # no content response
            self.send_header('content-type', mimetype)
            self.end_headers()

            bdict = qsp['bc']
            bdict = json.loads(bdict[0])
            b = chatcrypto.Block.from_dict(bdict)  # get last entry
            hc = qsp['headhash'][0]
            hs = b.compute_block_hash()
            self.wfile.write(b'1' if hs == hc else b'0')
            
        elif self.path.startswith('/submit'):
            pass
        elif self.path.startswith('/poll'):
            # server sent event init

            mimetype = 'text/event-stream'

        else:
            if '.' in self.path:
                # file request case
                folder = './web'
                if self.path.endswith('.css'):
                    mimetype = 'text/css'
                if self.path.endswith('.js'):
                    mimetype = 'application/javascript'
                if self.path.endswith('.json'):
                    mimetype = 'text/json'
                    folder = './data'

                try:
                    self.send_response(200)
                    self.send_header('content-type', mimetype)
                    self.end_headers()
                    print(self.path)
                    with open(folder + self.path, 'rb') as f:
                        self.wfile.write(f.read())
                except:
                    self.send_response(404)


            else:
                # group chat case
                if self.path[1:] in self.CONVOS.keys():
                    # group exists case
                    mimetype = 'text/html'
                    self.send_response(200)
                    self.send_header('content-type', mimetype)
                    self.end_headers()
                    # with open('./web' + self.path, 'rb') as f:
                    #     self.wfile.write(f.read())
                    with open('./web/chat.html', 'rb') as f:
                        self.wfile.write(f.read())

                else:
                    # no group case
                    mimetype = 'text/html'
                    self.send_response(200)
                    self.send_header('content-type', mimetype)
                    self.end_headers()
                    with open('./web/error.html', 'rb') as f:
                        self.wfile.write(f.read())

def get_id():
    s = ''
    for _ in range(6):
        s += random.choice(string.ascii_letters + string.digits)
    return s

def start_server():
    ScanHandler.CONVOS = temp_loader.populate_convos()
    server = HTTPServer(('', 7531), ScanHandler)
    try:
        print('Server start')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server stop')
        server.socket.close()


if __name__ == "__main__":
    start_server()