# encoding:utf-8
"""
Created on 18-2-6

@author: zhangqingwei
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from account.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        with transaction.atomic():
            get_user_model().objects.create_user(
                username='12345678',
                password='12345678',
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS('ok'))
