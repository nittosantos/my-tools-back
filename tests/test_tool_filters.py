import pytest
from model_bakery import baker

from marketplace.models import Tool


@pytest.mark.django_db
def test_filter_tools_by_category(auth_client, owner_user):
    """Testa filtro por categoria"""
    baker.make(Tool, owner=owner_user, category="construcao", title="Furadeira")
    baker.make(Tool, owner=owner_user, category="jardinagem", title="Cortador")
    baker.make(Tool, owner=owner_user, category="construcao", title="Martelete")

    response = auth_client.get("/api/tools/?category=construcao")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) == 2
    assert all(item["category"] == "construcao" for item in items)


@pytest.mark.django_db
def test_filter_tools_by_multiple_categories(auth_client, owner_user):
    """Testa filtro por múltiplas categorias"""
    baker.make(Tool, owner=owner_user, category="construcao", title="Furadeira")
    baker.make(Tool, owner=owner_user, category="jardinagem", title="Cortador")
    baker.make(Tool, owner=owner_user, category="pintura", title="Rolo")

    response = auth_client.get("/api/tools/?category=construcao&category=jardinagem")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) == 2
    categories = [item["category"] for item in items]
    assert "construcao" in categories
    assert "jardinagem" in categories
    assert "pintura" not in categories


@pytest.mark.django_db
def test_filter_tools_by_state(auth_client, owner_user):
    """Testa filtro por estado"""
    baker.make(Tool, owner=owner_user, state="SP", title="Ferramenta SP")
    baker.make(Tool, owner=owner_user, state="RJ", title="Ferramenta RJ")
    baker.make(Tool, owner=owner_user, state="SP", title="Outra SP")

    response = auth_client.get("/api/tools/?state=SP")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) == 2
    assert all(item["state"] == "SP" for item in items)


@pytest.mark.django_db
def test_filter_tools_by_city(auth_client, owner_user):
    """Testa filtro por cidade (busca parcial)"""
    baker.make(Tool, owner=owner_user, city="São Paulo", title="Ferramenta 1")
    baker.make(Tool, owner=owner_user, city="São Bernardo", title="Ferramenta 2")
    baker.make(Tool, owner=owner_user, city="Rio de Janeiro", title="Ferramenta 3")

    response = auth_client.get("/api/tools/?city=São")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) == 2
    assert all("São" in item["city"] for item in items)


@pytest.mark.django_db
def test_search_tools_by_text(auth_client, owner_user):
    """Testa busca textual em título e descrição"""
    baker.make(Tool, owner=owner_user, title="Furadeira Elétrica", description="Potente")
    baker.make(Tool, owner=owner_user, title="Martelete", description="Furadeira profissional")
    baker.make(Tool, owner=owner_user, title="Serra", description="Corta madeira")

    response = auth_client.get("/api/tools/?search=furadeira")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) == 2
    # Verifica que pelo menos um dos campos contém "furadeira"
    for item in items:
        assert "furadeira" in item["title"].lower() or "furadeira" in item["description"].lower()


@pytest.mark.django_db
def test_order_tools_by_price(auth_client, owner_user):
    """Testa ordenação por preço"""
    from decimal import Decimal
    
    tool1 = baker.make(Tool, owner=owner_user, price_per_day=Decimal("100.00"))
    tool2 = baker.make(Tool, owner=owner_user, price_per_day=Decimal("50.00"))
    tool3 = baker.make(Tool, owner=owner_user, price_per_day=Decimal("75.00"))

    response = auth_client.get("/api/tools/?ordering=price_per_day")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    prices = [float(item["price_per_day"]) for item in items]
    assert prices == sorted(prices)


@pytest.mark.django_db
def test_order_tools_by_price_desc(auth_client, owner_user):
    """Testa ordenação por preço decrescente"""
    from decimal import Decimal
    
    tool1 = baker.make(Tool, owner=owner_user, price_per_day=Decimal("100.00"))
    tool2 = baker.make(Tool, owner=owner_user, price_per_day=Decimal("50.00"))
    tool3 = baker.make(Tool, owner=owner_user, price_per_day=Decimal("75.00"))

    response = auth_client.get("/api/tools/?ordering=-price_per_day")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    prices = [float(item["price_per_day"]) for item in items]
    assert prices == sorted(prices, reverse=True)


@pytest.mark.django_db
def test_combine_filters(auth_client, owner_user):
    """Testa combinação de múltiplos filtros"""
    baker.make(Tool, owner=owner_user, category="construcao", state="SP", city="São Paulo")
    baker.make(Tool, owner=owner_user, category="construcao", state="RJ", city="Rio de Janeiro")
    baker.make(Tool, owner=owner_user, category="jardinagem", state="SP", city="São Paulo")

    response = auth_client.get("/api/tools/?category=construcao&state=SP")

    assert response.status_code == 200
    data = response.json()
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) == 1
    assert items[0]["category"] == "construcao"
    assert items[0]["state"] == "SP"

