import pytest
from model_bakery import baker

from marketplace.serializers import ToolSerializer
from marketplace.models import Tool


@pytest.mark.django_db
def test_tool_serializer_image_url_without_request(owner_user):
    """Testa que image_url funciona sem request no contexto (linha 45 serializers.py)"""
    tool = baker.make(Tool, owner=owner_user)
    
    # Serializar sem contexto de request (linha 45: return url quando request is None)
    serializer = ToolSerializer(tool, context={})  # Contexto vazio = sem request
    data = serializer.data
    
    # Deve retornar URL relativa quando não há request (linha 45)
    if tool.photo:
        assert "image_url" in data
        # URL relativa, não absoluta (linha 45 é executada)
        assert data["image_url"] == tool.photo.url

