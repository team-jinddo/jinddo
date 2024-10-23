from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    image = models.ImageField(upload_to='profile/', null=True)
    nickname = models.CharField(max_length=20, unique=True, null=True)
    message = models.CharField(max_length=100, null=True)

    sweetness = models.IntegerField(default=3)  # Default rating
    spiciness = models.IntegerField(default=3)
    saltiness = models.IntegerField(default=3)
    sourness = models.IntegerField(default=3)
    cleanliness = models.IntegerField(default=3)
    categories = models.CharField(max_length=255, blank=True) # Store selected categories as a comma-separated string

    asian = models.FloatField(null=True, blank=True)
    bar = models.FloatField(null=True, blank=True)
    bistro = models.FloatField(null=True, blank=True)
    buffet = models.FloatField(null=True, blank=True)
    chinese = models.FloatField(null=True, blank=True)
    dessert = models.FloatField(null=True, blank=True)
    donkatsu = models.FloatField(null=True, blank=True)
    etc = models.FloatField(null=True, blank=True)
    fastfood = models.FloatField(null=True, blank=True)
    japanese = models.FloatField(null=True, blank=True)
    korean = models.FloatField(null=True, blank=True)
    meat = models.FloatField(null=True, blank=True)
    seafood = models.FloatField(null=True, blank=True)
    snack = models.FloatField(null=True, blank=True)
    soup = models.FloatField(null=True, blank=True)
    western = models.FloatField(null=True, blank=True)