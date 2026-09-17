from django.urls import path
from . import api_views

app_name = "admin"

# 传统视图路由（保留兼容）
# DRF API 路由
urlpatterns = [
    path('stats/', api_views.AdminStatsView.as_view(), name='admin_stats'),
    path('categories/', api_views.AdminCategoryView.as_view(), name='admin_category_list'),
    path('categories/<int:pk>/', api_views.AdminCategoryView.as_view(), name='admin_category_detail'),
    # 博客管理
    path('blogs/', api_views.AdminBlogView.as_view(), name='admin_blog_list'),
    path('blogs/<int:pk>/', api_views.AdminBlogView.as_view(), name='admin_blog_detail'),
    path('comments/', api_views.AdminCommentView.as_view(), name='admin_comment_list'),
    path('comments/<int:pk>/', api_views.AdminCommentView.as_view(), name='admin_comment_detail'),
    path('users/', api_views.AdminUserView.as_view(), name='admin_user_list'),
    path('users/<int:pk>/', api_views.AdminUserView.as_view(), name='admin_user_detail'),
    path('users/<int:pk>/toggle/', api_views.AdminActiveView.as_view(), name='admin_user_toggle'),
]