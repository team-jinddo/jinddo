from django.urls import path

from venueapp.views import VenueDetailView, VenueListView

app_name = 'venueapp'

urlpatterns = [
    path('list/', VenueListView.as_view(), name='list'),
    path('detail/<int:pk>', VenueDetailView.as_view(), name='detail'),
]