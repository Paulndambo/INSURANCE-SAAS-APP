from django.contrib import admin
from .models import User, Profile, PolicyHolderRelative, PolicyHolder, Membership, MembershipConfiguration, MembershipStatusUpdates

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role"]
admin.site.register(Profile)
admin.site.register(PolicyHolder)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "scheme_group", "policy"]


@admin.register(MembershipConfiguration)
class MembershipConfigurationAdmin(admin.ModelAdmin):
    list_display = ["id", "membership_id"]

admin.site.register(MembershipStatusUpdates)


@admin.register(PolicyHolderRelative)
class PolicyHolderRelativeAdmin(admin.ModelAdmin):
    list_display = ["id", "relative_name", "relative_key"]