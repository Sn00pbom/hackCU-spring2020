from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
import random
import string

import temp_loader



class ScanHandler(BaseHTTPRequestHandler):
    CONVOS = {}

    def do_POST(self):
        """Serve POST Request"""
        datalen = int(self.headers['Content-Length'])
        wl_io = StringIO(self.rfile.read(datalen).decode('utf-8'))
        self.send_response(200)
        self.end_headers()

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
        else:
            if '.' in self.path:
                # file request case
                if self.path.endswith('.css'):
                    mimetype = 'text/css'

                try:
                    self.send_response(200)
                    self.send_header('content-type', mimetype)
                    self.end_headers()
                    print(self.path)
                    with open('./web' + self.path, 'rb') as f:
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
                    with open('./web' + '/chathome.html', 'rb') as f:
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