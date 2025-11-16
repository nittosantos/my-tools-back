# 🛠️ Marketplace de Aluguel de Ferramentas - Backend

Backend desenvolvido em Django + Django REST Framework para o sistema de marketplace de aluguel de ferramentas.

## 🚀 Stack Tecnológica

- **Django 5.2** - Framework web Python
- **Django REST Framework (DRF)** - API REST
- **SimpleJWT** - Autenticação JWT
- **SQLite** - Banco de dados (desenvolvimento)
- **Pillow** - Manipulação de imagens
- **pytest** + **pytest-django** - Testes unitários
- **pytest-cov** - Cobertura de testes
- **model-bakery** - Geração de dados de teste

## 📋 Funcionalidades

### ✅ Autenticação
- Login com JWT (access + refresh tokens)
- Endpoint `/api/auth/login/` para autenticação
- Endpoint `/api/auth/me/` para obter dados do usuário autenticado
- Tokens com validade configurável (access: 12h, refresh: 7 dias)

### 🛠️ Ferramentas (Tools)
- **CRUD completo** via `ModelViewSet`
- **Listagem pública** (`GET /api/tools/`) - Todas as ferramentas disponíveis
- **Listagem do usuário** (`GET /api/tools/my/`) - Ferramentas do usuário autenticado
- **Criar ferramenta** (`POST /api/tools/`) - Com upload de imagem
- **Editar ferramenta** (`PATCH /api/tools/:id/`) - Apenas o dono pode editar
- **Deletar ferramenta** (`DELETE /api/tools/:id/`) - Apenas o dono pode deletar
- **Visualizar detalhes** (`GET /api/tools/:id/`)

### 🔍 Filtros e Paginação
- **Filtro por categoria** - `GET /api/tools/?category=construcao` (suporta múltiplas)
- **Filtro por estado** - `GET /api/tools/?state=SP`
- **Filtro por cidade** - `GET /api/tools/?city=São Paulo`
- **Paginação** - 10 itens por página (configurável)
- **Combinação de filtros** - `GET /api/tools/?category=construcao&state=SP&city=São Paulo&page=1`

### 📦 Aluguéis (Rentals)
- **Criar aluguel** (`POST /api/rentals/`) - Com validações:
  - Ferramenta deve estar disponível
  - Datas válidas (fim >= início)
  - Cálculo automático do preço total
  - Bloqueio automático da ferramenta durante o período
- **Listar meus aluguéis** (`GET /api/rentals/my/`) - Aluguéis criados pelo usuário
- **Listar aluguéis recebidos** (`GET /api/rentals/received/`) - Solicitações para minhas ferramentas
- **Aprovar aluguel** (`PATCH /api/rentals/:id/approve/`) - Apenas o dono da ferramenta
- **Rejeitar aluguel** (`PATCH /api/rentals/:id/reject/`) - Apenas o dono da ferramenta
- **Status do aluguel**: `pending`, `approved`, `rejected`, `finished`

### 🏷️ Categorias
O sistema suporta as seguintes categorias de ferramentas:
- Construção
- Jardinagem
- Cozinha
- Oficina Mecânica
- Limpeza
- Elétrica
- Hidráulica
- Pintura
- Ferramentas Manuais
- Ferramentas Elétricas
- Automotiva
- Eventos
- Mudança
- Outros

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.10+
- pip
- virtualenv (recomendado)

### Passos

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd my_tools_back
```

2. **Crie e ative um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

**Nota:** Se não houver `requirements.txt`, instale manualmente:
```bash
pip install django djangorestframework djangorestframework-simplejwt Pillow pytest pytest-django pytest-cov model-bakery
```

4. **Execute as migrations**
```bash
python manage.py migrate
```

5. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

6. **Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000`

## 📁 Estrutura do Projeto

```
my_tools_back/
├── core/                 # Configurações do Django
│   ├── settings.py      # Configurações principais
│   ├── urls.py          # URLs principais
│   └── wsgi.py
├── marketplace/         # App principal
│   ├── models.py        # Modelos (Tool, Rental)
│   ├── views.py         # ViewSets e endpoints
│   ├── serializers.py   # Serializers DRF
│   ├── permissions.py   # Permissões customizadas
│   ├── auth.py          # View de login customizada
│   ├── urls.py          # Rotas da API
│   ├── admin.py         # Configuração do admin
│   └── migrations/      # Migrations do banco
├── tests/               # Testes unitários
│   ├── conftest.py      # Fixtures do pytest
│   ├── test_models.py
│   ├── test_views.py
│   └── ...
├── media/               # Arquivos de mídia (imagens)
├── manage.py
├── pytest.ini           # Configuração do pytest
└── db.sqlite3           # Banco de dados SQLite
```

