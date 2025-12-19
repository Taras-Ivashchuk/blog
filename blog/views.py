from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from blog.models import Theme, Article, ArticleImages, Author


def index(request: HttpRequest) -> HttpResponse:
    num_authors = get_user_model().objects.count()
    num_themes = Theme.objects.count()
    num_articles = Article.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    ctx = {
        "num_authors": num_authors,
        "num_themes": num_themes,
        "num_articles": num_articles,
        "num_visits": num_visits,
    }
    return render(request, "blog/index.html", ctx)


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class ThemeListView(generic.ListView):
    model = Theme
    paginate_by = 10

class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 10
