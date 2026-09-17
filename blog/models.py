from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=10)

class Blog(models.Model):
    title=models.CharField(max_length=20)
    category=models.ForeignKey(Category,on_delete=models.SET_DEFAULT,default=1)
    content=models.TextField()
    pub_time=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment=models.TextField()
    create_time=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)