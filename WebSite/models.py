from django.db import models
from django.contrib.auth.models import User


class Attractions(models.Model):
    link = models.CharField(max_length=300)
    img_link = models.CharField(max_length=20)
    name = models.CharField(max_length=100)


class UserRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    route_name = models.CharField(max_length=100)
    route_text = models.CharField(max_length=500)
    points_list = models.TextField()
    coordinates_list = models.TextField(null=True, default=None)
