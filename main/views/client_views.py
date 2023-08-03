
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse_lazy
from django.views import generic
from main.forms import MailingForm, ClientForm
from main.models import Message, Mailing, Client


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    login_url = 'users:login'
    redirect_field_name = 'next'


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    login_url = 'users:login'
    redirect_field_name = 'next'


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                message_instance = Message.objects.create(
                    creator=self.request.user,
                    client=self.object
                )
                if formset.is_valid():
                    formset.instance = message_instance
                    formset.save()

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
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = modelformset_factory(Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(
                self.request.POST,
                queryset=Mailing.objects.filter(client=self.object)
            )
        else:
            context_data['formset'] = MailingFormset(queryset=Mailing.objects.filter(
                client=self.object
            ))

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.client = self.object
                instance.save()

        return super().form_valid(form)




