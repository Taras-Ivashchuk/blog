from django.urls import path, include

app_name = "user"

urlpatterns = (
    [
        path("", include("django.contrib.auth.urls"))
    ]
)
