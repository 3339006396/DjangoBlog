from django.urls import path
from . import api_views

app_name='blog'
# DRF API 路由
urlpatterns = [
    path('blogs/', api_views.BlogListView.as_view(), name='blog_list'),
    path('blogs/my/', api_views.MyBlogListView.as_view(), name='my_blog_list'),
    path('blogs/create/', api_views.BlogCreateView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/', api_views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/<int:pk>/delete/', api_views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blogs/<int:pk>/comment/', api_views.CommentCreateView.as_view(), name='comment_create'),
    path('categories/', api_views.CategoryListView.as_view(), name='category_list'),
]
