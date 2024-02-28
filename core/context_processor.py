from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReviews, WishList, Address

# def default(request):
#     categories = Category.objects.all()
#     address = Address.objects.get(user=request.user)

#     return {
#         'categories':categories,
#         'address':address,
#     }




from django.contrib.auth.models import User
from django.db.models import Count, Min, Max

def default(request):
    categories = Category.objects.all()
    address = None  # Varsayılan olarak adresi None olarak ayarla
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:  # Kullanıcı giriş yapmışsa
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:  # Kullanıcının adresi yoksa
            pass

    return {
        'categories': categories,
        'min_max_price': min_max_price,
        'address': address,
        'vendors': vendors,
    }
