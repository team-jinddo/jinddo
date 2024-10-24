from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


# Create your models here.


class Venue(models.Model):
    biz_id = models.CharField(max_length=255, null=True)

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
    recommendations = models.CharField(max_length=255, default='') # Comma-separated venue IDs

    def get_recommended_venues(self):
        # Split the recommendations string into a list of IDs
        recommended_ids_str = self.recommendations.split(',')
        # Convert the list of string IDs to a list of integers
        recommended_ids = [
            int(id_str) for id_str in recommended_ids_str
            if id_str.isdigit() # Check if the string is a digit
        ]
        # Retrieve the Venue objects corresponding to these IDs
        venues = Venue.objects.filter(biz_id__in=recommended_ids)
        print(venues)
        return venues


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
