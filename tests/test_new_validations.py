"""
Testes para as novas validações implementadas conforme problemas.md
"""
from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from model_bakery import baker

from marketplace.models import Rental, Tool


@pytest.mark.django_db
def test_cannot_rent_own_tool(owner_client, owner_user):
    """Testa que não é possível alugar suas próprias ferramentas"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    payload = {
        "tool_id": tool.id,
        "start_date": today.isoformat(),
        "end_date": (today + timedelta(days=2)).isoformat(),
    }
    
    response = owner_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 400
    error_data = response.json()
    assert "tool_id" in error_data or "próprias" in str(error_data).lower() or "own" in str(error_data).lower()


@pytest.mark.django_db
def test_start_date_cannot_be_past(auth_client, owner_user):
    """Testa que data de início não pode ser no passado (normalizada para comparar apenas data)"""
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
    # Verificar se há erro relacionado a data passada
    assert "start_date" in error_data
    error_message = str(error_data["start_date"]).lower()
    assert "passado" in error_message or "past" in error_message or "datas" in error_message


@pytest.mark.django_db
def test_tool_remains_available_when_rental_created(auth_client, owner_user):
    """Testa que ferramenta permanece disponível quando aluguel é criado (status pending)"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    payload = {
        "tool_id": tool.id,
        "start_date": today.isoformat(),
        "end_date": (today + timedelta(days=2)).isoformat(),
    }

    response = auth_client.post("/api/rentals/", data=payload, format="json")

    assert response.status_code == 201
    tool.refresh_from_db()
    # Ferramenta deve permanecer disponível enquanto aluguel está pending
    assert tool.is_available is True


@pytest.mark.django_db
def test_tool_becomes_unavailable_when_rental_approved(owner_client, owner_user, user):
    """Testa que ferramenta fica indisponível quando aluguel é aprovado"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    # Criar aluguel pendente
    rental = baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="pending",
        start_date=today,
        end_date=today + timedelta(days=2),
    )
    
    # Aprovar aluguel
    response = owner_client.patch(f"/api/rentals/{rental.id}/approve/")
    
    assert response.status_code == 200
    tool.refresh_from_db()
    assert tool.is_available is False


@pytest.mark.django_db
def test_tool_becomes_available_when_rental_rejected(owner_client, owner_user, user):
    """Testa que ferramenta volta a ficar disponível quando aluguel é rejeitado"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    # Criar aluguel pendente
    rental = baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="pending",
        start_date=today,
        end_date=today + timedelta(days=2),
    )
    
    # Rejeitar aluguel
    response = owner_client.patch(f"/api/rentals/{rental.id}/reject/")
    
    assert response.status_code == 200
    tool.refresh_from_db()
    assert tool.is_available is True


@pytest.mark.django_db
def test_tool_becomes_available_when_rental_finished(owner_client, owner_user, user):
    """Testa que ferramenta volta a ficar disponível quando aluguel é finalizado"""
    tool = baker.make(Tool, owner=owner_user, is_available=False)
    today = timezone.now().date()
    
    # Criar aluguel aprovado
    rental = baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="approved",
        start_date=today,
        end_date=today + timedelta(days=2),
    )
    
    # Finalizar aluguel
    response = owner_client.patch(f"/api/rentals/{rental.id}/finish/")
    
    assert response.status_code == 200
    tool.refresh_from_db()
    assert tool.is_available is True


@pytest.mark.django_db
def test_cannot_delete_tool_with_active_rentals(owner_client, owner_user, user):
    """Testa que não é possível deletar ferramenta com aluguéis ativos ou pendentes"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    # Criar aluguel pendente
    baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="pending",
        start_date=today,
        end_date=today + timedelta(days=2),
    )
    
    # Tentar deletar ferramenta
    response = owner_client.delete(f"/api/tools/{tool.id}/")
    
    assert response.status_code == 409  # HTTP_409_CONFLICT
    error_data = response.json()
    assert "aluguéis" in str(error_data).lower() or "rentals" in str(error_data).lower()


@pytest.mark.django_db
def test_can_delete_tool_with_finished_rentals(owner_client, owner_user, user):
    """Testa que é possível deletar ferramenta quando todos os aluguéis estão finalizados"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    # Criar aluguel finalizado
    baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="finished",
        start_date=today - timedelta(days=5),
        end_date=today - timedelta(days=3),
    )
    
    # Deve ser possível deletar ferramenta
    response = owner_client.delete(f"/api/tools/{tool.id}/")
    
    assert response.status_code == 204  # No Content


