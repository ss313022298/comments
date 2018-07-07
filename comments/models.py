import uuid

from django.db import models

from pois.models import Poi
from tags.models import Tag


class BaseComment(models.Model):
    '''基础评论'''

    content = models.TextField('评论', max_length=500)
    create_time = models.DateTimeField('评论时间', auto_now_add=True)

    class Meta:
        abstract = True


class PoiComment(BaseComment):
    '''一级评论'''

    comment_id = models.CharField(max_length=32, default=uuid.uuid1().hex, db_index=True, primary_key=True)
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.CASCADE, verbose_name='评论所属标签')
    poi = models.ForeignKey(Poi, null=True, blank=True, on_delete=models.CASCADE, verbose_name='评论所属文章')

    class Meta:
        ordering = ['-create_time']

    def detail_info(self):
        return {
            'comment_id': self.comment_id,
            'content': self.content
        }


class PoiCommentReply(BaseComment):
    '''二级评论 '''
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='回复对象')
    comment = models.ForeignKey(PoiComment, null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                                verbose_name='一级评论')
    poi = models.ForeignKey(Poi, null=True, blank=True, on_delete=models.CASCADE, verbose_name='评论所属文章')

    class Meta:
        ordering = ['create_time']
