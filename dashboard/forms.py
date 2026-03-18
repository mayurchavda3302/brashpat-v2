from django import forms
from products.models import Product, Category, ProductImage
from blog.models import Post, Tag

class BaseDashboardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class ProductForm(BaseDashboardForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'short_description', 'description', 
                  'specifications', 'material', 'finish', 'size_range', 
                  'price', 'price_unit', 'moq', 'is_featured', 'is_active', 'is_customizable']
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'specifications': forms.Textarea(attrs={'rows': 4}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PostForm(BaseDashboardForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'featured_image', 'author', 'tags', 'is_published']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 8}),
        }
