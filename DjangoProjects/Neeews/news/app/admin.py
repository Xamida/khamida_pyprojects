from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "slug")
    search_fields = ("text", "slug")
    prepopulated_fields = {"slug": ("text", )}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display =("id", "slug", "author_name", "category", "date", "likes")
    search_fields = ("title", "slug", "descriptions")
    list_filter = ("category", "date")
    prepopulated_fields = {"slug": ("title", )}
    readonly_fields = ("views", "date")

@admin.register(ScrollNews)
class ScrollNewsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "slug", "author_name",
        "short_description", "category", "likes", "views", "date"
    )
    search_fields = ("title", "slug", "author_name")
    list_filter = ("category", "date")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("likes", "views", "date")