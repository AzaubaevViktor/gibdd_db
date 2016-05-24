from ora_adapter import Oracle
from database_init import delete_tables

conn_str = 'korovin13204/korovin13204@10.4.0.119:1521'

Oracle(conn_str)

delete_tables.drop()
