import ssl
import threading
import warnings
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer


def start_server(directory: str, port: int = 4443):
    warnings.simplefilter("ignore", ResourceWarning)
    handler_class = partial(SimpleHTTPRequestHandler,
                            directory=directory)
    server = HTTPServer(('localhost', port), handler_class)
    server.socket = ssl.wrap_socket(server.socket,
                                   keyfile="tests/certificates/key.pem",
                                   certfile='tests/certificates/cert.pem', server_side=True)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server
