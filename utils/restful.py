# restful 接口的风格
# http 或者 https

# 返回值 json
# 不使用 xml

# url链接中只能有名词，不能出现动词
# 比如获取文章列表
# http://api.qfedu.com/articles  名词
# http://api.qfedu.com/get_article  动词

# 请求方法  增删改查
# GET  相当于查数据，从服务器获取资源
# POST  创建一个资源
# PUT  更新资源，字段需要全部重新提交
# PATCH  更新资源，仅提交需要修改的字段
# DELETE  删除数据，从服务器删除资源

# GET  /users/  获取所有用户
# GET /user/<id>  根据id获取指定的用户
# POST  /user/  添加用户
# PUT  /user/<id>  更新某个id用户的信息，需要所有信息
# PATCH  /user/<id>  更新某个id用户的信息，仅需需修改的信息
# DELETE /user/<id>  删除某个id用户的信息

# 状态码
# 200 OK
# 301 永久重定向
# 302 临时重定向
# 4开头的是客户端问题
# 400 参数错误
# 401 用户没有权限
# 403 因为某些原因禁止访问
# 404 发送请求的url不存在
# 405 请求方法不被允许
# 5开头的是服务器问题
# 500 代码问题(语法)
# 502 上线时常遇，某些服务没有启动

"""
{"code": 400, "message": "", "data": ""}
"""
from django.http import JsonResponse


# 定义状态码，根据不同的状态码返回不同的数据
class HttpCode(object):
    success = 200
    params_error = 400
    unauth = 401
    method_error = 405
    server_error = 500


# 根据不同的状态码，返回不同的内容
def result(code=HttpCode.success, message='', data=None, kwargs=None):
    json_dict = {'code': code, 'message': message, 'data': data}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def success():
    return result()


def params_error(message='', data=None):  # 这个message为空是为了在不同的视图函数中手动返回内容
    return result(code=HttpCode.params_error, message=message, data=data)


def unauth(message='', data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_error(message='', data=None):
    return result(code=HttpCode.method_error, message=message, data=data)


def server_error(message='', data=None):
    return result(code=HttpCode.server_error, message=message, data=data)
