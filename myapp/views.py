from fileinput import filename

from Crypto.PublicKey.DSA import generate
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
# from setuptools.sandbox import save_path

from exts.token_create import create_token
from .models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.serializers import ImageField
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserLoginSerializer, UserRegisterSerializer

import os
import requests
from s2i import settings
from exts import token_create
from exts.MyRequest.getimage import send_message_and_receive_image
from exts.xfyun_auth import draw_picture

# Create your views here.
class UserLogin(APIView):
    authentication_classes = []
    
    def post(self, request):
        print("登录请求数据:", request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(username=username)
                print(f"找到用户: {user.username}")
                if user.check_password(password):
                    print("密码验证成功")
                    token = create_token(user)
                    user_serializer = UserSerializer(user)
                    return Response({
                        'msg': '登录成功',
                        'token': token,
                        'user': user_serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    print("密码验证失败")
                    return Response({
                        'msg': '密码错误'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                print(f"用户不存在: {username}")
                return Response({
                    'msg': '用户不存在'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        print("序列化器验证失败:", serializer.errors)
        return Response({
            'msg': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserRegister(APIView):
    authentication_classes = []
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response({
                'msg': '注册成功',
                'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'msg': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class AiDrawPicture(APIView):
    def post(self, request):
        from django.conf import settings
        print("request.headers: ",request.headers)
        content = request.data.get('content')
        print("请求内容:", content)
        if not content:
            return Response({'error': '缺少描述内容'}, status=400)
        # 从settings读取讯飞API配置
        appid = getattr(settings, 'XF_APPID', None)
        apikey = getattr(settings, 'XF_APIKEY', None)
        apisecret = getattr(settings, 'XF_APISECRET', None)
        if not all([appid, apikey, apisecret]):
            return Response({'error': '讯飞API配置缺失'}, status=500)
        try:
            base64_img = draw_picture(content, appid, apikey, apisecret)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        return Response({'img_base64': base64_img})





# class VoiceFileUpload(APIView):
#     def post(self,request, format=None):
#         if 'file' not in request.data:
#             return Response({'error':'No file was uploaded'})
#         print("The Data is: ",request.data)
#         file = request.data['file']
#         filename, file_extension = os.path.splitext(file.name)
#         # if(file_extension.lower() is not ".wav"):
#         #     return Response({'error':'File extension is not supported, you should upload \'.wav\' file'})

#         directory = os.path.join(settings.MEDIA_ROOT, 'voice')
#         if not os.path.exists(directory):
#             os.makedirs(directory)

#         file_path = os.path.join(directory, file.name)
#         with open(file_path, 'wb+') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)

#         asr_model = init_model()
#         print(file_path)
#         return_text = generate_text(asr_model, file_path)
#         print(return_text)

#         #更安全的方式是使用with语句来自动关闭文件
#         host = '127.0.0.1'
#         port = 6006
#         msg = {'msg': return_text}

#         # 发送给服务端生图模型
#         response_return_path = send_message_and_receive_image(host, port, return_text)

#         response = FileResponse(open(response_return_path, 'rb'))
#         response['Content-Type'] = 'image/jpg'  # 或者根据实际图片类型设置 Content-Type
#         response['Content-Disposition'] = f'inline; filename="{os.path.basename(response_return_path)}"'

#         print(response)
#         return response

# # 头像上传
# class AvatarUpload(APIView):
#     def post(self, request):
#         # check if file is uploaded
#         if 'file' not in request.data:
#             return Response({'error':'No avatar was uploaded'})
#         file = request.data['file']

#         # get avatar directory
#         directory = os.path.join(settings.MEDIA_ROOT,'images/avatar')
#         if not os.path.exists(directory):
#             os.mkdir(directory)
#         file_path = os.path.join(directory,file.name)

#         # write avatar file
#         with  open(file_path,'wb') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)

#         # save the db info
#         user_object = User.objects.get(user_id=request.user['user_id'])
#         user_object.avatar = file_path
#         user_object.save()
#         return Response({'msg':'Avatar uploaded successfully'})








