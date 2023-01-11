from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Иван"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Иванов"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': "you@example.com"}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "ул. Мира, дом 6"}))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Россия"}))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Иркутск"}))
    zipcode = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Почтовый код"}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Телефон"}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'country', 'city', 'zipcode', 'telephone')
