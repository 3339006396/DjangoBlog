from .serializers import *
from .models import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

class BlogListView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        blogs = Blog.objects.all().order_by("-pub_time")
        keyword = request.query_params.get("keyword")
        if keyword:
            blogs = blogs.filter(
                Q(title__contains=keyword)|
                Q(content__contains=keyword)|
                Q(category__name__contains=keyword)|
                Q(author__username__contains=keyword)
                )
        page = request.query_params.get("page",1)
        page_size = request.query_params.get("page_size",10)
        start = (int(page)-1)*int(page_size)
        end = start + int(page_size)
        total = blogs.count()
        blogs = blogs[start:end]
        serializer = BlogSerializer(blogs,many=True)
        return Response({
            "code":200,
            "msg":"获取博客列表成功",
            "data":{
                "total":total,
                "page":int(page),
                "page_size":int(page_size),
                "results":serializer.data
            }
        },status=status.HTTP_200_OK)

class MyBlogListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        blogs = Blog.objects.filter(author=user).order_by("-pub_time")
        serializer = BlogSerializer(blogs,many=True)
        return Response({
            "code":200,
            "msg":"获取我的博客列表成功",
            "data":{
                "results":serializer.data
            }
        },status=status.HTTP_200_OK)

class BlogCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = BlogCreateSerializer(
            data=request.data,
            context={"author":request.user}
        )
        if serializer.is_valid():
            blog = serializer.save()
            return Response({
                "code":200,
                "msg":"创建博客成功",
                "data":{
                    "id":blog.id,
                    "title":blog.title
                }
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                "code":400,
                "msg":"创建博客失败",
                "data":{
                    "errors":serializer.errors
                }
            },status=status.HTTP_400_BAD_REQUEST)

class BlogDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,pk):
        try:
            blog = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response({
                "code":404,
                "msg":"博客不存在",
            },status=status.HTTP_404_NOT_FOUND)
        blog_serializer = BlogSerializer(blog)
        comments = Comment.objects.filter(blog=blog).order_by("-create_time")
        comment_serializer = CommentSerializer(comments,many=True)
        return Response({
            "code":200,
            "msg":"获取博客详情成功",
            "data":{
                "blog":blog_serializer.data,
                "comments":comment_serializer.data
            }
        },status=status.HTTP_200_OK)

class BlogDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk):
        try:
            blog = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response({
                "code":404,
                "msg":"博客不存在",
            },status=status.HTTP_404_NOT_FOUND)
        if blog.author != request.user and not request.user.is_superuser:
            return Response({
                "code":403,
                "msg":"您没有权限删除该博客",
            },status=status.HTTP_403_FORBIDDEN)
        blog.delete()
        return Response({
            "code":200,
            "msg":"删除博客成功",
        },status=status.HTTP_200_OK)

class CommentCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        try:
            blog = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response({
                "code":404,
                "msg":"博客不存在",
            },status=status.HTTP_404_NOT_FOUND)
        user = request.user
        serializer = CommentCreateSerializer(
            data=request.data,
            context={"author":user,"blog":blog}
        )
        if serializer.is_valid():
            comment = serializer.save()
            return Response({
                "code":200,
                "msg":"创建评论成功",
                "data":{
                    "id":comment.id,
                    "comment":comment.comment,
                    "username":comment.author.username,
                    "avatar":comment.author.avatar.url
                },
                "status":status.HTTP_200_OK
            })
        return Response({
            "code":400,
            "msg":"评论失败",
            "data":{
                "errors":serializer.errors
            }
        },status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response({
            "code":200,
            "msg":"获取分类列表成功",
            "data":{
                "results":serializer.data
            }
        },status=status.HTTP_200_OK)