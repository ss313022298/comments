'''
Created on 2017年6月1日

@author: zhangqingwei
'''
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class MyModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                return None
        elif 'safemobile' in kwargs:
            try:
                user = UserModel.objects.get(safemobile=kwargs['safemobile'])
            except UserModel.DoesNotExist:
                return None
        else:
            return None
        if user.check_password(password):
            return user
