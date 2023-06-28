from django.contrib import admin
from apps.sales.models import TemporaryMemberData
# Register your models here.
@admin.register(TemporaryMemberData)
class TemporaryMemberDataAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "firstname", "lastname", "product", "processed"]
    filter_list = ["processed",]