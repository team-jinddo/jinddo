from django.urls import path

from venueapp.views import VenueDetailView, VenueListView, VenueRec1View, VenueRateView, VenueRec2View

app_name = 'venueapp'

urlpatterns = [
    path('list/', VenueListView.as_view(), name='list'),
    path('detail/<int:pk>', VenueDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/rate/', VenueRateView.as_view(), name='rate_venue'),
    path('reco1/', VenueRec1View.as_view(), name='reco1'),
    path('reco2/', VenueRec2View.as_view(), name='reco2'),
    # path('reco3/', VenueRec3View.as_view(), name='reco3'),
]