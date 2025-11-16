import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_returns_user_data():
    client = APIClient()
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="test@example.com",
    )

    response = client.post(
        "/api/auth/login/",
        {"username": "testuser", "password": "testpass123"},
        format="json",
    )

    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "user" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"


@pytest.mark.django_db
def test_login_invalid_credentials():
    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {"username": "invalid", "password": "wrong"},
        format="json",
    )

    assert response.status_code == 401

