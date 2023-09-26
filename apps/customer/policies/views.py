from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.customer.policies.serializers import CustomerPolicySerializer
from apps.policies.models import Policy, PolicyStatusUpdates
from apps.schemes.models import SchemeGroup


class CustomerPolicyViewSet(ModelViewSet):
    queryset = Policy.objects.select_related("schemegroups").all()
    serializer_class = CustomerPolicySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_serializer_context(self):
        return {"request": self.request }

    def get_queryset(self):
        user = self.request.user

        if user.role == "individual":
            scheme_group_ids = list(user.usermembership.values_list('scheme_group_id', flat=True))
            scheme_groups = SchemeGroup.objects.filter(id__in=scheme_group_ids).values_list('policy_id', flat=True)

            return self.queryset.filter(id__in=scheme_groups)
        return []