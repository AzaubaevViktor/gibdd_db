import datetime
import json
import traceback

import sys

import cx_Oracle


def _json_date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def render_answer(obj: dict, **kwargs) -> str:
    kwargs.update(obj)
    return json.dumps(kwargs, ensure_ascii=False, default=_json_date_handler).encode('utf-8')


INTEGRITY_STR = "Объект с таким именем существует;<br>" \
                "ИЛИ невозможно удалить объект, так как он связан с другими объектами<br>" \
                "(попробуйте удалить связанные объекты)<br>" \
                "ИЛИ произошло нечто совершенно безумное и ничего не поделаешь"


class ErrorHandlerAndSend:
    """
    Класс-декоратор, позволяющий обрабатывать ошибки и отправлять их через json
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, func):
        """

        :param func: Функция, которая возвращает dict с ответом
        :return:
        """

        def result_func(*args, **kwargs):
            try:
                answer = func(*args, **kwargs)
            except Exception as e:
                if self.app.config['ERROR_RAISING']:
                    raise e
                print(traceback.format_exc(), file=sys.stderr)

                desc = str(e)

                if isinstance(e, cx_Oracle.IntegrityError):
                    if e.args[0].code == 1:
                        desc = "Значение одного или нескольких полей повторяется"

                answer = {'status': 'error',
                          'description': desc,
                          'type': type(e).__name__}
            if not answer:
                answer = {'status': 'ok'}

            if 'status' not in answer:
                answer['status'] = 'ok'

            return render_answer(answer)

        return result_func
