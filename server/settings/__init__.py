__author__ = 'ktulhy'


class Config:
    ERROR_RAISING = False
    DEBUG = True
    SHARE = True
    CSRF_ENABLED = True
    SECRET_KEY = '8ha89bnqeuyidhuqo89nc98dhndundhwq0fhlfdasnfjkl'

    DEBUG_TB_INTERCEPT_REDIRECTS = DEBUG
    TEMPLATE_DEBUG = DEBUG

    LINE_STATEMENT_PREFIX = '%'
    APP_NAME = "ГИБДД БД"
    VERSION = " α"

    SEND_FILE_MAX_AGE_DEFAULT = 0
