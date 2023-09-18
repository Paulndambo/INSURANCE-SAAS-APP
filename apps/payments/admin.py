from django.contrib import admin

from apps.payments.models import (BankStatement, FuturePremiumTracking,
                                  MpesaResponseData, MpesaTransaction,
                                  PolicyPayment, PolicyPremium)

# Register your models here.
admin.site.register(MpesaResponseData)
admin.site.register(MpesaTransaction)

@admin.register(PolicyPremium)
class PolicyPremiumAdmin(admin.ModelAdmin):
    list_display = ["id", "policy", "membership", "expected_date", "expected_payment", "amount_paid", "balance", "reference", "status"]


@admin.register(PolicyPayment)
class PolicyPaymentAdmin(admin.ModelAdmin):
    list_display = ["policy", "membership", "premium", "state", "payment_date"]

@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    list_display = ["policy_number", "statement", "processed"]


@admin.register(FuturePremiumTracking)
class FuturePremiumTrackingAdmin(admin.ModelAdmin):
    list_display = ["policy", "membership", "processed"]