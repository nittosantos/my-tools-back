# Lista de Problemas

Este documento contém uma lista de problemas identificados no projeto que precisam ser resolvidos.

---

## Problemas Resolvidos (Frontend)

### ✅ 1. Modal de Edição de Ferramenta - Campos Vazios

**Status:** ✅ Resolvido no Frontend

**Solução Implementada:**
- Uso de `useMemo` para calcular `defaultValues` baseado em `tool` e `open`
- Key no componente `Form` ajustada para garantir remontagem quando necessário: `edit-${tool.id}` ou `create-${timestamp}`
- Sem necessidade de `useEffect` - solução mais performática usando apenas `useMemo` e `key`

**Arquivos Modificados:**
- `src/components/CreateToolDialog.tsx`
  - Adicionado `useMemo` para calcular `defaultValues` dinamicamente
  - Key do Form ajustada para forçar remontagem quando `tool` ou `open` mudam

**Backend:** ❌ Não necessário

---

### ✅ 2. Descrição Longa Sem Quebra de Linha na Página de Detalhes

**Status:** ✅ Resolvido no Frontend

**Solução Implementada:**
- Adicionado `whitespace-pre-wrap break-words` na página de detalhes
- A listagem já tinha `line-clamp-3` funcionando corretamente

**Arquivos Modificados:**
- `src/routes/tools.$toolId.tsx` - Adicionado classes CSS para quebra de linha

**Backend:** ❌ Não necessário

---

### ✅ 3. Possibilidade de Alugar Próprias Ferramentas

**Status:** ✅ Resolvido no Frontend | ⚠️ **Requer validação no Backend**

**Solução Implementada no Frontend:**
- Validação na página de detalhes: botão desabilitado e mensagem quando usuário é o dono
- Validação na página de checkout: bloqueio completo com mensagem de erro
- Comparação entre `tool.owner` e `user.id` do contexto de autenticação

**Arquivos Modificados:**
- `src/routes/tools.$toolId.tsx` - Validação e desabilitação do botão
- `src/routes/tools.$toolId.rent.tsx` - Bloqueio na página de checkout

**Backend:** ⚠️ **NECESSÁRIO - Validação de Segurança**

**O que implementar no Backend:**
```python
# No serializer ou view de criação de aluguel (POST /rentals/)
def validate(self, data):
    tool = data.get('tool')
    renter = self.context['request'].user
    
    # Verificar se o usuário está tentando alugar sua própria ferramenta
    if tool.owner == renter:
        raise serializers.ValidationError({
            'tool': 'Você não pode alugar suas próprias ferramentas.'
        })
    
    return data
```

**Motivo:** Frontend pode ser contornado. Backend deve rejeitar a criação de aluguel quando `rental.renter` for igual a `tool.owner`.

---

### ✅ 4. Campo Valor com Comportamento Estranho

**Status:** ✅ Resolvido no Frontend

**Solução Implementada:**
- Ajustado para permitir campo vazio temporariamente durante digitação
- Melhorada a lógica de conversão para evitar valores indesejados
- Campo agora aceita valor vazio e converte corretamente para número

**Arquivos Modificados:**
- `src/components/CreateToolDialog.tsx` - Lógica de `onChange` melhorada

**Backend:** ❌ Não necessário

---

### ✅ 5. Aluguel Não Aparece em "Meus Aluguéis" Após Criação

**Status:** ✅ Resolvido no Frontend

**Solução Implementada:**
- Ajustado o hook `useCreateRental` para aguardar (`await`) a invalidação das queries antes de navegar
- Garantido que os dados sejam atualizados antes do redirecionamento

**Arquivos Modificados:**
- `src/hooks/useCreateRental.ts` - Adicionado `await` nas invalidações de queries

**Backend:** ❌ Não necessário

---

### ✅ 6. Página "Meus Aluguéis" Precisa de Divisão/Abas

**Status:** ✅ Resolvido no Frontend

