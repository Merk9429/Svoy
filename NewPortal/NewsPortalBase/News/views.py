from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse_lazy
from News.models import *
from News.filters import PostFilter
from News.forms import PostForm
from News.tasks import send_notifications


def forbidden_403(request, exception):
    context = RequestContext(request)
    error = render('403.html', context)
    error.status_code = 403
    return error


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class PostList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'newsone.html'
    context_object_name = 'newsone'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = 'NW'
        post.save()
        send_notifications.delay(post.pk)
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.path == f'/news/{post.pk}/edit/' and post.category == 'AR':
            return render(self.request, 'error_edit_post.html')

        return super(PostEdit, self).dispatch(request, *args, **kwargs)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post', )
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.path == f'/news/{post.pk}/delete/' and post.category == 'AR':
            return render(self.request, 'error_delete_post.html')

        return super(PostDelete, self).dispatch(request, *args, **kwargs)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = 'AR'
        post.save()
        send_notifications.delay(post.pk)
        return super().form_valid(form)


class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.path == f'/news/article/{post.pk}/edit/' and post.category == 'NW':
            return render(self.request, 'error_edit_article.html')

        return super(ArticleEdit, self).dispatch(request, *args, **kwargs)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post', )
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.path == f'/news/article/{post.pk}/delete/' and post.category == 'NW':
            return render(self.request, 'error_delete_article.html')

        return super(ArticleDelete, self).dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return contex


class PostSearch(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(dopCategory=self.category).order_by('-datetime')
        return queryset

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        contex['category'] = self.category
        return contex


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
