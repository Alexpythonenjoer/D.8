from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Posts
from datetime import datetime
from .filters import PostsFilter
from .forms import PostsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ListView):
    model = Posts
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class PostsDetail(DetailView):
    model = Posts
    template_name = 'news.html'
    context_object_name = 'post'


class PostsCreate(CreateView,PermissionRequiredMixin):
    form_class=PostsForm
    model=Posts
    template_name='posts_edit.html'
    permission_required = ('news.add_posts')


class PostsUpdate(UpdateView, LoginRequiredMixin):
    form_class = PostsForm
    model = Posts
    template_name = 'posts_edit.html'
    go_to_login=login_required(login_url= 'login/')


class PostsDelete(DeleteView):
    model = Posts
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('product_list')