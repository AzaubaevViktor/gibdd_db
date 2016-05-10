from flask import request

from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint("vta")
@ErrorHandlerAndSend(app)
def vta():
    name = request.form.get('name')  # type: str
    Oracle.execute("""
    INSERT INTO VehicleType(name) VALUES(:name)
    """, name=name).close()
