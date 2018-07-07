# encoding:utf-8
'''
Created on 2017年6月1日

@author: zhangqingwei
'''
import hashlib
import json
import logging
import random
import string
import time
import uuid

from django.core.paginator import Paginator, EmptyPage
from django.http.response import HttpResponse

# from oauth2.helper import UuTokenHelper
from utils.responses import HttpJsonResponse

logger = logging.getLogger('default')


def get_current_page(results, page_num=1, page_size=10):
    page_obj = Paginator(results, page_size)
    total_page = page_obj.num_pages
    try:
        results = page_obj.page(page_num)
    except EmptyPage:
        return None, 0
    return results, total_page


def response_errors(errors: object, status: object = 422) -> object:
    return HttpJsonResponse({
        "message": "Validation Failed", "errors": errors
    }, status=status)


def json_dumps(json_object):
    return json.dumps(json_object, ensure_ascii=False)


def uuid1_hex():
    return uuid.uuid1().hex


def unique_uuid():
    return uuid.uuid1().hex


def get_local_host(request):
    uri = request.build_absolute_uri()
    return uri[0:uri.find(request.path)]


def md5_hex_digest(value, encoding="raw_unicode_escape"):
    h = hashlib.md5(value.encode(encoding))
    return h.hexdigest()


def get_timestamp():
    return int(time.time() * 1000) / 1000.0


def validate_form(form_class, data):
    form = form_class(data)
    if form.is_valid():
        return True, form.cleaned_data
    errors = []
    for key, field in form.declared_fields.items():
        if field.required and key not in data:
            errors.append({"field": key, "code": "missing_field"})
        elif key in form.errors:
            errors.append({"field": key, "code": "invalid"})
    return False, errors


class HttpJsonResponse(HttpResponse):

    def __init__(self, data=None, encoder=None, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        kwargs.setdefault('status', 200)
        data = json.dumps(data, cls=encoder) if data is not None else ''
        super(HttpJsonResponse, self).__init__(content=data, *args, **kwargs)


def http_response(content=None, status=200):
    return HttpJsonResponse(content, status=status)


def create_random_string(length, letters=True, digits=True, filters=['O', 'o', '0']):
    if letters and not digits:
        raw_string = string.ascii_letters
    elif not letters and digits:
        raw_string = string.digits
    else:
        raw_string = string.ascii_letters + string.digits
    return ''.join(random.sample(filter((lambda x: False if x in filters else True), raw_string), length))


def exchange_interval(seconds):
    m, _ = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m



class RequestParamsHandle(object):

    @classmethod
    def get_time_range(cls, section):
        if not section:
            return 0, get_timestamp()
        try:
            min_stamp, max_stamp = section.split(',')
        except ValueError:
            return None, None
        if min_stamp is u'':
            if max_stamp is u'':
                return min_stamp, max_stamp
            return None, None
        else:
            if min_stamp == 'inf':
                return 'inf', None
            try:
                if max_stamp is u'':
                    min_stamp, max_stamp = float(min_stamp), get_timestamp()
                else:
                    min_stamp, max_stamp = float(min_stamp), float(max_stamp)
            except ValueError:
                return None, None
        if min_stamp > max_stamp:
            return None, None
        return min_stamp, max_stamp