**Solução Implementada:**
- Adicionadas abas para alternar entre "Aluguéis que Fiz" e "Aluguéis Recebidos"
- Ações específicas para cada tipo de aluguel:
  - **Aluguéis que Fiz:** Botão para finalizar quando status é "approved"
  - **Aluguéis Recebidos:** Botões para aprovar/rejeitar quando status é "pending", e finalizar quando "approved"

**Arquivos Modificados:**
- `src/routes/dashboard.my-rentals.tsx` - Implementação completa de abas e lógica condicional

**Backend:** ❌ Não necessário (endpoints já existem)

---

### ✅ 10. Validação Impede Aluguel no Mesmo Dia

**Status:** ✅ Resolvido no Frontend | ⚠️ **Requer validação no Backend**

**Solução Implementada no Frontend:**
- Ajustada a validação do schema para normalizar também a data de início (zerar horas)
- Agora permite aluguel no mesmo dia (apenas impede datas passadas)

**Arquivos Modificados:**
- `src/lib/schemas.ts` - Validação ajustada para normalizar ambas as datas

**Backend:** ⚠️ **NECESSÁRIO - Validação de Segurança**

**O que implementar no Backend:**
```python
# No serializer de criação de aluguel
def validate_start_date(self, value):
    from django.utils import timezone
    from datetime import date
    
    # Normalizar para comparar apenas a data (sem hora)
    today = timezone.now().date()
    start_date = value.date() if hasattr(value, 'date') else value
    
    if start_date < today:
        raise serializers.ValidationError(
            'Não é possível alugar para datas passadas.'
        )
    
    return value
```

**Motivo:** Frontend pode ser contornado. Backend deve validar que `start_date >= hoje` (considerando apenas a data, sem hora).

---

## Problemas Pendentes

> **Nota:** Os problemas abaixo ainda precisam de implementação no backend. Veja a seção "Resumo: O que Precisa ser Implementado no Backend" para detalhes técnicos completos.

---

### 7. Lógica de Disponibilidade de Ferramentas

**Descrição:** Tecnicamente, uma ferramenta só deveria ficar indisponível quando ela está realmente alugada (status "approved" ou durante o período de aluguel ativo), não apenas quando há um aluguel pendente.

**Comportamento Atual:** 
- A ferramenta fica indisponível assim que um aluguel é criado (status "pending")
- Isso impede que outros usuários vejam/aluguem a ferramenta mesmo que o aluguel seja rejeitado

**Comportamento Esperado:** 
- Ferramenta deve permanecer disponível enquanto o aluguel está "pending"
- Ferramenta fica indisponível apenas quando o aluguel é "approved" ou durante o período ativo
- Quando um aluguel é "rejected", a ferramenta volta a ficar disponível
- Quando um aluguel é "finished", a ferramenta volta a ficar disponível

**Arquivos Relacionados:**
- `src/mocks/handlers/rentals.handlers.ts` (linhas 83-84, 109-113, 137-141) - Lógica de disponibilidade nos mocks
- Backend: Lógica de atualização de `available` status da ferramenta

**Observações:**
- Pode ser necessário ajustar tanto frontend quanto backend
- Verificar se há lógica no backend que controla isso automaticamente
- Pode ser necessário verificar aluguéis ativos ao buscar ferramentas

---

### 8. Possibilidade de Deletar Ferramenta Alugada

**Descrição:** Como owner, é possível deletar uma ferramenta mesmo quando ela está alugada. É necessário avaliar se isso faz sentido do ponto de vista de negócio.

**Questões a Considerar:**
- O que acontece com aluguéis ativos/pendentes se a ferramenta for deletada?
- Deve ser permitido deletar ferramenta com aluguéis pendentes?
- Deve ser permitido deletar ferramenta com aluguéis aprovados/ativos?
- Deve ser permitido deletar ferramenta apenas quando não há aluguéis?

