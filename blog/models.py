from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse


class Author(AbstractUser):
    avatar = CloudinaryField("avatar")

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("blog:author-detail", kwargs={"pk": self.pk})


class Theme(models.Model):
    name = models.CharField(
        max_length=255, unique=True, blank=False, null=False
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=['name', ])
        ]

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(
        max_length=255, unique=True, blank=False, null=False
    )
    description = models.TextField(
        max_length=500,
    )
    themes = models.ManyToManyField(
        Theme,
        related_name="articles"
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.USER_AUTH_MODEL, on_delete=models.RESTRICT,
        related_name="articles"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default="", null=False)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=['theme', 'title', ])
        ]

    def __str__(self):
        return self.title


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.text[:50]}..."


class ArticleImages(models.Model):
    picture = CloudinaryField("picture")
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="pictures"
    )
