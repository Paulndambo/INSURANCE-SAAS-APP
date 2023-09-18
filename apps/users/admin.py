from django.contrib import admin

from .models import (Membership, MembershipConfiguration,
                     MembershipStatusUpdates, PolicyHolder,
                     PolicyHolderRelative, Profile, User)


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "user", "id_number", "gender"]

admin.site.register(PolicyHolder)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "scheme_group", "policy", "membership_premium"]


@admin.register(MembershipConfiguration)
class MembershipConfigurationAdmin(admin.ModelAdmin):
    list_display = ["id", "membership_id", "beneficiary", "pricing_plan", "cover_level"]

admin.site.register(MembershipStatusUpdates)


@admin.register(PolicyHolderRelative)
class PolicyHolderRelativeAdmin(admin.ModelAdmin):
    list_display = ["id", "relative_name", "relative_key", "use_type"]