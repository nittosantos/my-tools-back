import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_refresh_token_returns_new_access_token():
    """Testa que o refresh token retorna um novo access token"""
    client = APIClient()
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="test@example.com",
    )

    # Primeiro fazer login para obter tokens
    login_response = client.post(
        "/api/auth/login/",
        {"username": "testuser", "password": "testpass123"},
        format="json",
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access" in login_data
    assert "refresh" in login_data

    refresh_token = login_data["refresh"]

    # Usar refresh token para obter novo access token
    refresh_response = client.post(
        "/api/auth/refresh/",
        {"refresh": refresh_token},
        format="json",
    )

    assert refresh_response.status_code == 200
    refresh_data = refresh_response.json()
    assert "access" in refresh_data
    assert refresh_data["access"] != login_data["access"]  # Deve ser diferente


@pytest.mark.django_db
def test_refresh_token_with_invalid_token():
    """Testa que refresh token inválido retorna erro"""
    client = APIClient()

    response = client.post(
        "/api/auth/refresh/",
        {"refresh": "invalid_token"},
        format="json",
    )

    assert response.status_code == 401

