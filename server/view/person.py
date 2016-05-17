from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('psa')
@ErrorHandlerAndSend(app)
def psa():
    persons = {}

    cursor = Oracle.execute("""
    SELECT P.id, P.is_organization, P.full_name, P.address, P.chief, P1.full_name ChiefName
     FROM Person P LEFT JOIN Person P1 ON P1.id = P.chief
    """)
    for row in cursor.fetchall():
        _id = row[0]
        is_organization = row[1]
        full_name = row[2]
        address = row[3]
        chief = row[4]
        chief_full_name = row[5]
        persons[_id] = {
            'id': _id,
            'is_organization': is_organization,
            'full_name': full_name,
            'address': address,
            'chief': chief,
            'chief_full_name': chief_full_name
        }

    cursor.close()


    return {'persons': persons}
