from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='subcategories'
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    meta_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_representative_image(self):
        """Return category image or fall back to first product's primary image."""
        if self.image:
            return self.image.url
        # Try to get first product's primary image
        for product in self.products.all()[:1]:
            img = product.get_primary_image()
            if img:
                return img.image.url
        return None

    def get_products(self):
        """Return max 5 products for this category."""
        return self.products.filter(is_active=True)[:5]


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True, help_text="Brief product summary")
    description = models.TextField(blank=True, help_text="Detailed product description")
    specifications = models.TextField(blank=True, help_text="Technical specs, one per line or as table")
    material = models.CharField(max_length=200, blank=True, default="Brass")
    finish = models.CharField(max_length=100, blank=True)
    size_range = models.CharField(max_length=200, blank=True, help_text="e.g. M4 to M30")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=50, blank=True, default="Per Piece")
    moq = models.CharField(max_length=100, blank=True, help_text="Minimum Order Quantity")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customizable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_primary', 'order']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


INQUIRY_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]


class ProductInquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    quantity = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=INQUIRY_STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Inquiry"
        verbose_name_plural = "Product Inquiries"

    def __str__(self):
        return f"{self.name} - {self.product.name}"
