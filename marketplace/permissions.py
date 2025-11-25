from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsToolOwnerOrReadOnly(BasePermission):
    """
    Permite leitura para todos os usuários autenticados,
    mas restringe escrita ao dono da ferramenta.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsRentalParticipant(BasePermission):
    """
    Garante que o usuário só consegue interagir com aluguéis
    nos quais ele é o locador ou dono da ferramenta.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.renter == request.user or obj.tool.owner == request.user

        # Para ações de aprovação/rejeição, apenas o owner da ferramenta
        if getattr(view, "action", None) in {"approve", "reject"}:
            return obj.tool.owner == request.user

        # Para ação de finalizar, owner ou renter podem finalizar
        if getattr(view, "action", None) == "finish":
            return obj.renter == request.user or obj.tool.owner == request.user

        return obj.renter == request.user
