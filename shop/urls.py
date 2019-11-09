
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:category_slug>/products/', views.products_for_category, name='products_for_category'),
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),

]

