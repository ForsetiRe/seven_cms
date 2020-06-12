from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, email=None, **kwargs):
        if not telephone:
            raise ValueError('请传入手机号码')
        if not username:
            raise ValueError('请传入用户名')
        if not password:
            raise ValueError('请传入密码')
        user = self.model(telephone=telephone, username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, telephone, username, password, email=None, **kwargs):
        kwargs['is_staff'] = False
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, email, **kwargs)

    def create_superuser(self, telephone, username, password, email=None, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, email, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 主键不使用自增的
    # 使用shortuuid作为主键
    # pip install django-shortuuidfield
    uuid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_join = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_black_user(self):
        return self.objects.filter(is_active=False)
