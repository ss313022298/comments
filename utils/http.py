# encoding:utf-8
'''
Created on 2018年2月18日

@author: zhangqingwei
'''
from django.conf import settings
import requests
from .responses import HttpJsonResponse

from .helper import md5_hex_digest


class Request(object):

    def __init__(self):
        self.headers = {
            'X-CLIENT-ID': settings.PASSPORT_CLIENT_ID,
            'X-CLIENT-MD5': md5_hex_digest(
                '%s%s' % (
                    settings.PASSPORT_CLIENT_ID,
                    settings.PASSPORT_CLIENT_SECRET))
        }

    def get(self, url, params=None):
        return self.deal_resp(requests.get(
            url=url,
            params=params,
            headers=self.headers)
        )

    def head(self, url):
        return self.deal_resp(requests.head(
            url=url,
            headers=self.headers)
        )

    # data为字典类型
    def post(self, url, data=None):
        return self.deal_resp(requests.post(
            url=url,
            json=data,
            headers=self.headers)
        )

    def put(self, url, data=None):
        return self.deal_resp(requests.put(
            url=url,
            json=data,
            headers=self.headers)
        )

    def patch(self, url, data=None):
        return self.deal_resp(requests.patch(
            url=url,
            json=data,
            headers=self.headers)
        )

    def delete(self, url, **kwargs):
        return self.deal_resp(requests.delete(
            url=url,
            headers=self.headers)
        )

    def deal_resp(self, resp):
        data = None
        if resp.content:
            try:
                data = resp.json()
            except:
                data = resp.content.decode()
        link = resp.headers.get('Link', None)
        r = HttpJsonResponse(data, status=resp.status_code)
        if link:
            r['Link'] = link
        return r


class HTRequest(Request):

    def __init__(self):
        Request.__init__(self)
        self.headers = {
            'X-CLIENT-ID': settings.HT_PASSPORT_CLIENT_ID,
            'X-CLIENT-MD5': md5_hex_digest(
                '%s%s' % (
                    settings.HT_PASSPORT_CLIENT_ID,
                    settings.HT_PASSPORT_CLIENT_SECRET)
            )
        }


class UURequest(Request):

    def __init__(self):
        Request.__init__(self)
        self.headers = {
            'X-CLIENT-ID': settings.UU_PASSPORT_CLIENT_ID,
            'X-CLIENT-MD5': md5_hex_digest(
                '%s%s' % (
                    settings.PASSPORT_CLIENT_ID,
                    settings.PASSPORT_CLIENT_SECRET)
            )
        }


new_req = Request()
