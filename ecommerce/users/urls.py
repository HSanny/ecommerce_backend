from django.urls import path
from .views import CartItemView, ClearCartView, CustomTokenObtainPairView, RegisterView, RemoveCartItemView, UpdateCartItemView, csrf_token
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # csrf token url
    path('csrf-token/', csrf_token, name='csrf_token'),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    # cart operation
    path('cart/', CartItemView.as_view(), name='add_to_cart'),
    path('cart/<int:item_id>', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<int:item_id>', RemoveCartItemView.as_view(), name='remove_item'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
]