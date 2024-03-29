from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReviews, WishList, Address
from taggit.models import Tag
from django.db.models import Avg, Count
from core.forms import ProductReviewForm
from django.template.loader import render_to_string

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
    reviews = ProductReviews.objects.filter(product=product).order_by("-date")

    # Getting average of reviews
    average_rating = ProductReviews.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product review form
    review_form = ProductReviewForm

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReviews.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False


    
    context = {
        'product':product,
        'make_review':make_review,
        'review_form':review_form,
        'p_images':p_images,
        'products':products,
        'reviews':reviews,
        'average_rating':average_rating,
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

def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    review = ProductReviews.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )


    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_ratings = ProductReviews.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse({
        'bool': True, 
        'context': context, 
        'average_ratings': average_ratings
        })

def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains=query).order_by('-date')

    context = {
        'products': products,
        'query': query,
    }

    return render(request, "core/search.html", context=context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    context = {
        'products': products
    }
    
    data = render_to_string("core/async/product-list.html", context=context)
    return JsonResponse({'data': data})