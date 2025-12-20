from cloudinary.forms import CloudinaryFileField
from django import forms

from blog.models import Article


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "description", "themes", "content",)
