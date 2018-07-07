'''
Created on 2018年2月7日

@author: zhangqingwei
'''
import json
import logging
from django.http.response import HttpResponseForbidden, HttpResponseBadRequest
import re

# from client.helper import ClientTokenHelper

logger = logging.getLogger('default')


def session_required(
        required=True, json_stream=True, has_version=True,
        methods=["GET", "POST", "PUT", "DELETE", "PATCH"]):
    def _session_required(view):
        def __decorator(self, request, *args, **kwargs):
            if request.method not in methods:
                return view(request, *args, **kwargs)
            if not request.user.is_authenticated():
                return HttpResponseForbidden(json.dumps({
                    "message": "Authorization failed"}))
            if not _deal_request(request):
                return HttpResponseBadRequest(json.dumps({
                    "message": "Problems parsing JSON"}))
            return view(self, request, *args, **kwargs)

        return __decorator

    return _session_required


def json_required(
        required=True, json_stream=True, has_version=True,
        methods=["GET", "POST", "PUT", "DELETE", "PATCH"]):
    def _json_required(view):
        def __decorator(self, request, *args, **kwargs):
            if request.method not in methods:
                return view(request, *args, **kwargs)
            if not _deal_request(request):
                return HttpResponseBadRequest(json.dumps({
                    "message": "Problems parsing JSON"}))
            return view(self, request, *args, **kwargs)

        return __decorator

    return _json_required


def api_required(methods=["GET", "POST", "PUT", "DELETE", "PATCH"]):
    def _api_required(view):
        def __decorator(self, request, *args, **kwargs):
            if request.method not in methods:
                return view(request, *args, **kwargs)
            try:
                request.access_token = re.match(
                    '^token (\w+)', request.META['HTTP_AUTHORIZATION']
                ).groups()[0]
            except (KeyError, AttributeError):
                request.access_token = None
            # client_info = ClientTokenHelper.verify(request.access_token)
            # if not client_info:
            #     return HttpResponseForbidden(json.dumps({
            #         "message": "Authorization failed"}))
            # request.client_id = client_info['client_id']
            if not _deal_request(request):
                return HttpResponseBadRequest(json.dumps({
                    "message": "Problems parsing JSON"}))
            return view(self, request, *args, **kwargs)

        return __decorator

    return _api_required


def _deal_request(request, json_stream=True, has_version=True):
    if json_stream and request.method in ['PUT', 'POST', 'PATCH', 'DELETE']:
        stream = request.body
        if stream:
            try:
                if isinstance(stream, bytes):
                    stream = stream.decode()
                request.jsondata = json.loads(stream)
            except Exception as e:
                if isinstance(e, ValueError):
                    request.jsondata = {}
                else:
                    return False
        else:
            request.jsondata = {}
    return True
