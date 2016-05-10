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


@app.endpoint("vtd")
@ErrorHandlerAndSend(app)
def vtd():
    _id = request.form.get('id')
    Oracle.execute("""
    DELETE FROM VehicleType
    WHERE id=:id
    """, id=_id).close()


@app.endpoint("vte")
@ErrorHandlerAndSend(app)
def vte():
    _id = request.form.get('id')
    name = request.form.get('name')
    Oracle.execute("""
    UPDATE VehicleType
    SET name=:name
    WHERE id=:id
    """, id=_id, name=name).close()
