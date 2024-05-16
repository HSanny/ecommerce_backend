# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, CartItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


## Cart Item

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'name', 'image', 'amount', 'price']

class UserSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True, default=[])
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'password',
            'phone_number',
            'shipping_address',
            'billing_address',
            'default_shipping_method',
            'cart_items',
            'payment_method'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token