from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length=255)

    location = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    sweetness = models.FloatField(default=3)
    spiciness = models.FloatField(default=3)
    saltiness = models.FloatField(default=3)
    sourness = models.FloatField(default=3)
    cleanliness = models.FloatField(default=3)
    category = models.CharField(max_length=255)

    biz_id = models.CharField(max_length=255, default='')

class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Venue, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)

