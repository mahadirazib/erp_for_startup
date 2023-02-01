from django.db import models
from django.contrib.auth.models import User
from userAuth.models import userInfo

# Create your models here.

class notice(models.Model):

    user = models.ManyToManyField(userInfo)

    title = models.CharField(max_length=200)
    details = models.TextField()
    needToComplete = models.BooleanField(default=False)
    deadLine = models.DateField(blank=True, null=True)
    completedBy = models.CharField( max_length=10, blank=True)




