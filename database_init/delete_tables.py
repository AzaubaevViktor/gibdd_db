from ora_adapter import Oracle
from .create_tables import databases


def drop():
    for table in databases:
        Oracle.try_execute("""
        DROP TABLE :tbl  cascade constraints
        """, tbl=table)
