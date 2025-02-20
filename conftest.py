import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture()
def staff():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="user@test.com",
        password="testpass",
        is_staff=True,
    )


@pytest.fixture()
def client():
    """Return an instance of Django test client."""
    return Client()
