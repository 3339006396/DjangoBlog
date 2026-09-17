"""
本地私有配置模板。

使用方法：把本文件复制为同目录下的 local_settings.py，然后填入自己的真实配置。
local_settings.py 已被 .gitignore 忽略，不会被提交到仓库。
"""

SECRET_KEY = "把 django-admin startproject 生成的 SECRET_KEY 填在这里"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "Django",
        "USER": "root",
        "PASSWORD": "你的 MySQL 密码",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

# 163 邮箱 SMTP 配置（发送注册验证码用）
EMAIL_HOST_USER = "你的邮箱@163.com"
EMAIL_HOST_PASSWORD = "邮箱 SMTP 授权码"
DEFAULT_FROM_EMAIL = "你的邮箱@163.com"
