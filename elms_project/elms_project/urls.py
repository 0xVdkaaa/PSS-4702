from django.contrib import admin
from django.urls import path
from coreapp.views import testing, course_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testing/', testing, name='testing'),
    path('courses/', course_list, name='courses'),
]