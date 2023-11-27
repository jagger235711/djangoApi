from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """用户表"""

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    # 临时方式，以后可以存到redis、jwt
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)
