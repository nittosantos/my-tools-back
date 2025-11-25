from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient

from marketplace.models import Tool


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="user_default",
        email="user@example.com",
        password="password123",
    )


@pytest.fixture
def owner_user(db) -> User:
    return User.objects.create_user(
        username="owner_default",
        email="owner@example.com",
        password="password123",
    )


@pytest.fixture
def other_user(db) -> User:
    return User.objects.create_user(
        username="other_default",
        email="other@example.com",
        password="password123",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def owner_client(api_client, owner_user):
    api_client.force_authenticate(user=owner_user)
    return api_client


@pytest.fixture
def other_client(api_client, other_user):
    api_client.force_authenticate(user=other_user)
    return api_client


@pytest.fixture
def tool(owner_user) -> Tool:
    return baker.make(Tool, owner=owner_user, is_available=True)


@pytest.fixture
def tool_factory(owner_user):
    def _factory(**kwargs):
        defaults = {"owner": owner_user}
        defaults.update(kwargs)
        return baker.make(Tool, **defaults)

    return _factory
