from decimal import Decimal
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from PIL import Image

from marketplace.models import Tool


@pytest.mark.django_db
def test_create_tool_assigns_owner(auth_client, user):
    # Criar uma imagem válida
    img = Image.new("RGB", (100, 100), color="red")
    img_io = BytesIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)
    image = SimpleUploadedFile("tool.jpg", img_io.read(), content_type="image/jpeg")
    payload = {
        "title": "Martelete SDS",
        "description": "Ferramenta potente",
        "category": "construcao",
        "price_per_day": "120.00",
        "photo": image,
    }

    response = auth_client.post("/api/tools/", data=payload, format="multipart")

    assert response.status_code == 201
    data = response.json()
    assert data["owner"] == user.id
    tool = Tool.objects.get(id=data["id"])
    assert tool.owner == user


@pytest.mark.django_db
def test_my_tools_returns_only_owner_tools(auth_client, user, other_user):
    baker.make(Tool, owner=user, title="Minha Furadeira")
    baker.make(Tool, owner=other_user, title="Ferramenta de outro usuário")

    response = auth_client.get("/api/tools/my/")

    assert response.status_code == 200
    data = response.json()
    # Com paginação, pode vir em "results" ou direto como lista
    items = data.get("results", data) if isinstance(data, dict) else data
    titles = [item["title"] for item in items]
    assert "Minha Furadeira" in titles
    assert len(titles) == 1


@pytest.mark.django_db
def test_update_tool_denied_for_non_owner(auth_client, tool):
    response = auth_client.patch(
        f"/api/tools/{tool.id}/",
        data={"price_per_day": "200.00"},
    )

    assert response.status_code == 403
    tool.refresh_from_db()
    assert tool.price_per_day != Decimal("200.00")

