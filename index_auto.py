from ora_adapter import Oracle


def set_auto_increment(table, field):
    table_ais = "{table}_ais".format(table=table)
    table_trig = "{table}_ait".format(table=table)

    query_seq = "CREATE SEQUENCE {table_ais}".format(table_ais=table_ais)
    Oracle.try_execute(query_seq)

    query = """
    CREATE OR REPLACE TRIGGER {table_trig}
      BEFORE INSERT ON {table}
      FOR EACH ROW

      BEGIN
        SELECT {table_ais}.nextval
        INTO :new.{field}
        FROM dual;
      END;
    """.format(
        table=table,
        table_ais=table_ais,
        table_trig=table_trig,
        field=field
    )
    Oracle.execute(query)
