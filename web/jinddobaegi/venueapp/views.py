from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from venueapp.models import Venue


# Create your views here.

class VenueDetailView(DetailView):
    model = Venue
    context_object_name = 'target_venue'
    template_name = 'venueapp/detail.html'

    paginate_by = 25


class VenueListView(ListView):
    model = Venue
    context_object_name = 'venue_list'
    template_name = 'venueapp/list.html'
    paginate_by = 5