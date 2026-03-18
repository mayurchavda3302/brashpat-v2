from django.db import models


class SiteSettings(models.Model):
    """Global site settings - only ONE row should exist."""
    company_name = models.CharField(max_length=200, default="Suraj Brass Industries")
    tagline = models.CharField(max_length=300, blank=True)
    email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=10, blank=True)
    # Social Links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    # SEO
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    # Logo
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    # About
    about_short = models.TextField(blank=True, help_text="Short about text for homepage")
    about_full = models.TextField(blank=True, help_text="Full about us page content")
    established_year = models.CharField(max_length=10, blank=True)
    # Stats
    products_count = models.CharField(max_length=20, default="500+")
    clients_count = models.CharField(max_length=20, default="1000+")
    countries_count = models.CharField(max_length=20, default="50+")
    experience_years = models.CharField(max_length=20, default="20+")
    # Google Map embed URL
    map_embed_url = models.TextField(blank=True)
    # Certifications
    iso_certified = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super().save(*args, **kwargs)


class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True, default="Explore Products")
    button_url = models.CharField(max_length=200, blank=True, default="/products/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Homepage Banner"

    def __str__(self):
        return self.title


class WhyChooseUs(models.Model):
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class e.g. fa-star")
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Why Choose Us Point"
        verbose_name_plural = "Why Choose Us Points"

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.company}"


class QualityFeature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='quality/', blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Quality Feature"

    def __str__(self):
        return self.title


class Certification(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='certifications/')
    year = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContactInquiry(models.Model):
    """Stores contact form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=150, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.date()})"
