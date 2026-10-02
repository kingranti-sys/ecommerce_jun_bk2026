from django.db import models
from users.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        {"pending", "Pending"},
        {"delivered", "Delivered"},
        {"cancelled", "Cancelled"},
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    