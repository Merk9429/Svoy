from django.urls import path
from .views import forbidden_403
from .views import (
    PostList, PostDetail, PostCreate, PostEdit, PostDelete, PostSearch, ArticleCreate, ArticleEdit, ArticleDelete,
    IndexView, CategoryListView, subscribe
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('log/', IndexView.as_view()),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]

handler403 = forbidden_403
