import threading
import warnings
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer


def start_server(directory: str, port: int=8000):
    warnings.simplefilter("ignore", ResourceWarning)
    handler_class = partial(SimpleHTTPRequestHandler,
                            directory=directory)
    server = HTTPServer(('localhost', port), handler_class)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server
