from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from blog.models import Theme, Article, ArticleImages, Author


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_authors = get_user_model().objects.count()
    num_themes = Theme.objects.count()
    num_articles = Article.objects.count()

    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits

    ctx = {
        "num_authors": num_authors,
        "num_themes": num_themes,
        "num_articles": num_articles,
        "num_visits": num_visits,
    }
    return render(request, "blog/index.html", ctx)


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10


class ThemeListView(LoginRequiredMixin, generic.ListView):
    model = Theme
    paginate_by = 10


class ArticleListView(LoginRequiredMixin, generic.ListView):
    model = Article
    paginate_by = 10

    def get_queryset(self):
        return (
            Article.objects
            .select_related("author")
            .prefetch_related("themes")
        )


class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Article

    def get_queryset(self):
        return (
            Article.objects
            .select_related("author")
        )


class ThemeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Theme


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
