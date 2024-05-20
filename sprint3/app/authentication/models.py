from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, max_length=1000)
    profile_image = models.FileField(upload_to="profile_images", blank=True, null=True)
    cover_image = models.FileField(upload_to="cover_images", blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.TextField(blank=True, null=True, max_length=300)
    city = models.TextField(blank=True, null=True, max_length=300)
    street = models.TextField(blank=True, null=True, max_length=300)
    postcode = models.TextField(blank=True, null=True, max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return self.street + " " + self.city + " " + self.country + " " + self.postcode
