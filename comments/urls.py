from django.conf.urls import url

from comments.views import CommentsView, CommentView,CommentReply, CommentReplySub

urlpatterns = [
    # 创建文章下评论/获取文章评论列表/获取标签筛选评论列表
    url(r'^pois/(?P<poi_id>\w+)/comments$', CommentsView.as_view()),
    # 获取/删除单条评论
    url(r'^pois/(?P<poi_id>\w+)/comments/(?P<comment_id>\w+)$', CommentView.as_view()),
    # 评论回复
    url(r'^pois/(?P<poi_id>\w+)/comment/(?P<comment_id>\w+)/replies$', CommentReply.as_view()),
    # 回复的回复
    url(r'^pois/(?P<poi_id>\w+)/comment/(?P<comment_id>\w+)/replies/(?P<reply_id>\w+)/subreplies$',CommentReplySub.as_view())
]
