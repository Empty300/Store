from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import CommonMixin
from main import settings
from users.forms import (RegisterForm, UserLoginForm, UserProfileForm,
                         UserResetPassForm)
from users.models import EmailVerification, User


class UserLoginView(CommonMixin, LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Store - Авторизация'


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались! ' \
                      'На вашу почту было отправлено письмо для ' \
                      'подтверждения вашего email адресса'
    title = 'Store - Регистрация'


class UserProfileView(CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get(self, request, *args, **kwargs):
        if self.request.user.pk != self.kwargs['pk']:
            return HttpResponseRedirect(reverse('index'))
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(CommonMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


def password_reset(request):
    title = 'Store - сброс пароля'
    if request.method == 'GET':
        form = UserResetPassForm()
        context = {'form': form,
                   'title': title}
        return render(request, 'users/reset_pass.html', context)
    else:
        try:
            user = User.objects.get(email=request.POST["email"])
        except User.DoesNotExist:
            user = False
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = f'/users/password_reset/new_pass/{uid}/{token}/'
            verification_link = f'{settings.DOMAIN_NAME}{link}'
            subject = f'Сброс пароля для {request.user.username}'
            message = 'Для сброса пароля {} перейдите по ссылке: {}'.format(
                request.user.username,
                verification_link
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=(user.email,),
                fail_silently=False,
            )
            form = UserResetPassForm()
            context = {'msg': 'Письмо с ссылкой для сброса пароля отправлено вам на почту',
                       'form': form,
                       'title': title}

            return render(request, 'users/reset_pass.html', context)
        else:
            form = UserResetPassForm()
            context = {'msg': 'Пользователь с таким email не найден',
                       'form': form,
                       'title': title}
            return render(request, 'users/reset_pass.html', context)


class PasswordResetView(CommonMixin, SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'users/new_password.html'
    success_message = "Пароль успешно изменен"
    success_url = reverse_lazy("users:login")
    title = 'Store - сброс пароля'
