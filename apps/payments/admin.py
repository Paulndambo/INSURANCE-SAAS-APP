from django.contrib import admin
from apps.payments.models import PolicyPremium, PolicyPayment, BankStatement, FuturePremiumTracking
# Register your models here.
@admin.register(PolicyPremium)
class PolicyPremiumAdmin(admin.ModelAdmin):
    list_display = ["id", "policy", "membership", "expected_date", "expected_payment", "amount_paid", "balance", "reference"]


admin.site.register(PolicyPayment)

@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    list_display = ["policy_number", "statement", "processed"]


@admin.register(FuturePremiumTracking)
class FuturePremiumTrackingAdmin(admin.ModelAdmin):
    list_display = ["policy", "membership", "processed"]