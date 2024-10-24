from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from venueapp.models import Venue


from .api.db_content_based_recommendation import RestaurantRecommender

# Create your views here.

class VenueDetailView(DetailView):
    model = Venue
    context_object_name = 'target_venue'
    template_name = 'venueapp/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the current venue object
        venue = self.get_object()
        # Add the recommended venues to the context
        context['recommended_venues'] = venue.get_recommended_venues()

        recommender = RestaurantRecommender()

        user = self.request.user
        profile = user.profile
        user_preferences = {
            'sweetness': profile.sweetness,
            'spiciness': profile.spiciness,
            'saltiness': profile.saltiness,
            'sourness': profile.sourness,
            'cleanliness': profile.sourness
        }

        # Get recommendations based on user preferences
        recommendations = recommender.recommend(user_preferences, num_recommendations=5)
        biz_ids = recommendations.tolist()

        context['recommends'] = Venue.objects.filter(biz_id__in=biz_ids)


        return context


class VenueListView(ListView):
    model = Venue
    context_object_name = 'venue_list'
    template_name = 'venueapp/list.html'

    def get_queryset(self):
        # Return the top 10 venues ordered by score in descending order
        return Venue.objects.filter(recommendations__isnull=False).order_by('-score')[:10]