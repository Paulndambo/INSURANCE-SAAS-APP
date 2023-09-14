from django.contrib import admin
from apps.core.models import Insurer
# Register your models here.
@admin.register(Insurer)
class InsurerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "website", "email", "city", "country"]