from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    # _create_user : 클래스 내에서만 사용
    def _create_user(self, email, username, password, **extra_fields):
        # 원래 email 대신 username 으로 되어있음.
        if not email:
            raise ValueError('Email must be set.')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create_user : 클래스 밖에서도 사용
    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email',
                              max_length=100, unique=True)
    username = models.CharField(max_length=30)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 필수로 받고 싶은 필드 넣기.

    def __str__(self):
        return "<%d %s>" % (self.pk, self.email)
