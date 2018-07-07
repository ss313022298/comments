'''
Created on 2016年11月21日

@author: huangjunfeng
'''
import json
import re
import urllib.parse

from django.conf import settings
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden

from account.helper import TokenHelper
from utils.helper import get_token_verifying, get_client_verifying
from utils.helper import md5_hex_digest
import gzip
from io import BytesIO


_token_required_fashion = settings.TOKEN_REQUIRED_FASHION


def token_required(view, required=True, json_stream=True,
                   has_version=True, methods=[
        "GET", "POST", "PUT", "DELETE", "PATCH"]):
    def decorator(request, *args, **kwargs):
        if request.method not in methods:
            return view(request, *args, **kwargs)

        request.username = None

        try:
            request.access_token = re.match(
                '^token (\w+)', request.META['HTTP_AUTHORIZATION']).groups()[0]
        except (KeyError, AttributeError):
            request.access_token = None

        '''
        判断鉴权方式
        '''
        if _token_required_fashion == 'USERNAME_ONLY':
            request.username = TokenHelper.check(request.access_token)

        elif _token_required_fashion == 'PASSPORT':
            info = get_token_verifying(request.access_token)
            request.username = info['userid'] if info else None

        if not request.username:
            return HttpResponseForbidden()

        # 接收CLIENT_ID
        request.client_id = request.META.get('HTTP_X_CLIENT_ID')
        _deal_request(request)
        return view(request, *args, **kwargs)
    return decorator


def cloud_required(
        view, required=True, json_stream=True, has_version=True,
        methods=["GET", "POST", "PUT", "DELETE", "PATCH"]):
    def decorator(request, *args, **kwargs):
        if request.method not in methods:
            return view(request, *args, **kwargs)
        flag = False
        if 'HTTP_X_APP_ID' in request.META and \
                'HTTP_X_APP_MD5' in request.META:
            if request.META['HTTP_X_APP_MD5'] == md5_hex_digest(
                    '%s%s' % (
                        request.META['HTTP_X_APP_ID'],
                        settings.PROJECT_APP_SECRET)):
                flag = True
        if not flag:
            return HttpResponseForbidden(json.dumps({
                "message": "Authorization failed"}))
        _deal_request(request)
        return view(request, *args, **kwargs)
    return decorator


def client_required(
        required=True, json_stream=True, has_version=True,
        methods=["GET", "POST", "PUT", "DELETE", "PATCH"]):
    def _client_required(view):
        def __decorator(self, request, *args, **kwargs):
            if request.method not in methods:
                return view(request, *args, **kwargs)
            request.client_id = None
            try:
                request.access_token = re.match(
                    '^token (\w+)', request.META['HTTP_AUTHORIZATION']).groups()[0]
            except (KeyError, AttributeError):
                request.access_token = None
            info = get_client_verifying(request.access_token)
            request.client_id = info['client_id'] if info else None
            if not request.client_id:
                return HttpResponseForbidden(json.dumps({
                    "message": "Authorization failed"}))
            if json_stream:
                resp = _deal_request(request)
                if resp is not None:
                    return resp
            return view(self, request, *args, **kwargs)
        return __decorator
    return _client_required


def json_required(
        required=True, json_stream=True, methods=[
            "GET", "POST", "PUT", "DELETE", "PATCH"]):
    def _json_required(view):
        def __decorator(self, request, *args, **kwargs):
            if request.method not in methods:
                return view(request, *args, **kwargs)
            _deal_request(request)
            return view(self, request, *args, **kwargs)
        return __decorator
    return _json_required


def _deal_request(request, json_stream=True, has_version=True):
    if json_stream and request.method in ['PUT', 'POST', 'PATCH']:
        stream = request.body
        if stream:
            try:
                is_gzip = request.META.get('HTTP_CONTENT_ENCODING') == 'gzip'
                if is_gzip:
                    gz = gzip.GzipFile(fileobj=BytesIO(request.body))
                    stream = gz.read()
                    gz.close()
                if isinstance(stream, bytes):
                    stream = stream.decode()
                    request.jsondata = json.loads(stream)
            except:
                return HttpResponseBadRequest(json.dumps({
                    "message": "Problems parsing JSON"}))
        else:
            request.jsondata = {}
    if has_version:
        try:
            request.version = re.match(
                '^application/vnd.uucin.v(.+)\+json',
                request.META['HTTP_ACCEPT']).groups()[0]
        except (KeyError, AttributeError):
            request.version = None
