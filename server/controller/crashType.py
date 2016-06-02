from flask import request

from ora_adapter import Oracle
from server import app
from server.model import ErrorHandlerAndSend


@app.endpoint("ctae")
@ErrorHandlerAndSend(app)
def ctae():
    ct_id = request.form.get('id')  # type: int
    name = request.form.get('name')  # type: str

    if not ct_id:
        Oracle.execute("""
        INSERT INTO CrashType(name) VALUES(:name)
        """, name=name).close()
    else:
        Oracle.execute("""
            UPDATE CrashType
            SET name=:name
            WHERE id=:id
            """, id=ct_id, name=name).close()


@app.endpoint("ctd")
@ErrorHandlerAndSend(app)
def ctd():
    ct_id = request.form.get('id')

    Oracle.execute("""
    DELETE FROM CrashType
    WHERE id=:ct_id
    """, ct_id=ct_id).close()
