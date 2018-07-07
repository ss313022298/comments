import uuid

from django.db import models


# Create your models here.
class Tag(models.Model):
    tag_id = models.CharField(max_length=32, default=uuid.uuid1().hex, db_index=True, primary_key=True)
    tag_name = models.CharField(max_length=100)
    create_time = models.DateTimeField('标签创建时间', auto_now_add=True)

    def detail_info(self):
        return {
            'tag_id': self.tag_id,
            'tag_name': self.tag_name
        }
