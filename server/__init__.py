from flask import Flask
from werkzeug.routing import Rule

from ora_adapter import Oracle
from server.settings import Config

conn_str = 'korovin13204/korovin13204@10.4.0.119:1521'

Oracle(conn_str)

app = Flask(__name__)
app.config.from_object('settings.Config')
app.jinja_env.line_statement_prefix = Config.LINE_STATEMENT_PREFIX

app.url_map.add(Rule("/vehicleType/add", endpoint="vta", methods=['POST']))
app.url_map.add(Rule("/vehicleType/show_all", endpoint="vtsa", methods=['GET']))

from .model import *
from .view import *
from .controller import *
