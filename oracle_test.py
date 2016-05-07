import cx_Oracle

conn = cx_Oracle.connect('korovin13204/korovin13204@10.4.0.119:1521')
cursor = conn.cursor()

cursor.execute('SELECT * FROM groups')

for line in cursor.fetchall():
    print(line)
