from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic

from blog.forms import ArticleEditForm
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


class ArticleEditView(LoginRequiredMixin, generic.UpdateView):
    model = Article
    form_class = ArticleEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pictures = self.object.pictures.all()
        ctx["picture_list"] = pictures
        return ctx

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save()

                pictures = self.request.FILES.getlist('new_pictures')
                for picture in pictures:
                    ArticleImages.objects.create(
                        article=self.object,
                        picture=picture
                    )

                return super().form_valid(form)

        except Exception:
            return self.form_invalid(form)


class ArticleImagesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ArticleImages
    template_name = "blog/articleimages_confirm_delete.html"

    def get_success_url(self):
        # Return to the article edit page after deletion
        return reverse("blog:article-edit", kwargs={'slug': self.object.article.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.object.article.slug
        return context


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    form_class = ArticleEditForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        try:
            with transaction.atomic():
                response = super().form_valid(form)

                pictures = self.request.FILES.getlist('new_pictures')
                for picture in pictures:
                    ArticleImages.objects.create(
                        article=self.object,
                        picture=picture
                    )

                return response

        except Exception:
            return self.form_invalid(form)
