from django.core.management.base import BaseCommand
from catalog.models import Brand, Category, Product, Variant

class Command(BaseCommand):
    help = "Seed demo catalog data"

    def handle(self, *args, **options):
        # --- 2 categories ---
        flower, _ = Category.objects.get_or_create(
            name="Flower",
            defaults = {"sort_order": 1, "limit_group": "flower"},
        )

        edibles, _ = Category.objects.get_or_create(
            name="Edibles",
            defaults = {"sort_order": 2, "limit_group": "none"},
        )

        # --- 2 brands ---
        grey_matter, _ = Brand.objects.get_or_create(name="Grey Matter")
        sunny, _ = Brand.objects.get_or_create(name="Sunny Farms")

        # --- 4 products, eachw ith 2 sizes
        products = [
            #(brand, category, name, slug, sizes)
            (grey_matter, flower, "Blue Dream", "grey-matter-blue-dream",
             [("3.5 g", 3.5, 3500), ("7 g", 7, 6500)]),

            (grey_matter, flower, "OG Kush", "grey-matter-og-kush",
             [("3.5 g", 3.5, 4000), ("7 g", 7, 7500)]),

            (sunny, edibles, "Mango Gummies", "sunny-farms-mango-gummies",
             [("10 pack", None, 2000), ("20 pack", None, 3600)]),

            (sunny, edibles, "Chocolar Bar", "sunny-farms-chocolate-bar",
             [("Single",None, 1800), ("3 Pack", None, 4800)]),
        ]

        for brand, category, name, slugs, sizes in products:
            #look up by slug; eveyrthing else goes in default

            product, _ = Product.objects.get_or_create(
                slug = slugs,
                defaults = {"brand": brand, "category": category, "name": name},
            )

            for label, grams, price in sizes:
                Variant.objects.get_or_create(
                    product = product,
                    label = label,
                    defaults = {
                        "weight_grams": grams,
                        "price_cents": price,
                        "stock_on_hand": 20,
                    },
                )

        self.stdout.write("Seeded")