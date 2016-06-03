from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('psa')
@ErrorHandlerAndSend(app)
def psa():
    persons = {}

    cursor = Oracle.execute("""
    SELECT P.id, P.is_organization, P.full_name, P.address, P.chief_id, P1.full_name ChiefName
     FROM Person P LEFT JOIN Person P1 ON P1.id = P.chief_id
    """)
    for row in cursor.fetchall():
        _id = row[0]
        is_organization = row[1]
        full_name = row[2]
        address = row[3]
        chief_id = row[4]
        chief_full_name = row[5]
        persons[_id] = {
            'id': _id,
            'is_organization': is_organization,
            'full_name': full_name,
            'address': address,
            'chief_id': chief_id,
            'chief_full_name': chief_full_name
        }

    cursor.close()

    return {'persons': persons}


@app.endpoint('ps')
@ErrorHandlerAndSend(app)
def ps(p_id):
    cursor = Oracle.execute("""
    SELECT P.IS_ORGANIZATION, P.FULL_NAME, P.ADDRESS, P.CHIEF_ID,
      C.FULL_NAME chief_full_name
      FROM Person P
        LEFT JOIN Person C ON C.id=P.CHIEF_ID
      WHERE P.id=:p_id
    """, p_id=p_id)

    row = cursor.fetchone()
    cursor.close()

    person = {
        'id': p_id,
        'is_organization': row[0],
        'full_name': row[1],
        'address': row[2],
        'chief_id': row[3],
        'chief_full_name': row[4],
        'vehicles': {}
    }

    cursor = Oracle.execute("""
    SELECT V.id, VT.name, V.reg_number
      FROM Vehicle V
        LEFT JOIN VehicleType VT ON V.vehicle_type_id=VT.id
      WHERE V.chief_id=:p_id
    """, p_id=p_id)

    for row in cursor.fetchall():
        person['vehicles'][row[0]] = {
            'id': row[0],
            'vehicle_type_name': row[1],
            'reg_number': row[2]
        }

    cursor.close()

    return person