**Arquivos Relacionados:**
- `src/routes/dashboard.my-tools.tsx` (linhas 82-96) - Função de deletar
- `src/hooks/useDeleteTool.ts` - Hook de deleção
- Backend: Endpoint DELETE `/api/tools/:id/`

**Observações:**
- Pode ser necessário adicionar validação no backend para impedir deleção quando há aluguéis ativos
- Pode ser necessário mostrar mensagem apropriada no frontend
- Pode ser necessário desabilitar botão de deletar quando há aluguéis ativos/pendentes

#### 📋 Onde Implementar a Validação? (Abordagem: Defesa em Profundidade)

**Resposta:** Implementar nos **3 ambientes** (Frontend, Backend e Banco de Dados) para minimizar a chance de falhas.

**1. Frontend (UX + Primeira Camada de Proteção)**
- **O que fazer:**
  - Desabilitar botão de deletar quando há aluguéis ativos/pendentes
  - Mostrar tooltip/mensagem explicativa ao usuário
  - Verificar antes de mostrar o diálogo de confirmação
- **Vantagens:** Melhor experiência do usuário, evita tentativas desnecessárias
- **Limitação:** Não confiar apenas no frontend para segurança (pode ser bypassado)

**2. Backend (Validação Principal - PRIORITÁRIO)**
- **O que fazer:**
  - Verificar se existem aluguéis com status `approved` ou `pending` antes de deletar
  - Retornar erro HTTP 400/409 com mensagem clara se houver aluguéis ativos
  - Permitir deleção apenas se não houver aluguéis ativos/pendentes
- **Vantagens:**
  - Mensagens de erro claras e específicas
  - Lógica de negócio centralizada e testável
  - Fácil de manter e modificar
  - Pode incluir lógica complexa (ex: permitir deletar se todos os aluguéis estão "finished")
- **Exemplo de implementação:**
  ```python
  # Verificar aluguéis ativos/pendentes antes de deletar
  active_rentals = Rental.objects.filter(
      tool=tool,
      status__in=['pending', 'approved']
  ).exists()
  
  if active_rentals:
      return Response(
          {"detail": "Não é possível deletar ferramenta com aluguéis ativos ou pendentes"},
          status=status.HTTP_409_CONFLICT
      )
  ```

**3. Banco de Dados (Última Linha de Defesa)**
- **O que fazer:**
  - **Opção A (Recomendada):** Foreign Key com `ON DELETE RESTRICT`
    ```sql
    ALTER TABLE rentals 
    ADD CONSTRAINT fk_rental_tool 
    FOREIGN KEY (tool_id) REFERENCES tools(id) 
    ON DELETE RESTRICT;
    ```
    - Impede deleção se houver registros relacionados
    - Erro do banco: "Cannot delete or update a parent row"
  
  - **Opção B:** Trigger ou Stored Procedure
    - Verificar status dos aluguéis antes de permitir DELETE
    - Mais complexo, mas permite lógica customizada
- **Vantagens:**
  - Última linha de defesa contra erros/bugs
  - Garante integridade mesmo em caso de acesso direto ao banco
  - Proteção contra race conditions
  - Garante consistência mesmo se backend tiver bug

**Por que essa abordagem?**
- Se o frontend falhar → backend bloqueia
- Se o backend tiver bug → banco protege
- Se alguém acessar o banco diretamente → constraint impede
- Se houver race condition → banco garante consistência

**Resumo:** Tratar nos 3 ambientes cria camadas redundantes de segurança, onde se uma falhar, as outras protegem. Isso minimiza a chance de falhas e garante maior segurança e integridade dos dados.

---

### 9. Edição de Ferramentas Alugadas/Indisponíveis

**Descrição:** Ferramentas que estão indisponíveis (alugadas) não podem ser editadas, especialmente o preço, pois isso poderia alterar o valor de um aluguel já em andamento.

**Comportamento Esperado:** 
- Impedir edição de ferramentas que têm aluguéis aprovados/ativos
- Ou pelo menos bloquear edição do campo `price_per_day` durante aluguéis ativos
- Permitir edição de outros campos que não afetam aluguéis existentes?

