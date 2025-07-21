import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

def http_server():
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

http_server()