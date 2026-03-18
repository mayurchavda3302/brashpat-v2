from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Banner, WhyChooseUs, TeamMember,
    Testimonial, QualityFeature, Certification, ContactInquiry
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Info', {
            'fields': ('company_name', 'tagline', 'logo', 'favicon', 'established_year', 'iso_certified')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone_primary', 'phone_secondary', 'whatsapp_number', 'address', 'city', 'state', 'country', 'pincode')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url', 'youtube_url')
        }),
        ('About Content', {
            'fields': ('about_short', 'about_full')
        }),
        ('Stats Counter', {
            'fields': ('products_count', 'clients_count', 'countries_count', 'experience_years')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Google Map', {
            'fields': ('map_embed_url',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;"/>', obj.image.url)
        return '-'
    preview_image.short_description = 'Preview'


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'preview_photo', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'designation')

    def preview_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:50px; border-radius:50%;"/>', obj.photo.url)
        return '-'
    preview_photo.short_description = 'Photo'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'country', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('rating', 'is_active', 'country')
    search_fields = ('client_name', 'company', 'message')


@admin.register(QualityFeature)
class QualityFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'preview_image', 'is_active')
    list_editable = ('is_active',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;"/>', obj.image.url)
        return '-'
    preview_image.short_description = 'Certificate'


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'subject', 'is_read', 'created_at')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('name', 'email', 'phone', 'company', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
