
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from main.forms import MailingForm
from main.models import Mailing, LogiMail, Client
from django.http import Http404


class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Менеджеры').exists():
            return self.model.objects.all()
        else:
            return self.model.objects.filter(mailing_owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.mailing_owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    permission_required = 'main.stop_mailing'
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_create.html'
    success_url = reverse_lazy('main:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.user.is_superuser:
            form.fields['client'].queryset = Client.objects.all()
            return form
        else:
            form.fields['client'].queryset = Client.objects.filter(client_owner=self.request.user)
            return form

    def form_valid(self, form):
        form.instance.mailing_owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['mailing_owner'].queryset = Client.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail:mailing_list')
    template_name = 'main/mailing_delete.html'


class LogiListView(LoginRequiredMixin, generic.ListView):
    model = LogiMail
    template_name = 'main/logimail_list.html'
