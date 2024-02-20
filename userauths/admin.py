from django.contrib import admin
from userauths.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','bio'] # admin panelde kullanıcı bilgilerinin hangilerinin gösterileceğini yazdık.

admin.site.register(User, UserAdmin) # admin paneli üzerinde models.py deki User modelinin görüntülenmesini sağlar