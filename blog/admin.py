from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'featured_image_preview', 'is_published', 'published_at', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'tags', 'published_at')
    search_fields = ('title', 'content', 'excerpt', 'author')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image', 'author', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="height:50px;"/>', obj.featured_image.url)
        return '-'
    featured_image_preview.short_description = 'Image'
