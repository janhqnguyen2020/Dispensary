from django.contrib import admin

from .models import Brand, Category

# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "limit_group")
    list_filter = ("limit_group",)
    search_fields = ("name", "slug")