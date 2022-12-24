import uuid
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from  django import forms




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Введите имя пользователя"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': "Введите пароль"
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Введите имя пользователя"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': "Введите пароль еще раз"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': "Введите email"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Введите ваше имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Введите вашу фамилию"}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'readonly': True}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input',
        'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
