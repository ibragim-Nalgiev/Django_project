
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from main.forms import MailingForm
from main.models import Mailing, LogiMail


class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    login_url = 'users:login'
    redirect_field_name = 'next'


class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mailing
    login_url = 'users:login'
    redirect_field_name = 'next'


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail:mailing_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


class LogiListView(LoginRequiredMixin, generic.ListView):
    model = LogiMail
    login_url = 'users:login'
    redirect_field_name = 'next'