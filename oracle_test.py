import ora_adapter as ora


conn_str = 'korovin13204/korovin13204@10.4.0.119:1521'


class TestTable(ora.Table):
    id = ora.Number(10, primary_key=True)
    string_data = ora.VarChar2(30, default="default v")
    float_data = ora.Float(16)
    # date_data = ora.Date()

    _table_name = "test_table"

    def __init__(self, _id, s, flo, dt):
        self.id = _id
        self.string_data = s
        self.float_data = flo

ora.Oracle(conn_str)

# TestTable.create_table()
row = TestTable(1, "test", 123.333)
row.insert()
ora.Oracle.commit()
ora.Oracle.close()

# import cx_Oracle
#
# conn = cx_Oracle.connect('korovin13204/korovin13204@10.4.0.119:1521')
# cursor = conn.cursor()
#
# cursor.execute('INSERT INTO faculties(id, name) VALUES (8, \'test from python\')')
#
# cursor.close()
# conn.commit()
#
# conn.close()
#
#
#
# exit()
#
# for line in cursor.fetchall():
#     print(line)
