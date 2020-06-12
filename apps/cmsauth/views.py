from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from utils import restful
from .models import User
from django.contrib.auth import login


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
        print(telephone, username, password)
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)  # 注册成功之后直接登录
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())
