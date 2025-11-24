from datetime import date, timedelta

import pytest
from model_bakery import baker

from marketplace.models import Rental, Tool


@pytest.mark.django_db
def test_create_rental_fails_with_past_date(auth_client, owner_user):
    """Testa que não é possível criar aluguel com data no passado"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    yesterday = date.today() - timedelta(days=1)
    
    payload = {
        "tool_id": tool.id,
        "start_date": yesterday.isoformat(),
        "end_date": date.today().isoformat(),
    }

    response = auth_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 400
    error_data = response.json()
    error_str = str(error_data).lower()
    assert "passado" in error_str or "past" in error_str


@pytest.mark.django_db
def test_create_rental_fails_with_date_conflict(auth_client, owner_user):
    """Testa que não é possível criar aluguel com conflito de datas"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    
    # Criar um aluguel aprovado existente
    existing_start = date.today() + timedelta(days=5)
    existing_end = date.today() + timedelta(days=10)
    baker.make(
        Rental,
        tool=tool,
        renter=owner_user,
        status="approved",
        start_date=existing_start,
        end_date=existing_end,
    )

    # Tentar criar outro aluguel que conflita (sobrepõe)
    new_start = date.today() + timedelta(days=7)  # Dentro do período existente
    new_end = date.today() + timedelta(days=12)
    
    payload = {
        "tool_id": tool.id,
        "start_date": new_start.isoformat(),
        "end_date": new_end.isoformat(),
    }

    response = auth_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 400
    error_data = response.json()
    error_str = str(error_data).lower()
    assert "conflito" in error_str or "período" in error_str or "conflict" in error_str


@pytest.mark.django_db
def test_create_rental_fails_with_pending_conflict(auth_client, owner_user):
    """Testa que conflito também é detectado com aluguéis pendentes"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    
    # Criar um aluguel pendente existente
    existing_start = date.today() + timedelta(days=5)
    existing_end = date.today() + timedelta(days=10)
    baker.make(
        Rental,
        tool=tool,
        renter=owner_user,
        status="pending",
        start_date=existing_start,
        end_date=existing_end,
    )

    # Tentar criar outro aluguel que conflita
    new_start = date.today() + timedelta(days=6)
    new_end = date.today() + timedelta(days=9)
    
    payload = {
        "tool_id": tool.id,
        "start_date": new_start.isoformat(),
        "end_date": new_end.isoformat(),
    }

    response = auth_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 400
    error_data = response.json()
    error_str = str(error_data).lower()
    assert "conflito" in error_str or "período" in error_str


@pytest.mark.django_db
def test_create_rental_allows_when_finished_rental_exists(auth_client, owner_user):
    """Testa que é possível criar aluguel mesmo com aluguel finalizado existente"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    
    # Criar um aluguel finalizado
    existing_start = date.today() + timedelta(days=5)
    existing_end = date.today() + timedelta(days=10)
    baker.make(
        Rental,
        tool=tool,
        renter=owner_user,
        status="finished",
        start_date=existing_start,
        end_date=existing_end,
    )

    # Deve ser possível criar novo aluguel no mesmo período (aluguel anterior já finalizou)
    new_start = date.today() + timedelta(days=5)
    new_end = date.today() + timedelta(days=10)
    
    payload = {
        "tool_id": tool.id,
        "start_date": new_start.isoformat(),
        "end_date": new_end.isoformat(),
    }

    response = auth_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_rental_allows_when_rejected_rental_exists(auth_client, owner_user):
    """Testa que é possível criar aluguel mesmo com aluguel rejeitado existente"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    
    # Criar um aluguel rejeitado
    existing_start = date.today() + timedelta(days=5)
    existing_end = date.today() + timedelta(days=10)
    baker.make(
        Rental,
        tool=tool,
        renter=owner_user,
        status="rejected",
        start_date=existing_start,
        end_date=existing_end,
    )

    # Deve ser possível criar novo aluguel no mesmo período
    new_start = date.today() + timedelta(days=5)
    new_end = date.today() + timedelta(days=10)
    
    payload = {
        "tool_id": tool.id,
        "start_date": new_start.isoformat(),
        "end_date": new_end.isoformat(),
    }

    response = auth_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 201

