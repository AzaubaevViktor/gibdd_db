from ora_adapter import Oracle

conn_str = 'korovin13204/korovin13204@10.4.0.119:1521'

Oracle(conn_str)

from database_init import create_tables, index_auto

create_tables.create()

for table_name in create_tables.databases:
    index_auto.set_auto_increment(table_name, 'id')
