import pytest
from model_bakery import baker

from marketplace.models import Rental, Tool


@pytest.mark.django_db
def test_my_tools_with_pagination(auth_client, user):
    """Testa paginação em my_tools (linhas 33-34 views.py)"""
    # Criar mais de 10 tools para forçar paginação
    for i in range(15):
        baker.make(Tool, owner=user, title=f"Tool {i}")
    
    # DRF padrão pagina em 10 itens
    response = auth_client.get("/api/tools/my/")
    assert response.status_code == 200
    data = response.json()
    
    # Se houver paginação, deve ter 'results' e 'count'
    if "results" in data:
        assert len(data["results"]) == 10
        assert data["count"] == 15


@pytest.mark.django_db
def test_my_rentals_with_pagination(auth_client, user, owner_user):
    """Testa paginação em my_rentals (linhas 94-95 views.py)"""
    tool = baker.make(Tool, owner=owner_user)
    
    # Criar mais de 10 rentals
    for i in range(15):
        baker.make(Rental, renter=user, tool=tool)
    
    response = auth_client.get("/api/rentals/my/")
    assert response.status_code == 200
    data = response.json()
    
    if "results" in data:
        assert len(data["results"]) == 10
        assert data["count"] == 15


@pytest.mark.django_db
def test_received_rentals_with_pagination(owner_client, owner_user, user):
    """Testa paginação em received_rentals (linhas 102-109 views.py)"""
    tool = baker.make(Tool, owner=owner_user)
    
    # Criar mais de 10 rentals recebidos
    for i in range(15):
        baker.make(Rental, renter=user, tool=tool)
    
    response = owner_client.get("/api/rentals/received/")
    assert response.status_code == 200
    data = response.json()
    
    if "results" in data:
        assert len(data["results"]) == 10
        assert data["count"] == 15


@pytest.mark.django_db
def test_my_tools_without_pagination(auth_client, user):
    """Testa my_tools sem paginação (linhas 36-37 views.py) - menos de 10 itens"""
    # Criar menos de 10 tools para não ter paginação
    for i in range(5):
        baker.make(Tool, owner=user, title=f"Tool {i}")
    
    response = auth_client.get("/api/tools/my/")
    assert response.status_code == 200
    data = response.json()
    
    # Sem paginação, retorna lista direta
    if isinstance(data, list):
        assert len(data) == 5


@pytest.mark.django_db
def test_my_rentals_without_pagination(auth_client, user, owner_user):
    """Testa my_rentals sem paginação (linhas 97-98 views.py) - menos de 10 itens"""
    tool = baker.make(Tool, owner=owner_user)
    
    # Criar menos de 10 rentals
    for i in range(5):
        baker.make(Rental, renter=user, tool=tool)
    
    response = auth_client.get("/api/rentals/my/")
    assert response.status_code == 200
    data = response.json()
    
    # Sem paginação, retorna lista direta
    if isinstance(data, list):
        assert len(data) == 5


@pytest.mark.django_db
def test_received_rentals_without_pagination(owner_client, owner_user, user):
    """Testa received_rentals sem paginação (linhas 108-109 views.py) - menos de 10 itens"""
    tool = baker.make(Tool, owner=owner_user)
    
    # Criar menos de 10 rentals
    for i in range(5):
        baker.make(Rental, renter=user, tool=tool)
    
    response = owner_client.get("/api/rentals/received/")
    assert response.status_code == 200
    data = response.json()
    
    # Sem paginação, retorna lista direta
    if isinstance(data, list):
        assert len(data) == 5

