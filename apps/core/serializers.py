from rest_framework import serializers
from apps.core.models import Insurer

class InsurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = "__all__"