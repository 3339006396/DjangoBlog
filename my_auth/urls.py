from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import api_views

app_name = 'my_auth'

urlpatterns = [
    # ===== JWT 官方接口 =====
    # 获取 Token（登录时使用）
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新 Token（Access Token 过期时使用）
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证 Token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ===== 自定义业务接口 =====
    # 注册
    path('register/', api_views.RegisterView.as_view(), name='register'),
    # 登录（返回 Token）
    path('login/', api_views.LoginView.as_view(), name='login'),
    # 登出（将 Token 加入黑名单）
    path('logout/', api_views.LogoutView.as_view(), name='logout'),
    # 获取/更新用户信息
    path('user/info/', api_views.UserInfoView.as_view(), name='user_info'),
    # 发送验证码
    path('captcha/', api_views.SendCaptchaView.as_view(), name='send_captcha'),
]