from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.views import index

app_name = "blog"

urlpatterns = (
    [
        path("", index, name="index"),
    ]
)
