from flask import request

from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint("vftae")
@ErrorHandlerAndSend(app)
def vftae():
    _id = request.form.get('id')
    name = request.form.get('name')  # type: str
    variable_type = request.form.get('variable_type')
    if not _id:
        Oracle.execute("""
        INSERT INTO VehicleFeatureType(name, variable_type) VALUES(:name, :variable_type)
        """, name=name, variable_type=variable_type).close()
    else:
        Oracle.execute("""
        UPDATE VehicleFeatureType
        SET name          = :name,
            variable_type = :variable_type
        WHERE id = :id
        """, id=_id, name=name, variable_type=variable_type).close()


@app.endpoint("vftd")
@ErrorHandlerAndSend(app)
def vftd():
    _id = request.form.get('id')
    Oracle.execute("""
    DELETE FROM VehicleFeatureType
    WHERE id=:id
    """, id=_id).close()
