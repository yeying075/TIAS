import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from zjj.code.mysqlTranslate import Tran
from zjj.code.mysqlUsers import User
from zjj.code.cat import getunionid

tr = Tran()
us = User()


def get(request):  # request为接受到的信息
    if request.method == 'GET':  # 检查请求方式
        sou = request.GET.get('sou')
        tar = request.GET.get('tar')
        word = request.GET.get('word')
        re = tr.tra(sou, tar, word)  # 调用函数，操作数据库
        return JsonResponse({'code': 100200, 'data': [re]})  # 返回信息
    else:
        return JsonResponse({'code': 100101})  # 100101为错误代码


@csrf_exempt
def post(request):  # request为接受到的信息
    if request.method == 'POST':  # 检查请求方式
        data = json.loads(request.body.decode('utf-8'))  # 解码
        tar = data.get('tar')
        word1 = data.get('word1')
        word2 = data.get('word2')
        re = tr.ins(tar, word1, word2)  # 调用函数，操作数据库
        return JsonResponse({'code': 100200, 'data': [re]})  # 返回信息
    else:
        return JsonResponse({'code': 100101})  # 100101为错误代码


@csrf_exempt
def login(request):  # request为接受到的信息
    if request.method == 'POST':  # 检查请求方式
        data = json.loads(request.body.decode('utf-8'))  # 解码
        code = data.get('code')
        openid = getunionid(code)  # 调用函数，通过微信官方接口获取用户唯一标识。
        times = us.change(openid)  # 调用函数，操作数据库
        return JsonResponse({'code': 100200, 'data': [times]})  # 返回用户的登录次数
    else:
        return JsonResponse({'code': 100101})  # 100101为错误代码

# 192.168.124.222 192.168.3.198
# http://127.0.0.1:8000/zjj/post/
# python manage.py runserver 0.0.0.0:8000
