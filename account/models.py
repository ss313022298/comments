from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.datetime_utils import datetime_to_timestamp


# Create your models here.


class User(AbstractUser):
    '''用户信息'''

    created_time = models.DateTimeField(auto_now_add=True)

    updated_time = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'account_user'