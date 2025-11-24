from decimal import Decimal

import pytest
from model_bakery import baker

from marketplace.models import Tool


@pytest.mark.django_db
def test_get_tool_detail(auth_client, owner_user):
    """Testa que é possível obter detalhes de uma ferramenta"""
    tool = baker.make(
        Tool,
        owner=owner_user,
        title="Furadeira Elétrica",
        description="Furadeira potente",
        category="construcao",
        price_per_day=Decimal("50.00"),
    )

    response = auth_client.get(f"/api/tools/{tool.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tool.id
    assert data["title"] == "Furadeira Elétrica"
    assert data["description"] == "Furadeira potente"
    assert data["category"] == "construcao"
    assert data["price_per_day"] == "50.00"
    assert data["owner"] == owner_user.id


@pytest.mark.django_db
def test_get_tool_detail_not_found(auth_client):
    """Testa que retorna 404 para ferramenta inexistente"""
    response = auth_client.get("/api/tools/99999/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_tool_by_owner(owner_client, owner_user):
    """Testa que o owner pode deletar sua ferramenta"""
    tool = baker.make(Tool, owner=owner_user)

    response = owner_client.delete(f"/api/tools/{tool.id}/")

    assert response.status_code == 204
    assert not Tool.objects.filter(id=tool.id).exists()


@pytest.mark.django_db
def test_delete_tool_denied_for_non_owner(auth_client, tool):
    """Testa que apenas o owner pode deletar a ferramenta"""
    tool_id = tool.id

    response = auth_client.delete(f"/api/tools/{tool_id}/")

    assert response.status_code == 403
    assert Tool.objects.filter(id=tool_id).exists()  # Ferramenta ainda existe


@pytest.mark.django_db
def test_delete_tool_not_found(owner_client):
    """Testa que retorna 404 ao tentar deletar ferramenta inexistente"""
    response = owner_client.delete("/api/tools/99999/")

    assert response.status_code == 404

