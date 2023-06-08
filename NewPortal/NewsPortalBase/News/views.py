from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'newsone.html'
    context_object_name = 'newsone'
