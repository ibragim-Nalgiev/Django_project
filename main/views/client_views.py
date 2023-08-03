
from django.contrib.auth.mixins import LoginRequiredMixin
from main.forms import ClientForm
from main.models import Client
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    login_url = 'users:login'
    redirect_field_name = 'next'


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    login_url = 'users:login'
    redirect_field_name = 'next'


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client_create.html'

    def form_valid(self, form):
        form.instance.client_owner = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client_create.html'

    def get_object(self, queryset=None):

        self.object = super().get_object(queryset)
        if self.object.client_owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object




