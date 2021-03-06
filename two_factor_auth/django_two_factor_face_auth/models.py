from django.contrib.auth.models import User
from django.db import models
import time
import os

def content_file_name(instance, filename):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name, extension = os.path.splitext(filename)
    return os.path.join('content', instance.user.username, timestr + extension)

class UserFaceImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    home_address = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)