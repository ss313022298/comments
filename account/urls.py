from django.conf.urls import url

from account.views import LoginView, LogoutView

urlpatterns = [
    # 登录
    url(r'^login$',LoginView.as_view()),
    # 退出
    url(r'^logout$',LogoutView.as_view()),
]
