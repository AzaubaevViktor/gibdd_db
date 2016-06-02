from flask import request

from ora_adapter import Oracle
from server import app, expand_request
from server.model import ErrorHandlerAndSend


@app.endpoint("cae")
@ErrorHandlerAndSend(app)
def cae():
    c_id = request.form.get('id')

    data = {k: v for k, v in expand_request(request).items() if 'vehicle_' not in k}
    data['victims'] = int(data['victims'])
    data['crash_type_id'] = int(data['crash_type_id'])
    data['damage_cost'] = float(data['damage_cost'])

    if not c_id:
        Oracle.execute("""
        INSERT INTO Crash (cdate,crash_type_id,address,about,victims,damage_cost,cause,road_condition)
        VALUES (TO_DATE(:cdate, 'DD.MM.YYYY'), :crash_type_id, :address, :about, :victims, :damage_cost, :cause, :road_condition)
        """, **data).close()

        cursor = Oracle.execute("""
        SELECT MAX(id) FROM Crash
        """)

        c_id = cursor.fetchone()[0]
    else:
        Oracle.execute("""
        UPDATE Crash
        SET cdate=:cdate,
            crash_type_id=:crash_type_id,
            address=:address,
            about=:about,
            victims=:victims,
            damage_cost=:damage_cost,
            cause=:cause,
            road_condition=:road_condition
        WHERE id=:id
        """, **data).close()

    vehicles = []
    for k, v in request.form.items():
        print(v)
        if ('vehicle_' == k[:8]) and ('true' == v):
            vehicles.append(int(k[8:]))

    Oracle.execute("""
    DELETE FROM CrashVehicleLink
    WHERE crash_id=:c_id
    """, c_id=c_id).close()

    for v_id in vehicles:
        Oracle.execute("""
        INSERT INTO CrashVehicleLink
        (crash_id, vehicle_id)
        VALUES (:c_id, :v_id)
        """, c_id=c_id, v_id=v_id).close()


@app.endpoint("cd")
@ErrorHandlerAndSend(app)
def cd():
    Oracle.execute("""
    DELETE FROM Crash
    WHERE id=:id
    """, **expand_request(request)).close()
