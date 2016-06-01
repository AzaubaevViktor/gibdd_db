from flask import request

from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint("vtae")
@ErrorHandlerAndSend(app)
def vtae():
    vt_id = request.form.get('id')  # type: int
    name = request.form.get('name')  # type: str

    query_feature_inserts = []
    for k, v in request.form.items():
        if 'vft_' == k[:4]:
            if not (v == 'false'):
                query_feature_inserts.append("""
                INSERT INTO
                VehicleTypeFeatureTypeLink(vehicle_type_id, vehicle_feature_type_id)
                VALUES(:vt_id, {})
                """.format(k[4:]))

    if not vt_id:
        Oracle.execute("""
        INSERT INTO VehicleType(name) VALUES(:name)
        """, name=name).close()

        cursor = Oracle.execute("""
        SELECT id FROM VehicleType WHERE name=:name
        """, name=name)
        vt_id = cursor.fetchone()[0]
        cursor.close()

        Oracle.execute("""
        INSERT INTO FreeRegNum(vehicle_type_id, sta, end)
        VALUES(:vt_id, 0, 11390625)
        """, vt_id=vt_id).close()
    else:
        Oracle.execute("""
            UPDATE VehicleType
            SET name=:name
            WHERE id=:id
            """, id=vt_id, name=name).close()

    Oracle.execute("""
    DELETE FROM VehicleTypeFeatureTypeLink WHERE vehicle_type_id=:vt_id
    """, vt_id=int(vt_id)).close()
    for query in query_feature_inserts:
        Oracle.execute(query, vt_id=int(vt_id)).close()


@app.endpoint("vtd")
@ErrorHandlerAndSend(app)
def vtd():
    vt_id = request.form.get('id')
    Oracle.execute("""
    DELETE FROM VehicleTypeFeatureTypeLink
    WHERE vehicle_type_id=:vt_id
    """, vt_id=vt_id).close()

    Oracle.execute("""
    DELETE FROM VehicleType
    WHERE id=:vt_id
    """, vt_id=vt_id).close()


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
