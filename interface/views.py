import json
import os

import cv2
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Djiango import settings
from interface.code.faceRecognition import file_face
from interface.code.objectRecognition import file_text

# python manage.py runserver 0.0.0.0:8000


@csrf_exempt
def face(request):  # request为接受到的信息
    if request.method == 'POST':  # 检查请求方式
        img = request.FILES['faceImage']
        path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(path, 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        re = file_face(path)
        return JsonResponse({'code': 100200, 'data': [re]})  # 返回信息
    else:
        return JsonResponse({'code': 100101})  # 100101为错误代码


@csrf_exempt
def text(request):  # request为接受到的信息
    if request.method == 'POST':  # 检查请求方式
        img = request.FILES['textImage']
        path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(path, 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        re = file_text(path, 1)
        return JsonResponse({'code': 100200, 'data': [re]})  # 返回信息
    else:
        return JsonResponse({'code': 100101})  # 100101为错误代码


# @csrf_exempt
# def login(request):  # request为接受到的信息
#     if request.method == 'POST':  # 检查请求方式
#         data = json.loads(request.body.decode('utf-8'))  # 解码
#         code = data.get('code')
#         openid = getunionid(code)  # 调用函数，通过微信官方接口获取用户唯一标识。
#         times = us.change(openid)  # 调用函数，操作数据库
#         return JsonResponse({'code': 100200, 'data': [times]})  # 返回用户的登录次数
#     else:
#         return JsonResponse({'code': 100101})  # 100101为错误代码

# 192.168.124.222 192.168.3.198
# http://127.0.0.1:8000/zjj/post/

