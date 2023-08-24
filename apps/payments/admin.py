from django.contrib import admin
from apps.payments.models import PolicyPremium, PolicyPayment, BankStatement
# Register your models here.
admin.site.register(PolicyPremium)
admin.site.register(PolicyPayment)

@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    list_display = ["policy_number", "statement", "processed"]