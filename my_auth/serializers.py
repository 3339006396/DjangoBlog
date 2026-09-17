from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(min_length=2,max_length=14)
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,min_length=6,max_length=16)
    confirm_password=serializers.CharField(write_only=True)
    captcha=serializers.CharField(max_length=6)

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已存在")
        return value

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate(self,attrs):
        if attrs.get('password')!= attrs.get('confirm_password'):
            raise serializers.ValidationError("两次密码不一致")
        captcha = attrs.get('captcha')
        email=attrs.get('email')
        right_captcha=cache.get(f"captcha:{email}")
        if captcha!=right_captcha:
            raise serializers.ValidationError("验证码错误")
        return attrs

    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(min_length=2,max_length=14)
    password=serializers.CharField(write_only=True,min_length=6,max_length=16)

    def validate(self,attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户名或密码错误")
        if not user.is_active:
            raise serializers.ValidationError("用户已被禁用，请联系管理员")
        if not user.check_password(password):
            raise serializers.ValidationError("用户名或密码错误")
        return attrs

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    is_superuser = serializers.BooleanField()
    date_joined = serializers.DateTimeField()
    avatar = serializers.CharField(source="avatar.url")

class UpdateUserSerializer(serializers.Serializer):
    username=serializers.CharField(min_length=2,max_length=14,required=False)
    email=serializers.EmailField(required=False)
    avatar=serializers.ImageField(required=False)

    def validate_email(self,value):
        if self.instance and User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("邮箱已存在")
        return value

    def validate_username(self,value):
        if self.instance and User.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("用户名已存在")
        return value