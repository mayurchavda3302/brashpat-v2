"""
Run this with: python manage.py seed_data
Creates initial demo data so you can see the site immediately.
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings as django_settings
from core.models import SiteSettings, Banner, WhyChooseUs, QualityFeature
from products.models import Category, Product, ProductImage
from blog.models import Post, Tag
from django.utils import timezone


# Map each (category, type_number) to a unique image file
PRODUCT_IMAGE_MAP = {
    ("Brass Fittings", 1): "brass_fittings.png",
    ("Brass Fittings", 2): "brass_fittings_2.png",
    ("Brass Fittings", 3): "brass_fittings_3.png",
    ("Brass Inserts", 1): "brass_inserts.png",
    ("Brass Inserts", 2): "brass_inserts_2.png",
    ("Brass Inserts", 3): "brass_inserts_3.png",
    ("Brass Connectors", 1): "brass_connectors.png",
    ("Brass Connectors", 2): "brass_connectors_2.png",
    ("Brass Connectors", 3): "brass_connectors_3.png",
    ("Brass Valves", 1): "brass_valves.png",
    ("Brass Valves", 2): "brass_valves_2.png",
    ("Brass Valves", 3): "brass_valves_3.png",
    ("Brass Fasteners", 1): "brass_fasteners.png",
    ("Brass Fasteners", 2): "brass_fasteners_2.png",
    ("Brass Fasteners", 3): "brass_fasteners_3.png",
    ("Custom Brass Parts", 1): "brass_custom_parts.png",
    ("Custom Brass Parts", 2): "brass_custom_parts_2.png",
    ("Custom Brass Parts", 3): "brass_custom_parts.png",  # Reuse Type 1 (rate limit)
}


class Command(BaseCommand):
    help = 'Seed initial demo data'

    def _assign_product_images(self):
        """Copy unique static product images to media and assign to products."""
        static_img_dir = os.path.join(django_settings.BASE_DIR, 'static', 'images', 'products')
        media_products_dir = os.path.join(django_settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)

        for (category_name, type_num), image_filename in PRODUCT_IMAGE_MAP.items():
            src_path = os.path.join(static_img_dir, image_filename)
            if not os.path.exists(src_path):
                self.stdout.write(self.style.WARNING(f'  Image not found: {src_path}'))
                continue

            product_name = f"{category_name} - Type {type_num}"
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                continue

            # Delete existing images for this product to reassign
            product.images.all().delete()

            # Copy image to media directory with unique name
            dest_filename = f"{product.slug}.png"
            dest_path = os.path.join(media_products_dir, dest_filename)
            shutil.copy2(src_path, dest_path)

            # Create ProductImage record
            ProductImage.objects.create(
                product=product,
                image=f"products/{dest_filename}",
                alt_text=f"{product.name} - High quality brass component",
                is_primary=True,
                order=0,
            )
            self.stdout.write(f'  Assigned unique image to: {product.name}')

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Site Settings
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.company_name = "Kedarnath Industry"
        settings.tagline = "Precision Brass Components Manufacturer"
        settings.email = "info@kedarnathindustry.com"
        settings.phone_primary = "+91 98765 43210"
        settings.address = "123, Industrial Area, GIDC"
        settings.city = "Jamnagar"
        settings.state = "Gujarat"
        settings.country = "India"
        settings.pincode = "361004"
        settings.about_short = ("Kedarnath Industry is a leading manufacturer of precision brass components "
                                 "supplying to clients across 50+ countries. With over 20 years of experience, "
                                 "we deliver quality, reliability, and innovation in every product.")
        settings.established_year = "2003"
        settings.products_count = "500+"
        settings.clients_count = "1000+"
        settings.countries_count = "50+"
        settings.experience_years = "20+"
        settings.iso_certified = True
        settings.save()
        self.stdout.write(self.style.SUCCESS('✓ Site settings created'))

        # Why Choose Us
        why_items = [
            ("fa-certificate", "ISO Certified", "All products meet international quality standards and are ISO certified."),
            ("fa-globe", "Global Export", "We export to 50+ countries including USA, Europe, Australia, and Middle East."),
            ("fa-cogs", "Custom Manufacturing", "Custom designs and specifications accepted. OEM manufacturing available."),
            ("fa-shipping-fast", "On-Time Delivery", "Reliable supply chain with on-time delivery for bulk orders."),
        ]
        for i, (icon, title, desc) in enumerate(why_items):
            WhyChooseUs.objects.get_or_create(title=title, defaults={'icon': icon, 'description': desc, 'order': i})
        self.stdout.write(self.style.SUCCESS('✓ Why Choose Us items created'))

        # Quality Features
        quality_items = [
            ("Raw Material Testing", "All brass alloys are tested for composition and purity before production."),
            ("In-Process Inspection", "100% dimensional inspection during manufacturing with precision instruments."),
            ("Final Quality Check", "Finished products undergo rigorous testing before packaging and dispatch."),
        ]
        for i, (title, desc) in enumerate(quality_items):
            QualityFeature.objects.get_or_create(title=title, defaults={'description': desc, 'order': i})
        self.stdout.write(self.style.SUCCESS('✓ Quality features created'))

        # Product Categories & Products
        cat_data = [
            ("Brass Fittings", "High-quality brass fittings for plumbing, pneumatic, and hydraulic systems."),
            ("Brass Inserts", "Precision brass inserts for plastic molding, thread repair, and PCB applications."),
            ("Brass Connectors", "Durable brass connectors for electrical and industrial use."),
            ("Brass Valves", "Industrial brass valves for fluid and gas control systems."),
            ("Brass Fasteners", "Precision brass fasteners including nuts, bolts, and screws."),
            ("Custom Brass Parts", "Custom CNC machined brass components to your exact specifications."),
        ]
        for cat_name, cat_desc in cat_data:
            cat, created = Category.objects.get_or_create(name=cat_name, defaults={'description': cat_desc})
            if created:
                self.stdout.write(f'  Created category: {cat_name}')
                # Add sample products to each category
                for j in range(1, 4):
                    Product.objects.create(
                        category=cat,
                        name=f"{cat_name} - Type {j}",
                        short_description=f"Premium quality {cat_name.lower()} manufactured to international standards.",
                        material="Brass (CuZn39Pb3)",
                        finish="Natural / Chrome Plated",
                        size_range="M4 to M24",
                        moq="100 Pieces",
                        is_featured=(j == 1),
                    )
        self.stdout.write(self.style.SUCCESS('✓ Categories and products created'))

        # Assign unique product images
        self.stdout.write('Assigning unique product images...')
        self._assign_product_images()
        self.stdout.write(self.style.SUCCESS('✓ Product images assigned'))

        # Blog
        tag1, _ = Tag.objects.get_or_create(name="Industry News")
        tag2, _ = Tag.objects.get_or_create(name="Manufacturing")
        tag3, _ = Tag.objects.get_or_create(name="Export")

        posts_data = [
            ("Kedarnath Industry Achieves ISO 9001:2015 Certification",
             "We are proud to announce our ISO 9001:2015 certification, reaffirming our commitment to quality.",
             "Kedarnath Industry has successfully obtained the ISO 9001:2015 certification. This achievement reflects our unwavering dedication to quality management and customer satisfaction across all our manufacturing processes.",
             [tag1]),
            ("Expanding Our Export Reach to 50+ Countries",
             "Our brass components are now reaching customers in over 50 countries worldwide.",
             "We are thrilled to share that Kedarnath Industry now exports to more than 50 countries, from the USA to Australia, Europe to the Middle East. Our global footprint continues to grow thanks to our commitment to quality.",
             [tag3]),
            ("New CNC Machining Facility Inaugurated",
             "State-of-the-art CNC facility enhances our custom manufacturing capabilities.",
             "We recently inaugurated our new CNC machining facility equipped with the latest technology. This expansion enables us to handle more complex custom brass components with tighter tolerances and faster turnaround times.",
             [tag2]),
        ]
        for title, excerpt, content, tags in posts_data:
            post, created = Post.objects.get_or_create(title=title, defaults={
                'excerpt': excerpt, 'content': content,
                'is_published': True, 'published_at': timezone.now()
            })
            if created:
                post.tags.set(tags)
        self.stdout.write(self.style.SUCCESS('✓ Blog posts created'))

        self.stdout.write(self.style.SUCCESS('\n✅ All demo data seeded successfully!'))
        self.stdout.write('Next step: python manage.py createsuperuser')
