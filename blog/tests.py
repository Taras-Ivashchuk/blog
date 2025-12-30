from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import io
from PIL import Image
from django.urls import reverse

from blog.forms import AuthorCreationForm
from blog.models import Article, Theme


class AuthorFormTest(TestCase):
    def create_image(self):
        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        return SimpleUploadedFile(
            name="test_avatar.jpg",
            content=image_io.read(),
            content_type="image/jpeg"
        )

    def setUp(self):
        self.author_data = {
            "username": "testauthor",
            "first_name": "Test",
            "last_name": "Author",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }

        self.file_data = {
            "avatar": self.create_image()
        }

        self.superuser = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(self.superuser)

    def test_author_creation_form_is_valid(self):
        form = AuthorCreationForm(data=self.author_data, files=self.file_data)

        self.assertTrue(form.is_valid())

    @patch("cloudinary.uploader.upload")
    def test_author_creation_success(self, mock_upload):
        mocked_response = {
            'public_id': 'test_author_avatar',
            'type': 'upload',
            'version': 123456789,
            "resource_type": "image",
        }

        mock_upload.return_value = mocked_response
        post_data = {
            **self.author_data,
            "avatar": self.file_data["avatar"],
        }
        print("post_data", post_data)
        self.client.post(reverse(
            "blog:author-create"),
            data=post_data,
        )
        new_author_created = get_user_model().objects.filter(
            username=self.author_data["username"]
        )

        avatar_created = new_author_created.first().avatar

        self.assertTrue(new_author_created.exists())
        self.assertEqual(avatar_created.public_id, mocked_response["public_id"])


class ArticeFormTest(TestCase):
    def create_image(self):
        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        return SimpleUploadedFile(
            name="test_avatar.jpg",
            content=image_io.read(),
            content_type="image/jpeg"
        )

    def setUp(self):
        self.theme = Theme.objects.create(name="TestTheme")
        self.article_data = {
            "title": "TestTitle",
            "description": "TestDescription",
            "content": "TestContent",
            "themes": self.theme.id,
        }
        self.file_data = {
            "picture": self.create_image()
        }
        self.superuser = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(self.superuser)

    @patch("cloudinary.uploader.upload")
    def test_article_creation_form_is_valid(self, mocked_upload):
        mocked_upload.return_value = {
            'public_id': 'test_picture',
            'type': 'upload',
            'version': 1234567890,
            "resource_type": "image",
        }

        response = self.client.post(
            reverse("blog:article-create"),
            data={
                **self.article_data,
                "new_pictures": self.file_data["picture"],
            },
        )

        new_article_created = Article.objects.filter(
            title=self.article_data["title"]

        )

        pictures_created = new_article_created.first().pictures

        self.assertTrue(new_article_created.exists())
        self.assertEqual(pictures_created.count(), 1)
