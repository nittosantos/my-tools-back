from django.contrib.auth.models import User

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Tool, Rental


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ToolSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    available = serializers.BooleanField(source="is_available", read_only=True)
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Tool
        fields = [
            "id",
            "title",
            "description",
            "category",
            "price_per_day",
            "photo",
            "image_url",
            "available",
            "state",
            "city",
            "created_at",
            "owner",
            "owner_username",
        ]
        read_only_fields = ["owner", "created_at", "is_available"]

    def validate_price_per_day(self, value):
        """
        Impede alterar o preço de uma ferramenta com aluguéis ativos ou pendentes.
        """
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

    def validate_photo(self, value):
        """
        Valida o tamanho e formato da imagem.
        Limite: 5MB
        Formatos permitidos: JPEG, PNG, WEBP
        """
        if value:
            # Limite de 5MB (5 * 1024 * 1024 bytes)
            max_size = 5 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError(
                    "A imagem é muito grande. Tamanho máximo permitido: 5MB."
                )

            # Verificar formato (extensão)
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            file_extension = value.name.lower().split('.')[-1]
            if f'.{file_extension}' not in valid_extensions:
                raise serializers.ValidationError(
                    "Formato de imagem inválido. Use JPEG, PNG ou WEBP."
                )

        return value

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_image_url(self, obj):
        if not obj.photo:
            return None

        request = self.context.get("request")
        url = obj.photo.url

        if request is not None:
            return request.build_absolute_uri(url)
        return url


class RentalSerializer(serializers.ModelSerializer):
    renter_username = serializers.CharField(source="renter.username", read_only=True)
    owner_username = serializers.CharField(source="tool.owner.username", read_only=True)
    tool_details = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = [
            "id",
            "tool",
            "tool_details",
            "renter",
            "renter_username",
            "owner_username",
            "start_date",
            "end_date",
            "total_price",
            "status",
            "created_at",
        ]
        read_only_fields = ["renter", "total_price", "created_at"]

    @extend_schema_field(ToolSerializer)
    def get_tool_details(self, obj):
        return ToolSerializer(obj.tool, context=self.context).data


class RentalCreateSerializer(serializers.ModelSerializer):
    tool_id = serializers.PrimaryKeyRelatedField(
        queryset=Tool.objects.all(),
        source="tool",
        write_only=True,
    )

    class Meta:
        model = Rental
        fields = [
            "tool_id",
            "start_date",
            "end_date",
        ]

    def validate_start_date(self, value):
        """
        Valida que a data de início não pode ser no passado.
        Compara apenas a data (sem hora).
        """
        from django.utils import timezone
        
        today = timezone.now().date()
        start_date = value.date() if hasattr(value, 'date') else value
        
        if start_date < today:
            raise serializers.ValidationError(
                'Não é possível alugar para datas passadas.'
            )
        
        return value

    def validate(self, attrs):
        """
        Valida que o usuário não pode alugar suas próprias ferramentas.
        """
        tool = attrs.get('tool')
        request = self.context.get('request')
        
        if request and tool and tool.owner == request.user:
            raise serializers.ValidationError({
                'tool_id': 'Você não pode alugar suas próprias ferramentas.'
            })
        
        return attrs

    def to_representation(self, instance):
        return RentalSerializer(instance, context=self.context).data