from django import forms
from django.core import validators
from apps.forms import FormMixin


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3-8]\d{9}', message='请输入正确的手机号')])
    password = forms.CharField(max_length=30, min_length=6, error_messages={"max_length": "密码最多不能超过30个字符", "min_length": '最短不能少于6个字符'})
    remember = forms.IntegerField(required=False)

