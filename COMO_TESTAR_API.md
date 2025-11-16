# 🚀 Como Testar a API - Guia Rápido

Existem **3 formas** de testar a API sem ter que criar rota por rota manualmente:

---

## 📦 Opção 1: Collection do Insomnia (Recomendado)

### Como usar:

1. **Abra o Insomnia**
2. **Importe a collection:**
   - Clique em **"Create"** → **"Import/Export"** → **"Import Data"**
   - Selecione o arquivo `insomnia_collection.json` que está na raiz do projeto backend
   - Ou arraste o arquivo para dentro do Insomnia

3. **Configure as variáveis de ambiente:**
   - A collection já vem com variáveis pré-configuradas
   - Você pode editar em **"Manage Environments"** (ícone de engrenagem)
   - Variáveis disponíveis:
     - `base_url`: `http://127.0.0.1:8000` (já configurado)
     - `access_token`: Preencha após fazer login
     - `refresh_token`: Preencha após fazer login
     - `tool_id`: ID da ferramenta para testes
     - `rental_id`: ID do aluguel para testes

4. **Fluxo de teste:**
   ```
   1. Execute "Login" → Copie o access_token e refresh_token
   2. Cole os tokens nas variáveis de ambiente
   3. Agora todas as outras rotas já vão funcionar automaticamente!
   ```

### ✅ Vantagens:
- ✅ Todas as rotas já configuradas
- ✅ Headers de autenticação automáticos
- ✅ Parâmetros de exemplo já preenchidos
- ✅ Organizado em pastas (Autenticação, Ferramentas, Aluguéis)
- ✅ Variáveis de ambiente para facilitar

---

## 🌐 Opção 2: DRF Browsable API (Mais Rápido)

O Django REST Framework já vem com uma interface web para testar a API!

### Como usar:

1. **Inicie o servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Acesse no navegador:**
   - Listar ferramentas: `http://127.0.0.1:8000/api/tools/`
   - Listar aluguéis: `http://127.0.0.1:8000/api/rentals/`
   - Login: `http://127.0.0.1:8000/api/auth/login/`

3. **Na interface:**
   - Você verá um formulário HTML para fazer requisições
   - Para autenticação, use o botão "Authorize" no topo
   - Cole o token JWT no formato: `Bearer <seu_token>`

### ✅ Vantagens:
- ✅ Não precisa instalar nada
- ✅ Interface visual amigável
- ✅ Testa direto no navegador
- ✅ Mostra documentação automática

### ⚠️ Limitação:
- Precisa autenticar manualmente em cada requisição (ou usar o botão "Authorize")

---

## 📚 Opção 3: Swagger/OpenAPI (Documentação Interativa)

Se quiser uma documentação ainda mais completa, podemos adicionar o `drf-spectacular`:

```bash
pip install drf-spectacular
```

Depois adicionar no `settings.py` e criar rotas de documentação. Isso gera uma interface tipo Swagger UI.

**Quer que eu implemente isso?** É só pedir! 😊

---

## 🎯 Recomendação

**Use a Collection do Insomnia** para testes rápidos e repetitivos. É a forma mais prática e você não precisa criar nada manualmente!

**Use o DRF Browsable API** quando quiser testar algo rapidamente sem abrir o Insomnia.

---

## 📝 Notas Importantes

- **Autenticação:** Todas as rotas (exceto login) precisam do header:
  ```
  Authorization: Bearer <access_token>
  ```

- **Token expira em 12 horas:** Se der erro 401, faça login novamente ou use o endpoint de refresh token.

- **Upload de imagens:** Use `multipart/form-data` no Insomnia para criar ferramentas com foto.

- **Filtros:** Os filtros de ferramentas podem ser combinados:
  ```
  /api/tools/?category=construcao&state=SP&city=São Paulo&search=furadeira&ordering=price_per_day&page=1
  ```

