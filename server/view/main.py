from flask import render_template

from server import app


@app.route("/", methods=['GET'])
def main_page():

    return render_template('index.html')

