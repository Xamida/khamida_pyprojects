from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):         #categorialar_ucun
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):            #brandlar_ucun
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline): #product_rasmi_ucun
    model = ProductImage
    extra = 1
    fields = ("image", "is_main", "sort_order")


class ProductSpecInline(admin.TabularInline):   #blmiman
    model = ProductSpec
    extra = 1
    fields = ("key", "value")

class ColorVariantInline(admin.TabularInline):  #ranglari_ucun
    model = ColorVariant
    extra = 1
    fields = ("name", "hex_code", "extra_price")

class ReviewInline(admin.TabularInline):        #reviewlar_sonini_ko'rish_ucun
    model = Review
    extra = 0
    fields = ("name", "rating", "is_published", "created_at")
    readonly_fields = ("created_at", )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):          #admin_qowoladigan_narsalar_ucun
    list_display = (
        "id", "title", "category", "brand",
        "price", "old_price",
        "stock", "sold",
        "rating_avg", "reviews_count",
        "is_active", "created_at"
    )
    list_filter = ("is_active", "category", "brand", "created_at")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("rating_avg", "reviews_count", "created_at", "updated_at")

    inlines = [ProductImageInline, ProductSpecInline, ColorVariantInline, ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):            #adminga_otzivlani_berkitadi(admin_ulani_qo'womiydi)
    list_display = ("id", "product", "name", "rating", "is_published", "created_at")
    list_filter = ("is_published", "rating", "created_at")
    search_fields = ("product__title", "name", "comment")
    readonly_fields = ("created_at",)