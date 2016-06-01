from ora_adapter import Oracle
from .create_tables import databases


def drop():
    s = ""
    for table in databases:
        s += """
        DROP TABLE {tbl} cascade constraints;
        """.format(tbl=table)
    print(s)
