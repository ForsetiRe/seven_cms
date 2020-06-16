from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from utils import restful
from .models import User
from django.contrib.auth import login, logout
from utils.captcha import Captcha
from io import BytesIO
from django.core.cache import cache
from utils.aliyun_sms import send_sms


# Create your views here.
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                    return restful.success()
            else:
                return restful.unauth(message='您的账号被冻结了')
        else:
            return restful.params_error(message='手机号或者密码错误')
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


# 注册视图
@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        image_captcha = form.cleaned_data.get('image_captcha')
        print(telephone, username, password, image_captcha)
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)  # 注册成功之后直接登录
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def image_captcha(request):
    text, image = Captcha.gene_graph_captcha()
    # 图片是一个流数据，也就是存到一个管道中，不像字符串可以用容器来保存
    out = BytesIO()  # 创建一个管道
    image.save(out, 'png')  # 保存图片的流数据
    # 读取的时候从0开始，为了防止读不到数据，指针一定要回0
    out.seek(0)  # 指针回0
    # 把图片返回到浏览器上，通过response对象返回
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(), text.lower(), 5*60)
    return response


def sms_captcha(request):
    code = Captcha.gene_text(4)  # 生成随机字符串
    print("短信验证码：%s" % code)
    # 接收手机号
    # /sms_captcha/?telephone=xxxxxxxxxxxx
    telephone = request.GET.get('telephone')

    # 调用第三方发送短信验证码的接口
    send_sms(telephone, code)
    return restful.success()
