from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique = True, null=False)
    username = models.CharField(max_length=100) 
    bio = models.CharField(max_length=100)

    USERNAME_FIELD = "email" # bu alanın içindeki değer REQUIRED_FIELDS listesi içinde olmamamalıdır.
    REQUIRED_FIELDS = ["username",] # bu kullanıcı oluştururken zorunlu girilmesi gereken alanları tanımlarken kullanılır

    def __str__(self):
        return self.username
    

