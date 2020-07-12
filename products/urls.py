from django.urls import path
from . import views
from .views import ProductsListView


urlpatterns = [
    path('',views.products_home,name='products_home'),
#    path('products',ProductsListView.as_view(),name='products'),
    path('products',views.ProductsListView,name='products'),
    path('assets',views.AssetsListView,name='asset_store'),
]
