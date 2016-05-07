from flask import Flask

from server.settings import Config

import cx_Oracle

conn = cx_Oracle.connect('korovin13204/korovin13204@10.4.0.119:1521')
cursor = conn.cursor()

app = Flask(__name__)
app.config.from_object('settings.Config')
app.jinja_env.line_statement_prefix = Config.LINE_STATEMENT_PREFIX
