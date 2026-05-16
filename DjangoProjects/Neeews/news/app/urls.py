from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('about-us/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login_page, name='login'),
    path('login_user/', login_user, name='login_user'),
    path('register/', register_page, name='register'),
    path('register_user/', register_user, name='register_user'),
    path('error/', error, name='error'),
    path('news/<slug:slug>/', news_detail, name='news'),
    path('news_list/', views.news_list, name='news_list'),
    path('news_list/<slug:category_slug>/', news_list, name='news_list_category'),
    path('search/', search, name='search'),
    path('logout/', logout_user, name='logout_user'),
    path('featured/', views.featured_news, name='featured_news'),
    path('popular/', views.popular_news, name='popular_news'),
    path('hot/', views.hot_news, name='hot_news'),
    path('trending/', views.trending_news, name='trending_news'),
    path('watched/', views.most_watched_news, name='most_watched_news'),
]