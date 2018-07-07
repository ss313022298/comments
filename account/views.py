# Create your views here.
import base64
import json

from django.conf import settings
from django.core.mail import send_mail
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseNotFound, HttpResponse

from account.forms import LoginForm

from utils.responses import HttpJsonResponse
from utils.forms import validate_form
from utils.helper import response_errors, http_response

from utils.datetime_utils import datetime_to_timestamp as dtt
from django.contrib import auth
from oauth2.decorator import session_required, json_required
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    @json_required()
    def post(self, request):
        '''登录'''
        flag, data = validate_form(LoginForm, request.jsondata)
        if not flag:
            return HttpJsonResponse({
                'message': 'Validation Failed', 'errors': data
            }, status=422)

        try:
            get_user_model().objects.get(username=data['username'],
                                         is_active=True)
        except get_user_model().DoesNotExist:
            return http_response({
                'message': 'Validation Failed', 'errors': [
                    {"field": "username", "code": "invalid"}]
            }, status=422)

        user = auth.authenticate(
            username=data['username'],
            password=data['password']
        )

        if user:
            auth.login(request, user)
            return HttpJsonResponse({'username': user.username}, status=200)
        else:
            return http_response({
                'message': 'Validation Failed', 'errors': [
                    {"field": "password", "code": "invalid"}]
            }, status=422)



class LogoutView(View):
    def post(self, request):
        '''退出登录'''
        auth.logout(request)
        return HttpJsonResponse(status=204)
