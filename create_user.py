#!/usr/bin/env python
"""Script temporário para criar usuário no Railway"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do usuário - ALTERE AQUI
username = 'nitto'
email = 'nitto@exemplo.com'
password = 'senha123'

# Criar usuário normal (não superusuário)
if User.objects.filter(username=username).exists():
    print(f'Usuário {username} já existe!')
else:
    User.objects.create_user(username=username, email=email, password=password)
    print(f'Usuário {username} criado com sucesso!')

