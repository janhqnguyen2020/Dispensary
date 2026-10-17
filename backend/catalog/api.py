from ninja import Router
from .models import Category, Brand

router = Router()

@router.get("/categories")
def list_categories(request):
    categories = Category.objects.all().order_by("sort_order","name")

    return [
        {
            "name": category.name,
            "slug": category.slug,
        }

        for category in categories
    ]

@router.get("/brands")
def list_brands(request):
    brands = Brand.objects.all().order_by("name")

    return [
        {
            "name": brand.name,
            "slug":brand.slug,
        }

        for brand in brands
    ]