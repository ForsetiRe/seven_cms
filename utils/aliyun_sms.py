#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('LTAI4G7aWBVr6kVen7Asf53f', 'zq3IIV4k34xZpzQZzjMrKYozj8mH0n', 'cn-hangzhou')


def send_sms(phone, code):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "red博客")
    request.add_query_param('TemplateCode', "SMS_193236791")
    request.add_query_param('TemplateParam', "{\"code\": \"%s\"}" % code)

    response = client.do_action(request)
    print(str(response, encoding='utf-8'))
