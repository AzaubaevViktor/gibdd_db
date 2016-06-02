from flask import request

from ora_adapter import Oracle
from server import app, expand_request
from server.model import ErrorHandlerAndSend


@app.endpoint("ctae")
@ErrorHandlerAndSend(app)
def ctae():
    ct_id = request.form.get('id')  # type: int

    if not ct_id:
        Oracle.execute("""
        INSERT INTO CrashType(name) VALUES(:name)
        """, **expand_request(request)).close()
    else:
        Oracle.execute("""
            UPDATE CrashType
            SET name=:name
            WHERE id=:id
            """, **expand_request(request)).close()


@app.endpoint("ctd")
@ErrorHandlerAndSend(app)
def ctd():
    Oracle.execute("""
    DELETE FROM CrashType
    WHERE id=:id
    """, expand_request(request)).close()