**Arquivos Relacionados:**
- `src/components/CreateToolDialog.tsx` - Modal de edição
- `src/routes/dashboard.my-tools.tsx` (linha 77-80) - Função `handleEdit`
- Backend: Endpoint PATCH `/api/tools/:id/`

**Observações:**
- Pode ser necessário verificar se há aluguéis ativos antes de permitir edição
- Pode ser necessário desabilitar campo de preço quando há aluguéis ativos
- Pode ser necessário mostrar mensagem explicativa ao usuário
- Verificar se há validação no backend para isso

---

## Observações Gerais

⚠️ **Importante:** Nem todos esses problemas podem ser resolvidos apenas no frontend. Alguns podem requerer mudanças no backend também. É necessário verificar cada caso e documentar as dependências.

---

## 📋 Resumo: O que Precisa ser Implementado no Backend

### 🔴 Prioridade Alta (Segurança)

#### 1. Validação: Impedir Alugar Próprias Ferramentas
**Endpoint:** `POST /rentals/`

**Validação Necessária:**
```python
# No serializer ou view
if tool.owner == request.user:
    return Response(
        {"detail": "Você não pode alugar suas próprias ferramentas."},
        status=status.HTTP_400_BAD_REQUEST
    )
```

**Motivo:** Frontend pode ser contornado. Esta é uma regra de negócio crítica.

---

#### 2. Validação: Data de Início Não Pode Ser Passada
**Endpoint:** `POST /rentals/`

**Validação Necessária:**
```python
from django.utils import timezone
from datetime import date

# No serializer
def validate_start_date(self, value):
    today = timezone.now().date()
    start_date = value.date() if hasattr(value, 'date') else value
    
    if start_date < today:
        raise serializers.ValidationError(
            'Não é possível alugar para datas passadas.'
        )
    
    return value
```

**Motivo:** Frontend pode ser contornado. Validação de integridade de dados.

---

### 🟡 Prioridade Média (Lógica de Negócio)

#### 3. Lógica de Disponibilidade de Ferramentas
**Endpoints Afetados:** 
- `POST /rentals/` (criar aluguel)
- `PATCH /rentals/{id}/approve/` (aprovar aluguel)
- `PATCH /rentals/{id}/reject/` (rejeitar aluguel)
- `PATCH /rentals/{id}/finish/` (finalizar aluguel)

**Lógica Necessária:**

1. **Ao criar aluguel (status "pending"):**
   - ❌ NÃO alterar `tool.available` para `False`
   - Ferramenta permanece disponível para outros usuários

2. **Ao aprovar aluguel (status "approved"):**
   - ✅ Alterar `tool.available = False`
   - Verificar se a data de início já passou (se sim, marcar como indisponível imediatamente)

3. **Ao rejeitar aluguel (status "rejected"):**
   - ✅ Verificar se não há outros aluguéis ativos/pendentes
   - Se não houver, alterar `tool.available = True`

4. **Ao finalizar aluguel (status "finished"):**
   - ✅ Verificar se não há outros aluguéis ativos/pendentes
   - Se não houver, alterar `tool.available = True`

**Exemplo de Implementação:**
```python
# Método helper para atualizar disponibilidade
def update_tool_availability(tool):
    from django.utils import timezone
    
    # Verificar se há aluguéis aprovados e dentro do período ativo
    active_rentals = Rental.objects.filter(
        tool=tool,
        status='approved',
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    ).exists()
    
    # Verificar se há aluguéis aprovados que ainda vão começar
    future_approved_rentals = Rental.objects.filter(
        tool=tool,
        status='approved',
        start_date__gt=timezone.now().date()
    ).exists()
    
    # Ferramenta fica indisponível se houver aluguéis ativos ou futuros aprovados
    tool.available = not (active_rentals or future_approved_rentals)
    tool.save()
```

