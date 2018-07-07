# encoding:utf-8
import json
import uuid
from datetime import datetime

from django.http.response import HttpResponse


__all__ = (
    'HttpJsonResponse',
)


class UUJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, uuid.UUID):
            return o.hex
        elif isinstance(o, datetime):
            return o.timestamp()
        return super(UUJSONEncoder, self).default(o)


class HttpJsonResponse(HttpResponse):

    def __init__(self, data=None, encoder=None, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json; charset=utf-8')
        kwargs.setdefault('status', 200)
        encoder = encoder if encoder else UUJSONEncoder
        data = json.dumps(data, cls=encoder) if data is not None else ''
        super(HttpJsonResponse, self).__init__(content=data, *args, **kwargs)

_error_codes = (
    ('missing_field', '字段缺失'),
    ('missing', '依赖条件缺失'),
    ('invalid', '字段不可用。类型错误或格式错误'),
    ('number_limits', '数量限制'),
    ('not_allow', '不允许的操作对象'),
    ('already_exists', '资源已存在'),
    ('not_found', '资源不存在'),
)


def errors_422(errors, message=''):
    """
    用来组装422错误

    errors: 是一个列表，格式一般为
        {'field': '', 'code': ''}
        {'resource': '', 'code': ''}
    """
    return {
        'message': message,
        'errors': errors,
    }
