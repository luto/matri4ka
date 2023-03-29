import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

from jinja2 import Environment, PackageLoader, select_autoescape

from . import config

state = [ [ 0 for _ in range(config.SIZE) ] for _ in range(config.SIZE) ]

env = Environment(
    loader=PackageLoader("matri4ka", "templates"),
    autoescape=select_autoescape()
)

def is_set(n):
    x, y = n
    return state[x][y] == 1

env.tests["set"] = is_set

class Matri4kaApiServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
 
    def do_GET(self):
        if self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(state).encode("utf-8"))
        elif self.path.startswith("/api/toggle/"):
            x, y = re.search(r"([0-9]+)/([0-9]+)", self.path).groups()
            y = int(y)
            x = int(x)
            state[x][y] = 0 if state[x][y] else 1
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            tpl = env.get_template("index.html")
            self.wfile.write(tpl.render(config=config).encode("utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((config.HOSTNAME, config.POST), Matri4kaApiServer)
    print("Server started http://%s:%s" % (config.HOSTNAME, config.POST))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
