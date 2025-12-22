from django.urls import path

from blog.views import *

app_name = "blog"

urlpatterns = (
    [
        path("", index, name="index"),
        path("authors/", AuthorListView.as_view(), name="author-list"),
        path("authors/create/", AuthorCreateView.as_view(), name="author-create"),
        path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
        path("authors/<int:pk>/update/", AuthorUpdateView.as_view(), name="author-update"),
        path("authors/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author-delete"),
        path("themes/", ThemeListView.as_view(), name="theme-list"),
        path("themes/<int:pk>/", ThemeDetailView.as_view(), name="theme-detail"),
        path("themes/<int:pk>/edit/", ThemeEditView.as_view(), name="theme-edit"),
        path("themes/<int:pk>/delete/", ThemeDeleteView.as_view(), name="theme-delete"),
        path("themes/create/", ThemeCreateView.as_view(), name="theme-create"),
        path("articles/", ArticleListView.as_view(), name="article-list"),
        path("articles/<str:slug>/", ArticleDetailView.as_view(), name="article-detail"),
        path("articles/<str:slug>/edit/", ArticleEditView.as_view(), name="article-edit"),
        path("article-images/<int:pk>/delete/", ArticleImagesDeleteView.as_view(), name="article_image-delete"),
        path("article/create/", ArticleCreateView.as_view(), name="article-create"),
        path("article/<str:slug>/delete/", ArticleDeleteView.as_view(), name="article-delete"),
        path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    ]
)
