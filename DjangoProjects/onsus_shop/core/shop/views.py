from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, message
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title

from .models import Product, Category, PromoCode
from .utils import generate_promo_code


# Create your views here.


def index(request):
    product = Product.objects.filter(
        is_active=True,
        slug__isnull=False
    ).exclude(slug="").prefetch_related("images").order_by("-created_at")

    q = (request.GET.get("q") or "").strip()
    category_slug = request.GET.get("category", "").strip()

    products = product

    if q:
        products = products.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = Category.objects.all()

    featured_product = product.first()
    other_product = list(product[:9])

    ctx = {
        "featured_product": featured_product,
        "other_product": other_product,
        "categories": categories,
        "q": q,
        "category_slug": category_slug
    }

    return render(request, 'index.html', ctx)

def error404(request):
    return render(request, '404.html')

def about(request):
    return render(request, 'about.html')

def blog_detail(request):
    return render(request, 'blog-detail.html')

def blog_grid(request):
    return render(request, 'blog-grid.html')

def checkout(request):
    return render(request, 'checkout.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')


@login_required
def my_account(request):
    return render(request, 'my-account.html')


@login_required
def my_acc_address(request):
    return render(request, 'my-account-address.html')


@login_required
def my_account_edit(request):
    return render(request, 'my-account-edit.html')


@login_required
def my_acc_orders(request):
    return render(request, 'my-account-orders.html')


@login_required
def order_details(request):
    return render(request, 'order-details.html')

def privacy(request):
    return render(request, 'privacy.html')

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)    #product qo'shish uchun

    featured_product = (
        Product.objects.filter(is_active=True).exclude(id=product.id).first()
        ) or product

    ctx = {
        "product": product,
        "images": product.images.all(),
        "specs": product.specs.all(),
        "colors": product.colors.all(),
        "reviews": product.reviews.filter(is_published=True),
        "featured_product": featured_product
    }
    return render(request, 'product-detail.html', ctx)

def product_thumbs(request):
    return render(request, 'product-thumbs-right.html')

def shop_cart(request):
    product = Product.objects.filter(
        is_active=True,
        slug__isnull=False
    ).exclude(slug="").prefetch_related("images").order_by("-created_at")

    featured_product = product.first()

    ctx = {
        "featured_product": featured_product
    }
    return render(request, 'shop-cart.html', ctx)

def shop_default(request):
    q = (request.GET.get("q") or "").strip()

    product = Product.objects.filter(
        is_active=True,
        slug__isnull=False
    ).exclude(slug="").prefetch_related("images").order_by("-created_at")

    if q:
        product = product.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    featured_product = product.first()
    paginator = Paginator(product, 5)
    page_number = request.GET.get("page")
    product = paginator.get_page(page_number)

    ctx = {
        "featured_product": product,
        "q": q
    }

    return render(request, 'shop-default.html', ctx)

def track_your_order(request):
    return render(request, 'track-your-order.html')

def wishlist(request):
    product = Product.objects.filter(
        is_active=True,
        slug__isnull=False
    ).exclude(slug="").prefetch_related("images").order_by("-created_at")

    featured_product = product.first()

    ctx = {
        "featured_product": featured_product
    }
    return render(request, 'wishlist.html', ctx)




def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('my_account')
        else:
            return redirect('/?login=1')


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect('/?login=1')

        User.objects.create_user(username=username, password=password)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('my_account')


def logout_user(request):
    logout(request)
    return redirect('home')


def subscribe_views(request):

    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Email kiriting")
            return redirect('/')

        code = generate_promo_code()
        PromoCode.objects.create(email=email, code=code)

        send_mail(
            subject="Join Our Community",
            message=f"Siz Communitiyimizga qo'shildingiz va {code} ga ega bo'ldingiz. Bu orqali 30% chegirmaga ega bo'ldingiz",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [email],
            fail_silently = False,
        )

        messages.success(request, "Promokod email pochtaga yuborildi!")
        return redirect('/')







