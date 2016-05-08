import cx_Oracle


class Oracle:
    class __Oracle:
        def __init__(self, addr):
            self.addr = addr
            self.conn = None
            self.connect()

        def connect(self):
            self.conn = cx_Oracle.connect('korovin13204/korovin13204@10.4.0.119:1521')

        def disconnect(self):
            self.conn.close()

    instance = None

    def __init__(self, addr):
        if not Oracle.instance:
            Oracle.instance = Oracle.__Oracle(addr)
        else:
            Oracle.instance.disconnect()
            Oracle.instance.addr = addr
            Oracle.instance.connect()

    @classmethod
    def execute(cls, query: str):
        cursor = cls.instance.conn.cursor()
        print("Debug: `{}`".format(query))
        cursor.execute(query)
        print("Ok")
        return cursor

    @classmethod
    def commit(cls):
        cls.instance.conn.commit()

    @classmethod
    def close(cls):
        cls.instance.conn.close()

    @classmethod
    def __getattr__(cls, item):
        return getattr(cls.instance, item)
