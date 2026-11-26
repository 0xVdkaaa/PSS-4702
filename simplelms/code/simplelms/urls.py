from django.contrib import admin
from django.urls import path, include
from core.api import api

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
] 

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
