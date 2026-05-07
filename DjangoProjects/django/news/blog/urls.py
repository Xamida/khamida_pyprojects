from django.urls import path
from .views import index, error_404, about, category, contact, contact_us,search_result, login_view, logout_view, register_view

urlpatterns = [
    path('', index, name='home'),
    path('404/', error_404, name='404-error'),
    path('about/<int:id>/', about, name='about'),
    path('news/category/', category, name='category'),
    path('news/contact/', contact, name='contact'),
    path('news/contact-us/', contact_us, name='contact_us'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('news/search-result/', search_result, name='search-result')
]

