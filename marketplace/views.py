from decimal import Decimal

from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Tool, Rental
from .permissions import IsToolOwnerOrReadOnly, IsRentalParticipant
from .serializers import (
    ToolSerializer,
    RentalSerializer,
    RentalCreateSerializer,
)


class ToolViewSet(ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [IsAuthenticated, IsToolOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtro por categoria (suporta múltiplas categorias)
        categories = self.request.query_params.getlist("category")
        if categories:
            queryset = queryset.filter(category__in=categories)

        # Filtro por estado (UF)
        state = self.request.query_params.get("state")
        if state:
            queryset = queryset.filter(state__iexact=state)

        # Filtro por cidade (busca parcial, case-insensitive)
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Busca textual em título e descrição (param search)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Ordenação (created_at, price_per_day)
        ordering = self.request.query_params.get("ordering")
        if ordering in ["created_at", "-created_at", "price_per_day", "-price_per_day"]:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my_tools(self, request):
        queryset = self.get_queryset().filter(owner=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated, IsRentalParticipant]

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.select_related("tool", "renter", "tool__owner").filter(
            Q(renter=user) | Q(tool__owner=user)
        )

    def get_serializer_class(self):
        if self.action == "create":
            return RentalCreateSerializer
        return RentalSerializer

    def perform_create(self, serializer):
        tool = serializer.validated_data["tool"]
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]

        if not tool.is_available:
            raise ValidationError("Esta ferramenta não está disponível para aluguel.")

        if end_date < start_date:
            raise ValidationError("A data final deve ser maior ou igual à data inicial.")

        days = (end_date - start_date).days + 1
        if days <= 0:
            raise ValidationError("Período de aluguel inválido.")

        total_price = (tool.price_per_day or Decimal("0")) * days

        tool.is_available = False
        tool.save(update_fields=["is_available"])

        serializer.save(
            renter=self.request.user,
            total_price=total_price,
        )

    def _ensure_tool_owner(self, rental, user):
        if rental.tool.owner != user:
            raise PermissionDenied("Você não tem permissão para alterar este aluguel.")

    def _ensure_pending(self, rental):
        if rental.status != "pending":
            raise ValidationError("Apenas aluguéis pendentes podem ser alterados.")

    @action(detail=False, methods=["get"], url_path="my")
    def my_rentals(self, request):
        queryset = self.get_queryset().filter(renter=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="received")
    def received_rentals(self, request):
        queryset = self.get_queryset().filter(tool__owner=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def approve(self, request, pk=None):
        rental = self.get_object()
        self._ensure_tool_owner(rental, request.user)
        self._ensure_pending(rental)

        rental.status = "approved"
        rental.tool.is_available = False
        rental.tool.save(update_fields=["is_available"])
        rental.save(update_fields=["status"])

        serializer = self.get_serializer(rental)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):
        rental = self.get_object()
        self._ensure_tool_owner(rental, request.user)
        self._ensure_pending(rental)

        rental.status = "rejected"
        rental.tool.is_available = True
        rental.tool.save(update_fields=["is_available"])
        rental.save(update_fields=["status"])

        serializer = self.get_serializer(rental)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })