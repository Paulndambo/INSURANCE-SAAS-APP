from rest_framework import serializers
from apps.schemes.models import Scheme, SchemeGroup


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = "__all__"


class SchemeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeGroup
        fields = "__all__"

    
