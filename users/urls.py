from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import UserRegistrationView, UserProfileView, UserLoginView, EmailVerificationView, password_reset, \
    PasswordResetView
from django.contrib.auth.decorators import login_required
app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/new_pass/<uidb64>/<token>/', PasswordResetView.as_view(), name='new_pass'),
]
