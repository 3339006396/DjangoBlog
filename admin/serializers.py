from rest_framework import serializers
from blog.models import *

#展示分类列表
class AdminCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

#添加分类
class AdminCategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)

    def validate_name(self,value):
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError("分类名称长度必须在2到20之间")
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("分类名称已存在")
        return value

    def create(self,validated_data):
        return Category.objects.create(name=validated_data['name'])

class AdminCategoryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)

    def validate_name(self,value):
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError("分类名称长度必须在2到20之间")
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("分类名称已存在")
        return value

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.save()
        return instance

#展示博客列表
class AdminBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    pub_time = serializers.DateTimeField()
    category = serializers.IntegerField(source="category.id")
    category_name = serializers.CharField(source="category.name")
    author = serializers.IntegerField(source="author.id")
    author_username = serializers.CharField(source="author.username")

#展示评论列表
class AdminCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    comment = serializers.CharField()
    create_time = serializers.DateTimeField()
    blog = serializers.IntegerField(source="blog.id")
    blog_title = serializers.CharField(source="blog.title")
    author = serializers.IntegerField(source="author.id")
    author_username = serializers.CharField(source="author.username")
    author_avatar = serializers.CharField(source="author.avatar.url")

class AdminUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()
    avatar = serializers.CharField(source="avatar.url")
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()

class AdminUserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已存在")
        return value

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def update(self,instance,validated_data):
        if validated_data.get('username'):
            instance.username = validated_data.get('username')
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        if validated_data.get('is_staff'):
            instance.is_staff = validated_data.get('is_staff')
        if validated_data.get('is_active'):
            instance.is_active = validated_data.get('is_active')
        instance.save()
        return instance