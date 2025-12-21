from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from blog.models import Article


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "description", "themes", "content",)


class AuthorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "avatar",
        )


class AuthorUpdateForm(UserChangeForm):
    avatar = CloudinaryFileField(required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the password field from update form
        if 'password' in self.fields:
            del self.fields['password']
