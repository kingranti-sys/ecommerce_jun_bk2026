from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product, ProductImage, Category
from .serializers import ProductSerializer, ProductImageSerializer, CategorySerializer

# from django.http import HttpResponse, JsonResponse


'''
def home(request):
    return HttpResponse("Welcome to our E-commerce API")

def about(request):
    return HttpResponse("Welcome to our store")

def products(request):
    search = request.GET.get("search")
    return HttpResponse(f"You searched for {search}")

def product_detail(request, id):
    return HttpResponse(f"You requestes product {id}")

def category(request):
    return HttpResponse("Here are categories of our items")

def category_detail(request, id):
    return HttpResponse(f"You have selected {id}")

def product_list(request):
    products = [
    {
        "id": 1,
        "name": "Samsung S26 Ultra",
        "price": 1500
    },
    {
        "id": 2,
        "name": "Nike Air Force1",
        "price": 500
    },
    {
        "id": 3,
        "name": "MacBook Air",
        "price": 1800
    }
]
'''
    # return JsonResponse(products, safe=False)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes =[IsAuthenticated]