from django.contrib import admin

from .models import StoreSettings

# Register your models here.
#admin.site.register(StoreSettings) replaced down below
@admin.register(StoreSettings)

#custom admin config
class StoreSettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False