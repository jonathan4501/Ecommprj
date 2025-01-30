from django.shortcuts import render, get_object_or_404
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

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published').order_by('-id')

    context = {
        'vendor': vendor,
        'products': products
    }
    return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    #product = get_object_or_404(Product, pid=pid)
    images = ProductImages.objects.filter(product=product)
    vendor = Vendor.objects.get(vid=product.vendor.vid)

    context = {
        'product': product,
        'images': images,
        'vendor': vendor
    }
    return render(request, 'core/product-detail.html', context)