from django import forms
#
from .models import UserVisit


class VenueRatingForm(forms.ModelForm):
    class Meta:
        model = UserVisit
        fields = ['score', 'saltiness', 'sourness', 'spiciness', 'sweetness', 'cleanliness']
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(6)]),
            'saltiness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
            'sourness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
            'spiciness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
            'sweetness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
            'cleanliness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
        }

