import uuid

from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from oauth2.decorator import json_required
from tags.forms import TagsForms
from tags.models import Tag
from utils.datetime_utils import datetime_to_timestamp
from utils.forms import validate_form
from utils.helper import response_errors, http_response
from django.core.cache import cache


class TagView(View):
    @json_required()
    def post(self, request):
        '''创建标签'''
        status, data = validate_form(TagsForms, request.jsondata)
        if not status:
            return response_errors(data)
        data['tag_id'] = uuid.uuid1().hex
        tag = Tag.objects.create(**data)
        return http_response({
            'tag_id': tag.tag_id,
            'tag_name':tag.tag_name,
            'create_time': datetime_to_timestamp(tag.create_time)
        }, status=201)


    def get(self, request):
        '''获取标签列表'''

        key = 'tag_list'
        if key in cache:
            tags = cache.get(key)
            result = [_.detail_info() for _ in tags]
            return http_response(result, status=200)
        else:
            tags = Tag.objects.all()

            cache.set(key, tags, 1 * 60)
            result = [_.detail_info() for _ in tags]
            return http_response(result, status=200)
