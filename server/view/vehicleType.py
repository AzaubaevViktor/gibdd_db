from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('vtsa')
@ErrorHandlerAndSend(app)
def vtsa():
    vehicleTypes = {}

    cursor = Oracle.execute("""
    SELECT VT.id, VT.name FROM VehicleType VT
    """)
    for row in cursor.fetchall():
        _id = row[0]
        name = row[1]
        vehicleTypes[_id] = {
            'id': _id,
            'name': name,
            'features': {}
        }

    cursor.close()

    cursor = Oracle.execute("""
    SELECT VT.id, VT.name, VFT.id, VFT.name, VFT.variable_type FROM VehicleType  VT
      JOIN VehicleTypeFeatureTypeLink VTFTL ON VTFTL.vehicle_type_id = VT.id
      JOIN VehicleFeatureType VFT           ON VFT.id = VTFTL.vehicle_feature_type_id
    """)

    for row in cursor.fetchall():
        _id = row[0]
        name = row[1]
        feature_id = row[2]
        feature = {
            'id': feature_id,
            'name': row[3],
            'variable_type': row[4]
        }

        vehicleTypes[_id]['features'][feature_id] = feature

    cursor.close()

    return {'vehicleTypes': vehicleTypes}
