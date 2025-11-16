# 📋 Checklist do Backend – Marketplace de Aluguel (Django + DRF)

Este arquivo lista todas as etapas pendentes para finalizar o backend do marketplace.
As tarefas estão organizadas por prioridade e área do sistema.

---

## ✅ 1. Implementado até agora
- Estrutura inicial do Django
- App `marketplace`
- Models `Tool` e `Rental`
- Upload de imagem com `ImageField`
- Serializers com campos read-only corretos
- CRUD automático com ViewSets
- Configuração do MEDIA_URL e MEDIA_ROOT
- Autenticação com JWT (login, refresh, /auth/me)
- Proteção de rotas com `IsAuthenticated`
- Criação automática de:
  - `owner` ao criar ferramenta
  - `renter` ao criar rental
  - `total_price` calculado
- Criação de Tools e Rentals testada via Insomnia

---

## 📌 2. O que falta implementar (próximos passos)

### 🟦 **A. Lógica de Disponibilidade**
- [ ] Marcar `tool.is_available = False` ao criar um rental  
- [ ] Criar lógica para marcar `is_available = True` ao finalizar ou rejeitar aluguel

---

### 🟦 **B. Endpoints Específicos para Fluxo de Aluguel**
- [ ] Criar endpoint `PATCH /rentals/<id>/approve/`
- [ ] Criar endpoint `PATCH /rentals/<id>/reject/`
- [ ] Criar endpoint `PATCH /rentals/<id>/finish/`

Regras:

- Apenas o **owner da ferramenta** pode aprovar, rejeitar ou finalizar.
- Se rejeitar → `tool.is_available = True`
- Se finalizar → `tool.is_available = True`

---

### 🟦 **C. Filtros e Listagens Úteis**
- [ ] Listar **minhas ferramentas**  
      `GET /tools/my/`

- [ ] Listar **suas solicitações de aluguel (como renter)**  
      `GET /rentals/my/`

- [ ] Listar **solicitações recebidas (como owner das tools)**  
      `GET /rentals/received/`

---

### 🟦 **D. Melhorias de Segurança**
- [ ] Garantir que só o dono da ferramenta pode editar/deletar sua Tool
- [ ] Garantir que só o dono do rental pode ver seu rental
- [ ] Garantir que só owner pode aprovar/rejeitar rentals da sua ferramenta

---

### 🟦 **E. Melhorias Gerais**
- [ ] Paginação nas listas (optional)
- [ ] Ordenação por data (opcional)
- [ ] Tratar erros customizados (mensagens amigáveis)
- [ ] Criar rota `/healthcheck` opcional para deploy futuro

---

## 📌 3. Tarefas Futuras (não obrigatórias para MVP)

- [ ] Sistema de mensagens entre renter e owner  
- [ ] Histórico de aluguel por ferramenta  
- [ ] Perfis mais completos de usuário  
- [ ] Avaliações / reviews das ferramentas  
- [ ] Favoritos  
- [ ] Busca avançada  
- [ ] Cálculo de períodos ocupados (disponibilidade por datas)

---

## ⭐ MVP (Versão que já dá para usar com frontend)
Para o MVP funcionar com frontend React, precisamos apenas:

- [ ] Endpoints de aluguel (approve/reject/finish)
- [ ] Filtros básicos (my tools, my rentals, received rentals)
- [ ] Disponibilidade automática da ferramenta

Depois disso → **o backend está pronto para produção do MVP**.

---
