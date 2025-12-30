from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import generic, View

from blog.forms import ArticleEditForm, AuthorCreationForm, AuthorUpdateForm
from blog.models import Theme, Article, ArticleImages, Comments


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
    model = get_user_model()
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = AuthorCreationForm


class AuthorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = AuthorUpdateForm


class AuthorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("blog:author-list")


class ThemeListView(LoginRequiredMixin, generic.ListView):
    model = Theme
    paginate_by = 10


class ThemeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Theme


class ThemeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Theme
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("blog:theme-list")


class ThemeEditView(LoginRequiredMixin, generic.UpdateView):
    model = Theme
    fields = "__all__"


class ThemeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Theme
    success_url = reverse_lazy("blog:theme-list")


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

                objs = (
                    ArticleImages(article=self.object, picture=picture)
                    for picture in pictures
                )
                ArticleImages.objects.bulk_create(objs)

                return super().form_valid(form)

        except Exception:
            return self.form_invalid(form)


class ArticleImagesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ArticleImages
    template_name = "blog/articleimages_confirm_delete.html"

    def get_success_url(self):
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

                objs = (
                    ArticleImages(article=self.object, picture=picture)
                    for picture in pictures
                )
                ArticleImages.objects.bulk_create(objs)
                return response

        except Exception:
            return self.form_invalid(form)


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Article

    def get_success_url(self):
        return reverse_lazy("blog:article-list")


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request):
        content = request.POST.get('comment-content')
        article_slug = request.POST.get('article_slug')

        article = get_object_or_404(Article, slug=article_slug)

        Comments.objects.create(
            text=content,
            article=article,
            author=request.user
        )

        return redirect('blog:article-detail', slug=article_slug)
