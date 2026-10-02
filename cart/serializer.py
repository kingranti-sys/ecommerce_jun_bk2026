from rest_framework import serializers
from .models import Cart, CartItem

class CartItemserializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "quantity",
        ]

    def get_product_image(self, obj):
        request = self.context.get("request")

        image = obj.product.images.first()

        if image:
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url

        return None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemserializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["user", "created_at", "updated_at"]