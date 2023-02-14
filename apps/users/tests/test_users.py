from unittest import TestCase
from django.test import Client
from django.urls import reverse
from apps.uses.models import User, Profile, Membership, PolicyHolder, PolicyHolderRelative
import json
import pytest

users_url = reverse("users-list")
pytestmark = pytest.mark.django_db


def test_users_get_should_return_a_list(client):
    response = client.get(users_url)
    assert response.status_code == 200


