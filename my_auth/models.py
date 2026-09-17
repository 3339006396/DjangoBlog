from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=6)


class MyUserManager(BaseUserManager):
    """自定义用户管理器"""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名不能为空')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)    # 加密密码
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    完全自定义的用户模型
    - AbstractBaseUser 提供: password, last_login
    - PermissionsMixin 提供: is_superuser, groups, user_permissions
    """
    username = models.CharField(max_length=14, unique=True, verbose_name='用户名')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    avatar = models.ImageField(upload_to='avatar', blank=True, verbose_name='头像',default='avatar/default_avatar.jpg')
    is_staff = models.BooleanField(default=False, verbose_name='是否管理员')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_superuser = models.BooleanField(default=False, verbose_name='是否超级用户')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    USERNAME_FIELD = 'username'     # 登录凭证字段
    REQUIRED_FIELDS = ['email']     # createsuperuser 时必须填写的字段

    objects = MyUserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'