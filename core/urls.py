from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

from marketplace.auth import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas do app marketplace
    path('api/', include('marketplace.urls')),

    # Rotas de autenticação JWT
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Configuração para arquivos de mídia (imagens)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
