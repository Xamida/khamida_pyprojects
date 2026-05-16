from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    text = models.CharField(max_length=130, unique=True)
    slug = models.SlugField(max_length=130, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

class News(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=130, unique=True, blank=False, null=False)
    author_name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=80)
    descriptions = models.TextField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment

class Views(models.Model):
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.views

class ScrollNews(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=130, unique=True, blank=False, null=False)
    author_name = models.CharField(max_length=100)
    descriptions = models.TextField()
    short_description = models.CharField(max_length=80)
    image = models.ImageField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='scrollnews')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class MostWatchedNews(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=130, unique=True, blank=True)
    author_name = models.CharField(max_length=100)
    descriptions = models.TextField()
    short_description = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='mostwatchednews')
    image = models.ImageField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title