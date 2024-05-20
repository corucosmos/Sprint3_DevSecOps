from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone as tz


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False, max_length=1000)
    image = models.ImageField(upload_to="post_images", blank=True, null=True)
    created_date = models.DateTimeField(null=False, blank=False, default=tz.now)
