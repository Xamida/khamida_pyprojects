from django.urls import path
from .views import index, about, blog_detail, blog_grid, checkout, contact, faq, my_account, my_acc_address, \
    my_acc_orders, my_account_edit, order_details, privacy, product_detail, product_thumbs, shop_cart, shop_default, \
    track_your_order, wishlist, error404, login_user, logout_user, register_user, subscribe_views

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('blog_detail/', blog_detail, name='blog_detail'),
    path('blog_grid/', blog_grid, name='blog_grid'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('acc_address/', my_acc_address, name='my_acc_address'),
    path('acc_edit/', my_account_edit, name='my_account_edit'),
    path('acc_orders/', my_acc_orders, name='my_acc_orders'),
    path('order_details/', order_details, name='order_details'),
    path('privacy/', privacy, name='privacy'),
    path('product_thumb/', product_thumbs, name='product_thumb'),
    path('cart/', shop_cart, name='shop_cart'),
    path('shop-default/', shop_default, name='shop_default'),
    path('track/', track_your_order, name='track'),
    path('wishlist/', wishlist, name='wishlist'),
    path('error/', error404, name='error'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),

    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register_user, name='register_user'),
    path('my_account/', my_account, name='my_account'),
    path('subscribe/', subscribe_views, name='subscribe')
]



