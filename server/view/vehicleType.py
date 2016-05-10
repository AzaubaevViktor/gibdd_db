from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('vtsa')
@ErrorHandlerAndSend(app)
def vtsa():
    cursor = Oracle.execute("""
    SELECT id, name FROM VehicleType ORDER BY id
    """)

    vehicleTypes = []

    for row in cursor.fetchall():
        vehicleTypes.append({
            'id': row[0],
            'name': row[1]
        })

    return {'vehicleTypes': vehicleTypes}
