from django.db import models

from django.utils.text import slugify

# Create your models here.
class Brand(models.Model):

    name = models.CharField(max_length = 300, unique = True)
    slug = models.SlugField(max_length=200, unique = True, blank = True)

    def save(self, *args, **kwargs):

        #only gen slug when one has not been supplied
        if not self.slug:
            self.slug = slugify(self.name)

        #normal save, write obj to database
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    LIMIT_GROUP_CHOICES = [
        ("none", "None"),
        ("flower","Flower"),
        ("concentrate", "Concentrate"),
    ]

    name = models.CharField(max_length = 200, unique= True)
    slug = models.SlugField(max_length = 200, unique = True, blank = True)
    sort_order = models.PositiveIntegerField(default = 0)
    limit_group = models.CharField(
        max_length = 20, 
        choices = LIMIT_GROUP_CHOICES, 
        default = "none",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("archived", "Archived"),
    ]

    brand = models.ForeignKey(
        Brand,
        on_delete = models.PROTECT,
        related_name = "products",
    )

    category = models.ForeignKey(
        Category,
        on_delete = models.PROTECT,
        related_name = "products",
    )

    name = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 400, unique = True, blank = True)

    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = "active",
    )

    strain_type = models.CharField(max_length = 50, blank = True)
    thc_value = models.DecimalField(
        max_digits = 6, decimal_places = 2, null = True, blank = True
    )
    cbd_value = models.DecimalField(
        max_digits = 6, decimal_places = 2, null = True, blank = True
    )
    potency_unit = models.CharField(
        max_length = 2,
        choices = [("%","%"),("mg", "mg")],
        default="%",
    )
    summary = models.TextField(blank=True)
    effects = models.TextField(blank=True)
    image_url = models.URLField(blank = True)
    is_featured = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)

    @property
    def effects_list(self):
        return [effect.strip() for effect in self.effects.split(",") if effect.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    

class Variant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
        related_name = "variants",
    )

    label = models.CharField(max_length = 100)
    price_cents = models.PositiveIntegerField()
    stock_on_hand = models.PositiveIntegerField(default = 0)
    stock_reserved = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)

    @property
    def available(self):
        return max(0, self.stock_on_hand - self.stock_reserved)

    def __str__(self):
        return f"{self.product.name} - {self.label}"