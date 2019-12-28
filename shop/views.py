from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import CommentForm
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models.functions import Lower
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


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


@login_required
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


class CategoriesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    query_set = Category.objects.all()
    ordering = [Lower('name')]

    def test_func(self):
        return self.request.user.is_staff


class CategoryCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('shop:staff_show_categories')

    def get_success_message(self, cleaned_data):
        return f"Kategoria '{cleaned_data['name']}' została utworzona"

    def test_func(self):
        return self.request.user.is_staff


class CategoryUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('shop:staff_show_categories')

    def get_success_message(self, cleaned_data):
        return f"Kategoria '{cleaned_data['name']}' została zaktualizowana"

    def test_func(self):
        return self.request.user.is_staff


class CategoryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('shop:staff_show_categories')

    def test_func(self):
        return self.request.user.is_staff


class ProductsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    query_set = Product.objects.all()
    ordering = [Lower('name')]

    def test_func(self):
        return self.request.user.is_staff


class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'image', 'description', 'categories']
    success_url = reverse_lazy('shop:staff_show_products')

    def get_success_message(self, cleaned_data):
        return f"Produkt '{cleaned_data['name']}' został utworzony"

    def test_func(self):
        return self.request.user.is_staff


class ProductDetete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('shop:staff_show_products')

    def test_func(self):
        return self.request.user.is_staff


class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'image', 'description', 'categories']
    success_url = reverse_lazy('shop:staff_show_products')

    def get_success_message(self, cleaned_data):
        return f"Książka '{cleaned_data['name']}' została zaktualizowana"

    def test_func(self):
        return self.request.user.is_staff
