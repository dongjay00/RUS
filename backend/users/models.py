from django.db import models

# Create your models here.
class User(models.Model):
    account_email = models.CharField(max_length=200)
    nickname = models.CharField(max_length=50)
    profile_img = models.CharField(max_length=1000)


class Group(models.Model):
    name = models.CharField(max_length=150)
    leader_pk = models.IntegerField()
    max_user = models.IntegerField()
    group_img = models.CharField(max_length=1000)
    description = models.TextField()
    member = models.ManyToManyField(
        User,
        related_name='group',
    )