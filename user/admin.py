from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import Author


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("avatar",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("avatar",)}),
    )
