from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from model_bakery import baker
from rest_framework.test import APIClient

from marketplace.models import Tool

# Mock do Cloudinary para testes (evita upload real)
@pytest.fixture(autouse=True)
def mock_cloudinary():
    """Mock do Cloudinary para todos os testes - evita upload real"""
    import cloudinary

    # Configura o Cloudinary com valores fake para testes
    cloudinary.config(
        cloud_name='test',
        api_key='123456789012345',
        api_secret='test_secret'
    )

    # Mock do método upload_resource do Cloudinary que faz o upload real
    # Isso evita que o Cloudinary tente fazer upload real durante os testes
    with patch('cloudinary.uploader.upload_resource') as mock_upload_resource:
        # Retorna apenas o public_id como string (formato esperado pelo CloudinaryField)
        # O CloudinaryField armazena apenas o public_id no banco
        mock_upload_resource.return_value = 'tools/test_image_123'

        # Mock do descriptor __get__ do CloudinaryField para converter string em objeto com .url
        original_get = None
        try:
            from cloudinary.models import CloudinaryField

            # Salva o método original
            original_get = CloudinaryField.__get__

            def mock_get(self, instance, owner):
                # Chama o método original para obter o valor
                value = original_get(self, instance, owner)
                # Se retornou uma string (public_id do banco), converte em objeto com .url
                if isinstance(value, str) and value:
                    mock_resource = MagicMock()
                    mock_resource.public_id = value
                    mock_resource.url = f'https://res.cloudinary.com/test/image/upload/{value}'
                    mock_resource.__str__ = lambda: value
                    return mock_resource
                return value

            CloudinaryField.__get__ = mock_get
        except (ImportError, AttributeError):
            pass

        yield mock_upload_resource

        # Restaura o método original se foi modificado
        if original_get:
            try:
                from cloudinary.models import CloudinaryField
                CloudinaryField.__get__ = original_get
            except (ImportError, AttributeError):
                pass

# Configurar baker para lidar com CloudinaryField
def make_image():
    """Cria uma imagem fake para testes"""
    img = Image.new("RGB", (100, 100), color="red")
    img_io = BytesIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)
    return SimpleUploadedFile("test_tool.jpg", img_io.read(), content_type="image/jpeg")

# Configurar baker para usar imagem padrão quando photo não for especificado
baker.generators.add('cloudinary.models.CloudinaryField', make_image)


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
