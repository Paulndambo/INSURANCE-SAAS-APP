from django.contrib import admin

from apps.entities.models import Brokerage, SalesAgent

# Register your models here.
admin.site.register(Brokerage)

@admin.register(SalesAgent)
class SalesAgentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "broker", "phone_number"]