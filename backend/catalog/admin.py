from django.contrib import admin

from .models import Brand, Category, Product, Variant

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

#shows variant rows (sizes) inside product edit page
class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    readonly_fields = ("stock_reserved",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "status", "is_featured","slug")
    search_fields = ("name", "brand__name", "slug")
    list_filter = ("status", "category", "brand", "is_featured")

    list_editable = ("status", "is_featured")
    inlines = [VariantInline]#sizes on product

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "label",
        "price_cents",
        "stock_on_hand",
        "stock_reserved",
        "is_active",
    )

    list_filter = ("is_active",)

    search_fields = ("product__name", "label")
    readonly_fields = ("stock_reserved",)