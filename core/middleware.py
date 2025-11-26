"""
Middleware customizado para garantir que headers CORS sejam sempre enviados
"""
from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):
    """
    Middleware que força headers CORS para todas as requisições.
    Garante que funcionem mesmo se django-cors-headers tiver problemas.
    """

    def process_response(self, request, response):
        # Origem permitida (da variável de ambiente)
        import os
        allowed_origins_env = os.environ.get('CORS_ALLOWED_ORIGINS', '').strip()
        origin = request.META.get('HTTP_ORIGIN', '')

        # Se temos origem configurada
        if allowed_origins_env:
            # Remove barras finais e espaços
            allowed_list = [o.strip().rstrip('/') for o in allowed_origins_env.split(',') if o.strip()]

            # Se a origem da requisição está na lista de permitidas
            if origin in allowed_list:
                response['Access-Control-Allow-Origin'] = origin
            elif allowed_list:
                # Se não está na lista mas temos origens configuradas, usa a primeira
                # Isso permite que funcione mesmo se a origem não corresponder exatamente
                response['Access-Control-Allow-Origin'] = allowed_list[0]
        else:
            # Fallback para desenvolvimento (localhost)
            if origin and ('localhost' in origin or '127.0.0.1' in origin):
                response['Access-Control-Allow-Origin'] = origin

        # Headers CORS sempre presentes se tivermos origem configurada
        if 'Access-Control-Allow-Origin' in response:
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken, X-Requested-With'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Max-Age'] = '86400'  # 24 horas

        # Responde OPTIONS requests (preflight) com sucesso
        if request.method == 'OPTIONS':
            response.status_code = 200

        return response
