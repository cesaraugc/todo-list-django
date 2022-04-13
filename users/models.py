from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField('unique login', max_length=255, unique=True)
    name = models.CharField('name of the user', max_length=255)
    email = models.EmailField('email address')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.login
