from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import CommentForm
from django.shortcuts import redirect


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'all_categories': categories, 'products': products}
    return render(request, 'shop/index.html', context)


def products_for_category(request, category_slug):
    categories = Category.objects.all()
    chosen_category = get_object_or_404(Category, slug=category_slug)
    products = chosen_category.product_set.all()
    request.session['chosen_category_id'] = chosen_category.id
    context = {'all_categories': categories, 'chosen_category_id': chosen_category.id, 'products': products}
    return render(request, 'shop/index.html', context)


def product_detail(request, product_slug):
    categories = Category.objects.all()
    chosen_product = get_object_or_404(Product, slug=product_slug)
    if 'chosen_category_id' in request.session:
        chosen_category_id = request.session['chosen_category_id']
    else:
        chosen_category_id = None
    context = {'all_categories': categories, 'chosen_category_id': chosen_category_id, 'product': chosen_product}
    return render(request, 'shop/product_detail.html', context)


def product_add_comment(request, product_slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            product = get_object_or_404(Product, slug=product_slug)
            f.product = product
            product.update_product_rating(f.rating)

            f.save()

            return redirect('shop:product_detail', product_slug=product_slug)
    else:
        form = CommentForm()
    return render(request, 'shop/add_comment.html', {'form': form})
