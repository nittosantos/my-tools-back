# 🚀 Guia de Deploy no Railway

Este guia explica como fazer o deploy do projeto My Tools Backend no Railway.

## 📋 Pré-requisitos

1. Conta no [Railway](https://railway.app)
2. Repositório Git (GitHub, GitLab, etc.)
3. Projeto configurado e funcionando localmente

## 🔧 Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que todos os arquivos necessários estão no repositório:
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `requirements.txt` (com dependências de produção)
- ✅ `core/settings.py` (configurado para produção)

### 2. Criar Projeto no Railway

1. Acesse [railway.app](https://railway.app) e faça login
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"** (ou GitLab)
4. Escolha o repositório do projeto
5. O Railway detectará automaticamente que é um projeto Python/Django

### 3. Adicionar Banco de Dados PostgreSQL

1. No dashboard do projeto, clique em **"+ New"**
2. Selecione **"Database"** → **"Add PostgreSQL"**
3. O Railway criará automaticamente um banco PostgreSQL e configurará a variável `DATABASE_URL`

### 4. Configurar Variáveis de Ambiente

No dashboard do projeto, vá em **"Variables"** e adicione:

#### Obrigatórias:
- `SECRET_KEY`: Gere uma chave secreta segura (pode usar: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG`: `False` (para produção)
- `ALLOWED_HOSTS`: Seu domínio do Railway (ex: `seu-projeto.railway.app`) - você pode adicionar múltiplos separados por vírgula

#### Opcionais (mas recomendadas):
- `CORS_ALLOWED_ORIGINS`: URL do seu frontend em produção separada por vírgula (ex: `https://meu-frontend.vercel.app,https://outro-dominio.com`)

#### Cloudinary (Recomendado para armazenar imagens):
- `CLOUDINARY_CLOUD_NAME`: Nome da sua conta no Cloudinary
- `CLOUDINARY_API_KEY`: Chave API do Cloudinary
- `CLOUDINARY_API_SECRET`: Segredo da API do Cloudinary

**Nota:** Se você não configurar o Cloudinary, o sistema usará armazenamento local (que pode ser perdido no Railway). Veja a seção "Configurar Cloudinary" abaixo.

**Nota:** O Railway já configura automaticamente:
- `DATABASE_URL` (quando você adiciona o PostgreSQL)
- `PORT` (porta onde o servidor deve rodar)
- `RAILWAY_ENVIRONMENT` (indica que está rodando no Railway)

### 5. Deploy Automático

O Railway fará o deploy automaticamente quando você:
- Fizer push para o branch conectado
- Ou clicar em **"Deploy"** manualmente

### 6. Verificar o Deploy

1. Após o deploy, o Railway fornecerá uma URL (ex: `https://seu-projeto.railway.app`)
2. Acesse a URL para verificar se está funcionando
3. Acesse `/api/docs/` para ver a documentação Swagger

### 7. Executar Migrations

As migrations são executadas automaticamente pelo `Procfile` antes de iniciar o servidor:
```
web: python manage.py migrate && gunicorn core.wsgi --bind 0.0.0.0:$PORT
```

Se precisar executar migrations manualmente:
1. No dashboard do Railway, vá em **"Deployments"**
2. Clique nos três pontos do deployment mais recente
3. Selecione **"View Logs"** ou **"Open Shell"**
4. Execute: `python manage.py migrate`

### 8. Configurar Cloudinary (Recomendado) 🌟

O Cloudinary é um serviço **gratuito** para armazenar imagens. É ideal para projetos acadêmicos porque:
- ✅ **25 GB de armazenamento gratuito**
- ✅ **25 GB de largura de banda mensal**
- ✅ **Sem cartão de crédito necessário**
- ✅ **Sem limite de tempo**
- ✅ **Imagens não são perdidas quando o Railway reinicia**

#### Passo a passo:

1. **Criar conta no Cloudinary:**
   - Acesse [cloudinary.com](https://cloudinary.com)
   - Clique em **"Sign Up for Free"**
   - Faça login com Google, GitHub ou email (sem cartão de crédito)

2. **Obter credenciais:**
   - Após criar a conta, você verá o **Dashboard**
   - Na página inicial, você verá:
     - **Cloud Name** (ex: `dxyz1234`)
     - **API Key** (ex: `123456789012345`)
     - **API Secret** (ex: `abcdefghijklmnopqrstuvwxyz`)
   - **Importante:** Anote essas informações!

3. **Configurar no Railway:**
   - No dashboard do Railway, vá em **"Variables"**
   - Adicione as três variáveis:
     - `CLOUDINARY_CLOUD_NAME`: Seu Cloud Name
     - `CLOUDINARY_API_KEY`: Sua API Key
     - `CLOUDINARY_API_SECRET`: Seu API Secret
   - Clique em **"Add"** para cada uma

4. **Fazer novo deploy:**
   - Após adicionar as variáveis, o Railway fará um novo deploy automaticamente
   - Ou você pode clicar em **"Deploy"** manualmente

5. **Testar:**
   - Após o deploy, teste fazendo upload de uma imagem via API
   - A imagem será salva no Cloudinary e não será perdida!

**Nota:** Se você não configurar o Cloudinary, o sistema funcionará normalmente, mas as imagens serão salvas localmente e podem ser perdidas quando o container reiniciar.

### 9. Criar Superusuário (Opcional)

Para acessar o admin (`/admin/`), você precisa criar um superusuário:

1. No dashboard do Railway, vá em **"Deployments"**
2. Clique nos três pontos do deployment mais recente
3. Selecione **"Open Shell"**
4. Execute: `python manage.py createsuperuser`
5. Siga as instruções para criar o usuário

## 📝 Variáveis de Ambiente no Railway

### Como adicionar variáveis:

1. No dashboard do projeto, clique em **"Variables"**
2. Clique em **"+ New Variable"**
3. Adicione o nome e valor da variável
4. Clique em **"Add"**

### Variáveis importantes:

| Variável | Descrição | Exemplo | Obrigatória |
|----------|-----------|---------|-------------|
| `SECRET_KEY` | Chave secreta do Django | `django-insecure-...` (gere uma nova!) | ✅ Sim |
| `DEBUG` | Modo debug | `False` | ✅ Sim |
| `ALLOWED_HOSTS` | Domínios permitidos | `seu-projeto.railway.app,localhost` | ✅ Sim |
| `CORS_ALLOWED_ORIGINS` | URLs do frontend | `https://meu-frontend.vercel.app` | ⚠️ Se tiver frontend |
| `DATABASE_URL` | URL do banco (automático) | Configurado automaticamente | ✅ Sim (automático) |
| `CLOUDINARY_CLOUD_NAME` | Nome da conta Cloudinary | `dxyz1234` | ⚠️ Recomendado |
| `CLOUDINARY_API_KEY` | Chave API do Cloudinary | `123456789012345` | ⚠️ Recomendado |
| `CLOUDINARY_API_SECRET` | Segredo da API Cloudinary | `abcdefghijklmnopqrstuvwxyz` | ⚠️ Recomendado |

## 🔍 Troubleshooting

### Erro: "DisallowedHost"

**Solução:** Adicione o domínio do Railway em `ALLOWED_HOSTS`:
```
ALLOWED_HOSTS=seu-projeto.railway.app
```

### Erro: "No module named 'gunicorn'"

**Solução:** Verifique se `gunicorn` está no `requirements.txt` e faça um novo deploy.

### Erro: "Database connection failed"

**Solução:** 
1. Verifique se o serviço PostgreSQL foi adicionado
2. Verifique se a variável `DATABASE_URL` está configurada
3. Verifique os logs do Railway para mais detalhes

### Arquivos estáticos não aparecem

**Solução:** O WhiteNoise está configurado para servir arquivos estáticos. Se ainda não funcionar:
1. Verifique se `STATIC_ROOT` está configurado
2. Execute `python manage.py collectstatic` (pode adicionar ao Procfile)

### CORS não funciona

**Solução:** Adicione a URL do frontend em `CORS_ALLOWED_ORIGINS`:
```
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app
```

## 📦 Arquivos de Mídia (Imagens)

### ⚠️ Problema: Armazenamento Temporário no Railway

O Railway tem armazenamento **temporário** (ephemeral). Isso significa que arquivos salvos na pasta `media/` podem ser perdidos quando:
- O container reiniciar
- Você fizer um novo deploy
- O Railway atualizar o serviço

### ✅ Solução: Cloudinary (Recomendado)

O projeto está configurado para usar **Cloudinary** automaticamente quando as credenciais estiverem configuradas. Veja a seção "Configurar Cloudinary" acima.

**Vantagens do Cloudinary:**
- ✅ **Gratuito** (25 GB de armazenamento + 25 GB de largura de banda/mês)
- ✅ **Sem cartão de crédito** necessário
- ✅ **Imagens nunca são perdidas**
- ✅ **CDN global** (imagens carregam rápido)
- ✅ **Transformações automáticas** (redimensionar, otimizar, etc.)

**Como funciona:**
- Se você configurar as variáveis do Cloudinary → imagens vão para o Cloudinary
- Se não configurar → imagens vão para armazenamento local (podem ser perdidas)

### 🔄 Alternativas (se não quiser usar Cloudinary):

1. **Railway Volume** (3 GB gratuito, mas pode ser perdido se recriar o serviço)
2. **AWS S3** (mais complexo, pode ter custos)
3. **Outros serviços** (Imgur, etc.)

**Recomendação:** Use Cloudinary! É gratuito e perfeito para projetos acadêmicos.

## 🔗 Links Úteis

- [Documentação do Railway](https://docs.railway.app)
- [Django no Railway](https://docs.railway.app/guides/django)
- [PostgreSQL no Railway](https://docs.railway.app/databases/postgresql)

## ✅ Checklist de Deploy

- [ ] Repositório conectado ao Railway
- [ ] Serviço PostgreSQL adicionado
- [ ] Variável `SECRET_KEY` configurada
- [ ] Variável `DEBUG` configurada como `False`
- [ ] Variável `ALLOWED_HOSTS` configurada com o domínio do Railway
- [ ] Variável `CORS_ALLOWED_ORIGINS` configurada (se tiver frontend)
- [ ] **Conta Cloudinary criada** (recomendado)
- [ ] **Variáveis do Cloudinary configuradas** (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`)
- [ ] Deploy realizado com sucesso
- [ ] Migrations executadas
- [ ] Superusuário criado (se necessário)
- [ ] API testada e funcionando
- [ ] **Upload de imagem testado** (verificar se está salvando no Cloudinary)

---

**Boa sorte com o deploy! 🚀**

