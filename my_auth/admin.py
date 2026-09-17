from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, CaptchaModel
# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ('username','email','is_staff','is_active','date_joined')
    list_filter = ('is_staff','is_active','is_superuser')
    search_fields = ('username','email')
    ordering = ('date_joined',)
    fieldsets = (
        (None,{'fields':('username','password')}),
        ('个人信息',{'fields':('email','avatar')}),
        ('权限信息',{'fields':('is_staff','is_active','is_superuser')}),
        ('注册时间',{'fields':('date_joined',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('username','email','password1','password2','is_staff','is_active'),
        }),
    )

admin.site.register(MyUser,MyUserAdmin)
