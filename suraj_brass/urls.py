from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('dashboard.urls')),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Suraj Brass Industries Admin"
admin.site.site_title = "Suraj Brass Admin"
admin.site.index_title = "Welcome to Suraj Brass Industries Admin Panel"
