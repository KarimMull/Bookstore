from django.contrib import admin
from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name",]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price", "discount"]
    list_editable = ["discount",]
    search_fields = ["name", "description"]
    list_filter = ["discount", "quantity", "category"]

    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        "image_2",  # Добавлено поле для второго изображения
        "image_3",  # Добавлено поле для третьего изображения
        ("price", "discount"),
        "quantity",
    ]
