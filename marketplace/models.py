from django.db import models
from django.contrib.auth.models import User


class Tool(models.Model):
    CATEGORIES = [
        ("construcao", "Construção"),
        ("jardinagem", "Jardinagem"),
        ("cozinha", "Cozinha"),
        ("oficina_mecanica", "Oficina Mecânica"),
        ("limpeza", "Limpeza"),
        ("eletrica", "Elétrica"),
        ("hidraulica", "Hidráulica"),
        ("pintura", "Pintura"),
        ("ferramentas_manuais", "Ferramentas Manuais"),
        ("ferramentas_eletricas", "Ferramentas Elétricas"),
        ("automotiva", "Automotiva"),
        ("eventos", "Eventos"),
        ("mudanca", "Mudança"),
        ("outros", "Outros"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to="tools/")
    state = models.CharField(max_length=2, blank=True, null=True, help_text="Estado (UF) - ex: SP, RJ, MG")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="Cidade - ex: São Paulo, Rio de Janeiro")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Rental(models.Model):
    STATUS = [
        ("pending", "Pendente"),
        ("approved", "Aprovado"),
        ("rejected", "Recusado"),
        ("finished", "Finalizado"),
    ]

    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tool.title} - {self.renter.username}"
