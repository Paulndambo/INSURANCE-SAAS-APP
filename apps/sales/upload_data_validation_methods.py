from apps.users.models import Profile, Membership, User
from apps.schemes.models import Scheme, SchemeGroup


def check_if_member_exists_on_the_plaftorm(identification_number: str, email: str):
    user = User.objects.get(email=email)

    membership = Membership.objects.get()
