from django import forms
from django.forms import ModelForm

from products.models import Reviews


class ReviewsForm(ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'input',
        'placeholder': 'Ваш отзыв'}))
    stars = forms.ChoiceField(choices=((5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")),
                              widget=forms.Select(attrs={'class': 'input'}))

    class Meta:
        model = Reviews
        fields = ('review', 'stars')
