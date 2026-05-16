from rest_framework import serializers
from .models import Product, User, Users


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class UsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = "__all__"