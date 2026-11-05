from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Begal rute logout admin
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='home')),
    path('admin/', admin.site.urls),
    
    # Dashboard profiling Django Silk
    path('silk/', include('silk.urls', namespace='silk')),
    
    # Sambungan ke rute aplikasi lu
    path('', include('coreapp.urls')),
]

# --- TAMBAHAN WAJIB BUAT NAMPILIN GAMBAR ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)