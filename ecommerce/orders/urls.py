from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create-order'),
    path('<int:order_id>/received/', views.mark_order_as_received, name='mark-order-as-received'),
]
