from django.urls import path
from .views import *

urlpatterns = [
    path("products/", product_list),
    path("products/<int:pk>/", product_detail),
    path("products/create", product_create),
    path("product/update/<int:pk>/", product_update),
    path("product/delete/<int:pk>/", product_delete),

    path("users/", UserList.as_view()),
    path("userssss/", UsersLists.as_view()),
    path("userssss/<int:pk>/", UsersLists.as_view()),
]