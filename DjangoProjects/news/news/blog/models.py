from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=130, null=True)
    text = models.CharField(max_length=130)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super(Category, self).save(*args, **kwargs)

class ScrollNews(models.Model):
    name = models.CharField(max_length=20, blank=False)
    image = models.ImageField(upload_to='ScrollNews')
    title = models.TextField(max_length=100, blank=False)
    date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class PopularPost(models.Model):
    number = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="popular_post")
    title = models.TextField(max_length=130)

    def __str__(self):
        return str(self.number)

class AboutPage(models.Model):
    name = models.CharField(max_length=130)
    image = models.ImageField(upload_to='AboutPage')
    date = models.DateField()
    title = models.CharField(max_length=130, blank=True)
    description = models.TextField(max_length=500)
    url = models.URLField()

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
