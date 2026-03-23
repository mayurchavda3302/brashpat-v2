from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    SiteSettings, Banner, WhyChooseUs, TeamMember,
    Testimonial, QualityFeature, Certification, ContactInquiry
)
from .forms import ContactInquiryForm
from products.models import Category, Product
from blog.models import Post


def home(request):
    banners = Banner.objects.filter(is_active=True)
    categories = Category.objects.filter(parent=None, is_active=True)[:6]
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    why_us = WhyChooseUs.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    latest_posts = Post.objects.filter(is_published=True).order_by('-published_at')[:3]
    certifications = Certification.objects.filter(is_active=True)

    context = {
        'banners': banners,
        'categories': categories,
        'featured_products': featured_products,
        'why_us': why_us,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'certifications': certifications,
    }
    return render(request, 'core/home.html', context)


def about(request):
    team = TeamMember.objects.filter(is_active=True)
    certifications = Certification.objects.filter(is_active=True)
    why_us = WhyChooseUs.objects.filter(is_active=True)
    context = {'team': team, 'certifications': certifications, 'why_us': why_us}
    return render(request, 'core/about.html', context)


def quality(request):
    features = QualityFeature.objects.filter(is_active=True)
    certifications = Certification.objects.filter(is_active=True)
    context = {'features': features, 'certifications': certifications}
    return render(request, 'core/quality.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your inquiry has been received. We will contact you shortly.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactInquiryForm()
    return render(request, 'core/contact.html', {'form': form})
