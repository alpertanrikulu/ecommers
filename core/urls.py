from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    # Homepage
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product_list"),
    path("products/<pid>/", views.product_detail_view, name="product_detail_view"),

    # Category
    path("category/", views.category_list_view, name="category_list"),
    path("category/<cid>/", views.category_product_list_view, name="category_product_list_view"),
    
    # Vendor
    path("vendors/", views.vendor_list_view, name="vendor_list_view"),
    path("vendors/<vid>/", views.vendor_detail_view, name="vendor_detail_view"),

    # Tags
    path("products/tags/<slug:tag_slug>/", views.tag_list, name="tag_list"), # slug: ifadesi url deki parametrenin türünü belirtir int str gibi

    # Add Review
    path("ajax-add-review/<pid>", views.ajax_add_review, name="ajax_add_review"),

    # Search
    path("search/", views.search_view, name="search_view"),
    path("filter-products/", views.filter_product, name="filter_product"),
]