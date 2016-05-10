from flask import Flask
from werkzeug.routing import Rule

from ora_adapter import Oracle
from server.settings import Config

conn_str = 'korovin13204/korovin13204@10.4.0.119:1521'

Oracle(conn_str)

app = Flask(__name__)
app.config.from_object('settings.Config')
app.jinja_env.line_statement_prefix = Config.LINE_STATEMENT_PREFIX

# VehicleType
# view
app.url_map.add(Rule("/vehicleType/show_all", endpoint="vtsa", methods=['GET']))
# controller
app.url_map.add(Rule("/vehicleType/add", endpoint="vta", methods=['POST']))
app.url_map.add(Rule("/vehicleType/delete", endpoint="vtd", methods=['POST']))
app.url_map.add(Rule("/vehicleType/edit", endpoint="vte", methods=['POST']))

# VehicleFeatureType
# view
app.url_map.add(Rule("/vehicleFeatureType/show_all", endpoint="vftsa", methods=['GET']))
# controller
app.url_map.add(Rule("/vehicleFeatureType/add_edit", endpoint="vftae", methods=['POST']))
app.url_map.add(Rule("/vehicleFeatureType/delete", endpoint="vftd", methods=['POST']))

from .model import *
from .view import *
from .controller import *
