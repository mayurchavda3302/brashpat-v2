from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

# Models
from products.models import Product, ProductInquiry, ProductImage
from blog.models import Post
from core.models import ContactInquiry


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user is logged in and is a staff member."""
    login_url = reverse_lazy('dashboard:login')
    
    def test_func(self):
        return self.request.user.is_staff


class CustomLoginView(LoginView):
    """Custom login view for the dashboard."""
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:home')


class DashboardHomeView(AdminRequiredMixin, TemplateView):
    """Main dashboard overview page."""
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = Product.objects.count()
        context['blog_count'] = Post.objects.count()
        context['unread_product_inquiries'] = ProductInquiry.objects.filter(is_read=False).count()
        context['unread_contact_inquiries'] = ContactInquiry.objects.filter(is_read=False).count()
        
        # Recent activity
        context['recent_contacts'] = ContactInquiry.objects.order_by('-created_at')[:5]
        context['recent_product_inquiries'] = ProductInquiry.objects.order_by('-created_at')[:5]
        
        return context

# --- PRODUCTS ---

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import ProductForm, ProductImageForm, PostForm

class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('dashboard:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle single image upload for simplicity
        image = self.request.FILES.get('primary_image')
        if image:
            ProductImage.objects.create(product=self.object, image=image, is_primary=True)
        messages.success(self.request, "Product created successfully.")
        return response

class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('dashboard:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        image = self.request.FILES.get('primary_image')
        if image:
            # Overwrite or create new primary image
            ProductImage.objects.filter(product=self.object, is_primary=True).update(is_primary=False)
            ProductImage.objects.create(product=self.object, image=image, is_primary=True)
        messages.success(self.request, "Product updated successfully.")
        return response

class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = self.success_url
        return ctx

# --- BLOGS ---

class PostListView(AdminRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

class PostCreateView(AdminRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/post_form.html'
    success_url = reverse_lazy('dashboard:post_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)

class PostUpdateView(AdminRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/post_form.html'
    success_url = reverse_lazy('dashboard:post_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

class PostDeleteView(AdminRequiredMixin, DeleteView):
    model = Post
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:post_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = self.success_url
        return ctx

# --- INQUIRIES ---

from django.views.generic import DetailView

class ContactInquiryListView(AdminRequiredMixin, ListView):
    model = ContactInquiry
    template_name = 'dashboard/inquiry_list.html'
    context_object_name = 'inquiries'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['inquiry_type'] = 'Contact'
        ctx['detail_url_name'] = 'dashboard:contact_detail'
        return ctx

class ContactInquiryDetailView(AdminRequiredMixin, DetailView):
    model = ContactInquiry
    template_name = 'dashboard/inquiry_detail.html'
    context_object_name = 'inquiry'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save()
        return response

class ProductInquiryListView(AdminRequiredMixin, ListView):
    model = ProductInquiry
    template_name = 'dashboard/inquiry_list.html'
    context_object_name = 'inquiries'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['inquiry_type'] = 'Product'
        ctx['detail_url_name'] = 'dashboard:product_inquiry_detail'
        return ctx

class ProductInquiryDetailView(AdminRequiredMixin, DetailView):
    model = ProductInquiry
    template_name = 'dashboard/inquiry_detail.html'
    context_object_name = 'inquiry'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save()
        return response

