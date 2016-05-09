from ora_adapter import Oracle
from .field_types import FieldType


class Table:
    _table_name = ""
    __fields = {}

    def __new__(cls, *args):
        """
        Перехватывает создание instanc-а
        :param args:
        :return:
        """
        cls.__fields = cls._get_fields()
        new_table = super(Table, cls).__new__(cls)

        field_values = {}

        for name, field in cls.__fields.items():
            field_values[name] = None

            def field_getter(self):
                print("get")
                return field.get_value(self.__fields_values[name])

            def field_setter(self, value):
                print("set `{}`".format(value))
                self.__field_values[name] = field.set_value(value)

            new_table.__dict__[name] = property(field_getter, field_setter)

        new_table.__fields_values = field_values
        return new_table

    @classmethod
    def _get_fields(cls):
        fields = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, FieldType):
                fields[k] = v
        return fields

    @classmethod
    def create_table(cls):
        """
        Создаёт таблицу
        :return:
        """
        fields = []
        for k, v in cls._get_fields().items():
            fields.append(
                v.build(name=k)
            )
        query = "CREATE TABLE {name} (\n{fields}\n)".format(
            name=cls._table_name,
            fields=",\n".join(fields)
        )

        Oracle.execute(query).close()

    def insert(self):
        field_names = []
        values = []
        for name, field in self.__fields.items():
            field_names.append(name)
            values.append(field.check_value(self.__dict__[name]))

        query = "INSERT INTO {table_name}({field_names})\n" \
                "VALUES ({values})".format(
            table_name=self._table_name,
            field_names=", ".join(field_names),
            values=", ".join(values)
        )
        Oracle.execute(query)
