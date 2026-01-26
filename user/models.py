from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.urls import reverse


class Author(AbstractUser):
    avatar = CloudinaryField("avatar")

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"
        db_table = 'blog_author'  # use existing table

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("blog:author-detail", kwargs={"pk": self.pk})
