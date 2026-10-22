from django.test import TestCase

# Create your tests here.
from catalog.models import Brand, Category, Product, Variant


class ProductListTests(TestCase):
    def setUp(self):
        flower = Category.objects.create(name="Flower", limit_group="flower")
        edibles = Category.objects.create(name = "Edibles")
        grey = Brand.objects.create(name="Grey Matter")
        sunny = Brand.objects.create(name="Sunny Farms")

        self.blue = Product.objects.create(
            brand=grey, category = flower, name = "Blue Dream",
            strain_type = "Hybrid", effects = "Relaxed, Happy", is_featured = True,
        )

        self.og = Product.objects.create(
            brand=grey, category = flower, name="OG Kush", strain_type = "Indica",
        )

        Product.objects.create(brand =sunny, category = edibles, name = "Mango Gummies", summary = "Tropical fruit chews")
        Product.objects.create(brand = sunny, category = edibles, name = "Hidden Draft", status = "draft")

        Variant.objects.create(product = self.blue, label = "3.5 g", price_cents = 3500)
        Variant.objects.create(product = self.blue, label = "7 g", price_cents = 6500)
        Variant.objects.create(product = self.blue, label = "1 g", price_cents = 100, is_active = False)

        Variant.objects.create(product = self.og, label = "3.5 g", price_cents = 2500,)

    def names(self, params = None):
        response = self.client.get("/api/v1/products", params or {})
        self.assertEqual(response.status_code, 200)

        return sorted(product["name"] for product in response.json()["items"])

    def test_list_hides_drafts(self):
        self.assertEqual(self.names(), ["Blue Dream", "Mango Gummies", "OG Kush"])


    def test_search_by_name(self):
        self.assertEqual(self.names({"search":"blue"}), ["Blue Dream"])

    def test_search_by_brand(self):
        self.assertEqual(self.names({"search":"grey"}), ["Blue Dream", "OG Kush"])

    def test_search_by_summary(self):
        self.assertEqual(self.names({"search":"tropical"}), ["Mango Gummies"])

    def test_search_by_effects(self):
        self.assertEqual(self.names({"search":"happy"}), ["Blue Dream"])

    def test_search_no_match(self):
        self.assertEqual(self.names({"search":"nosuch123"}), [])

    def test_filter_category(self):
        self.assertEqual(self.names({"category":"flower"}),["Blue Dream", "OG Kush"])

    def test_filter_brand(self):
        self.assertEqual(self.names({"brand":"sunny-farms"}), ["Mango Gummies"])

    def test_filter_strain(self):
        self.assertEqual(self.names({"strain":"hybrid"}), ["Blue Dream"])

    def test_filter_featured(self):
        self.assertEqual(self.names({"featured":"true"}), ["Blue Dream"])

    def test_filters_combined(self):
        self.assertEqual(self.names({"category": "flower", "search":"kush"}), ["OG Kush"])

    def test_from_price_ignores_inactive_variants(self):
        response = self.client.get("/api/v1/products")
        data = response.json()["items"]

        blue = next(product for product in data if product["slug"] == "grey-matter-blue-dream")
        self.assertEqual(blue["from_price_cents"], 3500)

    def ordered_names(self, response):
        return [item["name"] for item in response.json()["items"]]

    def test_sort_price_asc(self):
        response = self.client.get("/api/v1/products", {"sort":"price_asc"},)

        self.assertEqual(response.status_code, 200)

        names = self.ordered_names(response)
        self.assertEqual(names[0], "OG Kush")

    def test_unknown_sort_falls_back_to_name(self):
        default_response = self.client.get("/api/v1/products")
        unknown_reponse = self.client.get("/api/v1/products", {"sort":"banana"},)

        self.assertEqual(
            self.ordered_names(unknown_reponse),
            self.ordered_names(default_response),
        )

    def test_pagination_metadata(self):
        response = self.client.get("/api/v1/products")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["pages"], 1)
        self.assertEqual(data["total"], 3)
        self.assertEqual(len(data["items"]), 3)

    def test_page_999_returns_last_page(self):
        response = self.client.get("/api/v1/products", {"page": 999},)

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["pages"], 1)
        self.assertEqual(data["total"], 3)

    def test_total_counts_filtred_results(self):
        response = self.client.get("/api/v1/products", {"category":"edibles"},)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["total"], 1)
        self.assertEqual(
            [item["name"] for item in data["items"]],
            ["Mango Gummies"],
        )

    def test_empty_catalog(self):
        Product.objects.all().delete()

        response = self.client.get("/api/v1/products")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["items"], [])
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["pages"], 1)
        self.assertEqual(data["total"], 0)