from django.contrib import admin
from .models import PolicyCancellation, Policy
# Register your models here.
admin.site.register(PolicyCancellation)
admin.site.register(Policy)