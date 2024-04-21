from django.urls import path
from .views import login_view, register, logout_view, add_to_cart, update_cart_item, remove_item, clear_cart

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # cart operation
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('update-cart-item/<int:item_id>/', update_cart_item, name='update-cart-item'),
    path('remove-item/<int:item_id>/', remove_item, name='remove-item'),
    path('clear-cart/', clear_cart, name='clear-cart'),
]