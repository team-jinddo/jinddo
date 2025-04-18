from django import forms
#
# from venueapp.models import UserVisit


# class VenueRatingForm(forms.ModelForm):
#     class Meta:
#         model = UserVisit
#         fields = ['score', 'saltiness', 'sourness', 'spiciness', 'sweetness', 'cleanliness']
#         widgets = {
#             'score': forms.Select(choices=[(i, i) for i in range(6)]),
#             'saltiness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
#             'sourness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
#             'spiciness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
#             'sweetness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
#             'cleanliness': forms.Select(choices=[(i, i) for i in range(-5, 6)]),
#         }

class VenueRatingForm(forms.Form):
    score = forms.ChoiceField(
        choices=[(i, i) for i in range(6)],
        label='Score',
        widget=forms.Select
    )
    flavor1 = forms.ChoiceField(
        choices=[(i, i) for i in range(-5, 6)],
        label='Flavor 1',
        widget=forms.Select
    )
    flavor2 = forms.ChoiceField(
        choices=[(i, i) for i in range(-5, 6)],
        label='Flavor 2',
        widget=forms.Select
    )
    flavor3 = forms.ChoiceField(
        choices=[(i, i) for i in range(-5, 6)],
        label='Flavor 3',
        widget=forms.Select
    )
    flavor4 = forms.ChoiceField(
        choices=[(i, i) for i in range(-5, 6)],
        label='Flavor 4',
        widget=forms.Select
    )
    flavor5 = forms.ChoiceField(
        choices=[(i, i) for i in range(-5, 6)],
        label='Flavor 5',
        widget=forms.Select
    )

