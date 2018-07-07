import uuid

from django.db import models


# Create your models here.
class Poi(models.Model):
    '''文章'''
    poi_id = models.CharField(max_length=32, default=uuid.uuid1().hex, db_index=True, primary_key=True)
    poi_title = models.CharField(max_length=20, default="文章标题为空")
    poi_content = models.CharField(max_length=1000, default="文章内容为空")
    create_time = models.DateTimeField('文章创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
