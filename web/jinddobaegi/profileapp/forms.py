from django.core.exceptions import ValidationError
from django.forms import ModelForm, ChoiceField, MultipleChoiceField, CheckboxSelectMultiple, Select

from profileapp.models import Profile

TASTE_CHOICES = [(i, str(i)) for i in range(1, 6)]
CATEGORY_CHOICES = [
    ('asian', '아시안'),
    ('bistro', '요리주점'),
    ('korean', '한식'),
    ('snack', '분식'),
    ('chinese', '중식당'),
    ('meat', '육류/고기요리'),
    ('dessert', '카페/디저트'),
    ('japanese', '일식당'),
    ('western', '양식'),
    ('seafood', '해산물'),
    ('soup', '국물'),
    ('fastfood', '패스트푸드'),
    ('bar', '바(BAR)'),
    ('donkatsu', '돈가스'),
    ('buffet', '뷔페'),
    ('etc', '기타'),
]

class ProfileCreationForm(ModelForm):
    sweetness = ChoiceField(
        choices=TASTE_CHOICES,
        label="선호하는 단맛 정도를 선택해주세요",
        widget=Select(attrs={'class': 'form-control'})
    )
    spiciness = ChoiceField(
        choices=TASTE_CHOICES,
        label="선호하는 매운맛 정도를 선택해주세요",
        widget=Select(attrs={'class': 'form-control'})
    )
    saltiness = ChoiceField(
        choices=TASTE_CHOICES,
        label="선호하는 짠맛 정도를 선택해주세요",
        widget=Select(attrs={'class': 'form-control'})
    )
    sourness = ChoiceField(
        choices=TASTE_CHOICES,
        label="선호하는 신맛 정도를 선택해주세요",
        widget=Select(attrs={'class': 'form-control'})
    )
    cleanliness = ChoiceField(
        choices=TASTE_CHOICES,
        label="선호하는 담백한맛 정도를 선택해주세요",
        widget=Select(attrs={'class': 'form-control'})
    )
    meal_categories = MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        label="선호하는 식당 타입을 최대 5개 까지 선택해주세요",
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Profile
        fields = ['sweetness', 'spiciness', 'saltiness', 'sourness', 'cleanliness',
                  'meal_categories', 'image', 'nickname', 'message']

    def clean_meal_categories(self):
        categories = self.cleaned_data.get('meal_categories')
        if len(categories) > 5:
            raise ValidationError("You can select up to 5 categories.")
        return categories