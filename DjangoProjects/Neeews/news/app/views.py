from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Category


def home(request):
    news = News.objects.all()

    featured = News.objects.order_by('-likes')[:5]
    trending = News.objects.order_by('-views', '-likes')[:10]
    hot = News.objects.order_by('-views')[:5]

    q = (request.GET.get("q") or "").strip()

    if q:
        news = news.filter(
            Q(title__icontains=q) |
            Q(descriptions__icontains=q)
        )

    category_slug = request.GET.get("category", "").strip()
    if category_slug:
        news = news.filter(category__slug=category_slug)

    categories = Category.objects.all()

    ctx = {
        "news": news,
        "featured_news": featured,
        "trending_news": trending,
        "hot_news": hot,
        "categories": categories,
        "category_slug": category_slug,
        "q": q
    }

    return render(request, 'home.html', ctx)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def error(request):
    return render(request, '404.html')


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    related = News.objects.filter(category=news.category).exclude(id=news.id)[:5]

    news.views += 1
    news.save(update_fields=["views"])

    ctx = {
        "news": news,
        "related_news": related
    }

    return render(request, 'news_detail.html', ctx)


def news_list(request, category_slug=None, slug=None):
    news = News.objects.all().order_by('-date')

    if slug:
        news = news.filter(slug=slug)

    if category_slug:
        news = news.filter(category__slug=category_slug)

    categories = Category.objects.all()
    q = (request.GET.get("q") or "").strip()

    if q:
        news = news.filter(
            Q(title__icontains=q) |
            Q(descriptions__icontains=q)
        )

    ctx = {
        "news": news,
        "categories": categories,
        "category_slug": category_slug,
        "q": q
    }
    return render(request, 'news_list.html', ctx)


def search(request):
    return render(request, 'search.html')


def profile(request):
    return render(request, 'profile.html')

def featured_news(request):
    news = News.objects.order_by('-likes')[:10]

    return render(request, 'news_list.html', {
        'news': news,
        'title': 'Featured News'
    })


def popular_news(request):
    news = News.objects.order_by('-likes', '-views')[:10]

    return render(request, 'news_list.html', {
        'news': news,
        'title': 'Most Popular'
    })


def hot_news(request):
    news = News.objects.order_by('-views')[:10]

    return render(request, 'news_list.html', {
        'news': news,
        'title': 'Hot News'
    })


def trending_news(request):
    news = News.objects.order_by('-views', '-likes')[:10]

    return render(request, 'news_list.html', {
        'news': news,
        'title': 'Trending News'
    })


def most_watched_news(request):
    news = News.objects.order_by('-views')[:10]

    return render(request, 'news_list.html', {
        'news': news,
        'title': 'Most Watched'
    })


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('profile')

        return redirect('login')


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('profile')

    return redirect('register')


def logout_user(request):
    logout(request)
    return redirect('home')