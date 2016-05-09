from flask import Flask

from ora_adapter import Oracle
from server.settings import Config

conn_str = 'korovin13204/korovin13204@10.4.0.119:1521'

Oracle(conn_str)

app = Flask(__name__)
app.config.from_object('settings.Config')
app.jinja_env.line_statement_prefix = Config.LINE_STATEMENT_PREFIX

from .view import *
