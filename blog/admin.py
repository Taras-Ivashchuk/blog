from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.models import Author, Article, ArticleImages, Comments, Theme


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("avatar",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("avatar",)}),
    )


class ArticleImageInstanceInline(admin.TabularInline):
    model = ArticleImages
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("author__username", "created_at",)
    list_filter = ("author", "created_at",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = admin.ModelAdmin.search_fields + (
        "author__username__icontains",
    )

    inlines = [ArticleImageInstanceInline]


@admin.register(ArticleImages)
class ArticleImagesAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("get_author",)
    list_filter = ("article", "article__author")
    search_fields = admin.ModelAdmin.search_fields + (
        "article__author__username__icontains",
        "article__title__icontains",)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("author", "article")
    list_filter = ("author", "article")
    search_fields = admin.ModelAdmin.search_fields + (
        "author__username__icontains", "article__title__icontains"
    )


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    search_fields = admin.ModelAdmin.search_fields + (
        "name__icontains",
    )
