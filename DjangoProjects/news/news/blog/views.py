from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import ScrollNews, PopularPost, AboutPage


# Create your views here.

def index(request):
    scroll = ScrollNews.objects.all()
    popular_post = PopularPost.objects.all()
    about_post = AboutPage.objects.all()

    ctx = {
        "scroll": scroll,
        "popular_post": popular_post,
        "about_post": about_post,
    }
    return render(request, 'index.html', ctx)

def error_404(request):
    return render(request, '404.html')

def about(request, id):
    about_post_post = get_object_or_404(AboutPage, id=id)

    ctx = {
        "post": about_post_post,
    }

    AboutPage.objects.filter(id=id).update(views=F('views'))
    about_post_post.refresh_from_db()

    return render(request, 'about-us.html', ctx)

def contact(request):
    return render(request, 'contact.html')

def contact_us(request):
    return render(request, 'contact-us.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Login yoki parol xato!")
            return redirect('login')

    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Parol mos emas!")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Bu email allaqachon mavjud!")
            return redirect('register')

        User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
            )
        messages.error(request, "Ro'yhatdan o'tdingiz!")
        return redirect('login')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def search_result(request):
    return render(request, 'search-result.html')

def category(request):
    return render(request, 'category.html')



