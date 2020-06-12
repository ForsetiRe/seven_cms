from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from utils import restful


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
def register_view(request):
    pass
