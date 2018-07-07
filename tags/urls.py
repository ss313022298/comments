from django.conf.urls import url

from pois.views import PoisView
from tags.views import TagView

urlpatterns = [
    # 创建标签
    url(r'^pois/comments/tags$', TagView.as_view()),
]
