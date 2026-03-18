from .models import Category


def nav_categories(request):
    categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    return {'nav_categories': categories}
