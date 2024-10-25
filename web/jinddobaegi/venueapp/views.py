from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import FormMixin

from venueapp.models import Venue


from .api.db_content_based_recommendation import RestaurantRecommender
from .forms import VenueRatingForm


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
        print("Context recommended_venues:", context['recommended_venues'])  # Debug statement

        return context


class VenueListView(ListView):
    model = Venue
    context_object_name = 'venue_list'
    template_name = 'venueapp/list.html'

    def get_queryset(self):
        # Return the top 10 venues ordered by score in descending order
        return Venue.objects.filter(recommendations__isnull=False).order_by('-score')[:10]

class VenueRec1View(ListView):
    model = Venue
    context_object_name = 'venue_list'
    template_name = 'venueapp/reco1.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the current venue object

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

class VenueRateView(FormView):
    template_name = 'venueapp/rate_venue.html'
    form_class = VenueRatingForm

    def form_valid(self, form):
        # Process the form data here
        # You can access the venue using self.kwargs['venue_id']
        venue = get_object_or_404(Venue, id=self.kwargs['pk'])
        # Save the rating data to the database
        # Example: venue.ratings.create(score=form.cleaned_data['score'], ...)
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the venue detail page after successful submission
        return reverse('venueapp:detail', kwargs={'pk': self.kwargs['pk']})