from django.contrib import admin

from .models import ScrollNews, PopularPost, Category, AboutPage

# Register your models here.

admin.site.register(ScrollNews)
admin.site.register(PopularPost)
admin.site.register(Category)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    exclude = ('views', )