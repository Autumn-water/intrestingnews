from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .forms import LoginForm, RegisterForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from utils.captcha.captcha import Captcha
from io import BytesIO
from utils import mcache
from utils.alisms.sms_send import send_sms
from .models import User
from utils import json_status



# 不验证 CSRF csrf_exempt
# 验证 CSRF csrf_protect  context 用在 render 模板渲染
# 403 forbidden
# @method_decorator([csrf_exempt, ], name='dispatch')
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/login.html')

    def post(self, request, *args, **kwargs):
        # telephone = request.POST.get("telphone")
        form = LoginForm(request.POST)
        # form.cleaned_data.get("telephone", None)  获取不动
        # 如果验证通过 继续
        if form.is_valid():
            # cleaned_data 必须是通过 is_valid 验证后才能获取
            telephone = form.cleaned_data.get("telephone", None)
            password = form.cleaned_data.get('password', None)
            remember = form.cleaned_data.get("remember", None)
            # print(telephone, password)
            # alt + enter 判断用户是否存
            user = authenticate(username=telephone, password=password)
            # session 有效期是 浏览器 关闭的时候session
            if user:
                # 只有form登录才有效果
                # next_url = request.GET.get("next")
                # if next_url:
                #     return redirect(next_url)
                # 直接登录
                login(request, user)
                print('=================')
                print(remember)
                if remember:
                    # 默认值 默认值就是 2周 14天  单位应该是 秒
                    request.session.set_expiry(None)
                else:
                    # 0 表示默认值 当你浏览器关了  就session
                    request.session.set_expiry(0)
                print('=================')
                return json_status.result(message="登录成功")
                # return JsonResponse({"code": 2, "msg": "登录成功"})
            # return JsonResponse({"code": 1, "msg": "用户名或密码错误"})
            return json_status.params_error(message="用户名或密码错误")
        # return HttpResponse(json.dumps({"code": 1, "msg": "xsxx错误"}))
        # return  HttpResponse("xx") 就是一个对象 res["msg"]
        return json_status.params_error(message=form.get_error())
        # return JsonResponse({"code": 1, "msg": form.get_error()})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/register.html')

    def post(self, request, *args, **kwargs):
        # form.get_error()
        form = RegisterForm(request.POST)
        # True and None
        if form.is_valid() and form.check_data():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # print('^^^^^^^^^^^^^^^^^')
            # print(telephone)
            # print(username)
            # print(password)
            # print('^^^^^^^^^^^^^^^^^')
            # User对象 或 手机号
            user = User.objects.create_user(telephone=telephone, username=username, password=password)
            login(request, user)
            # return JsonResponse({"code": 2, "msg": "注册成功"})
            return json_status.result(message="注册成功")
        # return JsonResponse({"code": 1, "msg": form.get_error()})
        return json_status.params_error(message=form.get_error())

# 写视图函数 ==> urls
def logout_view(request):
    logout(request)
    # 退出登录之后 会跳转到登录页面 return JsonResponse({"code": 1, "msg": form.get_error()})
    # return JsonResponse({"code": 1, "msg": 'ss'})
    # 只要用了 redirect reverse 和 ajax 没关系  form层面
    return redirect(reverse("account:login"))


# JsonResponse / HttpResponse  BytesIo 是存放字节流
def graph_captcha(request):
    # 获取验证码
    text, img = Captcha.gene_code()
    # BytesIO 二进制
    out = BytesIO()
    # 塞管道 保存文件 保存完成之后 位置在后面 10010100101111
    img.save(out, 'png')
    # 回到最开始位置 游标  11111
    out.seek(0)

    # 返回一个 response JsonResponse(content_type) response
    resp = HttpResponse(content_type="image/png")
    # 前面已经塞进去  读出来
    resp.write(out.read())
    # 验证码存缓存  从前端获取值 和后台比较 如果一致 表示
    mcache.set_key(text.lower(), text.lower())
    return resp


# /account/sms/captcha/?telephone=177****5149
def sms_captcha(request):
    # 1. 获取手机号
    telephone = request.GET.get('telephone')
    # print(telephone)
    # 2. 生成验证码 随机四位验证码
    captcha = Captcha.gene_text()
    # 3. 发送短信  确保短信跑通了一次之后  并不会真正发送
    # ret = send_sms(telephone, captcha)
    # print(ret) b'{"Message":"OK","RequestId":"84DB9F38-C231-4635-8A90-BCF4BFD2AE1F","BizId":"170515639348811432^0","Code":"OK"}'
    # "{\"Message\":"OK"}"  u'在'
    # 验证码加缓存  单用户注册没有任何问题   set 最后一个为准  这种几率很小 很小 不区分大小写 在缓存里面 存的是小写
    # sTsw ==  stsw   sTsw/StSW/stsw  前端获取的时候  也小写
    mcache.set_key(captcha.lower(), captcha.lower())
    # 返回什么类型  对象/字符串
    print('手机号 {} 验证码{}'.format(telephone, captcha))
    # return JsonResponse(str(ret, encoding='utf-8'), safe=False)
    return JsonResponse({"code": 2})
