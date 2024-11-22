from django.shortcuts import render
from core.models import Category, Product, ProductImages, Vendor, Wishlist, ProductReview, CartOrder, CartOrderItem, Address

def index(request):
    #product = Product.objects.all().order_by('-id')
    product = Product.objects.filter(product_status='published', featured=True).order_by('-id')


    context = {
        'products': product
    }

    return render(request, 'core/index.html', context)

def product_list_view(request):
    product = Product.objects.filter(product_status='published').order_by('-id')

    context = {
        'products': product
    }

    return render(request, 'core/product-list.html', context)

def category_list_view(request):
    #product = Product.objects.all().order_by('-id')
    categories = Category.objects.all()


    context = {
        'categories': categories
    }

    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(category=category, product_status='published').order_by('-id')

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors
    }

    return render(request, 'core/vendor-list.html', context)