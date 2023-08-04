import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from main.forms import MessageForm
from main.models import Message, Mailing, Client, Blog


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

    def form_valid(self, form):
        message = form.save()
        message.user = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    pk_url_kwarg = 'pk'
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user:
            raise Http404
        return self.object

    def form_valid(self, form):
        form.instance.mailing_owner = self.request.user
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
