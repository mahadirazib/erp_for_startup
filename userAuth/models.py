from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class userInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    genders = (('male', 'male'), ('female', 'female'), ('other', 'other'))
    roles = (('1', 'Chief'), ('2', 'Moderator'), ('3', 'Human Resource'), ('4', 'Finance'), ('5', 'Office Employee'))
    bloodGroups = (('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'))

    phone = models.CharField(max_length=15)
    gender = models.TextField(choices=genders)
    role = models.TextField(choices=roles, default='5')
    proPic = models.ImageField(blank=True, upload_to='propic')
    fbLink = models.URLField(blank=True)
    bloodGroup = models.CharField(max_length=5, choices=bloodGroups, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + ' (' + self.roles[int(self.role)-1][1] + ')'



