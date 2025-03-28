from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'), 
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length= 10, max_length=20, prefix='cat', alphabet='abcdefgh12345678') 

    title = models.CharField(max_length=100, default='Category')
    image = models.ImageField(upload_to='category', default='category.jpg')

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))   

    def __str__(self):
        return self.title

#class Tags(models.Model):
 #   pass


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length= 10, max_length=20, prefix='ven', alphabet='abcdefgh12345678') # id = models.AutoField

    title = models.CharField(max_length=100, default='Vendor')
    image = models.ImageField(upload_to='user_directory_path', default='vendor.jpg')
    cover_image = models.ImageField(upload_to='user_directory_path', default='vendor.jpg')
    description = models.TextField(null=True, blank=True, default='This is the vendor')

    address = models.CharField(max_length=100, default='123 Main St')
    contact = models.CharField(max_length=100, default='123-456-7890')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
   

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='pro', alphabet='abcdefgh12345678') 

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor')

    title = models.CharField(max_length=100, default='Product')
    description = models.TextField(null=True, blank=True, default='This is the product')
    image = models.ImageField(upload_to='user_directory_path', default='product.jpg')

    price = models.DecimalField(max_digits=100, decimal_places=2, default='1.99')
    old_price = models.DecimalField(max_digits=100, decimal_places=2, default='2.99')
    
    specifications = models.TextField(null=True, blank=True, default='This is the specification')
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, default='in_review', max_length=100)
    


    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet='1234567890')

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage_off(self):

        new_price = (self.old_price - self.price)
        percentage_off = ((new_price / self.old_price) * 100)
        return percentage_off
        #new_price = (self.price/self.old_price) * 100
        #return new_price

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    images = models.ImageField(upload_to='product-images', default='product.jpg')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2, default='1.99')
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, default='process', max_length=30)

    class Meta:
        verbose_name_plural = 'Cart Order'

class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default='1.99')
    total = models.DecimalField(max_digits=100, decimal_places=2, default='1.99')

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField(null=True, blank=True, default='This is the review')
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default='123 Main St', null=True, blank=True)
    contact = models.CharField(max_length=100, default='123-456-7890', null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'

    