import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_me_endpoint_returns_user_data(auth_client, user):
    response = auth_client.get("/api/auth/me/")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["username"] == user.username
    assert data["email"] == user.email


@pytest.mark.django_db
def test_me_endpoint_requires_authentication(api_client):
    response = api_client.get("/api/auth/me/")

    assert response.status_code == 401

