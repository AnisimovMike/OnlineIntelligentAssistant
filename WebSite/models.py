from django.db import models
from django.contrib.auth.models import User


class Attractions(models.Model):
    name = models.CharField(max_length=100)
    img_link = models.CharField(max_length=30)
    address = models.TextField(null=True, default=None)
    latitude = models.CharField(max_length=100, null=True, default=None)
    longitude = models.CharField(max_length=100, null=True, default=None)
    short_description = models.TextField(null=True, default=None)


class AttractionTags(models.Model):
    attraction = models.ForeignKey(Attractions, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30)


class UserRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    route_name = models.CharField(max_length=100)
    route_text = models.TextField(null=True, default=None)


class RouteAttractions(models.Model):
    route = models.ForeignKey(UserRoute, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attractions, on_delete=models.CASCADE)


class UserMess(models.Model):
    name = models.CharField(max_length=100)
    gmail = models.CharField(max_length=50)
    theme = models.CharField(max_length=100)
    mes = models.TextField()
