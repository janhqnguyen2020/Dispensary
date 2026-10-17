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