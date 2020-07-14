from django.shortcuts import render
from django.views.generic import (
   ListView,
   DetailView,
)
from .models import Products

# Create your views here.

def products_home(request):
   context = {
      'welcome_msg' : 'Welcome to Home page.',
   }
   return render(request,'products/home.html',context)


def ProductsListView(request):
   user_id=request.user.id
   data = Products.objects.all().filter(ToBeSell=True).exclude(p_owner=user_id)
   context = {
      'product_data' : data,
   }
   return render(request,'products/products.html',context)
def AssetsListView(request):
   user_id=request.user.id
   data = Products.objects.all().filter(p_owner=user_id)
   context = {
      'product_data' : data,
   }
   return render(request,'products/products.html',context)
