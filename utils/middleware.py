import json
import re
import urllib

from django.conf import settings
from django.http.response import HttpResponse

__all__ = (
    'SignalsAutoloadMiddleware',
    'ProcessRequestDataMiddleware',
    'CORSMiddleware',
    'RemoteAddressMiddleware',
)


class SignalsAutoloadMiddleware(object):

    def __init__(self):
        for apps in settings.INSTALLED_APPS:
            try:
                __import__('%s.signals' % apps)
            except Exception:
                pass


class ProcessRequestDataMiddleware(object):
    '''
    处理请求数据
    现阶段只支持3中格式：json、form表单、文件上传
 
    请求的时候需要添加请求头：Content-Type（可以不加，不加使用默认值）
        json：application/json
        form表单：application/x-www-form-urlencoded或text/plain
        文件上传：multipart/form-data
 
    GET请求Content-Type默认值为text/plain
    其他请求Content-Type默认值为application/json
 
    请求方法：GET、POST、PATCH、PUT、DELETE
    '''

    matchs = {
        'json': re.compile(r'application/json.*'),
        'form': re.compile(r'application/x-www-form-urlencoded.*'),
        'file_upload': re.compile(r'multipart/form-data.*'),
        'text': re.compile(r'text/plain.*'),
    }

    def process_request(self, request):
        if request.method in ['HEAD', 'OPTIONS']:
            return
        if request.method == 'GET':
            content_type = request.META.get('CONTENT_TYPE', 'text/plain')
        else:
            content_type = request.META.get('CONTENT_TYPE', 'application/json')

        content_type = content_type.lower()
        b, m = True, None
        if self.matchs['json'].match(content_type):
            b, m = self._json(request)
        elif self.matchs['file_upload'].match(content_type):
            b, m = True, None
        #             b, m = self._form(request)
        elif self.matchs['text'].match(content_type):
            b, m = self._form(request)
        elif self.matchs['form'].match(content_type):
            b, m = self._form(request)
        else:
            '''不被支持的格式'''
            b, m = False, '{"message": ""}'

        if b:
            return None
        else:
            m = m if m else ''
            return HttpResponse(m, status=400, content_type='application/json')

    def _json(self, request):
        '''json格式'''
        if request.method == 'GET':
            query_string = request.META.get('QUERY_STRING')
            query_string = urllib.parse.unquote(query_string)
            datastr = query_string if query_string else '{}'
        else:
            datastr = request.body.decode()

        try:
            request.data = json.loads(datastr)
            return True, None
        except:
            if datastr == '':
                return True, {}
            return False, '{"message": "Body should be a JSON Hash"}'

    def _form(self, request):
        '''普通form表单格式'''
        if request.method == 'GET':
            query_string = request.META.get('QUERY_STRING')
            datastr = query_string if query_string else ''
        else:
            datastr = request.body.decode()

        querylist = urllib.parse.parse_qsl(datastr)
        data = {}
        for key, value in querylist:
            data[key] = value
        request.data = data
        return True, None

    def _xml(self, request):
        request.data = {}
        return True, None


class CORSMiddleware(object):
    cors_allow_origin = '*'  # any domain
    cors_allow_credentials = False
    cors_allow_methods = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS',
        'HEAD',
    )
    cors_allow_headers = (
        'Authorization',
        'DNT',
        'X-CustomHeader',
        'Keep-Alive',
        'User-Agent',
        'X-Requested-With',
        'If-Modified-Since',
        'Cache-Control',
        'Content-Type',
        'Content-Range',
        'Range',
    )
    cors_expose_headers = cors_allow_headers + (
        'Date',
        'Link',
    )
    cors_max_age = 864000  # 10 days

    def make_actual_headers(self, request_origin, allow_origin=None,
                            allow_credentials=None, expose_headers=None):
        allow_origin = allow_origin or self.cors_allow_origin
        allow_credentials = allow_credentials or self.cors_allow_credentials
        expose_headers = expose_headers or self.cors_expose_headers
        allow_methods = self.cors_allow_methods
        allow_headers = self.cors_allow_headers
        max_age = self.cors_max_age

        if allow_origin == '*' and request_origin is not None:
            allow_origin = request_origin
            allow_credentials = True

        headers = {
            'Access-Control-Allow-Origin': allow_origin,
            'Access-Control-Allow-Methods': ', '.join(allow_methods),
            'Access-Control-Allow-Headers': ', '.join(allow_headers),
            'Access-Control-Expose-Headers': ', '.join(expose_headers),
            'Access-Control-Max-Age': max_age,
        }
        if allow_credentials:
            headers.update({'Access-Control-Allow-Credentials': 'true'})
        if allow_origin != '*':
            headers.update({'Vary': 'Origin'})

        return headers

    def process_response(self, request, response):
        request_origin = request.META.get('HTTP_ORIGIN')
        headers = self.make_actual_headers(request_origin)
        for k, v in headers.items():
            response[k] = v
        return response


class RemoteAddressMiddleware(object):
    '''
    中间件，作用为通过请求的header获取远程IP地址，并将其绑定到request对象上
    '''

    def process_request(self, request):
        '''
        @summary: 先后对X-Forwarded-Protocol, X-Forwarded-Protocol,
                   request.META['REMOTE_ADDR']进行IP地址格式判别。
                   判定成功则将其绑定到request.remote_addr上，
                   判定失败request.remote_addr为IP地址未知。
        '''
        # IP地址的正则表达式
        ip_regex = r'^(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}$'

        # 先对X-Forwarded-Protocol进行判别，若是IP地址，退出方法
        x_forwarded_protocol = request.META.get('HTTP_X_FORWARDED_PROTOCOL')
        if isinstance(x_forwarded_protocol, str
                      ) and re.match(ip_regex, x_forwarded_protocol):
            request.remote_addr = x_forwarded_protocol
        else:
            # X-Forwarded-Protocol不是IP地址，再对X-Real-IP进行类似判别
            real_ip = request.META.get('HTTP_X_REAL_IP')
            if isinstance(real_ip, str) and re.match(ip_regex, real_ip):
                request.remote_addr = real_ip
            elif re.match(ip_regex, request.META['REMOTE_ADDR']):
                # 使用META进行判别
                request.remote_addr = request.META['REMOTE_ADDR']
            else:
                # 其他情况IP地址未知
                request.remote_addr = 'IP地址未知'
