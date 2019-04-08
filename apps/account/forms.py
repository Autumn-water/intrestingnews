from django import forms
from apps.forms import FormMixin
from utils import mcache


# 表单验证
class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={"min_length": "手机号长度有误", "max_length": "手机号长度有误",
                                                "required": "手机号不能为空"})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度有误", "max_length": "密码长度有误", "required": "密码不能为空"})
    remember = forms.BooleanField(required=False)


# 提前写好了  FormMixin get_error 获取表单里面验证错误
class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={"min_length": "手机号长度有误", "max_length": "手机号长度有误",
                                                "required": "手机号不能为空"})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度有误", "max_length": "密码长度有误", "required": "密码不能为空"})
    sms_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={"required": "短信验证码不能为空", "min_length": "短信验证码长度错误",
                                                  "max_length": "短信验证码长度错误"})
    password_repeat = forms.CharField(max_length=20, min_length=6,
                                      error_messages={"min_length": "密码长度有误", "max_length": "密码长度有误",
                                                      "required": "确认密码不能为空"})
    username = forms.CharField(max_length=50, min_length=2,
                               error_messages={"required": "用户名不能为空", "max_length": "用户名最大长度不能超过50",
                                               "min_length": "用户长度过低"})

    graph_captcha = forms.CharField(max_length=4, min_length=4,
                                    error_messages={"required": "图形验证码不能为空", "min_length": "短信验证码长度错误",
                                                    "max_length": "图形验证码长度错误"})

    # 自定义方法 验证密码一致 验证码 None
    def check_data(self):
        # 密码是否一致  self  form = xxxForm()  form
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            # add_error  表单属性  报错提示
            return self.add_error('password', '两次密码不一致')

        # 判断手机验证码和图形验证  安装 memcached
        sms_captcha = self.cleaned_data.get('sms_captcha')
        # 缓存里面 没有从缓存里获取到值
        sms_captcha_cache = mcache.get_key(sms_captcha)
        print('============')
        print(sms_captcha)
        print(sms_captcha_cache)
        print('============')
        if not sms_captcha_cache and sms_captcha != sms_captcha_cache:
            return self.add_error('sms_captcha', '短信验证码验证错误')

        graph_captcha = self.cleaned_data.get('graph_captcha')
        # 缓存里面 没有从缓存里获取到值  不要粘贴复制错了
        graph_captcha_cache = mcache.get_key(graph_captcha)
        print('****************')
        print(graph_captcha)
        print(graph_captcha_cache)
        print('****************')
        if not graph_captcha_cache and graph_captcha != graph_captcha_cache:
            return self.add_error('sms_captcha', '图形验证码验证错误')

        # 没有这一步 验证不能通过
        return True
