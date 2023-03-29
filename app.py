import json
import re

from flask import Flask
from flask import render_template
from flask import redirect
from flask import Request
from flask import Response
from flask import request
from flask import url_for

import config

state = [[0 for _ in range(config.SIZE)] for _ in range(config.SIZE)]
app = Flask(__name__)


class auth_middleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        token = request.headers.get("x-auth-token", None)

        if token == config.TOKEN:
            return self.app(environ, start_response)
        else:
            res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
            return res(environ, start_response)

app.wsgi_app = auth_middleware(app.wsgi_app)

@app.template_test("set")
def is_set(s):
    x, y = s
    return state[x][y] == 1


@app.route("/api/state")
def api_state():
    return json.dumps(state)


@app.route("/api/set")
def api_set():
    x = int(request.args["x"])
    y = int(request.args["y"])
    v = int(request.args["v"])
    state[x][y] = v
    return redirect(url_for("index"))


@app.route("/ui")
def index():
    return render_template(
        "index.html",
        config=config,
    )
