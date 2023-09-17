from django.contrib import admin

from apps.pet_insure.models import Pet, PetBreed


# Register your models here.
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "pet_type", "size", "color", "breed", "policy", "scheme_group", "owner"]

admin.site.register(PetBreed)