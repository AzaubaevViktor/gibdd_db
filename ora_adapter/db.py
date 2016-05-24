import os
import traceback

os.environ['NLS_LANG'] = 'RUSSIAN_RUSSIA.AL32UTF8'

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
    def try_execute(cls, query: str, *args, **kwargs):
        try:
            cls.execute(query, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()

    @classmethod
    def execute(cls, query: str, *args, **kwargs):
        """
        Выполнить запрос в БД
        :param query: строка запроса
        :return:
        """
        cursor = cls.instance.conn.cursor()
        print("Debug: `{}`:{}::{}".format(query, args, kwargs))
        cursor.execute(query, *args, **kwargs)
        print("Ok")
        cls.commit()
        return cursor

    @classmethod
    def commit(cls):
        """
        Выгрузить данные в таблицу
        :return:
        """
        cls.instance.conn.commit()

    @classmethod
    def close(cls):
        """
        Закрыть соединение
        :return:
        """
        cls.instance.conn.close()

    @classmethod
    def __getattr__(cls, item):
        return getattr(cls.instance, item)
