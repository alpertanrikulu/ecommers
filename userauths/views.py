from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User


# User = settings.AUTH_USER_MODEL

# Create your views here.

def register_view(request):
    if request.method == "POST":
        print("User registered successfully!!!")
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"New user {username} created successfully!!!")
            new_user = authenticate(username=form.cleaned_data["email"],
                                    password = form.cleaned_data["password1"])
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm(request.POST or None)
        print("The user cannot be registered")
    context = {
        'form':form
    }
    return render(request, "userauths/sign-up.html", context=context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey you are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "User does not exits.\nCreate an account!!!")
        except:
            messages.warning(request, f"User with {email} e-mail address is not exits!!!")


    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")