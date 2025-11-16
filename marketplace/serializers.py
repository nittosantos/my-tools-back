from django.contrib.auth.models import User

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