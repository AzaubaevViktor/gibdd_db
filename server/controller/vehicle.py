from flask import request

from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend

feature_field_list = ['value_date', 'data_str', 'data_int', 'data_float']
data_adapter = [
    lambda d: d,
    lambda d: d,
    lambda d: int(d),
    lambda d: float(d)
]
data_wrapper = [
    "TO_DATE(:data, 'DD.MM.YYYY')",
    ":data",
    ":data",
    ":data"
]


@app.endpoint("vae")
@ErrorHandlerAndSend(app)
def vae():
    v_id = request.form.get('id')
    vehicle_type_id = request.form.get('vehicle_type_id')
    reg_number = request.form.get('reg_number')
    chief_id = request.form.get('chief_id')

    # Вот эта ебала чтобы обработать фичи
    features = {}
    # Тут мы получаем значения из формы
    for k, v in request.form.items():
        if 'vft_' == k[:4]:
            features[int(k[4:])] = {'value': v if v else None}
    # А тут мы их сопоставляем с тем, что есть в БД
    cursor = Oracle.execute("""
        SELECT id, name, variable_type FROM VehicleFeatureType ORDER BY id
        """)

    for row in cursor.fetchall():
        f_id = row[0]
        f_name = row[1]
        f_vt = int(row[2])
        feature = features.get(f_id, None)
        if not feature or not feature['value']:
            continue

        try:
            # Добавляем в какое поле надо писать
            feature['sql_field'] = feature_field_list[f_vt]
            feature['data_wrapper'] = data_wrapper[f_vt]
            # И обрабатываем переменную
            feature['value'] = data_adapter[f_vt](feature['value'])
        except Exception as e:
            return {'status': 'error',
                    'description': "Ошибка при обработке поля `{}`: '{}'".format(
                        f_name, str(e)
                    ),
                    'type': type(e).__name__}

    if not v_id:
        Oracle.execute("""
        INSERT INTO Vehicle(VEHICLE_TYPE_ID, REG_NUMBER, chief_id)
        VALUES (:vehicle_type_id, :reg_number, :chief_id)
        """, vehicle_type_id=vehicle_type_id,
                       reg_number=reg_number,
                       chief_id=chief_id).close()
        cursor = Oracle.execute("""
        SELECT id FROM Vehicle
        WHERE reg_number=:reg_number
        """, reg_number=reg_number)

        v_id = cursor.fetchone()[0]
        cursor.close()
    else:
        Oracle.execute("""
        UPDATE VEHICLE
        SET
          vehicle_type_id=:vehicle_type_id,
          reg_number=:reg_number,
          chief_id=:chief_id
        WHERE id=:v_id
        """, v_id=v_id,
                       vehicle_type_id=vehicle_type_id,
                       reg_number=reg_number,
                       chief_id=chief_id
                       ).close()

    for f_id, feature in features.items():
        if feature['value']:
            Oracle.execute("""
            MERGE INTO VehicleFeatureLink vfl
              USING dual
              ON (vfl.vehicle_id=:v_id AND vfl.vehicle_feature_type_id=:vft_id)
              WHEN MATCHED THEN
                UPDATE SET vfl.{field}={data_wrapper}
              WHEN NOT MATCHED THEN
                INSERT (vfl.vehicle_id, vfl.VEHICLE_FEATURE_TYPE_ID, vfl.{field}) VALUES (:v_id, :vft_id, {data_wrapper})
            """.format(field=feature['sql_field'],
                       data_wrapper=feature['data_wrapper']),
                           v_id=v_id,
                           vft_id=f_id,
                           data=feature['value']).close()
        else:
            Oracle.execute("""
            DELETE FROM VehicleFeatureLink
            WHERE vehicle_id=:v_id AND vehicle_feature_type_id=:vft_id
            """,
                           v_id=v_id,
                           vft_id=f_id).close()


@app.endpoint("vd")
@ErrorHandlerAndSend(app)
def vd():
    v_id = request.form.get('id')
    Oracle.execute("""
    DELETE FROM VehicleFeatureLink
    WHERE vehicle_id=:v_id
    """, v_id=v_id).close()

    Oracle.execute("""
    DELETE FROM Vehicle
    WHERE id=:v_id
    """, v_id=v_id).close()