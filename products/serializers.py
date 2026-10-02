from rest_framework import serializers
from .models import Product, ProductImage, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
           "id",
           "name",
           "description",
           "created_at", 
        ]
    read_only_fields = ["id", "created_at"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "created_at",
        ]

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "stock",
            "is_available",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "images", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")

        product = Product.objects.create(**validated_data)

        if request:
            images = request.FILES.getlist("images")

            for image in images:
                ProductImage.objects.create(
                     product=product,
                    image=image
                    )
        return product