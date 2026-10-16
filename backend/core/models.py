from django.db import models

# Create your models here.

class StoreSettings(models.Model):
    
    store_name = models.CharField(max_length = 100, default = "Dispensary")
    hours = models.CharField(max_length = 200, default="Daily 9 AM - 9 PM")

    def __str__(self):
        return "Store Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk = 1)
        return obj