from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractUser):
    """Requires email and password, username can be blank"""

    # username = None
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        max_length=50, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.username:
            return self.username

        return self.email

    def un(self):
        if self.username:
            return self.username
        else:
            return self.email.split('@')[0]
