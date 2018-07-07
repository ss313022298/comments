# poi_comments

## 用户登录

#### 请求地址

```
POST /login
```

#### 请求参数

Name       |Type      |NN |Comments
-----------|----------|---|----------
username   |string    |T  |用户名
password   |string	  |T  |密码

#### 响应

##### 200： 成功

##### 422： 返回错误实体

```
status: 200 OK
{
    "username": "12345678"
}
status: 422 Unprocessable Entity
{
    "errors": [
        {
            "code": "invalid",
            "field": "username"/"field": "password"
        }
    ],
    "message": "Validation Failed"
```

## 用户退出

#### 请求地址

```
POST /logout
```

#### 响应

##### 204： 退出成功

```
status: 204 No Content
```

## 创建文章

#### 请求地址

```
GET /pois
```

#### 请求参数

Name       |Type      |NN |Comments
-----------|----------|---|----------
poi_title  |string    |T  |文章标题
poi_content|string    |T  |文章内容

#### 响应

##### 201： 已创建

##### 403： 未授权

##### 422： 返回错误实体

```
status: 201 CREATE
{
    "poi_id": "1f98f7067f3111e8be3f309c23a2312b",
    "create_time": 1530670959.508391
}

status: 403 Forbidden

status: 422 Unprocessable Entity
{
    "message": "Validation Failed",
    "errors": [
        {
            "code": "missing_field",
            "field": "poi_title"
        },
        {
            "code": "missing_field",
            "field": "poi_content"
        }
    ]
}

```

## 创建评论标签

#### 请求地址

```
POST /pois/comments/tags
```

#### 请求参数

Name       |Type      |NN |Comments
-----------|----------|---|----------
tag_name   |string	  |T  |标签名称

#### 响应

##### 201: 创建成功

##### 403: 未授权

##### 422: 返回错误实体

```
status： 201 CREATE
{
    "tag_name": "xxxxx",
    "create_time": 1530686534.031511,
    "tag_id": "62bc8aa67f5511e8be3f309c23a2312b"
}

Status: 403 Forbidden

status: 422 Unprocessable Entity
{
    message: '',
    errors: [
    ]
}
```

## 获取评论标签列表

#### 请求地址

```
GET /pois/comments/tags
```

#### 响应

##### 200： OK

```
status: 200 OK
[
    {
        "tag_id": "65d2bbf27f5a11e8be3f309c23a2312b",
        "tag_name": "xxxx"
    },
    {
        "tag_id": "f79c94c47f5d11e8be3f309c23a2312b",
        "tag_name": "xxxx"
    }
]

```

## 创建文章评论

#### 请求地址

```
POST /pois/:poi_id/comments
```

#### 请求参数

Name      |Type      |NN |Comments
----------|----------|---|----------
content   |string    |T  |评论内容
tag       |string    |T  |评论标签

#### 响应

##### 201： 已创建

##### 403： 未授权

##### 404： 未找到

```
status: 201 Created
{
    "comment_id": "be3f91587f3611e8be3f309c23a2312b",
    "create_time": 1530673373.160115
}

status: 403 Forbidden

status: 404 Not Found
```

## 获取文章评论列表

#### 请求地址

```
GET /pois/:poi_id/comments
```

#### 响应

##### 200： OK

##### 404： 未找到

```
status: 200 OK
[
    {
        "content": "xxxxx",
        "comment_id": "be3f91587f3611e8be3f309c23a2312b",
        "tag": "xxx"
    },
    {
        "content": "xxxxx",
        "comment_id": "58a39afc7f3511e8be3f309c23a2312b",
        "tag": "xxx"
    },
    {
        "content": "xxxxx",
        "comment_id": "700b06547f3411e8be3f309c23a2312b",
        "tag": "xxx"
    }
]

status: 404 Not Found
```

## 获取标签评论列表

#### 请求地址

```
GET /pois/:poi_id/comments
```

#### 响应

##### 200: OK

##### 404: 未找到

```
status: 404 Not Found

status: 200 OK
{
    "comments": [
        {
            "comment_id": "2e89f3007f5e11e8be3f309c23a2312b",
            "content": "xxxxxx"
        }
}

```


## 获取单个评论

#### 请求地址

```
GET /pois/:poi_id/comments/:comment_id
```

#### 响应

##### 200： OK

##### 404： 未找到

```
status: 200 OK
{
    "content": "xxxxx",
    "tag": "xxxxx",
    "comment_id": "be3f91587f3611e8be3f309c23a2312b"
}

status: 404 Not Found
```


## 删除单个评论

#### 请求地址

```
DELETE /pois/:poi_id/comments/:comment_id
```

#### 响应

##### 204： 删除成功

##### 403： 未授权

##### 404： 未找到

```
Status: 204 No Content

Status: 403 Forbidden

Status: 404 Not Found

```



## 创建评论回复

#### 请求地址

```
POST /pois/:poi_id/comment/:comment_id/replies
```

#### 请求参数

Name       |Type      |NN |Comments
-----------|----------|---|----------
content    |string	  |T  |回复内容

#### 响应

##### 201： 已创建

##### 403： 未授权

##### 422： 返回错误实体

##### 404： 未找到

```
Status: 403 Forbidden

Status: 201 Create
{
    "connect": "xxxxx",
    "create_time": 1530754348.955935,
    "reply_id": 9,
}

Status: 422 Unprocessable Entity
{
    message: '',
    errors: [
    ]
}
status: 404 Not Found
```

## 创建评论回复下的回复

#### 请求地址

```
POST /pois/:poi_id/comment/:comment_id/replies/:reply_id/subreplies
```

#### 请求参数

Name       |Type      |NN |Comments
-----------|----------|---|----------
content    |string	  |T  |回复内容

#### 响应

##### 201： 已创建

##### 403： 未授权

##### 422： 返回错误实体

##### 404： 未找到

```
Status: 201 Create
{
    "create_time": 1530756311.947071,
    "connect": "xxxx",
    "reply_sub_id": 8,
}

Status: 422 Unprocessable Entity
{
    message: '',
    errors: [
    ]
}

Status: 403 Forbidden

status: 404 Not Found
```