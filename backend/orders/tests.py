from django.test import TestCase

from decimal import Decimal

from catalog.models import Brand, Category, Product, Variant
from core.models import StoreSettings
from orders.pricing import quote

class PricingTests(TestCase):
    def setUp(self):
        #set up predictable store pricing rules for every test.
        StoreSettings.objects.create(
            pk = 1,
            excise_tax_bps = 1500,
            sales_tax_bps = 775,
            delivery_fee_cents = 500,
            delivery_min_cents = 5000,
            delivery_zips = "92618",
            flower_limit_grams = Decimal("28.5"),
            concentrate_limit_grams = Decimal("8.0"),
        )

        self.brand = Brand.objects.create(
            name="Test Brand"
        )

        self.category = Category.objects.create(
            name="Test Category",
            limit_group = "none",
        )

        self.product = Product.objects.create(
            brand = self.brand,
            category = self.category,
            name="Test Product",
            status = "active",
        )

        self.variant = Variant.objects.create(
            product = self.product,
            label="3.5g",
            price_cents = 6000,
            stock_on_hand = 10,
            stock_reserved = 0,
            is_active = True,
        )

    def test_valid_pickup_quote(self):
        result = quote(
            items = [
                {
                    "variant_id": self.variant.id,
                    "qty": 1,
                }
            ],
            mode = "pickup",
            zip_code = "",
        )

        self.assertEqual(result["subtotal_cents"], 6000)
        self.assertEqual(result["tax_cents"], 1365)
        self.assertEqual(result["delivery_fee_cents"], 0)
        self.assertEqual(result["total_cents"], 7365)

    def test_insufficient_stock_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(
                items=[
                    {
                        "variant_id": self.variant.id,
                        "qty": 11,
                    }
                ],
                mode="pickup",
                zip_code="",
            )

    def test_invalid_variant_id_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(
                items=[
                    {
                        "variant_id": 999999,
                        "qty": 1,
                    }
                ],
                mode="pickup",
                zip_code="",
            )

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(
                items=[
                    {
                        "variant_id": self.variant.id,
                        "qty": 0,
                    }
                ],
                mode="pickup",
                zip_code="",
            )

    def test_unsupported_delivery_zip_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(
                items=[
                    {
                        "variant_id": self.variant.id,
                        "qty": 1,
                    }
                ],
                mode="delivery",
                zip_code="99999",
            )
