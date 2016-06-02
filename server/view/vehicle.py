from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint('vsa')
@ErrorHandlerAndSend(app)
def vsa():
    vehicles = {}

    # Получаем данные о машине
    cursor = Oracle.execute("""
    SELECT V.id, V.vehicle_type_id, V.reg_number, V.chief_id, VT.name, P.FULL_NAME
     FROM Vehicle V
     LEFT JOIN VehicleType VT ON VT.id = V.vehicle_type_id
     LEFT JOIN Person P ON P.id = V.chief_id
    """)
    for row in cursor.fetchall():
        _id = row[0]
        vehicle_type_id = row[1]
        reg_number = row[2]
        chief_id = row[3]
        vt_name = row[4]
        c_name = row[5]
        vehicles[_id] = {
            'id': _id,
            'vehicle_type_id': vehicle_type_id,
            'reg_number': reg_number,
            'chief_id': chief_id,
            'vt_name': vt_name,
            'c_name': c_name,
            'features': {}
        }
    cursor.close()

    # Получаем фичи о машине
    cursor = Oracle.execute("""
    SELECT vfl.VEHICLE_ID, vfl.vehicle_feature_type_id, vt.variable_type + 3 field_index, TO_CHAR(vfl.value_date, 'MM.DD.YYYY'), vfl.data_str, vfl.data_int, vfl.data_float
     FROM VehicleFeatureLink vfl
      LEFT JOIN VehicleFeatureType vt ON vt.id = vfl.vehicle_feature_type_id
    """)

    for row in cursor.fetchall():
        v_id = row[0]
        vft_id = row[1]
        field_index = row[2]
        data = row[field_index]
        vehicles[v_id]['features'][vft_id] = data

    cursor.close()

    return {'vehicles': vehicles}
