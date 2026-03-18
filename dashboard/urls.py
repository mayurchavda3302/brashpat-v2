from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Auth
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard:login'), name='logout'),

    # Home
    path('', views.DashboardHomeView.as_view(), name='home'),

    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Blogs
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/add/', views.PostCreateView.as_view(), name='post_add'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Inquiries
    path('inquiries/contact/', views.ContactInquiryListView.as_view(), name='contact_list'),
    path('inquiries/contact/<int:pk>/', views.ContactInquiryDetailView.as_view(), name='contact_detail'),
    path('inquiries/product/', views.ProductInquiryListView.as_view(), name='product_inquiry_list'),
    path('inquiries/product/<int:pk>/', views.ProductInquiryDetailView.as_view(), name='product_inquiry_detail'),
    # Inquiries
    path('inquiries/contact/', views.ContactInquiryListView.as_view(), name='contact_list'),
    path('inquiries/contact/<int:pk>/', views.ContactInquiryDetailView.as_view(), name='contact_detail'),
    path('inquiries/product/', views.ProductInquiryListView.as_view(), name='product_inquiry_list'),
    path('inquiries/product/<int:pk>/', views.ProductInquiryDetailView.as_view(), name='product_inquiry_detail'),
]
