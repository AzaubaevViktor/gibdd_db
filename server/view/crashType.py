from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('ctsa')
@ErrorHandlerAndSend(app)
def ctsa():
    crashTypes = {}

    cursor = Oracle.execute("""
    SELECT id, name FROM CrashType
    """)
    for row in cursor.fetchall():
        _id = row[0]
        name = row[1]
        crashTypes[_id] = {
            'id': _id,
            'name': name,
            'features': {}
        }

    cursor.close()

    return {'crashTypes': crashTypes}
