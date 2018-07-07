import uuid
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.cache import cache
from comments.models import PoiComment, PoiCommentReply
from oauth2.decorator import json_required
from pois.models import Poi
from tags.models import Tag
from utils.datetime_utils import datetime_to_timestamp
from utils.forms import validate_form
from comments.forms import CommentsForms, ReplyForms
from utils.helper import response_errors, http_response
from django.core import serializers


# Create your views here.
class CommentsView(View):
    @json_required()
    def post(self, request, poi_id):
        '''创建文章下评论'''
        status, data = validate_form(CommentsForms, request.jsondata)
        if not status:
            return response_errors(data)
        try:
            Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)

        data['comment_id'] = uuid.uuid1().hex
        data['poi_id'] = poi_id

        tag = Tag.objects.get(tag_name=data['tag'])
        data['tag'] = tag

        comment = PoiComment.objects.create(**data)
        return http_response({
            'comment_id': comment.comment_id,
            'create_time': datetime_to_timestamp(comment.create_time)
        }, status=201)

    def get(self, request, poi_id):
        try:
            poi = Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)
        # 获取文章评论列表
        if not request.GET:
            comments = poi.poicomment_set.all()

            result = [_.detail_info() for _ in comments]
            return http_response(result, status=200)
        # 获取标签筛选文章评论列表
        else:
            tag_id = request.GET.get('tag')
            print(tag_id)
            comments = poi.poicomment_set.all().filter(tag_id=tag_id)
            result = [_.detail_info() for _ in comments]
            return http_response(result, status=200)


class CommentView(View):
    def get(self, request, poi_id, comment_id):
        '''获取单条评论'''
        try:
            Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)
        try:
            comment = PoiComment.objects.get(comment_id=comment_id)
        except PoiComment.DoesNotExist:
            return http_response(status=404)
        result = comment.detail_info()
        return http_response(result, status=200)

    def delete(self, request, poi_id, comment_id):
        '''删除单条评论'''
        try:
            Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)
        try:
            comment = PoiComment.objects.get(comment_id=comment_id)
        except PoiComment.DoesNotExist:
            return http_response(status=404)
        comment.delete()
        return http_response(status=204)


class TagCommentsView(View):
    def get(self, request, poi_id, tag_id):
        '''通过标签筛选文章下的评论列表'''
        try:
            poi = Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)
        try:
            tag = Tag.objects.get(tag_id=tag_id)
        except Tag.DoesNotExist:
            return http_response(status=404)
        key = 'tag_comment_list'
        if key in cache:
            tag_comments = cache.get(key)
            result = [_.detail_info() for _ in tag_comments]
            return http_response({"comments": result}, status=200)

        else:
            tag_comments = poi.poicomment_set.all().filter(tag=tag)
            cache.set(key, tag_comments, 1 * 60)
            result = [_.detail_info() for _ in tag_comments]
            return http_response({"comments": result}, status=200)


class CommentReply(View):
    @json_required()
    def post(self, request, poi_id, comment_id):
        '''评论回复'''
        status, data = validate_form(ReplyForms, request.jsondata)
        if not status:
            return response_errors(data)

        try:
            poi = Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)

        try:
            comment = PoiComment.objects.get(comment_id=comment_id)
        except PoiComment.DoesNotExist:
            return http_response(status=404)

        data['comment_id'] = comment.comment_id
        data['poi_id'] = poi.poi_id
        reply = PoiCommentReply.objects.create(**data)

        return http_response({
            'reply_id': reply.id,
            'connect': reply.content,
            'create_time': datetime_to_timestamp(comment.create_time)
        }, status=201)


class CommentReplySub(View):
    '''回复评论的回复'''

    @json_required()
    def post(self, request, poi_id, comment_id, reply_id):

        status, data = validate_form(ReplyForms, request.jsondata)
        if not status:
            return response_errors(data)

        try:
            poi = Poi.objects.get(poi_id=poi_id)
        except Poi.DoesNotExist:
            return http_response(status=404)

        try:
            comment = PoiComment.objects.get(comment_id=comment_id)
        except PoiComment.DoesNotExist:
            return http_response(status=404)

        try:
            reply = PoiCommentReply.objects.get(id=reply_id)
        except PoiComment.DoesNotExist:
            return http_response(status=404)

        data['poi_id'] = poi.poi_id
        data['comment_id'] = comment.comment_id
        data['reply_id'] = reply.id

        reply = PoiCommentReply.objects.create(**data)
        return http_response({
            'connect': reply.content,
            'reply_sub_id': reply.id,
            'create_time': datetime_to_timestamp(reply.create_time)
        }, status=201)
