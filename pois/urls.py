from django.conf.urls import url

from pois.views import PoisView

urlpatterns = [
    # 创建文章
    url(r'^pois$', PoisView.as_view()),
]
