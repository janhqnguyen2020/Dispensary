from decimal import Decimal, ROUND_HALF_UP

from catalog.models import Variant

from core.models import StoreSettings

def quote(items, mode, zip_code):
    settings = StoreSettings.load()

    if mode not in ("pickup", "delivery"):
        raise ValueError("Invalid Ordering Mode.")

    if not isinstance(items, list) or not items:
        raise ValueError("Cart must contain at least one item.")

    subtotal = 0#tracks combined item prices in cents, before taxes and delivery
    flower_grams = Decimal("0")
    concentrate_grams = Decimal("0")
    quote_items = []

    #validate quantities and combine duplicate variant IDs
    quantities = {}

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each cart item must be an object.")

        #extract values from dict using keys
        variant_id = item.get("variant_id")
        qty = item.get("qty")

        #make sure qty is pos, be an integer, no bool
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise ValueError("Quantity must be a positive integer.")

        #make sure id is an integer and not a bool
        if isinstance(variant_id, bool) or not isinstance(variant_id, int):
            raise ValueError("Invalid variant ID.")

        #combine duplicate variant ID
        quantities[variant_id] = quantities.get(variant_id, 0) + qty

    #DJANGO's ORM
    #retrive variants from db
    variants = Variant.objects.filter(
        id__in = quantities
    ).select_related("product", "product__category")

    #turn result into dictionary
    variants_by_id = {variant.id : variant for variant in variants}

    #reject nonexistent variants
    if set(quantities) != set(variants_by_id):
        raise ValueError("One or more variants do not exist.")

    #loop through real variants
    for variant_id, qty in quantities.items():
        variant = variants_by_id[variant_id]#actual variant

        product = variant.product
        category = product.category

        if not variant.is_active:
            raise ValueError(f"{variant.label} is inactive.")

        if product.status != "active":
            raise ValueError(f"{product.name} is not available.")

        if variant.available < qty:
            raise ValueError(f"Not enough stock for {variant.label}.")

        line_total = variant.price_cents * qty
        subtotal += line_total

        #weight limit
        if category.limit_group in ("flower", "concentrate"):
            if variant.weight_grams is None:
                raise ValueError(f"Weight is missing for {variant.label}.")

            weight = variant.weight_grams * qty

            if category.limit_group == "flower":
                flower_grams += weight
            else:
                concentrate_grams += weight

        quote_items.append({
            "variant_id": variant.id,
            "product": product.name,
            "variant": variant.label,
            "qty": qty,
            "until_price_cents": variant.price_cents,
            "line_total_Cents": variant.price_cents * qty,
        })

    if flower_grams > settings.flower_limit_grams:
        raise ValueError("Flower purchase limit exceeded.")

    if concentrate_grams > settings.concentrate_limit_grams:
        raise ValueError("Concentrate purchase limit exceeded.")

    delivery_fee = 0

    if mode == "delivery":
        if not settings.delivers_to(zip_code or ""):
            raise ValueError("Delivery is not available for this ZIP code.")

        if subtotal < settings.delivery_min_cents:
            raise ValueError("Cart does not meet the delivery minimum.")

        delivery_fee = settings.delivery_fee_cents

    tax_bps = settings.excise_tax_bps + settings.sales_tax_bps

    tax_cents = int(
        (Decimal(subtotal) * Decimal(tax_bps) / Decimal(10000)).quantize(Decimal("1"), rounding = ROUND_HALF_UP)
    )

    total = subtotal + tax_cents + delivery_fee

    return {
        "items": quote_items,
        "subtotal_cents": subtotal,
        "tax_cents": tax_cents,
        "delivery_fee_cents": delivery_fee,
        "total_cents": total,
        "flower_grams": str(flower_grams),
        "concentrate_grams": str(concentrate_grams),
    }
    


