from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO


class ScanHandler(BaseHTTPRequestHandler):
    scan_func = None

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

        if self.path.endswith('.html'):
            mimetype = 'text/html'
            send_reply = True
        elif self.path.endswith('.css'):
            mimetype = 'text/css'
            send_reply = True
        elif self.path.endswith('.js'):
            mimetype = 'application/javascript'
            send_reply = True
        elif self.path.endswith('.json'):
            mimetype = 'application/json'
            send_reply = True
        elif self.path.endswith('.jpg'):
            mimetype = 'image/jpg'
            send_reply = True

        if send_reply:
            try:
                self.send_response(200)
                self.send_header('content-type', mimetype)
                self.end_headers()
                if self.path == '/data.json':
                    pass
                    #self.wfile.write(ScanHandler.get_table_data())
                else:
                    # with open('./webtable' + self.path, 'rb') as f:
                    #     self.wfile.write(f.read())
                    with open('./web' + self.path, 'rb') as f:
                        self.wfile.write(f.read())

            except IOError as e:
                self.send_response(404)
                print(e)

    @staticmethod
    def get_table_data():
        return bytes('hello world', 'utf-8')
        # df = ScanHandler.scan_func()
        # jsf = df.to_json(orient='records')
        # return bytes(jsf, 'utf-8')


def start_server(scan_function):
    ScanHandler.scan_func = scan_function
    server = HTTPServer(('', 7531), ScanHandler)
    try:
        print('Server start')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server stop')
        server.socket.close()


if __name__ == "__main__":
    start_server(lambda: True)