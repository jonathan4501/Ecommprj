from core.models import Category, Product, ProductImages, Vendor, Wishlist, ProductReview, CartOrder, CartOrderItem, Address

def default(request):
    categories = Category.objects.all()

    return {
        'categories': categories
        }