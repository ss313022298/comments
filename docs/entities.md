# poi_comments

## 文章

Name        |Type       |NN |Comments
------------|-----------|---|----------
poi_id      |string     |T  |文章id
poi_title   |string     |T  |文章标题
poi_content |string     |T  |文章内容
create_time |datetime   |T  |创建时间

## 标签

Name        |Type       |NN |Comments
------------|-----------|---|----------
tag_id      |string     |T  |标签id
tag_name    |string     |T  |标签名称
create_time |datetime   |T  |创建时间

## 评论

Name        |Type       |NN |Comments
------------|-----------|---|----------
poi_id      |int        |T  |文章id
comment_id  |string     |T  |文章评论id
user        |string     |T  |评论文章的用户
content     |string     |T  |评论文章的内容
tag         |string     |T  |评论的标签
create_time |datetime   |T  |创建时间


## 评论回复/评论回复的回复

Name        |Type       |NN |Comments
------------|-----------|---|----------
id          |int        |T  |评论回复id
reply_id    |int        |   |评论回复的回复id
poi         |string     |T  |回复所属文章
content     |string     |T  |回复内容
comment_id  |string     |T  |回复所属评论
create_time |datetime   |T  |创建时间


