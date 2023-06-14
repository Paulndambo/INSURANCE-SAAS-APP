from django.contrib import admin
from .models import User, Profile, PolicyHolderRelative, PolicyHolder, Membership, MembershipConfiguration, MembershipStatusUpdates

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(PolicyHolder)
admin.site.register(Membership)
admin.site.register(MembershipConfiguration)
admin.site.register(MembershipStatusUpdates)


@admin.register(PolicyHolderRelative)
class PolicyHolderRelativeAdmin(admin.ModelAdmin):
    list_display = ["id", "relative_name", "relative_key"]