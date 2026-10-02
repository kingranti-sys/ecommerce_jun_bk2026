from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from cart.models import Cart

from .serializers import OrderSerializer

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist: 
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.select_related("product")

        if not cart_items.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        for c in cart_items:
            if c.quantity > c.product.stock:
                return Response({"error": (
                    f"Not enough stock for"
                    f"{c.product.name}"
                    f"Only {c.product.stock} available")
                    }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            total_amount = 0

            order = Order.objects.create(
                user=request.user,
                total_amount=0
            )

            for c in cart_items:
                product = c.product

                price = product.price
                quantity = c.quantity

                item_total = price * quantity
                total_amount += item_total

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

                product.stock -= quantity
                product.save()

            order.total_amount = total_amount
            order.save()

            cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_201_CREATED)
