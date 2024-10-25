from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import FormMixin

from venueapp.models import Venue


from .api.db_content_based_recommendation import RestaurantRecommender
from .api.cf import CollaborativeFiltering
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
            'cleanliness': profile.cleanliness
        }

        # Get recommendations based on user preferences
        recommendations = recommender.recommend(user_preferences, num_recommendations=5)
        biz_ids = recommendations.tolist()

        context['recommends'] = Venue.objects.filter(biz_id__in=biz_ids)
        context['user'] = user

        return context


class VenueRec2View(ListView):
    model = Venue
    context_object_name = 'venue_list'
    template_name = 'venueapp/reco2.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the current venue object

        recommender = CollaborativeFiltering()

        user = self.request.user
        profile = user.profile
        # user_preferences = {
        #     'sweetness': profile.sweetness,
        #     'spiciness': profile.spiciness,
        #     'saltiness': profile.saltiness,
        #     'sourness': profile.sourness,
        #     'cleanliness': profile.cleanliness
        # }
        user_taste_vector = [profile.saltiness, profile.sourness,
                             profile.spiciness, profile.sweetness, profile.cleanliness]

        taste_similarity_df_by_taste = recommender.calculate_pearson_sim_by_taste(user_taste_vector)  # 피어슨 유사도
        visit_list_by_taste = recommender.get_visit_list(taste_similarity_df_by_taste)
        recommended_ids_by_taste = recommender.recommended_bizid(visit_list_by_taste)


        context['recommends'] = Venue.objects.filter(id__in=recommended_ids_by_taste)
        context['user'] = user

        return context

    # class VenueRateView(FormView):
    #     template_name = 'venueapp/rate_venue.html'
    #     form_class = VenueRatingForm
    #
    #     def form_valid(self, form):
    #         # Process the form data here
    #         # You can access the venue using self.kwargs['venue_id']
    #         venue = get_object_or_404(Venue, id=self.kwargs['pk'])
    #         # Create a new Rating instance but don't save it to the database yet
    #         rating = form.save(commit=False)
    #         # Set the venue and user for the rating
    #         rating.restaurant = venue.biz_id
    #         rating.user = self.request.user
    #
    #         # Save the rating data to the database
    #         rating.save()
    #         # Example: venue.ratings.create(score=form.cleaned_data['score'], ...)
    #         return super().form_valid(form)
    #
    #
    #     def get_success_url(self):
    #         # Redirect to the venue detail page after successful submission
    #         return reverse('venueapp:detail', kwargs={'pk': self.kwargs['pk']})
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

    class VenueRec3View(ListView):
        model = Venue
        context_object_name = 'venue_list'
        template_name = 'venueapp/reco3.html'

        def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Get the current venue object

            recommender = CollaborativeFiltering()

            user = self.request.user
            profile = user.profile
            # user_preferences = {
            #     'sweetness': profile.sweetness,
            #     'spiciness': profile.spiciness,
            #     'saltiness': profile.saltiness,
            #     'sourness': profile.sourness,
            #     'cleanliness': profile.cleanliness
            # }
            user_type_vector = [profile.asian, profile.bar, profile.bistro, profile.buffet, profile.chinese,
                                 profile.dessert, profile.donkatsu, profile.etc, profile.fastfood, profile.japanese,
                                 profile.korean, profile.meat, profile.seafood, profile.snack, profile.soup, profile.western]

            taste_similarity_df_by_type = recommender.calculate_adjusted_cos_sim_by_type(user_type_vector)  # 피어슨 유사도
            visit_list_by_type = recommender.get_visit_list(taste_similarity_df_by_type)
            recommended_ids_by_type = recommender.recommended_bizid(visit_list_by_type)

            context['recommends'] = Venue.objects.filter(id__in=recommended_ids_by_type)
            context['user'] = user

            return context
