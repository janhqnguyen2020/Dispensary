from ninja import Router

from django.db.models import Min, Q

from .models import Category, Brand, Product

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

@router.get("/products")
def list_products(request):
    products = Product.objects.filter(status="active").select_related("brand","category").annotate(from_price=Min("variants__price_cents",filter=Q(variants__is_active = True),)).order_by("name","id")

    return [
        {
            "slug": product.slug,
            "name": product.name,
            "brand": product.brand.name,
            "category": product.category.name,

            "from_price_cents": product.from_price,
            "strain_type": product.strain_type,
            "thc_value": product.thc_value,
            "cbd_value": product.cbd_value,
            "potency_unit": product.potency_unit,
            "image_url": product.image_url,
            "category_slug": product.category.slug,
        }

        for product in products
    ]