import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory, modelformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from main.forms import MessageForm, MailingForm, ClientForm, BlogForm
from main.models import Message, Mailing, LogiMail, Client, Blog


class IndexView(generic.View):
    def get(self, request):
        count_mailing = Message.objects.all().count()
        count_mailing_active = Mailing.objects.filter(is_active=True).count()
        count_unique_client = Client.objects.all().distinct('email').count()
        blog_random = []
        count_blog = Blog.objects.filter(is_public=True).count()

        if count_blog > 0:
            while len(blog_random) < 3:
                pk_for_random = random.randint(1, count_blog)
                blog_list = Blog.objects.filter(is_public=True).filter(pk=pk_for_random).first()
                if blog_list and blog_list not in blog_random:
                    blog_random.append(blog_list)

        context = {
            'count_mailing': count_mailing,
            'count_mailing_active': count_mailing_active,
            'count_unique_client': count_unique_client,
            'blog_random': blog_random,
            'title': 'Главная'
        }

        return render(request, 'main/index.html', context)


class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Message
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST)
        else:
            context_data['formset'] = SubjectFormset()

        return context_data

    def form_valid(self, form):
        form.instance.creator = self.request.user
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    login_url = 'users:login'
    redirect_field_name = 'next'
    pk_url_kwarg = 'pk'

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
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()

        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    success_url = reverse_lazy('main:home')
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user:
            raise Http404
        return self.object


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


class BlogListView(generic.ListView):
    model = Blog


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_object(self, queryset=None):
        blog = super().get_object(queryset=queryset)
        blog.num_views += 1
        blog.save()
        return blog


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('main:blog_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('main:blog_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('main:blog_list')
    login_url = 'users:login'
    redirect_field_name = 'next'


