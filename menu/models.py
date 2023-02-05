from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings


class Meal(models.Model):
    """Model for Meal object"""
    name = models.CharField(max_length=100, unique=True)
    cover = CloudinaryField('image')
    price = models.FloatField()
    description = models.CharField(max_length=1000)
