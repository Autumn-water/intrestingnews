from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


class UserManager(BaseUserManager):
    # 创建用户
    def _create_user(self, username, telephone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        #
        user = self.model(username=username, telephone=telephone, **extra_fields)
        # 加密  set_password  password=password(明文) authenticated 就不会通过
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone, password, **extra_fields):
        extra_fields["is_superuser"] = False
        extra_fields["is_staff"] = False
        return self._create_user(username, telephone, password, **extra_fields)

    def create_superuser(self, username, telephone, password, **extra_fields):
        extra_fields["is_superuser"] = True
        extra_fields["is_staff"] = True
        print(extra_fields) # {'email': 'tzxw@qq.com', 'is_superuser': True, 'is_staff': True}
        return self._create_user(username, telephone, password, **extra_fields)
# user.objects.create_user(telephone=telephone, username=username, password=password)
#  createsuperuser  makemigrations/migrate


class User(AbstractBaseUser, PermissionsMixin):
    """
        User 拓展
    """
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=50)
    # password = models.CharField(max_length=100)
    # password =  set_password()
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True)
    # null = True null
    is_staff = models.BooleanField(blank=True)

    # 以后发送邮件的时候 指定的字段
    EMAIL_FIELD = 'email'
    # form 通过验证
    # auth ==> authenticate(username=telephone,password=password)
    # authenticate 向数据库 查下 用户名和密码是否一致
    USERNAME_FIELD = 'telephone'
    #  # python manage.py createsuperuser  (email)telephone username password
    # python manage.py createsuperuser  第一个字段  telephone 第二个字段 username 第三个 是密码
    # 第一个是USERNAME_FIELD 指定的字段    最后一个  password
    REQUIRED_FIELDS = ['username', 'email']

    # model objects
    # sxx.objects.filter  xxx.objects.get
    objects = UserManager()


