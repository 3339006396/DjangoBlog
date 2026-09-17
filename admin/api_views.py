import keyword

from .serializers import *
from .models import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import  BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class AdminStatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def get(self, request):
        return Response({
            "code": 200,
            "message": '网站数据获取成功',
            "data": {
                "blog_count": Blog.objects.count(),
                "user_count": User.objects.count(),
                "comment_count": Comment.objects.count(),
                "category_count": Category.objects.count(),
                "active_user_count": User.objects.filter(is_active=True).count(),
            }
        }, status=status.HTTP_200_OK)

class AdminCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def get(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(id=pk)
            except Category.DoesNotExist:
                return Response({
                    "code": 404,
                    "message": '分类不存在',
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = AdminCategorySerializer(category)
        else:
            categories = Category.objects.all()
            serializer = AdminCategorySerializer(categories, many=True)
        return Response({
            "code": 200,
            "message": '分类数据获取成功',
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdminCategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 201,
                "message": '分类创建成功',
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            "code": 400,
            "message": '分类创建失败',
            "data": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({
                "code": 404,
                "message": '分类不存在',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminCategoryUpdateSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 200,
                "message": '分类更新成功',
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        return Response({
            "code": 400,
            "message": '分类更新失败',
            "data": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({
                "code": 404,
                "message": '分类不存在',
            }, status=status.HTTP_404_NOT_FOUND)
        if category.id==1:
            return Response({
                "code": 400,
                "message": '默认分类不能删除',
            }, status=status.HTTP_400_BAD_REQUEST)
        category.delete()
        return Response({
            "code": 200,
            "message": '分类删除成功',
        }, status=status.HTTP_200_OK)

class AdminBlogView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def get(self, request, pk=None):
        if pk:
            try:
                blog = Blog.objects.get(id=pk)
            except Blog.DoesNotExist:
                return Response({
                    "code": 404,
                    "message": '博客不存在',
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = AdminBlogSerializer(blog)
        else:
            blogs = Blog.objects.all()
            keyword = request.query_params.get('keyword', "")
            if keyword:
                blogs = blogs.filter(
                    Q(title__contains=keyword)|
                    Q(content__contains=keyword)|
                    Q(category__name__contains=keyword)|
                    Q(author__username__contains=keyword)
                )
            blogs = blogs.order_by('-pub_time')
            serializer = AdminBlogSerializer(blogs, many=True)
        return Response({
            "code": 200,
            "message": '博客数据获取成功',
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        try:
            blog = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response({
                "code": 404,
                "message": '博客不存在',
            }, status=status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response({
            "code": 200,
            "message": '博客删除成功',
        }, status=status.HTTP_200_OK)

class AdminCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def get(self, request, pk=None):
        if pk:
            try:
                comment = Comment.objects.get(id=pk)
            except Comment.DoesNotExist:
                return Response({
                    "code": 404,
                    "message": '评论不存在',
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = AdminCommentSerializer(comment)
        else:
            comments = Comment.objects.all()
            keyword = request.query_params.get('keyword', "")
            if keyword:
                comments = comments.filter(
                    Q(content__contains=keyword)|
                    Q(author__username__contains=keyword)
                )
            comments = comments.order_by('-create_time')
            serializer = AdminCommentSerializer(comments, many=True)

        return Response({
            "code": 200,
            "message": '评论数据获取成功',
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({
                "code": 404,
                "message": '评论不存在',
            }, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({
            "code": 200,
            "message": '评论删除成功',
        }, status=status.HTTP_200_OK)

class AdminUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def get(self,request,pk=None):
        if pk:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({
                    "code": 404,
                    "message": '用户不存在',
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = AdminUserSerializer(user)
        else:
            users = User.objects.all()
            keyword = request.query_params.get('keyword', "")
            if keyword:
                users = users.filter(
                    Q(username__contains=keyword)|
                    Q(email__contains=keyword)
                    )
                users = users.order_by('-date_joined')
            serializer = AdminUserSerializer(users, many=True)
        return Response({
            "code": 200,
            "message": '用户数据获取成功',
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def put(self,request,pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({
                "code": 404,
                "message": '用户不存在',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 200,
                "message": '用户数据更新成功',
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 400,
                "message": '用户数据更新失败',
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({
                "code": 404,
                "message": '用户不存在',
            }, status=status.HTTP_404_NOT_FOUND)
        if user == request.user:
            return Response({
                "code": 400,
                "message": '不能删除自己用户',
            }, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({
            "code": 200,
            "message": '用户删除成功',
        }, status=status.HTTP_200_OK)

class AdminActiveView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def post(self,request,pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({
                "code": 404,
                "message": '用户不存在',
            }, status=status.HTTP_404_NOT_FOUND)

        action = request.query_params.get('action', "")
        if action == 'active':
            user.is_active = True
            user.save()
            return Response({
                "code": 200,
                "message": '用户激活成功',
            }, status=status.HTTP_200_OK)
        elif action == 'inactive':
            if user == request.user:
                return Response({
                    "code": 400,
                    "message": '不能禁用自己用户',
                }, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = False
            user.save()
            return Response({
                "code": 200,
                "message": '用户禁用成功',
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 400,
                "message": '操作参数错误',
            }, status=status.HTTP_400_BAD_REQUEST)