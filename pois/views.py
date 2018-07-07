import uuid

from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from oauth2.decorator import json_required
from pois.forms import PoisForms
from pois.models import Poi
from utils.datetime_utils import datetime_to_timestamp
from utils.forms import validate_form
from utils.helper import response_errors, http_response


class PoisView(View):
    @json_required()
    def post(self, request):
        '''创建文章'''
        status, data = validate_form(PoisForms, request.jsondata)
        if not status:
            return response_errors(data)
        data['poi_id'] = uuid.uuid1().hex
        poi = Poi.objects.create(**data)
        return http_response({
            'poi_id': poi.poi_id,
            'create_time': datetime_to_timestamp(poi.create_time)
        }, status=201)
