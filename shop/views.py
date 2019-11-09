from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'all_categories': categories, 'products': products}
    return render(request, 'shop/index.html', context)



def products_for_category(request, category_slug):
    categories = Category.objects.all()
    chosen_category = get_object_or_404(Category, slug=category_slug)
    products = chosen_category.product_set.all()
    context = {'all_categories': categories, 'chosen_category': chosen_category, 'products': products}
    return render (request, 'shop/index.html', context)



def product_detail(request, product_slug):
    pass