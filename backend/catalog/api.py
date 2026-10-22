from ninja import Router

from django.db.models import Min, Q, F

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
def list_products(
    request,
    category: str = None,
    brand: str = None,
    strain: str = None,
    featured: bool = None,
    search: str = None,
    sort: str = "name",
    ):
    #start with active products and calc lowest active variant
    products = Product.objects.filter(status="active").select_related("brand","category").annotate(
        from_price=Min(
            "variants__price_cents",
            filter=Q(variants__is_active = True),
            ))

    if category:
        products = products.filter(category__slug = category)

    if brand:
        products = products.filter(brand__slug = brand)

    if strain:
        products = products.filter(strain_type__iexact = strain)

    #only filter hwen user explicitly provide strue or false
    if featured is not None:
        products = products.filter(is_featured = featured)

    #search across product name, brand, summary, effects
    if search:
        products = products.filter(
            Q(name__icontains = search) | Q(brand__name__icontains = search)
            | Q(summary__icontains = search) | Q(effects__icontains = search)
        )

    #maps each supported option to db ordering fields
    sort_options = {
        "price_asc": (F("from_price").asc(nulls_last = True), "name"),
        "price_desc": (F("-from_price").desc(nulls_last=True), "name"),
        "newest": ("-created_at", "name"),
        "name": ("name", "id"),
    }

    #unpacks tuple and falls back to alphabetical ordering if error
    products = products.order_by(*sort_options.get(sort, sort_options["name"]))

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