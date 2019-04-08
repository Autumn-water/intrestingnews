from django.http import JsonResponse


class Code:
    ok = 2
    params_error = 1
    un_auth_error = 403
    method_error = 405
    server_error = 500
    bad_request = 400


def result(code=Code.ok, message='', data=None, kwargs=None):
    json_dict = {'code': code, 'msg': message, 'data': data}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def params_error(message='', data=None):
    """参数错误"""
    return result(Code.params_error, message=message, data=data)


def un_auth_error(message='', data=None):
    """权限错误"""
    return result(code=Code.un_auth_error, message=message, data=data)


def method_error(message='', data=None):
    """方法错误"""
    return result(code=Code.method_error, message=message, data=data)


def server_error(message='', data=None):
    """服务器内部错误"""
    return result(code=Code.server_error, message=message, data=data)
