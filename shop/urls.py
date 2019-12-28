
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>/products/', views.products_for_category, name='products_for_category'),
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:product_slug>/add-comment/', views.product_add_comment, name='product_add_comment'),
    path('staff/categories/', views.CategoriesListView.as_view(), name='staff_show_categories'),
    path('staff/categories/new/', views.CategoryCreate.as_view(), name='staff_new_category'),
    path('staff/categories/update/<slug:slug>/', views.CategoryUpdate.as_view(), name='staff_update_category'),
    path('staff/categories/delete/<slug:slug>/', views.CategoryDelete.as_view(), name='staff_delete_category'),
    path('staff/products/', views.ProductsListView.as_view(), name='staff_show_products'),
    path('staff/products/new/', views.ProductCreate.as_view(), name='staff_new_product'),
    path('staff/products/delete/<slug:slug>/', views.ProductDetete.as_view(), name='staff_delete_product'),
    path('staff/products/update/<slug:slug>/', views.ProductUpdate.as_view(), name='staff_update_product'),

]

