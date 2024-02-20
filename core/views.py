from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReviews, WishList, Address
from taggit.models import Tag

# Create your views here.

def index(request):
    products = Product.objects.filter(featured=True, product_status="published")
    pimages = ProductImages.objects.all()

    context = {
        'products':products,
        'pimages':pimages,
    }
    return render(request, 'core/index.html', context=context)

def product_list_view(request):
    products = Product.objects.filter(featured=True, product_status="published")

    context = {
        'products':products
    }
    print(context)
    return render(request, 'core/product-list.html', context=context)

def category_list_view(request):
    category = Category.objects.all()

    context = {
        'category':category
    }
    print(context)
    return render(request, 'core/category-list.html', context=context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category) # product ve category yi eşleştirmek için foreign key ile birbirlerine bağladık

    context = {
        'category': category,
        'products': products,
    }
    return render(request, "core/category-product-list.html", context= context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors':vendors,
    }
    return render(request, "core/vendor-list.html", context=context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    context = {
        'vendor':vendor,
        'products':products,
    }
    return render(request, "core/vendor-detail.html", context=context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    p_images = product.p_images.all()

    
    context = {
        'product':product,
        'p_images':p_images,
        'products':products,
    }
    return render(request, "core/product-detail.html", context=context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published",).order_by("-id")
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag]) #tags__in olayını pek anlamadım

    context = {
        'products':products,
        'tag':tag,
    }
    return render(request, "core/tag.html", context=context)