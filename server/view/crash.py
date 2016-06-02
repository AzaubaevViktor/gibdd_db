from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('csa')
@ErrorHandlerAndSend(app)
def csa():
    crashes = {}

    cursor = Oracle.execute("""
    SELECT C.id, C.address, C.about, TO_CHAR(C.cdate, 'DD.MM.YYYY') FROM Crash C
    """)

    for row in cursor.fetchall():
        _id = row[0]

        crashes[_id] = {
            'id': _id,
            'address': row[1],
            'about': row[2],
            'date': row[3]
        }

    cursor.close()

    return {'crashes': crashes}


@app.endpoint('cs')
@ErrorHandlerAndSend(app)
def cs(c_id):
    # Получаем основные данные о ДТП
    cursor = Oracle.execute("""
        SELECT id, TO_CHAR(cdate, 'DD.MM.YYYY'), CRASH_TYPE_ID, address, about, VICTIMS, DAMAGE_COST, CAUSE, ROAD_CONDITION
          FROM Crash
          WHERE id=:c_id
        """, c_id=c_id)

    crash = {}

    for row in cursor.fetchall():
        _id = row[0]
        crash = {
            'id': _id,
            'cdate': row[1],
            'crash_type_id': row[2],
            'address': row[3],
            'about': row[4],
            'victims': row[5],
            'damage_cost': row[6],
            'cause': row[7],
            'road_condition': row[8],
            'vehicles': []
        }

    cursor.close()

    # Получаем машины из этого ДТП

    cursor = Oracle.execute("""
    SELECT vehicle_id FROM CrashVehicleLink
    WHERE crash_id = :c_id
    """, c_id=c_id)

    for row in cursor.fetchall():
        crash['vehicles'].append(row[0])

    return crash
