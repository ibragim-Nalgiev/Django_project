
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from main.forms import BlogForm
from main.models import Blog


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
