from django.db import models
from users.models import User

# Create your models here.
class Active(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    start_time = models.CharField(max_length=100, blank=False, default="")
    end_time = models.CharField(max_length=100, blank=False, default="")


class ActiveDetail(models.Model):
    active = models.ForeignKey(
        Active,
        on_delete=models.CASCADE
    )
    active_type = models.IntegerField(null=False)
    startTime = models.CharField(max_length=100, blank=False, default="")
    endTime = models.CharField(max_length=100, blank=False, default="")