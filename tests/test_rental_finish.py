from datetime import date, timedelta

import pytest
from model_bakery import baker

from marketplace.models import Rental, Tool


@pytest.mark.django_db
def test_owner_can_finish_rental(owner_client, owner_user, user):
    """Testa que o owner da ferramenta pode finalizar um aluguel aprovado"""
    tool = baker.make(Tool, owner=owner_user, is_available=False)
    rental = baker.make(Rental, tool=tool, renter=user, status="approved")

    response = owner_client.patch(f"/api/rentals/{rental.id}/finish/")

    assert response.status_code == 200
    rental.refresh_from_db()
    assert rental.status == "finished"
    tool.refresh_from_db()
    assert tool.is_available is True


@pytest.mark.django_db
def test_renter_can_finish_rental(auth_client, owner_user, user):
    """Testa que o renter também pode finalizar um aluguel aprovado"""
    tool = baker.make(Tool, owner=owner_user, is_available=False)
    rental = baker.make(Rental, tool=tool, renter=user, status="approved")

    response = auth_client.patch(f"/api/rentals/{rental.id}/finish/")

    assert response.status_code == 200
    rental.refresh_from_db()
    assert rental.status == "finished"
    tool.refresh_from_db()
    assert tool.is_available is True


@pytest.mark.django_db
def test_finish_rental_denied_for_non_participant(auth_client, owner_user, user, other_user):
    """Testa que apenas owner ou renter podem finalizar"""
    tool = baker.make(Tool, owner=owner_user)
    rental = baker.make(Rental, tool=tool, renter=user, status="approved")

    # other_user não é owner nem renter
    response = auth_client.patch(f"/api/rentals/{rental.id}/finish/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_finish_rental_fails_when_not_approved(owner_client, owner_user, user):
    """Testa que apenas aluguéis aprovados podem ser finalizados"""
    tool = baker.make(Tool, owner=owner_user)
    
    # Testar com status pending
    rental_pending = baker.make(Rental, tool=tool, renter=user, status="pending")
    response = owner_client.patch(f"/api/rentals/{rental_pending.id}/finish/")
    assert response.status_code == 400
    error_data = response.json()
    error_str = str(error_data).lower()
    assert "aprovado" in error_str or "approved" in error_str

    # Testar com status rejected
    rental_rejected = baker.make(Rental, tool=tool, renter=user, status="rejected")
    response = owner_client.patch(f"/api/rentals/{rental_rejected.id}/finish/")
    assert response.status_code == 400

    # Testar com status finished
    rental_finished = baker.make(Rental, tool=tool, renter=user, status="finished")
    response = owner_client.patch(f"/api/rentals/{rental_finished.id}/finish/")
    assert response.status_code == 400

