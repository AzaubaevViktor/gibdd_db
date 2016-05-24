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
    chief_id = request.form.get('chief_id')
    if '-1' == chief_id:
        chief_id = None

    if not p_id:
        Oracle.execute("""
        INSERT INTO Person(is_organization, full_name, address, chief_id)
        VALUES (:is_organization, :full_name, :address, :chief_id)
        """, is_organization=is_organization,
                       full_name=full_name,
                       address=address,
                       chief_id=chief_id)
    else:
        Oracle.execute("""
        UPDATE Person
        SET
          is_organization=:is_organization,
          full_name=:full_name,
          address=:address,
          chief_id=:chief_id
        WHERE id=:p_id
        """, p_id=p_id,
                       is_organization=is_organization,
                       full_name=full_name,
                       address=address,
                       chief_id=chief_id
                       ).close()


@app.endpoint("pd")
@ErrorHandlerAndSend(app)
def pd():
    p_id = request.form.get('id')
    cursor = Oracle.execute("""
    SELECT COUNT(*) FROM Person WHERE chief_id=:p_id
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
