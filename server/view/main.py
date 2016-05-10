from flask import render_template

from ora_adapter import Oracle
from server import app


@app.route("/", methods=['GET'])
def main_page():

    return render_template('index.html')

