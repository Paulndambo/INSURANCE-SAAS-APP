from rest_framework import serializers

from apps.schemes.models import Scheme, SchemeGroup


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = "__all__"


class SchemeGroupSerializer(serializers.ModelSerializer):
    pricing_plan = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    group_premium = serializers.SerializerMethodField()

    class Meta:
        model = SchemeGroup
        fields = "__all__"


    def get_pricing_plan(self, obj):
        return obj.pricing_group.name

    def get_members_count(self, obj):
        return obj.schemegroupmembers.count()

    def get_group_premium(self, obj):
        return obj.policy.amount