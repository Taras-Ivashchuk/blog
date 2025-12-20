from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.views import *

app_name = "blog"

urlpatterns = (
    [
        path("", index, name="index"),
        path("authors/", AuthorListView.as_view(), name="author-list"),
        path("authors/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
        path("themes/", ThemeListView.as_view(), name="theme-list"),
        path("themes/<int:pk>", ThemeDetailView.as_view(), name="theme-detail"),
        path("articles/", ArticleListView.as_view(), name="article-list"),
        path("articles/<str:slug>", ArticleDetailView.as_view(), name="article-detail"),
    ]
)
