from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('vtftlsa')
@ErrorHandlerAndSend(app)
def vtftlsa():
    cursor = Oracle.execute("""
    SELECT VT.id, VT.name, VFT.name FROM VehicleType  VT
      JOIN VehicleTypeFeatureTypeLink VTFTL ON VTFTL.vehicle_type_id = VT.id
      JOIN VehicleFeatureType VFT           ON VFT.id = VTFTL.vehicle_feature_type_id
    """)

    vehicle_feature_types = {}

    for row in cursor.fetchall():
        _id = row[0]
        name = row[0]
        vehicle_feature_types.append({
            'id': row[0],
            'name': row[1],
            'variable_type': row[2]
        })

    cursor.close()

    return {'vehicleFeatureTypes': vehicle_feature_types}


@app.endpoint('vtftls')
@ErrorHandlerAndSend(app)
def vtftls(vt_id):
    cursor = Oracle.execute("""
    SELECT VFT.id FROM VehicleFeatureType AS VFT
    """)