## 🧪 Testes

O projeto utiliza `pytest` para testes unitários com cobertura.

### Executar todos os testes
```bash
# Usando o Python do venv
venv\Scripts\python.exe -m pytest

# Ou se o venv estiver ativo
pytest
```

### Executar testes com cobertura
```bash
venv\Scripts\python.exe -m pytest --cov=marketplace --cov-report=html
```

### Ver relatório de cobertura
Após executar com `--cov-report=html`, abra `htmlcov/index.html` no navegador.

### Cobertura Atual
- **95.22%** de cobertura de código
- Todos os modelos, views, serializers e permissions testados

## 📡 Endpoints da API

### Autenticação
- `POST /api/auth/login/` - Login (retorna access + refresh tokens)
- `GET /api/auth/me/` - Dados do usuário autenticado

### Ferramentas
- `GET /api/tools/` - Listar todas (com filtros e paginação)
- `GET /api/tools/my/` - Listar minhas ferramentas
- `GET /api/tools/:id/` - Detalhes de uma ferramenta
- `POST /api/tools/` - Criar ferramenta (multipart/form-data)
- `PATCH /api/tools/:id/` - Editar ferramenta
- `DELETE /api/tools/:id/` - Deletar ferramenta

### Aluguéis
- `GET /api/rentals/` - Listar aluguéis (do usuário ou recebidos)
- `GET /api/rentals/my/` - Listar meus aluguéis
- `GET /api/rentals/received/` - Listar aluguéis recebidos
- `POST /api/rentals/` - Criar aluguel
- `PATCH /api/rentals/:id/approve/` - Aprovar aluguel
- `PATCH /api/rentals/:id/reject/` - Rejeitar aluguel

## 🔐 Autenticação

Todas as rotas (exceto login) requerem autenticação via JWT.

**Header necessário:**
```
Authorization: Bearer <access_token>
```

**Exemplo de requisição:**
```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/tools/
```

## 📊 Modelos de Dados

### Tool (Ferramenta)
- `id` - ID único
- `owner` - Usuário dono (ForeignKey)
- `title` - Título
- `description` - Descrição
- `category` - Categoria (choices)
- `price_per_day` - Preço por dia
- `photo` - Foto (ImageField)
- `state` - Estado (UF)
- `city` - Cidade
- `is_available` - Disponível para aluguel
- `created_at` - Data de criação

### Rental (Aluguel)
- `id` - ID único
- `tool` - Ferramenta alugada (ForeignKey)
- `renter` - Usuário que está alugando (ForeignKey)
- `start_date` - Data de início
- `end_date` - Data de fim
- `total_price` - Preço total (calculado automaticamente)
- `status` - Status: `pending`, `approved`, `rejected`, `finished`
- `created_at` - Data de criação

## 🔧 Configurações Importantes

### Paginação
- **PAGE_SIZE**: 10 itens por página
- Configurado em `core/settings.py`

### JWT
- **ACCESS_TOKEN_LIFETIME**: 12 horas
- **REFRESH_TOKEN_LIFETIME**: 7 dias

### Mídia
- Arquivos de mídia salvos em `media/tools/`
- Acessíveis via `/media/tools/<nome_arquivo>`

## 🐛 Troubleshooting

### Erro ao executar migrations
- Certifique-se de que o venv está ativo
- Use `venv\Scripts\python.exe manage.py migrate` (Windows)

### Erro de permissão ao criar ferramenta
- Verifique se o token JWT está sendo enviado no header
- Token pode ter expirado (12h de validade)

### Erro ao fazer upload de imagem
- Verifique se a pasta `media/` existe
- Verifique permissões de escrita

## 📄 Licença

Este é um projeto acadêmico desenvolvido para a FATEC.

## 👥 Desenvolvido por

[Seu nome/equipe]

---

**Status:** ✅ Backend Completo com 95.22% de Cobertura de Testes

