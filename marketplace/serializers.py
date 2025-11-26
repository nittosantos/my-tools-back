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

    def to_representation(self, instance):
        return RentalSerializer(instance, context=self.context).data