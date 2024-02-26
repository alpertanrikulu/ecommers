from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReviews, WishList, Address

# def default(request):
#     categories = Category.objects.all()
#     address = Address.objects.get(user=request.user)

#     return {
#         'categories':categories,
#         'address':address,
#     }




from django.contrib.auth.models import User

def default(request):
    categories = Category.objects.all()
    address = None  # Varsayılan olarak adresi None olarak ayarla
    vendors = Vendor.objects.all()

    if request.user.is_authenticated:  # Kullanıcı giriş yapmışsa
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:  # Kullanıcının adresi yoksa
            pass

    return {
        'categories': categories,
        'address': address,
        'vendors': vendors,
    }
