import random
import string
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "code":200,
                "msg":"注册成功",
                "data":{
                    "username" : user.username,
                    "email"  : user.email
                }
            },status=status.HTTP_201_CREATED)
        return Response({
            "code":400,
            "msg":"注册失败",
            "data":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = User.objects.get(username=username)
            refresh = RefreshToken.for_user(user)

            return Response({
                "code" : 200,
                "msg":"登录成功",
                "data":{
                    "id" : user.id,
                    "username" : user.username,
                    "email"  : user.email,
                    "avatar" : user.avatar.url,
                    "is_superuser" : user.is_superuser
                },
                "tokens":{
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            },status=status.HTTP_200_OK)
        first_error = next(iter(serializer.errors.values()))[0]
        return Response({
            "code":400,
            "msg":first_error,
            "data":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        refresh_token = request.data.get('refresh')
        try:
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                "code":200,
                "msg":"退出成功",
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code":400,
                "msg":"退出失败",
                "data":str(e)
            },status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializers = UserSerializer(request.user)
        return Response({
            "code":200,
            "msg":"获取用户信息成功",
            "data":serializers.data
        },status=status.HTTP_200_OK)

    def put(self,request):
        user = request.user
        serializer = UpdateUserSerializer(instance=user,data=request.data)
        if not serializer.is_valid():
            return Response({
                "code":400,
                "msg":"更新用户信息失败",
                "data":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        validate = serializer.validated_data
        if validate.get('username'):
            user.username = validate.get('username')
        if validate.get('email'):
            user.email = validate.get('email')
        if validate.get('avatar'):
            user.avatar = validate.get('avatar')
        user.save()
        return Response({
            "code":200,
            "msg":"更新用户信息成功",
            "data":{
                "username" : user.username,
                "email"  : user.email,
                "avatar" : user.avatar.url
            }
        },status=status.HTTP_200_OK)

class SendCaptchaView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        email = request.query_params.get('email')
        if not email:
            return Response({
                "code":400,
                "msg":"邮箱不能为空",
            },status=status.HTTP_400_BAD_REQUEST)

        captcha = "".join(random.sample(string.digits, 6))
        cache.set(f"captcha:{email}",captcha,60*5)
        send_mail(
            "验证码",
            f"您的验证码是：{captcha},验证码有效期5分钟",
            None,
            [email],
        )
        return Response({
            "code":200,
            "msg":"验证码发送成功"
        },status=status.HTTP_200_OK)