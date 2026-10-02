from rest_framework import serializers
from .models import Order, OrderItem 

class OrderItemSerializer(serializers.Serializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price"]

class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "items", "total_amount", "status", "created_at", "updated_at"]
        read_only_fields = ["user", "total_amount", "status", "created_at", "updated_at"]