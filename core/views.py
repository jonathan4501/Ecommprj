from django.shortcuts import render
from core.models import Category, Product, ProductImages, Vendor, Wishlist, ProductReview, CartOrder, CartOrderItem, Address

def index(request):
    product = Product.objects.all()

    context = {
        'products': product
    }

    return render(request, 'core/index.html', context)