**Chamar este método:**
- Após aprovar aluguel
- Após rejeitar aluguel (para verificar se pode voltar a ficar disponível)
- Após finalizar aluguel (para verificar se pode voltar a ficar disponível)

---

#### 4. Validação: Impedir Deletar Ferramenta com Aluguéis Ativos
**Endpoint:** `DELETE /tools/{id}/`

**Validação Necessária:**
```python
# Na view ou serializer
def destroy(self, request, *args, **kwargs):
    tool = self.get_object()
    
    # Verificar se há aluguéis ativos ou pendentes
    active_rentals = Rental.objects.filter(
        tool=tool,
        status__in=['pending', 'approved']
    ).exists()
    
    if active_rentals:
        return Response(
            {
                "detail": "Não é possível deletar ferramenta com aluguéis ativos ou pendentes. "
                         "Aguarde a conclusão ou rejeição dos aluguéis."
            },
            status=status.HTTP_409_CONFLICT
        )
    
    return super().destroy(request, *args, **kwargs)
```

**Banco de Dados (Recomendado):**
```sql
-- Adicionar constraint para última linha de defesa
ALTER TABLE rentals 
ADD CONSTRAINT fk_rental_tool 
FOREIGN KEY (tool_id) REFERENCES tools(id) 
ON DELETE RESTRICT;
```

**Motivo:** Proteção de integridade de dados e experiência do usuário.

---

#### 5. Validação: Impedir Editar Preço de Ferramenta com Aluguéis Ativos
**Endpoint:** `PATCH /tools/{id}/`

**Validação Necessária:**
```python
# No serializer
def validate_price_per_day(self, value):
    # Se estiver editando uma ferramenta existente
    if self.instance:
        # Verificar se há aluguéis ativos ou pendentes
        active_rentals = Rental.objects.filter(
            tool=self.instance,
            status__in=['pending', 'approved']
        ).exists()
        
        if active_rentals:
            raise serializers.ValidationError(
                'Não é possível alterar o preço de uma ferramenta com aluguéis ativos ou pendentes.'
            )
    
    return value
```

**Alternativa (Permitir editar outros campos):**
```python
# Na view, permitir edição de outros campos mas bloquear price_per_day
def partial_update(self, request, *args, **kwargs):
    tool = self.get_object()
    
    # Verificar se está tentando alterar o preço
    if 'price_per_day' in request.data:
        active_rentals = Rental.objects.filter(
            tool=tool,
            status__in=['pending', 'approved']
        ).exists()
        
        if active_rentals:
            return Response(
                {
                    "detail": "Não é possível alterar o preço de uma ferramenta com aluguéis ativos ou pendentes."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return super().partial_update(request, *args, **kwargs)
```

**Motivo:** Alterar preço durante aluguel ativo pode causar inconsistências financeiras.

---

## 📝 Checklist de Implementação Backend

- [ ] **Validação 1:** Impedir alugar próprias ferramentas (`POST /rentals/`)
- [ ] **Validação 2:** Validar data de início não pode ser passada (`POST /rentals/`)
- [ ] **Lógica 3:** Atualizar disponibilidade ao aprovar aluguel (`PATCH /rentals/{id}/approve/`)
- [ ] **Lógica 3:** Atualizar disponibilidade ao rejeitar aluguel (`PATCH /rentals/{id}/reject/`)
- [ ] **Lógica 3:** Atualizar disponibilidade ao finalizar aluguel (`PATCH /rentals/{id}/finish/`)
- [ ] **Validação 4:** Impedir deletar ferramenta com aluguéis ativos (`DELETE /tools/{id}/`)
- [ ] **Validação 5:** Impedir editar preço com aluguéis ativos (`PATCH /tools/{id}/`)
- [ ] **Banco de Dados:** Adicionar constraint `ON DELETE RESTRICT` na foreign key `rentals.tool_id`

---

**Última atualização:** 2024-12-19 (Frontend resolvido, documentação backend atualizada)
