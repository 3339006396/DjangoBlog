from rest_framework import serializers
from blog.models import *

#展示博客详情
class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField(source="category.id")
    category_name = serializers.CharField(source="category.name")
    content = serializers.CharField()
    pub_time = serializers.DateTimeField()
    author = serializers.CharField(source="author.id")
    author_username = serializers.CharField(source="author.username")
    author_avatar = serializers.CharField(source="author.avatar.url")
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

#发博博客序列
class BlogCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    category = serializers.IntegerField()
    content = serializers.CharField()

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("标题长度不能小于2")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("内容不能为空")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("分类不存在")
        return value

    def create(self, validated_data):
        author = self.context.get("author")
        return Blog.objects.create(
            title=validated_data["title"],
            category_id=validated_data["category"],
            content=validated_data["content"],
            author=author,
        )

class BlogUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20,required=False)
    category = serializers.IntegerField(required=False)
    content = serializers.CharField(required=False)

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("标题长度不能小于2")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("内容不能为空")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("分类不存在")
        return value

    def update(self, instance, validated_data):
        if validated_data.get("title"):
            instance.title = validated_data["title"]
        if validated_data.get("category"):
            instance.category_id = validated_data["category"]
        if validated_data.get("content"):
            instance.content = validated_data["content"]
        instance.save()
        return instance

#分类展示
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=10)

#添加分类
class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("分类名称已存在")
        if len(value) < 2:
            raise serializers.ValidationError("分类名称长度不能小于2")
        return value

    def create(self, validated_data):
        return Category.objects.create(name=validated_data["name"])

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    blog = serializers.IntegerField(source="blog.id")
    comment = serializers.CharField()
    create_time = serializers.DateTimeField()
    author = serializers.CharField(source="author.id")
    author_username = serializers.CharField(source="author.username")
    author_avatar = serializers.CharField(source="author.avatar.url")

class CommentCreateSerializer(serializers.Serializer):
    comment = serializers.CharField(min_length=1)

    def validate_comment(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("评论内容长度不能小于1")
        return value

    def create(self, validated_data):
        blog = self.context.get("blog")
        author = self.context.get("author")
        return Comment.objects.create(
            blog=blog,
            comment=validated_data["comment"],
            author=author
        )