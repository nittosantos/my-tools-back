from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToolViewSet, RentalViewSet, me, create_user

router = DefaultRouter()
router.register(r'tools', ToolViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', me),
    path('auth/create-user/', create_user, name='create_user'),  # Temporário - remover depois
]
