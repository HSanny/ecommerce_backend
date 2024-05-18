from django.urls import path
from .views import ProductListView, SingleProductView, DataSummaryView

urlpatterns = [
    path('amazon_products/', ProductListView.as_view(), name='amazon_products_list'),
    path('single_product/<str:product_id>/', SingleProductView.as_view(), name='single_product'),
    path('data_summary/', DataSummaryView.as_view(), name='data_summary')
]