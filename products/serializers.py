from rest_framework import serializers

from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    # Explicitly formatting datetime fields (optional if default ISO 8601 format is sufficient)
    # created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)
    # updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)
    class Meta:
        model = Product
        fields = "__all__"