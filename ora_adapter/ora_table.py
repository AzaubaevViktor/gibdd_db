from ora_adapter import Oracle
from .field_types import FieldType


class Table:
    _table_name = ""

    @classmethod
    def create_table(cls):
        fields = []
        for k, v in cls.__dict__.items():
            if isinstance(v, FieldType):
                fields.append(
                    v.build(name=k)
                )
        query = "CREATE TABLE {name} (\n{fields}\n)".format(
            name=cls._table_name,
            fields=",\n".join(fields)
        )

        Oracle.execute(query).close()
