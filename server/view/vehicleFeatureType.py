from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('vftsa')
@ErrorHandlerAndSend(app)
def vftsa():
    cursor = Oracle.execute("""
    SELECT id, name, variable_type FROM VehicleFeatureType ORDER BY id
    """)

    vehicle_feature_types = []

    for row in cursor.fetchall():
        vehicle_feature_types.append({
            'id': row[0],
            'name': row[1],
            'variable_type': row[2]
        })

    return {'vehicleFeatureTypes': vehicle_feature_types}
