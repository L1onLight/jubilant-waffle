import datetime

from django.db import models
from django.utils import timezone

from user.models import CustomUser


class PasswordRestore(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, unique=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, unique=True)
    restoreCode = models.IntegerField()
    created_or_changed = models.DateTimeField(auto_now=True)

    def is_valid(self, code):
        return self.created_or_changed < (timezone.now() + datetime.timedelta(minutes=10)) and self.restoreCode == code
