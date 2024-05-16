from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, CustomTokenObtainPairSerializer, CartItemSerializer
from .models import CartItem

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Add your other view functions here

# Ensure CSRF token is set
def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

# Cart item views
class CartItemView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Additional views for updating and deleting cart items
class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class ClearCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        CartItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared successfully'}, status=204)