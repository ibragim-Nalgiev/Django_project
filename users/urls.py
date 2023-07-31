from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from django.views.generic import TemplateView
from users.apps import UsersConfig
from users.views import *


app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),

    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/<key>/', ConfirmView.as_view(), name='confirm_email'),

    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),

    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
