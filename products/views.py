from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, ProductInquiry


def product_list(request):
    """All main categories."""
    categories = Category.objects.filter(parent=None, is_active=True)
    return render(request, 'products/category_list.html', {'categories': categories})


def category_detail(request, slug):
    """Show subcategories or products for a category."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    subcategories = category.subcategories.filter(is_active=True)
    products = category.products.filter(is_active=True)[:5]  # Max 5
    context = {
        'category': category,
        'subcategories': subcategories,
        'products': products,
    }
    return render(request, 'products/category_detail.html', context)


def product_detail(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    if request.method == 'POST':
        inquiry = ProductInquiry(
            product=product,
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            quantity=request.POST.get('quantity', ''),
            message=request.POST.get('message', ''),
        )
        inquiry.save()
        messages.success(request, 'Inquiry submitted successfully! We will contact you soon.')
        return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'related_products': related_products,
        'images': product.images.all(),
    }
    return render(request, 'products/product_detail.html', context)
