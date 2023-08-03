
from random import randint

from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:invalid_verify')

    def form_valid(self, form):
        self.object = form.save()
        self.object.verification_key = ''.join([str(randint(0, 9))
                                                for _ in range(10)])

        send_mail(
            subject='Поздравляем с регистрацией',
            message=f'Для завершения регистрации, пожалуйста, перейдите по указанной ссылке '
                    f'http://localhost:8000/users/confirm_email/{self.object.verification_key}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)


class ConfirmView(generic.TemplateView):
    model = User

    def get(self, *args, **kwargs):
        key = self.kwargs.get('key')
        user = User.objects.filter(verification_key=key).first()
        if user:
            user.is_active = True
            user.verification_key = key
            user.save()
            login(self.request, user)
        return redirect('users:valid_verify')



