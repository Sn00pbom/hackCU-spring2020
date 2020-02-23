from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
import random


class ScanHandler(BaseHTTPRequestHandler):
    convos = []

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
            self.path = '/index.html'

        send_reply = False
        is_user_error = False

        if self.path == '/create':
            mimetype = 'text/plain'
            self.send_response(200)
            self.send_header('content-type', mimetype)
            self.end_headers()
            r = random.randint(111,999)
            print('create', r)
            self.wfile.write(bytes(str(r), 'utf-8'))

        elif self.path == '/index.html':
            mimetype = 'text/html'
            send_reply = True
        else:
            p = self.path[1:]
            try:
                p = int(p)
                mimetype = 'text/plain'
                send_reply = True

            except ValueError as e:
                mimetype = 'text/html'
                send_reply = True
                is_user_error = True

        if send_reply:
            if is_user_error:
                self.send_response(200)
                self.send_header('content-type', mimetype)
                self.end_headers()
                with open('./web' + '/error.html', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                try:
                    self.send_response(200)
                    self.send_header('content-type', mimetype)
                    self.end_headers()
                    if self.path == '/index.html':
                        with open('./web' + self.path, 'rb') as f:
                            self.wfile.write(f.read())
                    else:
                        self.wfile.write(bytes(self.path[1:], 'utf-8'))

                except IOError as e:
                    self.send_response(404)
                    print(e)


def start_server():
    server = HTTPServer(('', 7531), ScanHandler)
    try:
        print('Server start')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server stop')
        server.socket.close()


if __name__ == "__main__":
    start_server()