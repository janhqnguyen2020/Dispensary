from django.db import models

# Create your models here.

class StoreSettings(models.Model):
    
    store_name = models.CharField(max_length = 100, default = "Dispensary")
    hours = models.CharField(max_length = 200, default="Daily 9 AM - 9 PM")

    #store info
    license_number = models.CharField(max_length = 200, default="")
    store_address = models.CharField(max_length = 300, default="")
    store_latitude = models.DecimalField(max_digits = 9, decimal_places = 6, default = 0)
    store_longitude = models.DecimalField(max_digits = 9, decimal_places = 6, default = 0)
    instagram_handle = models.CharField(max_length = 100, default="")
    owner_email = models.EmailField(default="")

    #mode
    ORDERING_MODE_CHOICES = [
        ("demo", "Demo"),
        ("live", "Live")
    ]

    ordering_mode = models.CharField(
        max_length = 15,
        choices = ORDERING_MODE_CHOICES,
        default="demo",
    )

    #money
    excise_tax_bps = models.PositiveIntegerField(default = 1500)
    sales_tax_bps = models.PositiveIntegerField(default = 775)
    delivery_fee_cents = models.PositiveIntegerField(default = 500)
    delivery_min_cents = models.PositiveIntegerField(default = 5000)


    def __str__(self):
        return "Store Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk = 1)
        return obj