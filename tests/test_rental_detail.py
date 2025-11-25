import pytest
from model_bakery import baker

from marketplace.models import Rental, Tool


@pytest.mark.django_db
def test_get_rental_detail_by_renter(auth_client, owner_user, user):
    """Testa que o renter pode ver detalhes do seu aluguel"""
    tool = baker.make(Tool, owner=owner_user)
    rental = baker.make(Rental, tool=tool, renter=user)

    response = auth_client.get(f"/api/rentals/{rental.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == rental.id
    assert data["tool"] == tool.id
    assert data["renter"] == user.id
    assert "tool_details" in data


@pytest.mark.django_db
def test_get_rental_detail_by_owner(owner_client, owner_user, user):
    """Testa que o owner da ferramenta pode ver detalhes do aluguel"""
    tool = baker.make(Tool, owner=owner_user)
    rental = baker.make(Rental, tool=tool, renter=user)

    response = owner_client.get(f"/api/rentals/{rental.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == rental.id
    assert data["tool"] == tool.id
    assert data["renter"] == user.id


@pytest.mark.django_db
def test_get_rental_detail_denied_for_non_participant(other_client, owner_user, user):
    """Testa que apenas participantes podem ver o aluguel"""
    tool = baker.make(Tool, owner=owner_user)
    rental = baker.make(Rental, tool=tool, renter=user)

    # other_user não é owner nem renter
    response = other_client.get(f"/api/rentals/{rental.id}/")

    assert response.status_code == 404  # DRF retorna 404 para não expor existência


@pytest.mark.django_db
def test_get_rental_detail_not_found(auth_client):
    """Testa que retorna 404 para aluguel inexistente"""
    response = auth_client.get("/api/rentals/99999/")

    assert response.status_code == 404
