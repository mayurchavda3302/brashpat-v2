from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductInquiry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'preview_image', 'is_active', 'order', 'product_count')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;"/>', obj.image.url)
        return '-'
    preview_image.short_description = 'Image'

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = '# Products'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'alt_text', 'is_primary', 'order', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;"/>', obj.image.url)
        return '-'
    preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'primary_image_preview', 'material', 'price', 'is_featured', 'is_active', 'created_at')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('is_active', 'is_featured', 'category', 'material')
    search_fields = ('name', 'description', 'specifications', 'material')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'name', 'slug', 'short_description', 'description')
        }),
        ('Technical Details', {
            'fields': ('specifications', 'material', 'finish', 'size_range', 'is_customizable')
        }),
        ('Pricing & Ordering', {
            'fields': ('price', 'price_unit', 'moq')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active')
        }),
    )

    def primary_image_preview(self, obj):
        img = obj.get_primary_image()
        if img:
            return format_html('<img src="{}" style="height:50px;"/>', img.image.url)
        return '-'
    primary_image_preview.short_description = 'Image'


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'quantity', 'is_read', 'created_at')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'product__name', 'message')
    readonly_fields = ('name', 'email', 'phone', 'product', 'quantity', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