@pytest.mark.django_db
def test_cannot_update_price_with_active_rentals(owner_client, owner_user, user):
    """Testa que não é possível alterar preço de ferramenta com aluguéis ativos"""
    tool = baker.make(Tool, owner=owner_user, price_per_day=Decimal("50.00"), is_available=True)
    today = timezone.now().date()
    
    # Criar aluguel pendente
    baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="pending",
        start_date=today,
        end_date=today + timedelta(days=2),
    )
    
    # Tentar alterar preço
    payload = {"price_per_day": "75.00"}
    response = owner_client.patch(f"/api/tools/{tool.id}/", data=payload, format="json")
    
    assert response.status_code == 400
    error_data = response.json()
    error_str = str(error_data).lower()
    assert "preço" in error_str or "price" in error_str
    assert "aluguéis" in error_str or "rentals" in error_str


@pytest.mark.django_db
def test_can_update_price_without_active_rentals(owner_client, owner_user):
    """Testa que é possível alterar preço quando não há aluguéis ativos"""
    tool = baker.make(Tool, owner=owner_user, price_per_day=Decimal("50.00"), is_available=True)
    
    # Tentar alterar preço (sem aluguéis ativos)
    payload = {"price_per_day": "75.00"}
    response = owner_client.patch(f"/api/tools/{tool.id}/", data=payload, format="json")
    
    assert response.status_code == 200
    tool.refresh_from_db()
    assert tool.price_per_day == Decimal("75.00")


@pytest.mark.django_db
def test_tool_availability_with_future_approved_rental(owner_client, owner_user, user):
    """Testa que ferramenta fica indisponível quando há aluguel aprovado futuro"""
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    future_date = date.today() + timedelta(days=5)
    
    # Criar aluguel aprovado futuro
    rental = baker.make(
        Rental,
        tool=tool,
        renter=user,
        status="pending",
        start_date=future_date,
        end_date=future_date + timedelta(days=2),
    )
    
    # Aprovar aluguel futuro
    response = owner_client.patch(f"/api/rentals/{rental.id}/approve/")
    
    assert response.status_code == 200
    tool.refresh_from_db()
    # Ferramenta deve ficar indisponível mesmo sendo futuro
    assert tool.is_available is False


@pytest.mark.django_db
def test_tool_availability_with_multiple_rentals(owner_client, owner_user, user, other_user):
    """Testa lógica de disponibilidade com múltiplos aluguéis"""
    from rest_framework.test import APIClient
    user_client = APIClient()
    user_client.force_authenticate(user=user)
    
    tool = baker.make(Tool, owner=owner_user, is_available=True)
    today = timezone.now().date()
    
    # Criar aluguel pendente via API (usando hoje como início para estar ativo)
    payload = {
        "tool_id": tool.id,
        "start_date": today.isoformat(),
        "end_date": (today + timedelta(days=2)).isoformat(),
    }
    response = user_client.post("/api/rentals/", data=payload, format="json")
    assert response.status_code == 201
    rental1_id = response.json()["id"]
    
    # Aprovar aluguel (isso deve atualizar a disponibilidade)
    response = owner_client.patch(f"/api/rentals/{rental1_id}/approve/")
    assert response.status_code == 200
    
    tool.refresh_from_db()
    assert tool.is_available is False
    
    # Finalizar aluguel ativo
    response = owner_client.patch(f"/api/rentals/{rental1_id}/finish/")
    assert response.status_code == 200
    
    tool.refresh_from_db()
    # Deve voltar a ficar disponível
    assert tool.is_available is True

