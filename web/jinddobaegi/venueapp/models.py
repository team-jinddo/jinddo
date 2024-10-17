from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Venue(models.Model):
    biz_id = models.CharField(max_length=255)

    name = models.CharField(max_length=255)

    location = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    sweetness = models.FloatField(default=3)
    spiciness = models.FloatField(default=3)
    saltiness = models.FloatField(default=3)
    sourness = models.FloatField(default=3)
    cleanliness = models.FloatField(default=3)

    category = models.CharField(max_length=255)


    score = models.FloatField(default=3)
    recommendations = models.CharField(max_length=255, default='')


class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Venue, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)

    score = models.IntegerField(null=True)
    sweetness = models.IntegerField(null=True)
    spiciness = models.IntegerField(null=True)
    saltiness = models.IntegerField(null=True)
    sourness = models.IntegerField(null=True)
    cleanliness = models.IntegerField(null=True)

