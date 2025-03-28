from django.urls import path
from core.views import index, product_list_view, category_product_list_view, category_list_view, vendor_list_view, vendor_detail_view, product_detail_view

app_name = "core"

urlpatterns = [
    #home
    path("", index, name='index'),

    #products
    path("products/", product_list_view, name='product-list'),
    path("products/<pid>/", product_detail_view, name='product-detail'),

    #category
    path("category/", category_list_view, name='category-list'),
    path("category/<cid>/", category_product_list_view, name='category-product-list'),

    #vendors
    path("vendors/", vendor_list_view, name='vendor-list'),
    path("vendors/<vid>/", vendor_detail_view, name='vendor-detail'),
]