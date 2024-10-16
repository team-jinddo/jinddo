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
    meal_categories = models.CharField(max_length=255, blank=True) # Store selected categories as a comma-separated string