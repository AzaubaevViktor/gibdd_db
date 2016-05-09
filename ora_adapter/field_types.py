import json
from abc import ABC, abstractmethod


class FieldType(ABC):
    def __str__(self):
        return ""

    @abstractmethod
    def build(self, **kwargs):
        return ""


class Variable(FieldType):
    _type_s = "ABSTRACTTYPE"

    def __init__(self,
                 size=None,
                 default=None,
                 not_null=False,
                 unique=False,
                 primary_key=False,
                 ):
        self._value = None
        size = "({})".format(size) if size else ""
        not_null = "NOT NULL" if not_null else ""
        unique = "UNIQUE" if unique else ""
        primary_key = "PRIMARY KEY" if primary_key else ""
        default = ("DEFAULT '{}'".format(json.dumps(default))) if default else ""
        params = " ".join([not_null, unique, primary_key])
        self.fmt = '{name} ' +\
                   "{type_s}{size}{params} {default}".format(
                       type_s=self._type_s,
                       size=size,
                       params=params,
                       default=default
                   )

    def build(self, **kwargs):
        return self.fmt.format(**kwargs)

    def set_value(self, value):
        """
        Преобразовывает значение в сырое значение (которое хранится в экземпляре)
        :param value:
        :return:
        """
        return value

    def get_value(self, raw_value):
        """
        Преобразовывает сырое значение в несырое
        :param raw_value:
        :return:
        """
        return raw_value

    def check_value(self, raw_value):
        """
        Преобразует сырое значение в значение для запроса
        :param raw_value:
        :return:
        """
        return str(raw_value)


class VarChar2(Variable):
    _type_s = "VARCHAR2"

    def check_value(self, value):
        return "'{}'".format(str(value))


class Number(Variable):
    _type_s = "NUMBER"


class Date(Variable):
    _type_s = "DATE"


class Float(Variable):
    _type_s = "FLOAT"


class ForeignKey(FieldType):
    def __init__(self,
                 table_name,
                 field_name,
                 on_delete=""):
        on_delete = "ON DELETE {}".format(on_delete) if on_delete else ""
        self.fmt = "FOREIGN KEY ({name}) REFERENCES " + table_name + "({}) ".format(field_name) + on_delete

    def build(self, **kwargs):
        return self.fmt.format(kwargs)
