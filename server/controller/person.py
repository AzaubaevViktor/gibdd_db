from flask import request

from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint("pae")
@ErrorHandlerAndSend(app)
def pae():
    p_id = request.form.get('id')
    is_organization = bool(int(request.form.get('is_organization'))) # type: bool
    full_name = request.form.get('full_name')  # type: str
    address = request.form.get('address')  # type: str
    chief = request.form.get('chief')
    if '-1' == chief:
        chief = None

    if not p_id:
        Oracle.execute("""
        INSERT INTO Person(is_organization, full_name, address, chief)
        VALUES (:is_organization, :full_name, :address, :chief)
        """, is_organization=is_organization,
                       full_name=full_name,
                       address=address,
                       chief=chief)
    else:
        Oracle.execute("""
        UPDATE Person
        SET
          is_organization=:is_organization,
          full_name=:full_name,
          address=:address,
          chief=:chief
        WHERE id=:p_id
        """, p_id=p_id,
                       is_organization=is_organization,
                       full_name=full_name,
                       address=address,
                       chief=chief
                       ).close()


@app.endpoint("pd")
@ErrorHandlerAndSend(app)
def pd():
    p_id = request.form.get('id')
    cursor = Oracle.execute("""
    SELECT COUNT(*) FROM Person WHERE chief=:p_id
    """, p_id=p_id)
    childs = cursor.fetchone()[0]
    cursor.close()

    if 0 == childs:
        Oracle.execute("""
        DELETE FROM Person
        WHERE id=:p_id
        """, p_id=p_id).close()
    else:
        return {'status': 'error',
                'type': 'Database Error',
                'description': 'Невозможно удалить владельца организации'}
