from django.contrib import admin
from apps.dependents.models import Dependent, Beneficiary
# Register your models here.
admin.site.register(Dependent)
admin.site.register(Beneficiary)
